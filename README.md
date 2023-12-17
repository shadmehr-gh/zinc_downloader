# Zinc Downloader
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\
Zinc Database Downloader &amp; Merger

Due to the Zinc15 & Zinc20 database website's limitations on downloading big dataset files in .sdf, .smi & other formats, this tool will help you to easily download any dataset you want based on your zinc ID's list file.

## Prerequired Python libraries:
requests\
colorama

## Prerequiered files:
Zinc ID's list:\
To create your Zinc ID's list you can download the CSV file of your preferred dataset and convert it to a list TXT file or create the list TXT file manually. Be aware that the Zinc ID's list file must be created in .txt format. For more information on how the final file has to be you can take a look at the [list.txt](list.txt) file existing in the project files.

## How to Run:
Use the following command to run the script:
```
python zinc_downloader.py
```

## Script options:
### 1. Select your preferred Zinc database version:
* Choose between 15 & 20:
```
15
```
which refers to https://zinc15.docking.org database
```
20
```
which refers to https://zinc20.docking.org database
### 2. Select your preferred Zinc file type to download:
* Choose between SDF, SMI, CSV, XML or JSON:
```
sdf
```
which refers to the Structured Data File
```
smi
```
which refers to the SMILES File
```
csv
```
which refers to the Comma-separated values
```
xml or json
```
which refers to the other supported formats
### 3. Select your prepared Zinc IDs list:
* Default is list.txt(list.txt)
* It's recommended to move the list file next to the main script to prevent further errors
### 4. Choose if you want to merge all downloaded molecules to a final_dataset file at the end:
* Choose between yes or no.

## Final outputs:
The script creates two separate folders in its related folder at the end:
### 1.
```
dataset
```
which contains all downloaded dataset molecules
### 2.
```
merged_dataset
```
which contains one molecule created by merging molecules in the dataset folder

## Contact:
For further support and any questions, you can contact me via:\
![Static Badge](https://img.shields.io/badge/Telegram%20-%20https%3A%2F%2Ft.me%2Fshadmehr_g%20-%20blue?style=flat&logo=telegram&color=blue&link=https%3A%2F%2Ft.me%2Fshadmehr_g)
