#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2024 Arcangelo Massari <arcangelo.massari@unibo.it>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

from __future__ import annotations

import concurrent.futures
import csv
import json
import os
import re
from typing import Dict, List, Optional
from zipfile import ZipFile

import redis
from pebble import ProcessPool
from tqdm import tqdm

# Increase CSV field size limit to handle large fields
csv.field_size_limit(2**31 - 1)  # Set to max value for 32-bit systems

# Constants
FIELDNAMES = [
    "id",
    "title",
    "author",
    "issue",
    "volume",
    "venue",
    "page",
    "pub_date",
    "type",
    "publisher",
    "editor",
]

URI_TYPE_DICT = {
    "http://purl.org/spar/doco/Abstract": "abstract",
    "http://purl.org/spar/fabio/ArchivalDocument": "archival document",
    "http://purl.org/spar/fabio/AudioDocument": "audio document",
    "http://purl.org/spar/fabio/Book": "book",
    "http://purl.org/spar/fabio/BookChapter": "book chapter",
    "http://purl.org/spar/fabio/ExpressionCollection": "book section",
    "http://purl.org/spar/fabio/BookSeries": "book series",
    "http://purl.org/spar/fabio/BookSet": "book set",
    "http://purl.org/spar/fabio/ComputerProgram": "computer program",
    "http://purl.org/spar/doco/Part": "book part",
    "http://purl.org/spar/fabio/Expression": "",
    "http://purl.org/spar/fabio/DataFile": "dataset",
    "http://purl.org/spar/fabio/DataManagementPlan": "data management plan",
    "http://purl.org/spar/fabio/Thesis": "dissertation",
    "http://purl.org/spar/fabio/Editorial": "editorial",
    "http://purl.org/spar/fabio/Journal": "journal",
    "http://purl.org/spar/fabio/JournalArticle": "journal article",
    "http://purl.org/spar/fabio/JournalEditorial": "journal editorial",
    "http://purl.org/spar/fabio/JournalIssue": "journal issue",
    "http://purl.org/spar/fabio/JournalVolume": "journal volume",
    "http://purl.org/spar/fabio/Newspaper": "newspaper",
    "http://purl.org/spar/fabio/NewspaperArticle": "newspaper article",
    "http://purl.org/spar/fabio/NewspaperIssue": "newspaper issue",
    "http://purl.org/spar/fr/ReviewVersion": "peer review",
    "http://purl.org/spar/fabio/AcademicProceedings": "proceedings",
    "http://purl.org/spar/fabio/Preprint": "preprint",
    "http://purl.org/spar/fabio/Presentation": "presentation",
    "http://purl.org/spar/fabio/ProceedingsPaper": "proceedings article",
    "http://purl.org/spar/fabio/ReferenceBook": "reference book",
    "http://purl.org/spar/fabio/ReferenceEntry": "reference entry",
    "http://purl.org/spar/fabio/ReportDocument": "report",
    "http://purl.org/spar/fabio/RetractionNotice": "retraction notice",
    "http://purl.org/spar/fabio/Series": "series",
    "http://purl.org/spar/fabio/SpecificationDocument": "standard",
    "http://purl.org/spar/fabio/WebContent": "web content",
}

# Global cache for JSON files
_json_cache = {}


def init_redis_connection(
    host: str = "localhost", port: int = 6379, db: int = 2
) -> redis.Redis:
    """Initialize Redis connection with given parameters"""
    client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    # Test the connection by sending a PING command
    client.ping()  # This will raise redis.ConnectionError if connection fails
    return client


def increase_csv_field_limit() -> int:
    """Incrementally increase the CSV field size limit until it works.
    Returns the successful limit value."""
    current_limit = csv.field_size_limit()
    while True:
        try:
            csv.field_size_limit(current_limit)
            return current_limit
        except OverflowError:
            # If we get an overflow, try a smaller value
            if current_limit >= sys.maxsize:
                current_limit = int(sys.maxsize / 2)
            else:
                break
        except Exception:
            break

        # Try next value
        current_limit *= 2

    # If we get here, we need to try increasing from the default
    current_limit = csv.field_size_limit()
    while True:
        try:
            next_limit = current_limit * 2
            csv.field_size_limit(next_limit)
            current_limit = next_limit
            return current_limit
        except Exception as e:
            # If we can't increase further, return the last working value
            csv.field_size_limit(current_limit)
            return current_limit


