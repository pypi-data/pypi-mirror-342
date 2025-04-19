import argparse
import os
import gzip
import re
from typing import Match
from rdflib import ConjunctiveGraph, URIRef, Literal, XSD
from multiprocessing import Pool, Manager
from tqdm import tqdm
import json
import zipfile
import shutil
from filelock import FileLock
from dateutil import parser as dateparser

# Definitions of regex patterns for parsing IRIs
entity_regex: str = r"^(.+)/([a-z][a-z])/(0[1-9]+0)?((?:[1-9][0-9]*)|(?:\d+-\d+))$"
prov_regex: str = r"^(.+)/([a-z][a-z])/(0[1-9]+0)?((?:[1-9][0-9]*)|(?:\d+-\d+))/prov/([a-z][a-z])/([1-9][0-9]*)$"

BASE_IRI = "https://w3id.org/oc/meta/"
DIR_SPLIT = 10000
N_FILE_ITEM = 1000
IS_JSON = True
PUBLICATION_DATE_PREDICATE = URIRef("http://prismstandard.org/namespaces/basic/2.0/publicationDate")

def _get_match(regex: str, group: int, string: str) -> str:
    match: Match = re.match(regex, string)
    if match is not None:
        return match.group(group)
    else:
        return ""

def get_base_iri(res: URIRef) -> str:
    string_iri: str = str(res)
    if "/prov/" in string_iri:
        return _get_match(prov_regex, 1, string_iri)
    else:
        return _get_match(entity_regex, 1, string_iri)

def get_short_name(res: URIRef) -> str:
    string_iri: str = str(res)
    if "/prov/" in string_iri:
        return _get_match(prov_regex, 5, string_iri)
    else:
        return _get_match(entity_regex, 2, string_iri)

def get_prov_subject_short_name(prov_res: URIRef) -> str:
    string_iri: str = str(prov_res)
    if "/prov/" in string_iri:
        return _get_match(prov_regex, 2, string_iri)
    else:
        return ""  # non-provenance entities do not have a prov_subject!

def get_prefix(res: URIRef) -> str:
    string_iri: str = str(res)
    if "/prov/" in string_iri:
        return ""  # provenance entities cannot have a supplier prefix
    else:
        return _get_match(entity_regex, 3, string_iri)

def get_prov_subject_prefix(prov_res: URIRef) -> str:
    string_iri: str = str(prov_res)
    if "/prov/" in string_iri:
        return _get_match(prov_regex, 3, string_iri)
    else:
        return ""  # non-provenance entities do not have a prov_subject!

def get_count(res: URIRef) -> str:
    string_iri: str = str(res)
    if "/prov/" in string_iri:
        return _get_match(prov_regex, 6, string_iri)
    else:
        return _get_match(entity_regex, 4, string_iri)

def get_prov_subject_count(prov_res: URIRef) -> str:
    string_iri: str = str(prov_res)
    if "/prov/" in string_iri:
        return _get_match(prov_regex, 4, string_iri)
    else:
        return ""  # non-provenance entities do not have a prov_subject!

def get_resource_number(res: URIRef) -> int:
    string_iri: str = str(res)
    if "/prov/" in string_iri:
        return int(_get_match(prov_regex, 4, string_iri))
    else:
        return int(_get_match(entity_regex, 4, string_iri))

def find_local_line_id(res: URIRef, n_file_item: int = 1) -> int:
    cur_number: int = get_resource_number(res)

    cur_file_split: int = 0
    while True:
        if cur_number > cur_file_split:
            cur_file_split += n_file_item
        else:
            cur_file_split -= n_file_item
            break

    return cur_number - cur_file_split

