# Author: Shadmehr Ghorbani
# Github: https://github.com/shadmehr-gh/zinc_downloader
# Version: 1.0.0

import os
import sys

import requests
from colorama import Fore
# import wget
# import urllib3

zinc_id_list = []


def list_opener(input_id_list):
    try:
        url_list_file = open(input_id_list, 'r')
        url_list_file_lines = url_list_file.read().splitlines()

        for zinc_id in url_list_file_lines:
            zinc_id_list.append(zinc_id)

        # for item in zinc_id_list:
        #    print(item)
    except:
        print(Fore.RED + "No such file " + input_id_list + " exists.")
        print(Fore.RESET + "Exiting...")
        sys.exit()


def list_validator():
    for i in range(len(zinc_id_list)):
        if not zinc_id_list[i][0:4] == "ZINC":
            return False
    return True

def zinc_downloader(zinc_version, zinc_file_type):
    molecule_number = 1
    for item in zinc_id_list:
        print("Downloading molecule #" + str(molecule_number))
        print("Zinc ID: " + item)

        if not os.path.exists("dataset"):
            os.makedirs("dataset")

        url = "https://zinc" + zinc_version + ".docking.org/substances/" + item + "." + zinc_file_type
        response = requests.get(url)
        open("dataset/" + item + "." + zinc_file_type, "wb").write(response.content)

        molecule_number = molecule_number + 1

    print(Fore.GREEN + "All molecules downloaded successfully")
    print(Fore.RESET)


def zinc_merger(zinc_file_type):
    print("Merging final dataset...")

    if not os.path.exists("merged_dataset"):
        os.makedirs("merged_dataset")

    if os.path.exists("merged_dataset/final_dataset" + zinc_file_type):
        os.remove("merged_dataset/final_dataset" + zinc_file_type)

    f = open("merged_dataset/final_dataset." + zinc_file_type, "a")
    for item in zinc_id_list:
        try:
            separated_dataset_file = open("dataset/" + item + "." + zinc_file_type, 'r')
            separated_dataset_file_lines = separated_dataset_file.read().splitlines()

            for line in separated_dataset_file_lines:
                f.write(line + "\n")

        except:
            print(Fore.RED + "Unfortunately an error has occurred while merging files for final dataset.")
            print(Fore.RESET + "Exiting...")
            sys.exit()
    f.close()
    print(Fore.GREEN + "All molecules merged successfully")
    print(Fore.RESET)


def main():
    print(Fore.BLUE + "\n****************************************************")
    print("************* Zinc Molecule Downloader *************")
    print("****************************************************")
    print("************ Author: Shadmehr Ghorbani *************")
    print("** https://github.com/shadmehr-gh/zinc_downloader **")
    print("****************************************************\n")
    print(Fore.RESET + "Welcome.")

    zinc_version = input("Zinc version: (choose between 15 & 20)\n")
    while not (zinc_version == "15" or zinc_version == "20"):
        print(Fore.RED + "Invalid zinc version.")
        zinc_version = input(Fore.RESET + "Please choose a valid zinc version: (choose between 15 & 20)\n")
        if zinc_version == "15" or zinc_version == "20":
            break

    zinc_file_type = input("Which file type to download? (choose between sdf, smi, csv, xml, json)\n")
    while not (zinc_file_type == "sdf" or zinc_file_type == "smi" or zinc_file_type == "csv" or zinc_file_type == "xml" or zinc_file_type == "json"):
        print(Fore.RED + "Invalid file type.")
        zinc_file_type = input(Fore.RESET + "Please choose a valid file type: (choose between sdf, smi, csv, xml, json)\n")
        if zinc_file_type == "sdf" or zinc_file_type == "smi" or zinc_file_type == "csv" or zinc_file_type == "xml" or zinc_file_type == "json":
            break

    input_id_list = input("Zinc IDs list file: (default: list.txt; or to choose the default just press enter)\n")
    if input_id_list == "":
        input_id_list = "list.txt"
    list_opener(input_id_list)
    #while not os.path.exists(input_id_list):
        #print(Fore.RED + "No such file " + input_id_list + " exists.")
    #    input_id_list = input(Fore.RESET + "Please choose a valid zinc ids list file: (default: list.txt; to choose the default just press enter)\n")
    #    if input_id_list == "":
    #        input_id_list = "list.txt"
    #    list_opener(input_id_list)
    #    if os.path.exists(input_id_list):
    #1        break
    list_validation_state = list_validator()
    if list_validation_state == True:
        print(Fore.GREEN + "Zinc IDs list file is valid.")
        print(Fore.GREEN + "Your choosen list contains " + str(len(zinc_id_list)) + " molecules.")
        print(Fore.RESET)
    else:
        while not list_validation_state == True:
            print(Fore.RED + "The selected list has invalid zinc id entries. Please choose another.")
            input_id_list = input(Fore.RESET + "Please choose a valid zinc ids list file: (default: list.txt; to choose the default just press enter)\n")
            if input_id_list == "":
                input_id_list = "list.txt"
            zinc_id_list.clear()
            list_opener(input_id_list)
            list_validation_state = list_validator()
            if list_validation_state == True:
                print(Fore.GREEN + "Zinc IDs list file is valid.")
                print(Fore.GREEN + "Your choosen list contains " + str(len(zinc_id_list)) + " molecules.")
                print(Fore.RESET)
                break

    merge_bool = input("Merge files at the end? (type: yes or no)\n")
    while not (merge_bool == "yes" or merge_bool == "no"):
        merge_bool = input(Fore.RESET + "Just type yes or no:\n")
        if merge_bool == "yes" or merge_bool == "no":
            break

    print("****************************************************\n")

    zinc_downloader(zinc_version, zinc_file_type)

    print("****************************************************\n")

    if merge_bool == "yes":
        zinc_merger(zinc_file_type)


if __name__ == '__main__':
    main()