def load_processed_omids_to_redis(output_dir: str, redis_client: redis.Redis) -> int:
    """Load all previously processed OMID from existing CSV files into Redis.
    This is done only once at startup to create the initial cache."""
    if not os.path.exists(output_dir):
        return 0

    # Clear any existing data in Redis
    redis_client.delete("processed_omids")

    count = 0
    BATCH_SIZE = 1000  # Process commands in batches of 1000

    # Get list of CSV files first
    csv_files = [f for f in os.listdir(output_dir) if f.endswith(".csv")]
    print(f"Loading {len(csv_files)} CSV files into Redis cache...")

    # Read all CSV files and collect OMIDs with progress bar
    for filename in tqdm(csv_files, desc="Loading existing identifiers"):
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            batch_pipe = redis_client.pipeline()
            batch_count = 0

            for row in reader:
                # Extract all OMIDs from the id field
                omids = [
                    id_part.strip()
                    for id_part in row["id"].split()
                    if id_part.startswith("omid:br/")
                ]
                # Add to Redis pipeline
                for omid in omids:
                    batch_pipe.sadd("processed_omids", omid)
                    batch_count += 1
                    count += 1

                    # Execute batch if we've reached the batch size
                    if batch_count >= BATCH_SIZE:
                        batch_pipe.execute()
                        batch_pipe = redis_client.pipeline()
                        batch_count = 0

            # Execute any remaining commands in the pipeline
            if batch_count > 0:
                batch_pipe.execute()

    print(f"Loaded {count} identifiers into Redis cache")
    return count


def is_omid_processed(omid: str, redis_client: redis.Redis) -> bool:
    """Check if an OMID has been processed by looking it up in Redis"""
    return redis_client.sismember("processed_omids", omid)


def find_file(
    rdf_dir: str, dir_split_number: int, items_per_file: int, uri: str
) -> Optional[str]:
    """Find the file path for a given URI based on the directory structure"""
    entity_regex: str = (
        r"^(https:\/\/w3id\.org\/oc\/meta)\/([a-z][a-z])\/(0[1-9]+0)?([1-9][0-9]*)$"
    )
    entity_match = re.match(entity_regex, uri)
    if entity_match:
        cur_number = int(entity_match.group(4))
        cur_file_split = (
            (cur_number - 1) // items_per_file
        ) * items_per_file + items_per_file
        cur_split = (
            (cur_number - 1) // dir_split_number
        ) * dir_split_number + dir_split_number

        short_name = entity_match.group(2)
        sub_folder = entity_match.group(3) or ""
        cur_dir_path = os.path.join(rdf_dir, short_name, sub_folder, str(cur_split))
        cur_file_path = os.path.join(cur_dir_path, str(cur_file_split)) + ".zip"

        return cur_file_path if os.path.exists(cur_file_path) else None
    return None


def load_json_from_file(filepath: str) -> dict:
    """Load JSON data from a ZIP file, using cache if available"""
    if filepath in _json_cache:
        return _json_cache[filepath]

    try:
        with ZipFile(filepath, "r") as zip_file:
            json_filename = zip_file.namelist()[0]
            with zip_file.open(json_filename) as json_file:
                json_content = json_file.read().decode("utf-8")
                json_data = json.loads(json_content)
                _json_cache[filepath] = json_data
                return json_data
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        return {}


def process_identifier(id_data: dict) -> Optional[str]:
    """Process identifier data to extract schema and value"""
    try:
        id_schema = id_data["http://purl.org/spar/datacite/usesIdentifierScheme"][0][
            "@id"
        ].split("/datacite/")[1]
        literal_value = id_data[
            "http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue"
        ][0]["@value"]
        return f"{id_schema}:{literal_value}"
    except (KeyError, IndexError):
        return None


