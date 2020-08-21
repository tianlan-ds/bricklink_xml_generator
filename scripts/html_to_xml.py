#!/usr/bin/env python3
import sys
import logging

from xml_generator import html_file

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s [%(name)s] [%(process)d] %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main(html_name: str):
    soup = html_file.read_html_file(html_name)
    parser = html_file.HtmlTableParser(soup)
    xml_name = html_name.replace('.html', '.xml')
    parser.save_parsed_data_to_xml(xml_filename=xml_name)


if __name__ == "__main__":
    html_name = sys.argv[1]
    main(html_name)