def find_paths(res: URIRef, base_dir: str, base_iri: str, default_dir: str, dir_split: int,
               n_file_item: int, is_json: bool = True):
    """
    This function is responsible for looking for the correct JSON file that contains the data related to the
    resource identified by the variable 'string_iri'. This search takes into account the organisation in
    directories and files, as well as the particular supplier prefix for bibliographic entities, if specified.
    In case no supplier prefix is specified, the 'default_dir' (usually set to "_") is used instead.
    """
    string_iri: str = str(res)

    cur_number: int = get_resource_number(res)

    # Find the correct file number where to save the resources
    cur_file_split: int = 0
    while True:
        if cur_number > cur_file_split:
            cur_file_split += n_file_item
        else:
            break

    # The data have been split in multiple directories and it is not something related
    # with the provenance data of the whole corpus (e.g. provenance agents)
    if dir_split and not string_iri.startswith(base_iri + "prov/"):
        # Find the correct directory number where to save the file
        cur_split: int = 0
        while True:
            if cur_number > cur_split:
                cur_split += dir_split
            else:
                break

        if "/prov/" in string_iri:  # provenance file of a bibliographic entity
            subj_short_name: str = get_prov_subject_short_name(res)
            short_name: str = get_short_name(res)
            sub_folder: str = get_prov_subject_prefix(res)
            file_extension: str = '.json' if is_json else '.nq'
            if sub_folder == "":
                sub_folder = default_dir
            if sub_folder == "":
                sub_folder = "_"  # enforce default value

            cur_dir_path: str = base_dir + subj_short_name + os.sep + sub_folder + \
                os.sep + str(cur_split) + os.sep + str(cur_file_split) + os.sep + "prov"
            cur_file_path: str = cur_dir_path + os.sep + short_name + file_extension
        else:  # regular bibliographic entity
            short_name: str = get_short_name(res)
            sub_folder: str = get_prefix(res)
            file_extension: str = '.json' if is_json else '.nt'
            if sub_folder == "":
                sub_folder = default_dir
            if sub_folder == "":
                sub_folder = "_"  # enforce default value

            cur_dir_path: str = base_dir + short_name + os.sep + sub_folder + os.sep + str(cur_split)
            cur_file_path: str = cur_dir_path + os.sep + str(cur_file_split) + file_extension
    # Enter here if no split is needed
    elif dir_split == 0:
        if "/prov/" in string_iri:
            subj_short_name: str = get_prov_subject_short_name(res)
            short_name: str = get_short_name(res)
            sub_folder: str = get_prov_subject_prefix(res)
            file_extension: str = '.json' if is_json else '.nq'
            if sub_folder == "":
                sub_folder = default_dir
            if sub_folder == "":
                sub_folder = "_"  # enforce default value

            cur_dir_path: str = base_dir + subj_short_name + os.sep + sub_folder + \
                os.sep + str(cur_file_split) + os.sep + "prov"
            cur_file_path: str = cur_dir_path + os.sep + short_name + file_extension
        else:
            short_name: str = get_short_name(res)
            sub_folder: str = get_prefix(res)
            file_extension: str = '.json' if is_json else '.nt'
            if sub_folder == "":
                sub_folder = default_dir
            if sub_folder == "":
                sub_folder = "_"  # enforce default value

            cur_dir_path: str = base_dir + short_name + os.sep + sub_folder
            cur_file_path: str = cur_dir_path + os.sep + str(cur_file_split) + file_extension
    # Enter here if the data is about a provenance agent, e.g. /corpus/prov/
    else:
        short_name: str = get_short_name(res)
        prefix: str = get_prefix(res)
        count: str = get_count(res)
        file_extension: str = '.json' if is_json else '.nq'

        cur_dir_path: str = base_dir + short_name
        cur_file_path: str = cur_dir_path + os.sep + prefix + count + file_extension

    return cur_dir_path, cur_file_path

def log_error(log_dir, error_type, message, process_id):
    log_file_path = os.path.join(log_dir, f"log_{process_id}.json")
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            existing_log = json.load(log_file)
    else:
        existing_log = {}

    if error_type not in existing_log:
        existing_log[error_type] = []
    existing_log[error_type].append(message)

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump(existing_log, log_file, indent=4)

def merge_logs(log_dir, final_log_file):
    error_counts = {}
    final_log = {}

    for log_file_name in os.listdir(log_dir):
        if log_file_name.startswith("log_") and log_file_name.endswith(".json"):
            with open(os.path.join(log_dir, log_file_name), 'r', encoding='utf-8') as log_file:
                log_contents = json.load(log_file)
                for error_type, messages in log_contents.items():
                    if error_type not in final_log:
                        final_log[error_type] = []
                    final_log[error_type].extend(messages)

    for error_type, messages in final_log.items():
        error_counts[error_type] = len(messages)

    with open(final_log_file, 'w', encoding='utf-8') as flf:
        json.dump(final_log, flf, indent=4)

    summary_file_path = final_log_file.rsplit('.', 1)[0] + '_summary.json'
    with open(summary_file_path, 'w', encoding='utf-8') as sf:
        json.dump(error_counts, sf, indent=4)

    for log_file_name in os.listdir(log_dir):
        os.remove(os.path.join(log_dir, log_file_name))

def process_json_content(file_content, output_folder, zipped_output):
    subject_to_path_map = {}
    graph = ConjunctiveGraph()
    graph.parse(data=file_content, format='json-ld')
    for subject in graph.subjects(unique=True):
        _, cur_file_path = find_paths(subject, output_folder, BASE_IRI, "_", DIR_SPLIT, N_FILE_ITEM, IS_JSON)
        if zipped_output:
            cur_file_path = cur_file_path.replace('.json', '.zip')
        subject_to_path_map.setdefault(cur_file_path, []).append(subject)
    return graph, subject_to_path_map