def process_responsible_agent(
    ra_data: dict, ra_uri: str, rdf_dir: str, dir_split_number: int, items_per_file: int
) -> Optional[str]:
    """Process responsible agent data to extract name and identifiers"""
    try:
        # Process name
        family_name = ra_data.get("http://xmlns.com/foaf/0.1/familyName", [{}])[0].get(
            "@value", ""
        )
        given_name = ra_data.get("http://xmlns.com/foaf/0.1/givenName", [{}])[0].get(
            "@value", ""
        )
        foaf_name = ra_data.get("http://xmlns.com/foaf/0.1/name", [{}])[0].get(
            "@value", ""
        )

        # Determine name format
        if family_name or given_name:
            if family_name and given_name:
                name = f"{family_name}, {given_name}"
            elif family_name:
                name = f"{family_name},"
            else:
                name = f", {given_name}"
        elif foaf_name:
            name = foaf_name
        else:
            return None

        # Get OMID
        omid = ra_uri.split("/")[-1]
        identifiers = [f"omid:ra/{omid}"]

        # Process other identifiers
        if "http://purl.org/spar/datacite/hasIdentifier" in ra_data:
            for identifier in ra_data["http://purl.org/spar/datacite/hasIdentifier"]:
                id_uri = identifier["@id"]
                id_file = find_file(rdf_dir, dir_split_number, items_per_file, id_uri)
                if id_file:
                    id_data = load_json_from_file(id_file)
                    for graph in id_data:
                        for entity in graph.get("@graph", []):
                            if entity["@id"] == id_uri:
                                id_value = process_identifier(entity)
                                if id_value:
                                    identifiers.append(id_value)

        if identifiers:
            return f"{name} [{' '.join(identifiers)}]"
        return name
    except (KeyError, IndexError):
        return None


def process_venue_title(
    venue_data: dict,
    venue_uri: str,
    rdf_dir: str,
    dir_split_number: int,
    items_per_file: int,
) -> str:
    """Process venue title and its identifiers"""
    venue_title = venue_data.get("http://purl.org/dc/terms/title", [{}])[0].get(
        "@value", ""
    )
    if not venue_title:
        return ""

    # Get OMID
    omid = venue_uri.split("/")[-1]
    identifiers = [f"omid:br/{omid}"]

    # Process other identifiers
    if "http://purl.org/spar/datacite/hasIdentifier" in venue_data:
        for identifier in venue_data["http://purl.org/spar/datacite/hasIdentifier"]:
            id_uri = identifier["@id"]
            id_file = find_file(rdf_dir, dir_split_number, items_per_file, id_uri)
            if id_file:
                id_data = load_json_from_file(id_file)
                for graph in id_data:
                    for entity in graph.get("@graph", []):
                        if entity["@id"] == id_uri:
                            id_value = process_identifier(entity)
                            if id_value:
                                identifiers.append(id_value)

    return f"{venue_title} [{' '.join(identifiers)}]" if identifiers else venue_title


def process_hierarchical_venue(
    entity: dict, rdf_dir: str, dir_split_number: int, items_per_file: int
) -> Dict[str, str]:
    """Process hierarchical venue structure recursively"""
    result = {"volume": "", "issue": "", "venue": ""}
    entity_types = entity.get("@type", [])

    if "http://purl.org/spar/fabio/JournalIssue" in entity_types:
        result["issue"] = entity.get(
            "http://purl.org/spar/fabio/hasSequenceIdentifier", [{}]
        )[0].get("@value", "")
    elif "http://purl.org/spar/fabio/JournalVolume" in entity_types:
        result["volume"] = entity.get(
            "http://purl.org/spar/fabio/hasSequenceIdentifier", [{}]
        )[0].get("@value", "")
    else:
        # It's a main venue (journal, book series, etc.)
        result["venue"] = process_venue_title(
            entity, entity["@id"], rdf_dir, dir_split_number, items_per_file
        )
        return result

    # Process parent if exists
    if "http://purl.org/vocab/frbr/core#partOf" in entity:
        parent_uri = entity["http://purl.org/vocab/frbr/core#partOf"][0]["@id"]
        parent_file = find_file(rdf_dir, dir_split_number, items_per_file, parent_uri)
        if parent_file:
            parent_data = load_json_from_file(parent_file)
            for graph in parent_data:
                for parent_entity in graph.get("@graph", []):
                    if parent_entity["@id"] == parent_uri:
                        parent_info = process_hierarchical_venue(
                            parent_entity, rdf_dir, dir_split_number, items_per_file
                        )
                        # Merge parent info, keeping our current values
                        for key, value in parent_info.items():
                            if not result[key]:  # Only update if we don't have a value
                                result[key] = value

    return result


