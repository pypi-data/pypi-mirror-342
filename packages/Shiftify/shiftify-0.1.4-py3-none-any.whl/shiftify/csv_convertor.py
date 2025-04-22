"""
csv_convertor.py

A module to convert CSV files to various other formats.
Handles large CSV files by streaming data using Python's CSV module.
"""

import csv
import os
import json
import yaml
import pickle
from openpyxl import Workbook
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


class CSV:
    def __init__(self, csv_path):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"The file {csv_path} does not exist.")
        if os.path.getsize(csv_path) == 0:
            raise ValueError("The CSV file is empty.")
        self.csv_path = csv_path

    def to_json(self, json_file_path):
        """
        Converts CSV to a JSON array.
        The output file will contain a JSON array of objects.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(json_file_path, 'w', encoding='utf-8') as jsonfile:
                reader = csv.DictReader(csvfile)
                jsonfile.write('[')
                first = True
                for row in reader:
                    if not first:
                        jsonfile.write(',\n')
                    json.dump(row, jsonfile)
                    first = False
                jsonfile.write(']')
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to JSON: {e}")

    def to_sql(self, sql_file_path=None, table_name="table_name"):
        """
        Converts CSV rows into SQL INSERT statements.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                sql_statements = []
                for row in reader:
                    columns = ', '.join(row.keys())
                    # Escape single quotes in values
                    values = ', '.join(
                        f"'{str(value).replace('\'', '\'\'')}'" for value in row.values()
                    )
                    sql_statements.append(
                        f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
                    )
                sql_content = '\n'.join(sql_statements)

            if sql_file_path:
                with open(sql_file_path, 'w', encoding='utf-8') as f:
                    f.write(sql_content)
            else:
                return sql_content
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to SQL: {e}")

    def to_html(self, html_file_path):
        """
        Converts CSV to an HTML table.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(html_file_path, 'w', encoding='utf-8') as htmlfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                if not headers:
                    raise ValueError("CSV file does not contain headers.")
                
                htmlfile.write('<table border="1">\n')
                # Write table headers
                htmlfile.write('<tr>' + ''.join(f'<th>{header}</th>' for header in headers) + '</tr>\n')
                # Write table rows
                for row in reader:
                    htmlfile.write('<tr>' + ''.join(f'<td>{value}</td>' for value in row.values()) + '</tr>\n')
                htmlfile.write('</table>')
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to HTML: {e}")

    def to_text(self, text_file_path):
        """
        Converts CSV to plain text by writing each row (as a JSON string) on a new line.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(text_file_path, 'w', encoding='utf-8') as textfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    textfile.write(json.dumps(row, indent=4) + '\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to text: {e}")

    def to_yaml(self, yaml_file_path, key=None):
        """
        Converts CSV to YAML.
        If 'key' is provided, wraps each row's data in a dictionary under that key.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data_list = list(reader)
                if not data_list:
                    raise ValueError("CSV file is empty or does not contain valid data.")
                if key:
                    yaml_content = [{key: row} for row in data_list]
                else:
                    yaml_content = data_list

                with open(yaml_file_path, 'w', encoding='utf-8') as yamlfile:
                    yaml.dump(
                        yaml_content,
                        yamlfile,
                        default_flow_style=False,
                        sort_keys=False,
                        allow_unicode=True
                    )
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to YAML: {e}")

    def to_xml(self, xml_file_path, root_element="Root"):
        """
        Converts CSV to XML. Each CSV row becomes an <Item> element.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                root = ET.Element(root_element)
                for row in reader:
                    item_element = ET.SubElement(root, "Item")
                    for key, value in row.items():
                        child = ET.SubElement(item_element, key)
                        child.text = str(value)
                rough_string = ET.tostring(root, encoding='utf-8', method='xml')
                parsed = parseString(rough_string)
                pretty_xml = parsed.toprettyxml(indent="  ")
                with open(xml_file_path, 'w', encoding='utf-8') as xmlfile:
                    xmlfile.write(pretty_xml)
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to XML: {e}")

    def to_tsv(self, tsv_file_path):
        """
        Converts CSV to TSV (tab-separated values).
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(tsv_file_path, 'w', newline='', encoding='utf-8') as tsvfile:
                reader = csv.reader(csvfile)
                writer = csv.writer(tsvfile, delimiter='\t')
                for row in reader:
                    writer.writerow(row)
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to TSV: {e}")

    def to_toml(self, toml_file_path):
        """
        Converts CSV to TOML format.
        Since TOML supports dictionaries rather than arrays, each CSV row is stored as a key/value pair.
        """
        try:
            import toml
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                items = list(reader)
            toml_data = {f"item_{i}": item for i, item in enumerate(items)}
            with open(toml_file_path, 'w', encoding='utf-8') as tomlfile:
                toml.dump(toml_data, tomlfile)
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to TOML: {e}")

    def to_ndjson(self, ndjson_file_path):
        """
        Converts CSV to NDJSON (Newline-Delimited JSON).
        Each CSV row is output as a separate JSON object on its own line.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(ndjson_file_path, 'w', encoding='utf-8') as ndjsonfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ndjsonfile.write(json.dumps(row) + '\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to NDJSON: {e}")

    def to_excel(self, excel_file_path, sheet_name=None):
        """
        Converts CSV to an Excel spreadsheet.
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = sheet_name or "Sheet1"
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    ws.append(row)
            wb.save(excel_file_path)
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to Excel: {e}")

    def to_markdown_table(self, markdown_file_path):
        """
        Converts CSV to a Markdown table.
        Assumes the first row of the CSV contains headers.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(markdown_file_path, 'w', encoding='utf-8') as mdfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                if not rows:
                    raise ValueError("CSV file is empty or does not contain valid data.")
                # Write header row
                headers = rows[0]
                mdfile.write('| ' + ' | '.join(headers) + ' |\n')
                mdfile.write('| ' + ' | '.join(['---'] * len(headers)) + ' |\n')
                # Write data rows
                for row in rows[1:]:
                    mdfile.write('| ' + ' | '.join(row) + ' |\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to Markdown: {e}")

    def to_binary(self, binary_file_path):
        """
        Converts CSV rows into binary format using pickle.
        Each row is serialized separately with its length (in 4 bytes) prepended.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(binary_file_path, 'wb') as binaryfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    binary_data = pickle.dumps(row)
                    binaryfile.write(len(binary_data).to_bytes(4, byteorder='big'))
                    binaryfile.write(binary_data)
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to binary: {e}")

    def to_ini(self, ini_file_path, section_prefix="Section"):
        """
        Converts CSV to INI file format.
        Each CSV row is stored as a section.
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile, \
                 open(ini_file_path, 'w', encoding='utf-8') as inifile:
                reader = csv.DictReader(csvfile)
                for idx, row in enumerate(reader, start=1):
                    inifile.write(f'[{section_prefix}_{idx}]\n')
                    for key, value in row.items():
                        inifile.write(f'{key} = {value}\n')
                    inifile.write('\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting CSV to INI: {e}")