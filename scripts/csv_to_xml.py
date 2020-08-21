#!/usr/bin/env python3
import sys
import logging

from xml_generator.csv_file import read_csv_file
from xml_generator.xml_file import XmlGenerator

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s [%(name)s] [%(process)d] %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main(csv_name: str):
    data_list = read_csv_file(csv_name)

    xml_generator = XmlGenerator(input_data=data_list)
    xml_name = csv_name.replace('.csv', '.xml')
    xml_generator.save_to_xml_file(xml_name)


if __name__ == "__main__":
    html_name = sys.argv[1]
    main(html_name)