def find_first_ar_by_role(
    agent_roles: Dict, next_relations: Dict, role_type: str
) -> Optional[str]:
    """Find the first AR for a specific role type that isn't referenced by any other AR of the same role"""
    # Get all ARs of this role type
    role_ars = {
        ar_uri: ar_data
        for ar_uri, ar_data in agent_roles.items()
        if role_type
        in ar_data.get("http://purl.org/spar/pro/withRole", [{}])[0].get("@id", "")
    }

    # Get all "next" relations between ARs of this role type
    role_next_relations = {
        ar_uri: next_ar
        for ar_uri, next_ar in next_relations.items()
        if ar_uri in role_ars and next_ar in role_ars
    }

    # Find the AR that isn't referenced as next by any other AR of this role
    referenced_ars = set(role_next_relations.values())
    for ar_uri in role_ars:
        if ar_uri not in referenced_ars:
            return ar_uri

    # If no first AR found, take the first one from the role ARs
    return next(iter(role_ars)) if role_ars else None


def process_bibliographic_resource(
    br_data: dict, rdf_dir: str, dir_split_number: int, items_per_file: int
) -> Optional[Dict[str, str]]:
    """Process bibliographic resource data and its related entities"""
    # Skip if the entity is a JournalVolume or JournalIssue
    br_types = br_data.get("@type", [])
    if (
        "http://purl.org/spar/fabio/JournalVolume" in br_types
        or "http://purl.org/spar/fabio/JournalIssue" in br_types
    ):
        return None

    output = {field: "" for field in FIELDNAMES}

    try:
        # Extract OMID and basic BR information
        entity_id = br_data.get("@id", "")
        identifiers = [f'omid:br/{entity_id.split("/")[-1]}'] if entity_id else []

        output["title"] = br_data.get("http://purl.org/dc/terms/title", [{}])[0].get(
            "@value", ""
        )
        output["pub_date"] = br_data.get(
            "http://prismstandard.org/namespaces/basic/2.0/publicationDate", [{}]
        )[0].get("@value", "")

        # Extract type
        br_types = [
            t
            for t in br_data.get("@type", [])
            if t != "http://purl.org/spar/fabio/Expression"
        ]
        output["type"] = URI_TYPE_DICT.get(br_types[0], "") if br_types else ""

        # Process identifiers
        if "http://purl.org/spar/datacite/hasIdentifier" in br_data:
            for identifier in br_data["http://purl.org/spar/datacite/hasIdentifier"]:
                id_uri = identifier["@id"]
                id_file = find_file(rdf_dir, dir_split_number, items_per_file, id_uri)
                if id_file:
                    id_data = load_json_from_file(id_file)
                    for graph in id_data:
                        for entity in graph.get("@graph", []):
                            if entity["@id"] == id_uri:
                                id_value = process_identifier(entity)
                                if id_value:
                                    identifiers.append(id_value)
        output["id"] = " ".join(identifiers)

        # Process authors, editors and publishers through agent roles
        authors = []
        editors = []
        publishers = []

        # Create a dictionary to store agent roles and their next relations
        agent_roles = {}
        next_relations = {}

        if "http://purl.org/spar/pro/isDocumentContextFor" in br_data:
            # First pass: collect all agent roles and their next relations
            for ar_data in br_data["http://purl.org/spar/pro/isDocumentContextFor"]:
                ar_uri = ar_data["@id"]
                ar_file = find_file(rdf_dir, dir_split_number, items_per_file, ar_uri)
                if ar_file:
                    ar_data = load_json_from_file(ar_file)
                    for graph in ar_data:
                        for entity in graph.get("@graph", []):
                            if entity["@id"] == ar_uri:
                                # Store the agent role data
                                agent_roles[ar_uri] = entity
                                # Store the next relation if it exists
                                if "https://w3id.org/oc/ontology/hasNext" in entity:
                                    next_ar = entity[
                                        "https://w3id.org/oc/ontology/hasNext"
                                    ][0]["@id"]
                                    next_relations[ar_uri] = next_ar

            # Process each role type separately
            for role_type, role_list in [
                ("author", authors),
                ("editor", editors),
                ("publisher", publishers),
            ]:
                first_ar = find_first_ar_by_role(agent_roles, next_relations, role_type)
                if not first_ar:
                    continue

                # Process agent roles in order for this role type
                current_ar = first_ar
                processed_ars = set()
                max_iterations = len(agent_roles)
                iterations = 0

                while current_ar and current_ar in agent_roles:
                    if current_ar in processed_ars or iterations >= max_iterations:
                        print(
                            f"Warning: Detected cycle in hasNext relations or exceeded maximum iterations at AR: {current_ar}"
                        )
                        break

                    processed_ars.add(current_ar)
                    iterations += 1

                    # Process the current AR
                    entity = agent_roles[current_ar]
                    role = entity.get("http://purl.org/spar/pro/withRole", [{}])[0].get(
                        "@id", ""
                    )

                    # Only process if it matches our current role type
                    if role_type in role:
                        if "http://purl.org/spar/pro/isHeldBy" in entity:
                            ra_uri = entity["http://purl.org/spar/pro/isHeldBy"][0][
                                "@id"
                            ]
                            ra_file = find_file(
                                rdf_dir, dir_split_number, items_per_file, ra_uri
                            )
                            if ra_file:
                                ra_data = load_json_from_file(ra_file)
                                for ra_graph in ra_data:
                                    for ra_entity in ra_graph.get("@graph", []):
                                        if ra_entity["@id"] == ra_uri:
                                            agent_name = process_responsible_agent(
                                                ra_entity,
                                                ra_uri,
                                                rdf_dir,
                                                dir_split_number,
                                                items_per_file,
                                            )
                                            if agent_name:
                                                role_list.append(agent_name)

                    # Move to next agent role
                    current_ar = next_relations.get(current_ar)

            output["author"] = "; ".join(authors)
            output["editor"] = "; ".join(editors)
            output["publisher"] = "; ".join(publishers)

        # Process venue information
        if "http://purl.org/vocab/frbr/core#partOf" in br_data:
            venue_uri = br_data["http://purl.org/vocab/frbr/core#partOf"][0]["@id"]
            venue_file = find_file(rdf_dir, dir_split_number, items_per_file, venue_uri)
            if venue_file:
                venue_data = load_json_from_file(venue_file)
                for graph in venue_data:
                    for entity in graph.get("@graph", []):
                        if entity["@id"] == venue_uri:
                            venue_info = process_hierarchical_venue(
                                entity, rdf_dir, dir_split_number, items_per_file
                            )
                            output.update(venue_info)

        # Process page information
        if "http://purl.org/vocab/frbr/core#embodiment" in br_data:
            page_uri = br_data["http://purl.org/vocab/frbr/core#embodiment"][0]["@id"]
            page_file = find_file(rdf_dir, dir_split_number, items_per_file, page_uri)
            if page_file:
                page_data = load_json_from_file(page_file)
                for graph in page_data:
                    for entity in graph.get("@graph", []):
                        if entity["@id"] == page_uri:
                            start_page = entity.get(
                                "http://prismstandard.org/namespaces/basic/2.0/startingPage",
                                [{}],
                            )[0].get("@value", "")
                            end_page = entity.get(
                                "http://prismstandard.org/namespaces/basic/2.0/endingPage",
                                [{}],
                            )[0].get("@value", "")
                            if start_page or end_page:
                                output["page"] = f"{start_page}-{end_page}"

    except (KeyError, IndexError) as e:
        print(f"Error processing bibliographic resource: {e}")

    return output