def process_file(file_path, output_folder, log_dir, zipped_input, zipped_output, process_id, use_multiprocessing):
    if zipped_input:
        with zipfile.ZipFile(file_path, 'r') as zfile:
            for json_file_name in zfile.namelist():
                with zfile.open(json_file_name) as file:
                    file_content = file.read().decode('utf-8')
                    graph, subject_to_path_map = process_json_content(file_content, output_folder, zipped_output)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            graph, subject_to_path_map = process_json_content(file_content, output_folder, zipped_output)
    
    for cur_file_path, subjects in subject_to_path_map.items():
        if not os.path.exists(cur_file_path):
            error_message = f"File {cur_file_path} not found"
            log_error(log_dir, 'file_not_found', error_message, process_id)
            continue
        with FileLock(cur_file_path + ".lock"):
            target_graph = ConjunctiveGraph()
            if zipped_output:
                with zipfile.ZipFile(cur_file_path, 'r') as zfile:
                    json_file_name = zfile.namelist()[0]
                    with zfile.open(json_file_name) as file:
                        file_content = file.read().decode('utf-8')
            else:
                with open(cur_file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
            target_graph.parse(data=file_content, format='json-ld')
            update = False
            for subject in subjects:
                original_predicates = set(graph.predicates(subject, unique=True))
                target_predicates = set(target_graph.predicates(subject, unique=True))
                for predicate in original_predicates:
                    original_values = set(graph.objects(subject, predicate, unique=True))
                    target_values = set(target_graph.objects(subject, predicate, unique=True))
                    if original_values != target_values:
                        if predicate in target_predicates:
                            log_error(log_dir, 'different_predicate_value', f"Different values for predicate {predicate} for subject {subject} in {cur_file_path}", process_id)
                            context = target_graph.get_context(subject)
                            context.remove((subject, predicate, None))
                            for value in original_values:
                                context.add((subject, predicate, value))
                            update = True
                        else:
                            log_error(log_dir, 'missing_predicate', f"Predicate {predicate} missing for subject {subject} in {cur_file_path}", process_id)
            if update:
                if zipped_output:
                    with zipfile.ZipFile(cur_file_path, 'w') as zfile:
                        zfile.writestr(json_file_name, target_graph.serialize(format='json-ld', indent=None, ensure_ascii=False).encode('utf-8'))
                else:
                    with open(cur_file_path, 'w', encoding='utf-8') as file:
                        file.write(target_graph.serialize(format='json-ld', indent=None, ensure_ascii=False))
    if use_multiprocessing:
        queue.put(1)

def init_queue(q):
    global queue
    queue = q

def find_json_files(input_folder, exclude_dir='prov', zipped_input=None):
    """
    Recursively finds all files in the input folder, excluding those within directories named `exclude_dir`.
    """
    file_paths = []
    for root, dirs, files in os.walk(input_folder):
        if exclude_dir in root.split(os.sep):
            continue  # Skip files within directories named `exclude_dir`
        for file in files:
            if zipped_input and file.endswith('.zip'):
                file_paths.append(os.path.join(root, file))
            elif not zipped_input and file.endswith('.json'):
                file_paths.append(os.path.join(root, file))
    return file_paths

def main(input_folder, output_folder, use_multiprocessing, log_file_path, zipped_input, zipped_output):
    file_paths = find_json_files(input_folder, zipped_input=zipped_input)
    log_dir = log_file_path.rsplit('.', 1)[0] + "_logs"
    os.makedirs(log_dir, exist_ok=True)
    if use_multiprocessing:
        with Manager() as manager:
            queue = manager.Queue()
            with Pool(initializer=init_queue, initargs=(queue,)) as pool:
                for idx, filename in enumerate(file_paths):
                    file_path = os.path.join(input_folder, filename)
                    pool.apply_async(process_file, args=(file_path, output_folder, log_dir, zipped_input, zipped_output, idx, use_multiprocessing))
                pool.close()

                pbar = tqdm(total=len(file_paths))
                completed_tasks = 0
                while completed_tasks < len(file_paths):
                    queue.get()
                    completed_tasks += 1
                    pbar.update(1)
                pbar.close()

                pool.join()
    else:
        pbar = tqdm(file_paths, desc="Processing files", total=len(file_paths))
        for idx, filename in enumerate(file_paths):
            file_path = os.path.join(input_folder, filename)
            process_file(file_path, output_folder, log_dir, zipped_input, zipped_output, idx, use_multiprocessing)
            pbar.update()
        pbar.close()

    merge_logs(log_dir, log_file_path)
    shutil.rmtree(log_dir, ignore_errors=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process RDF data from JSONLD.GZ files.")
    parser.add_argument("input_folder", type=str, help="The folder containing .jsonld.gz files")
    parser.add_argument("output_folder", type=str, help="The folder to find matching files based on entities")
    parser.add_argument("--multiprocessing", action="store_true", help="Enable multiprocessing to process files")
    parser.add_argument("--log_file", type=str, required=True, help="The JSON file to log errors")
    parser.add_argument("--zipped_output", action="store_true", help="Indicate if the output files are zipped")
    parser.add_argument("--zipped_input", action="store_true", help="Indicate if the input files are zipped")

    args = parser.parse_args()

    main(args.input_folder, args.output_folder, args.multiprocessing, args.log_file, args.zipped_input, args.zipped_output)