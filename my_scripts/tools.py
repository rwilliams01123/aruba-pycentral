#!/usr/bin/env python3
# tools
'''
import as:
from tools import tools
'''
import os
import os.path
import json
import csv
from pprint import pprint
import re
import requests

def api_call_verify(method, url, headers, payload):
    response = requests.request(method, url, headers=headers, data=payload)
    if response.status_code >= 300:
        print(f'  ERROR: {response.text}')
    else:
        response = response.json()
        result = re.sub(r".+\.com\/(.+)", "\\1", url, 1)
        file_name = result.replace('/', '-')
        print(f'Success - {file_name}')
        export_json(response,'','','https__'+file_name)
        return response


def convertCsvToDict(csv_list):
    header = csv_list[0]
    del csv_list[0]
    new_list = [{x: i[header.index(x)] for x in header} for i in csv_list]
    return new_list


def moveDirectoryForward(folder_name):
    cwd = os.getcwd()
    if folder_name in cwd:
        return
    elif folder_name in os.listdir():
        os.chdir(folder_name)
        cwd = os.getcwd()
        return
    else:
        os.makedirs(folder_name)
        os.chdir(folder_name)
        cwd = os.getcwd()
        return


def moveDirectoryBack(folder_name):
    cwd = os.getcwd()
    if folder_name in cwd:
        head_tail = os.path.split(cwd)
        head = head_tail[0]
        os.chdir(head)
        cwd = os.getcwd()
    return


def quick_import_csv():
    quick_import = input("Import Desktop 0-api.csv file? [confirm]")
    if not quick_import:
        file_location = '/Users/robert/Desktop/0-api.csv'
    else:
        file_location = input("File location: ").strip().replace('\ ', ' ')
    #
    with open(file_location, 'r', encoding='utf-8-sig') as f:
        base_file = list(csv.DictReader(f))
    #
    update_file = [i for i in base_file if i['serial']]
    return update_file


def export_json(export_list, doc_number, siteName, file_name):
    if isinstance(doc_number, int):
        moveDirectoryForward('documentation')
    backup_filename = str(doc_number)+"-"+siteName+"-"+file_name+".json"
    backup_filename = backup_filename.replace('--', '-')
    backup_filename = re.sub(r'^-', '', backup_filename)
    #
    if backup_filename in os.listdir():
        file_exists = True
        file_addition = 1
        backup_filename = backup_filename.replace(".json", "(0).json")
        while (file_exists):
            backup_filename = re.sub(r"\(\d\)", f"({str(file_addition)})", backup_filename)
            if backup_filename in os.listdir():
                file_addition += 1
            else:
                file_exists = False
    #
    with open(backup_filename, 'w') as f:
        json.dump(export_list, f, indent=2)
    moveDirectoryBack('documentation')


def export_csv(export_list, doc_number, siteName, file_name):
    if isinstance(doc_number, int):
        moveDirectoryForward('documentation')
    backup_filename = str(doc_number)+"-"+siteName+"-"+file_name+".csv"
    backup_filename = backup_filename.replace('--', '-')
    backup_filename = re.sub(r'^-', '', backup_filename)
    #
    if backup_filename in os.listdir():
        file_exists = True
        file_addition = 1
        backup_filename = backup_filename.replace(".json", "(0).json")
        while (file_exists):
            backup_filename = re.sub(r"\(\d\)", f"({str(file_addition)})", backup_filename)
            if backup_filename in os.listdir():
                file_addition += 1
            else:
                file_exists = False
    #
    try:
        if isinstance(export_list, list) and isinstance(export_list[0], dict):
            keys = [x for i in export_list for x in i]
            csvheader = [x for i, x in enumerate(keys) if x not in keys[:i]]
            #
            with open(backup_filename, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(csvheader)
                for i in export_list:
                    csvrow = [i.get(x) for x in csvheader]
                    writer.writerow(csvrow)
        #
        elif isinstance(export_list, list) and isinstance(export_list[0], list):
            with open(backup_filename, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(export_list)
        #
        elif isinstance(export_list, list) and isinstance(export_list[0], str):
            with open(backup_filename,'w') as csvfile:
                writer = csv.writer(csvfile)
                for i in export_list:
                    writer.writerow([i])
        #
        elif isinstance(export_list, str):
            with open(backup_filename,'w') as csvfile:
                writer = csv.writer(csvfile)
                for i in export_list.splitlines(keepends=False):
                    writer.writerow([i])
        #
        else:
            print(f"Cannot export {export_list}")
    except:
        print(f"Cannot export {export_list}")
    #
    moveDirectoryBack('documentation')


def user_list_input():
    raw_entries = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        raw_entries.append(line)
         # Trim any blank entries
    entries = [i for i in raw_entries if i]
    return entries


def create_stepped_list(import_list, grouped_amount):
    '''
    Takes a called list and breaks the list up into a list of lists with the
    grouped_amount amount of entries.
    '''
    stepped_list = []
    start = 0
    end = len(import_list)
    step = grouped_amount
    for i in range(start, end, step):
        stepped_list.append(import_list[i:i+step])
    return stepped_list


def progress_report(list_length, iteration):
    '''
    Gives a percent finished after every 5 iterations. The iteration variable
    is used to keep track of the iteration of the external loop.

    Syntax:
    iteration = 0
    iteration = tools.progress_report(len(list_length), iteration)
    '''
    list_length = list_length-1
    try:
        progress = (iteration/(list_length))*100
    except:
        pass
    else:
        if iteration == list_length:
            print('100%')
        elif iteration % 5 == 0:
            print(f"{round(progress)}%")
    #
    iteration += 1
    return iteration