def process_single_file(args):
    """Process a single file and return the results"""
    filepath, input_dir, dir_split_number, items_per_file, redis_params = args
    results = []

    # Initialize Redis client once
    redis_client = redis.Redis(
        host=redis_params["host"],
        port=redis_params["port"],
        db=redis_params["db"],
        decode_responses=True,
    )

    data = load_json_from_file(filepath)
    for graph in data:
        for entity in graph.get("@graph", []):
            # Skip if this is a JournalVolume or JournalIssue
            entity_types = entity.get("@type", [])
            if (
                "http://purl.org/spar/fabio/JournalVolume" in entity_types
                or "http://purl.org/spar/fabio/JournalIssue" in entity_types
            ):
                continue

            # Extract OMID from entity ID
            entity_id = entity.get("@id", "")
            if entity_id:
                omid = f"omid:br/{entity_id.split('/')[-1]}"
                # Skip if already processed
                if is_omid_processed(omid, redis_client):
                    continue

            br_data = process_bibliographic_resource(
                entity, input_dir, dir_split_number, items_per_file
            )
            if br_data:
                results.append(br_data)

    return results


class ResultBuffer:
    """Buffer to collect results and write them when reaching the row limit"""

    def __init__(self, output_dir: str, max_rows: int = 3000):
        self.buffer = []
        self.output_dir = output_dir
        self.max_rows = max_rows
        self.file_counter = self._get_last_file_number() + 1
        self.pbar = None

    def _get_last_file_number(self) -> int:
        """Find the highest file number from existing output files"""
        if not os.path.exists(self.output_dir):
            return -1

        max_number = -1
        for filename in os.listdir(self.output_dir):
            if filename.startswith("output_") and filename.endswith(".csv"):
                try:
                    number = int(filename[7:-4])  # Extract number from 'output_X.csv'
                    max_number = max(max_number, number)
                except ValueError:
                    continue
        return max_number

    def set_progress_bar(self, total: int) -> None:
        """Initialize progress bar with total number of files"""
        self.pbar = tqdm(total=total, desc="Processing files")

    def update_progress(self) -> None:
        """Update progress bar"""
        if self.pbar:
            self.pbar.update(1)

    def close_progress_bar(self) -> None:
        """Close progress bar"""
        if self.pbar:
            self.pbar.close()

    def add_results(self, results: List[Dict[str, str]]) -> None:
        """Add results to buffer and write to file if max_rows is reached"""
        self.buffer.extend(results)
        while len(self.buffer) >= self.max_rows:
            self._write_buffer_chunk()

    def _write_buffer_chunk(self) -> None:
        """Write max_rows records to a new file"""
        chunk = self.buffer[: self.max_rows]
        output_file = os.path.join(self.output_dir, f"output_{self.file_counter}.csv")
        write_csv(output_file, chunk)
        self.buffer = self.buffer[self.max_rows :]
        self.file_counter += 1

    def flush(self) -> None:
        """Write any remaining results in buffer"""
        if self.buffer:
            output_file = os.path.join(
                self.output_dir, f"output_{self.file_counter}.csv"
            )
            write_csv(output_file, self.buffer)
            self.buffer = []
            self.file_counter += 1


