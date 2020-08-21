from typing import List, Dict
import logging

from lxml import etree
from lxml.builder import ElementMaker

from xml_generator.constants import ColumnNames, ONLY_NEW

logger = logging.getLogger(__name__)


class XmlGenerator:
    def __init__(self, input_data: List[Dict[str, str]], only_new: bool = ONLY_NEW):
        self._input_data: List[Dict[str, str]] = input_data
        self._only_new: bool = only_new

        self._em = ElementMaker()
        self._INVENTORY = self._em.INVENTORY
        self._ITEM = self._em.ITEM
        self._ITEM_TYPE = self._em.ITEMTYPE
        self._ITEM_ID = self._em.ITEMID
        self._COLOR = self._em.COLOR
        self._MIN_QTY = self._em.MINQTY
        self._CONDITION = self._em.CONDITION

        self._inventory = self._INVENTORY()

    def _build_item(self, item_data: Dict[str, str]):
        part_number = item_data.get(ColumnNames.PART_NUMBER)
        color_number = item_data.get(ColumnNames.COLOR_NUMBER)
        qty = item_data.get(ColumnNames.QUANTITY)

        item = self._ITEM(
            self._ITEM_TYPE('P'),
            self._ITEM_ID(part_number),
            self._COLOR(color_number),
            self._MIN_QTY(qty)
        )

        if self._only_new:
            item.append(self._CONDITION('N'))

        return item

    def _build_inventory(self):
        """
        Loop through self._input_data. Build an item a time and add the item into inventory.
        :return:
        """
        for item_data in self._input_data:
            item = self._build_item(item_data)
            self._inventory.append(item)

        logger.debug(etree.tostring(self._inventory, pretty_print=True))

    def save_to_xml_file(self, output_filename: str):
        self._build_inventory()

        tree = etree.ElementTree(self._inventory)
        tree.write(output_filename, pretty_print=True, xml_declaration=True, encoding="utf-8")

        logger.info(f'done saving xml file to {output_filename}')
