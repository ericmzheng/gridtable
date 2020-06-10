import xml.etree.ElementTree as ET

class TableException(Exception):
    pass

class Table:
    def __init__(self, table_dict):
        self.table_dict = table_dict
        self.rows = set()
        self.cols = set()
        self.validate()

    def validate(self):
        errors = []
        if not isinstance(self.table_dict, dict):
            errors.append(f"First level of table is not a dictionary type: {self.table_dict.__class__}")
        else:
            for row in self.table_dict:
                self.rows.add(row)
                if not isinstance(row, str) and not isinstance(row, int):
                    errors.append(f"Key for row of table is not a string or int: {row.__class__}")
                if not isinstance(self.table_dict[row], dict):
                    errors.append(f"Column of table is not a dictionary type: {self.table_dict[row].__class__}")
                for col in self.table_dict[row]:
                    self.cols.add(col)
                    if not isinstance(col, str) and not isinstance(col, int):
                        errors.append(f"Key for column in row `{row}' of table is not a string or int: {col.__class__}")
        if errors:
            raise TableException("Unable to create table:\n- " + "\n- ".join(errors))

    def get_etree(self):
        table = ET.Element("table")
        table.set("border", "1")

        col_headers = ET.SubElement(table, "tr")
        ET.SubElement(col_headers, "th")
        for col in sorted(self.cols):
            th = ET.SubElement(col_headers, "th")
            th.set("style", "font-weight: bold; height: 200px; white-space: nowrap;")
            thdiv = ET.SubElement(th, "div")
            thdiv.set("style", "width: 30px; transform: rotate(90deg);")
            thdivdiv = ET.SubElement(thdiv, "div")
            thdivdiv.set("style", "padding: 10px 10px;")
            thdivdiv.text = str(col)
        for row in sorted(self.rows):
            tr = ET.SubElement(table, "tr")
            rh = ET.SubElement(tr, "td")
            rh.text = str(row)
            rh.set("style", "font-weight: bold;")

            for col in sorted(self.cols):
                td = ET.SubElement(tr, "td")
                if col in self.table_dict[row]:
                    td.text = str(self.table_dict[row][col])
                else:
                    td.text = ""

        return table

    def dump_html(self, fname):
        html = ET.Element("html")
        head = ET.SubElement(html, "head")
        title = ET.SubElement(head, "title")
        title.text = "Table Dump"
        body = ET.SubElement(html, "body")
        body.append(self.get_etree())

        page = ET.ElementTree()
        page._setroot(html)
        page.write(fname)

