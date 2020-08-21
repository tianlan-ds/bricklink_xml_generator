import sys
import logging

from bs4 import BeautifulSoup
from xml_generator.csv_file import read_csv_file
from xml_generator.xml_file import XmlGenerator

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s [%(name)s] [%(process)d] %(message)s',
                    stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# def main():
    # file_name = 'rock_crawler.html'
    # f = open(file_name, encoding="utf8")
    # soup = BeautifulSoup(f, features='lxml')
    # f.close()
    #
    # # print(soup)
    #
    # table_list = [table for table in soup.find_all('table')]
    # # print(len(table_list))
    #
    # table = table_list[1]
    # tr_list = [tr for tr in table.find_all('tr')]
    # # print(tr_list[0])
    # th_list = [th.text for th in tr_list[0].find_all('th')]
    # print(th_list)
    #
    # print(tr_list[1])
    # part_number_list = [td.text for td in tr_list[1].find_all('td', class_=None)]
    # print(part_number_list[0])
    # color_number_list = [td.text for td in tr_list[1].find_all('td', class_="colorNumber")]
    # print(color_number_list)
    # quantity_list = [td.text for td in tr_list[1].find_all('td', class_="quantity")]
    # print(quantity_list)
    # desc_list = [td.text for td in tr_list[1].find_all('td', class_=None)]
    # print(desc_list[-1])
    # color_name_list = [td.text for td in tr_list[1].find_all('td', rowspan="2")]
    # print(color_name_list[0])

def main():
    file_name = 'rock_crawler_parts_mod.csv'
    data_list = read_csv_file(file_name)

    xml_generator = XmlGenerator(input_data=data_list)
    output_file_name = file_name.replace('.csv', '.xml')
    xml_generator.save_to_xml_file(output_file_name)

if __name__ == "__main__":
    main()
