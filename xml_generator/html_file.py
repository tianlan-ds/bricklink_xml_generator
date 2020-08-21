from typing import List, Dict
import csv
import re
import logging

from bs4 import BeautifulSoup

from xml_generator.constants import ColumnNames, LDCAD, ColorNumberMapping
from xml_generator.xml_file import XmlGenerator

logger = logging.getLogger(__name__)


def read_html_file(filename: str) -> BeautifulSoup:
    f = open(filename, encoding="utf8")
    soup = BeautifulSoup(f, features='lxml')
    f.close()
    return soup


class HtmlTableParser:
    class TableKeywords:
        PART = 'Part'
        COLOR = 'Color'
        QUANTITY = 'Quantity'
        DESCRIPTION = 'Description'

    HEAD_LIST = [TableKeywords.PART, TableKeywords.COLOR, TableKeywords.QUANTITY, TableKeywords.DESCRIPTION]

    def __init__(self, soup: BeautifulSoup):
        self._soup: BeautifulSoup = soup

        self._table_list: List = [table for table in soup.find_all('table')]
        self._key_table = self._determine_key_table()

        self._parsed_data: List[Dict[str, str]] = []

    def _determine_key_table(self):
        """
        Based on self._table_list, find out which table is the one with data.
        :return: table with data
        """
        possible_tables = []

        for table in self._table_list:
            tr_list = [tr for tr in table.find_all('tr')]
            for tr in tr_list:
                th_list = [th.text for th in tr.find_all('th')]
                if th_list == self.HEAD_LIST:
                    possible_tables.append(table)

        if len(possible_tables) == 0:
            raise Exception('unable to to parse the table content')
        elif len(possible_tables) > 1:
            raise Exception('multiple possible tables detected')
        else:
            return possible_tables[0]

    @staticmethod
    def _parse_row_content(tr, column_name: str) -> str:
        if column_name == ColumnNames.COLOR_DESCRIPTION:
            result_list = [td.text for td in tr.find_all('td', rowspan="2")]
        else:
            if column_name in [ColumnNames.PART_NUMBER, ColumnNames.PART_DESCRIPTION]:
                class_ = None
            elif column_name == ColumnNames.QUANTITY:
                class_ = ColumnNames.QUANTITY
            else:
                exception_msg = f"input {column_name} is not a supported column name"
                raise Exception(exception_msg)

            result_list = [td.text for td in tr.find_all('td', class_=class_)]

        if len(result_list) == 0:
            exception_msg = f'failed to parse the row content: {tr}'
            raise Exception(exception_msg)
        elif column_name in [ColumnNames.COLOR_NUMBER, ColumnNames.QUANTITY, ColumnNames.COLOR_DESCRIPTION]:
            if len(result_list) > 1:
                exception_msg = f"parsed multiple values for column {column_name}: {result_list}"
                raise Exception(exception_msg)
            else:
                column_value = result_list[0]
        elif column_name == ColumnNames.PART_NUMBER:
            column_value = result_list[0]
        elif column_name == ColumnNames.PART_DESCRIPTION:
            column_value = result_list[-1]

        # remove the extra letters in the part number if it contains
        if column_name == ColumnNames.PART_NUMBER:
            if not column_value.isnumeric():
                column_value = re.sub(r'[a-z]+', '', column_value, re.I)

        return column_value

    def parse_table_content(self) -> List[Dict[str, str]]:
        """
        Loop through the rows in the self._key_table and parse the content for each row.
        :return: the parsed data in the list of dictionaries.
        """
        tr_list = [tr for tr in self._key_table.find_all('tr')]
        for tr in tr_list:
            try:
                part_number = self._parse_row_content(tr, ColumnNames.PART_NUMBER)
                color_desc = self._parse_row_content(tr, ColumnNames.COLOR_DESCRIPTION)
                color_number = ColorNumberMapping.get(color_desc.lower(), None)
                if color_number is None:
                    exception_msg = f"unable to find the color number for {color_desc.lower()}"
                    raise Exception(exception_msg)
                quantity =  self._parse_row_content(tr, ColumnNames.QUANTITY)
                desc = self._parse_row_content(tr, ColumnNames.PART_DESCRIPTION)
            except Exception as e:
                logger.debug(e)
                continue

            row = {ColumnNames.PART_NUMBER: part_number,
                   ColumnNames.QUANTITY: quantity,
                   ColumnNames.COLOR_DESCRIPTION: color_desc,
                   ColumnNames.COLOR_NUMBER: color_number,
                   ColumnNames.PART_DESCRIPTION: desc}

            # if 'LDCad' is in the description, ignore the row
            if LDCAD in desc:
                msg = f'the following row is ignored: {row}'
                logger.warning(msg)
                continue

            self._parsed_data.append(row)

        return self._parsed_data

    def save_parsed_data_to_csv(self, csv_filename: str):
        self.parse_table_content()

        with open(csv_filename, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file,
                                fieldnames=self._parsed_data[0].keys())
            fc.writeheader()
            fc.writerows(self._parsed_data)

        logger.info(f'done writing {len(self._parsed_data)} rows parsed data into {csv_filename}')

    def save_parsed_data_to_xml(self, xml_filename: str):
        self.parse_table_content()

        xml_generator = XmlGenerator(input_data=self._parsed_data)
        xml_generator.save_to_xml_file(xml_filename)