def task_done(future: concurrent.futures.Future, result_buffer: ResultBuffer):
    """Callback function for completed tasks"""
    try:
        results = future.result()
        if results:
            result_buffer.add_results(results)
        result_buffer.update_progress()  # Update progress after task completion
    except Exception as e:
        print(f"Task failed: {e}")
        result_buffer.update_progress()  # Update progress even if task fails


def generate_csv(
    input_dir: str,
    output_dir: str,
    dir_split_number: int,
    items_per_file: int,
    zip_output_rdf: bool,
    redis_host: str = "localhost",
    redis_port: int = 6379,
    redis_db: int = 2,
) -> None:
    """Generate CSV files from RDF data using Pebble for process management"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize Redis connection and load initial cache
    redis_client = init_redis_connection(redis_host, redis_port, redis_db)
    processed_count = load_processed_omids_to_redis(output_dir, redis_client)

    # Process only files in the 'br' directory
    br_dir = os.path.join(input_dir, "br")
    if not os.path.exists(br_dir):
        print(f"Error: bibliographic resources directory not found at {br_dir}")
        return

    # Collect all ZIP files
    all_files = []
    for root, _, files in os.walk(br_dir):
        if "prov" in root:
            continue
        all_files.extend(os.path.join(root, f) for f in files if f.endswith(".zip"))

    if not all_files:
        print("No files found to process")
        return

    print(f"Processing {len(all_files)} files...")

    # Redis connection parameters to pass to worker processes
    redis_params = {"host": redis_host, "port": redis_port, "db": redis_db}

    # Create result buffer and initialize progress bar
    result_buffer = ResultBuffer(output_dir)
    result_buffer.set_progress_bar(len(all_files))

    # Process files one at a time using Pebble
    with ProcessPool(max_workers=os.cpu_count(), max_tasks=1) as executor:
        futures: List[concurrent.futures.Future] = []
        for filepath in all_files:
            future = executor.schedule(
                function=process_single_file,
                args=(
                    (
                        filepath,
                        input_dir,
                        dir_split_number,
                        items_per_file,
                        redis_params,
                    ),
                ),
            )
            future.add_done_callback(lambda f: task_done(f, result_buffer))
            futures.append(future)

        # Wait for all futures to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file: {e}")
                return  # Exit without clearing Redis if there's an error

    # Flush any remaining results and close progress bar
    result_buffer.flush()
    result_buffer.close_progress_bar()

    # Clear Redis cache only if we've successfully completed everything
    redis_client.delete("processed_omids")
    print("Processing complete. Redis cache cleared.")


def write_csv(filepath: str, data: List[Dict[str, str]]) -> None:
    """Write data to CSV file"""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)
