# Author: Shadmehr Ghorbani, Bibhu Prasad
# Github: https://github.com/shadmehr-gh/zinc_downloader
# Version: 1.1.0

import os
import sys
import requests
from colorama import Fore
from tqdm import tqdm
import concurrent.futures

def download_molecule(zinc_id, zinc_version, zinc_file_type):
    url = f"https://zinc{zinc_version}.docking.org/substances/{zinc_id}.{zinc_file_type}"
    file_path = f"dataset/{zinc_id}.{zinc_file_type}"

    # Check if the file already exists
    if os.path.exists(file_path):
        print(Fore.GREEN + f"Skipping {zinc_id}.{zinc_file_type} (already downloaded)" + Fore.RESET)
        return

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(Fore.GREEN + f"Downloaded {zinc_id}.{zinc_file_type}" + Fore.RESET)
        else:
            print(Fore.RED + f"Failed to download {zinc_id}.{zinc_file_type}" + Fore.RESET)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error downloading {zinc_id}.{zinc_file_type}: {e}" + Fore.RESET)

def list_opener(input_id_list):
    try:
        with open(input_id_list, 'r') as url_list_file:
            zinc_id_list = url_list_file.read().splitlines()
    except FileNotFoundError:
        print(Fore.RED + f"No such file {input_id_list} exists.")
        print(Fore.RESET + "Exiting...")
        sys.exit()

    valid_zinc_ids = []
    for zinc_id in zinc_id_list:
        if zinc_id.startswith("ZINC"):
            valid_zinc_ids.append(zinc_id)

    if not valid_zinc_ids:
        print(Fore.RED + "No valid zinc IDs found in the list.")
        print(Fore.RESET + "Exiting...")
        sys.exit()

    return valid_zinc_ids

def zinc_merger(zinc_file_type, zinc_id_list):
    print("Merging final dataset...")

    if not os.path.exists("merged_dataset"):
        os.makedirs("merged_dataset")

    merged_file_path = f"merged_dataset/final_dataset.{zinc_file_type}"
    if os.path.exists(merged_file_path):
        os.remove(merged_file_path)

    with open(merged_file_path, "a") as f:
        for zinc_id in zinc_id_list:
            try:
                file_path = f"dataset/{zinc_id}.{zinc_file_type}"
                if os.path.exists(file_path):
                    with open(file_path, 'r') as molecule_file:
                        f.write(molecule_file.read() + "\n")
            except Exception as e:
                print(Fore.RED + f"Error while merging {zinc_id}.{zinc_file_type}: {e}" + Fore.RESET)

    print(Fore.GREEN + "All molecules merged successfully" + Fore.RESET)

def main():
    print(Fore.BLUE + "\n****************************************************")
    print("************* Zinc Molecule Downloader *************")
    print("****************************************************")
    print("****** Author:Shadmehr Ghorbani, Bibhu Prasad ******")
    print("** https://github.com/shadmehr-gh/zinc_downloader **")
    print("****************************************************\n")
    print(Fore.RESET + "Welcome.")

    zinc_version = input("Zinc version: (choose between 15 & 20)\n")
    while zinc_version not in ["15", "20"]:
        print(Fore.RED + "Invalid zinc version.")
        zinc_version = input(Fore.RESET + "Please choose a valid zinc version: (choose between 15 & 20)\n")

    zinc_file_type = input("Which file type to download? (choose between sdf, smi, csv, xml, json)\n")
    while zinc_file_type not in ["sdf", "smi", "csv", "xml", "json"]:
        print(Fore.RED + "Invalid file type.")
        zinc_file_type = input(Fore.RESET + "Please choose a valid file type: (choose between sdf, smi, csv, xml, json)\n")

    input_id_list = input("Zinc IDs list file: (default: list.txt; or to choose the default just press enter)\n") or "list.txt"
    zinc_id_list = list_opener(input_id_list)

    print(Fore.GREEN + f"Your chosen list contains {len(zinc_id_list)} molecules." + Fore.RESET)

    merge_bool = input("Merge files at the end? (type: yes or no)\n")
    while merge_bool not in ["yes", "no"]:
        merge_bool = input(Fore.RESET + "Just type yes or no:\n")

    print("****************************************************\n")

    os.makedirs("dataset", exist_ok=True)

    # Download molecules using multithreading
    max_workers = os.cpu_count() * 2  # Adjust the number of workers as needed
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_molecule, zinc_id, zinc_version, zinc_file_type) for zinc_id in zinc_id_list]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), unit="molecules"):
            try:
                future.result()
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Fore.RESET)

    print("****************************************************\n")

    if merge_bool == "yes":
        zinc_merger(zinc_file_type, zinc_id_list)

if __name__ == '__main__':
    main()
