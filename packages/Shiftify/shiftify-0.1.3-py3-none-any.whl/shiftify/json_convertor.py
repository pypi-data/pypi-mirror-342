"""
json_convertor.py

A module to convert Json files to various other formats.
Handles large Json files by streaming data using Python's ijson module.
"""

import csv
import os
import json
import ijson
import yaml
import pickle
from openpyxl import Workbook
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

class JSON:
    def __init__(self, json_path):
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"The file {json_path} does not exist.")
        if os.path.getsize(json_path) == 0:
            raise ValueError("The JSON file is empty.")
        
        self.json_path = json_path

    def to_csv(self, csv_file_path, delimiter=',', quotechar='"'):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
                 open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                items = ijson.items(jsonfile, 'item')
                first_item = next(items)
                fieldnames = first_item.keys()
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter, quotechar=quotechar)
                writer.writeheader()
                writer.writerow(first_item)
                
                for item in items:
                    writer.writerow(item)
        except StopIteration:
            raise ValueError("JSON file is empty or does not contain a valid array.")
        except Exception as e:
            raise Exception(f"An error occurred while converting to CSV: {e}")

    def to_sql(self, sql_file_path=None, table_name="table_name"):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile:
                items = ijson.items(jsonfile, 'item')

                sql_statements = []
                for record in items:
                    columns = ', '.join(record.keys())
                    values = ', '.join(f"'{str(value).replace('\'', '\'\'')}'" for value in record.values())
                    sql_statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
                
                sql_content = '\n'.join(sql_statements)

                if sql_file_path:
                    with open(sql_file_path, 'w', encoding='utf-8') as f:
                        f.write(sql_content)
                else:
                    return sql_content
        except StopIteration:
            raise ValueError("JSON file is empty or does not contain a valid array.")
        except Exception as e:
            raise Exception(f"An error occurred while converting to SQL: {e}")

    def to_html(self, html_file_path):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
                 open(html_file_path, 'w', encoding='utf-8') as htmlfile:
                
                items = ijson.items(jsonfile, 'item')
                first_item = next(items)
                
                htmlfile.write('<table border="1">\n<tr>')
                htmlfile.write(''.join(f'<th>{key}</th>' for key in first_item.keys()))
                htmlfile.write('</tr>\n')
                
                def write_row(item):
                    return '<tr>' + ''.join(f'<td>{value}</td>' for value in item.values()) + '</tr>\n'

                htmlfile.write(write_row(first_item))
                for item in items:
                    htmlfile.write(write_row(item))
                
                htmlfile.write('</table>')
        except StopIteration:
            raise ValueError("JSON file is empty or does not contain a valid array.")
        except Exception as e:
            raise Exception(f"An error occurred while converting to HTML: {e}")

    def to_text(self, text_file_path):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
                 open(text_file_path, 'w', encoding='utf-8') as textfile:

                items = ijson.items(jsonfile, 'item')
                for item in items:
                    textfile.write(json.dumps(item, indent=4) + '\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting to text: {e}")

    def to_yaml(self, yaml_file_path, key=None):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile:
                # Stream JSON items incrementally
                items = ijson.items(jsonfile, 'item')

                # Convert streamed items into a list (still efficient for large files)
                data_list = list(items)
                
                if not data_list:
                    raise ValueError("JSON file is empty or does not contain a valid array.")

                if key:
                    # Wrap each item in a dictionary under the given key
                    yaml_content = [{key: item} for item in data_list]
                else:
                    # Use data as-is without a master key
                    yaml_content = data_list

                # Dump the YAML content with prettier formatting
                with open(yaml_file_path, 'w', encoding='utf-8') as yamlfile:
                    yaml.dump(
                        yaml_content,
                        yamlfile,
                        default_flow_style=False,  # Use block-style formatting
                        sort_keys=False,          # Maintain the key order
                        allow_unicode=True        # Handle special characters
                    )
        except ValueError as ve:
            raise ValueError(f"An error occurred: {ve}")
        except Exception as e:
            raise Exception(f"An error occurred while converting to YAML: {e}")


    def to_xml(self, xml_file_path, root_element="Root"):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile:
                items = ijson.items(jsonfile, 'item')

                root = ET.Element(root_element)
                for item in items:
                    item_element = ET.SubElement(root, "Item")
                    for key, value in item.items():
                        child = ET.SubElement(item_element, key)
                        child.text = str(value)

                # Convert the ElementTree to a string
                rough_string = ET.tostring(root, encoding='utf-8', method='xml')

                # Beautify the XML string
                parsed = parseString(rough_string)
                pretty_xml = parsed.toprettyxml(indent="  ")

                # Write the beautified XML to the file
                with open(xml_file_path, 'w', encoding='utf-8') as xmlfile:
                    xmlfile.write(pretty_xml)
        except Exception as e:
            raise Exception(f"An error occurred while converting to XML: {e}")
        
    def to_tsv(self, tsv_file_path):
        self.to_csv(tsv_file_path, delimiter='\t')

    def to_toml(self, toml_file_path):
        try:
            import toml
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile:
                items = list(ijson.items(jsonfile, 'item'))  # Load all items
            
            # Convert JSON to TOML format (TOML supports dicts, not arrays directly)
            toml_data = {f"item_{i}": item for i, item in enumerate(items)}
            
            with open(toml_file_path, 'w', encoding='utf-8') as tomlfile:
                toml.dump(toml_data, tomlfile)
        except Exception as e:
            raise Exception(f"An error occurred while converting to TOML: {e}")
    
    def to_ndjson(self, ndjson_file_path):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
                open(ndjson_file_path, 'w', encoding='utf-8') as ndjsonfile:
                items = ijson.items(jsonfile, 'item')
                for item in items:
                    ndjsonfile.write(json.dumps(item) + '\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting to NDJSON: {e}")
        
    def to_excel(self, excel_file_path, sheet_name=None):
        # Create a workbook and a worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name or "Sheet1"

        with open(self.json_path, 'r', encoding='utf-8') as jsonfile:
            # Use ijson to stream the JSON data
            items = ijson.items(jsonfile, 'item')

            # Write headers (keys of the first item)
            first_item = next(items, None)
            if not first_item:
                raise ValueError("JSON file is empty or does not contain a valid array.")
            headers = list(first_item.keys())
            ws.append(headers)  # Append headers as the first row

            # Write the first row of data
            ws.append(list(first_item.values()))

            # Write the rest of the rows
            for item in items:
                ws.append(list(item.values()))

        # Save the workbook to the specified file path
        wb.save(excel_file_path)
    
    def to_markdown_table(self, markdown_file_path):
        with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
             open(markdown_file_path, 'w', encoding='utf-8') as mdfile:
            
            items = ijson.items(jsonfile, 'item')
            headers_written = False
            for item in items:
                if not headers_written:
                    mdfile.write('| ' + ' | '.join(item.keys()) + ' |\n')
                    mdfile.write('| ' + ' | '.join(['---'] * len(item.keys())) + ' |\n')
                    headers_written = True
                mdfile.write('| ' + ' | '.join(map(str, item.values())) + ' |\n')
    
    def to_binary(self, binary_file_path):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
                open(binary_file_path, 'wb') as binaryfile:
                
                # Use ijson to stream items from JSON
                items = ijson.items(jsonfile, 'item')
                
                # Iterate over items and write each to the binary file
                for item in items:
                    # Serialize each item into binary format using pickle
                    binary_data = pickle.dumps(item)
                    # Write the binary data length first (to know where each item ends)
                    binaryfile.write(len(binary_data).to_bytes(4, byteorder='big'))
                    # Write the binary data
                    binaryfile.write(binary_data)
        except Exception as e:
            raise Exception(f"An error occurred while converting to binary: {e}")
    

    def to_ini(self, ini_file_path, section_prefix="Section"):
        """
        Converts the JSON array into an INI file format, where each JSON object becomes a section.
        
        :param ini_file_path: The file path to write the INI output.
        :param section_prefix: Prefix for each section name (e.g., Section_1, Section_2, ...).
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as jsonfile, \
                open(ini_file_path, 'w', encoding='utf-8') as inifile:
                
                items = list(ijson.items(jsonfile, 'item'))
                if not items:
                    raise ValueError("JSON file is empty or does not contain a valid array.")
                
                for idx, item in enumerate(items, start=1):
                    inifile.write(f'[{section_prefix}_{idx}]\n')
                    for key, value in item.items():
                        inifile.write(f'{key} = {value}\n')
                    inifile.write('\n')
        except Exception as e:
            raise Exception(f"An error occurred while converting to INI: {e}")