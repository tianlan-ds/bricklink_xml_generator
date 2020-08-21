from typing import List, Dict
import csv


def read_csv_file(filename: str) -> List[Dict[str, str]]:
    """
    Reading a csv file as a list of dictionaries, where the key is the column name.

    :param filename:
    :return:
    """
    final_list = []
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            row = dict(line)
            final_list.append(row)

    return final_list
