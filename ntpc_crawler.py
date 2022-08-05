import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from paddleocr import PaddleOCR
import threading
import json
import tempfile
import xml.dom.minidom
import pandas as pd

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_integer("license_year", None, "The year when the license was approved.")
flags.DEFINE_string("license_cat", None, "The category of the license.")
flags.DEFINE_integer("license_no", None, "The number of the license.")
flags.DEFINE_string("output_dir", None, "The directory for processed data.")

URL = "https://building-management.publicwork.ntpc.gov.tw/bm_query.jsp"

class CertificationCodeFetcher(threading.Thread):
    def __init__(self):
        super(CertificationCodeFetcher, self).__init__()
        self.code = None

    def run(self):
        self.code = self.get_certification_code()

    @staticmethod
    def get_certification_code(src):
        results = PaddleOCR(lang="en").ocr(src)
        detection, recognition = results[0]
        code, confidence = recognition
        return code

def get_driver(license_year, license_cat, license_no):
    driver = webdriver.Chrome()
    driver.get(URL)

    # The first page
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "/html//*//input[@value='關閉']")))
    driver.find_element(By.XPATH, "/html//*//input[@value='關閉']").click()
    driver.find_element(By.XPATH, "/html//*//input[@title='執照號碼-年度']").send_keys(str(license_year))
    driver.find_element(By.XPATH, "/html//*//input[@title='執照號碼-流水號']").send_keys(str(license_no))
    driver.find_element(By.XPATH, "/html//*//input[@title='執照號碼-類別(另開新視窗)']").click()

    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "/html//*//div[text()='{}']".format(str(license_cat)))))
    driver.find_element(By.XPATH, "/html//*//div[text()='{}']".format(str(license_cat))).click()
    driver.switch_to.window(driver.window_handles[0])

    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        driver.find_element(By.XPATH, "/html//*//img[@src='ImageServlet']").screenshot(f.name)
        driver.find_element(By.XPATH, "/html//*//input[@title='驗證碼']").send_keys(
            str(CertificationCodeFetcher.get_certification_code(f.name)))

    driver.find_element(By.XPATH, "/html//*//button[text()='查詢']").click()

    # The Second Page
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "/html//*//a[@class='list_row_link']")))
    driver.find_element(By.XPATH, "/html//*//a[@class='list_row_link']").click()
    return driver

def get_all_tables(driver):
    elems = driver.find_elements(By.XPATH, "/html//*//table[@class='responstable']")
    sources = ["<table>{}</table>".format(e.get_attribute("innerHTML")) for e in elems]
    sources = [xml.dom.minidom.parseString(s).toprettyxml() for s in sources]
    return sources

class DataElementGenerator:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return self.__next__()

    def __next__(self):
        return self.next()

    def next(self):
        for child in [node for node in self.data.childNodes if not __class__.is_skipped(node)]:
            if not [node for node in child.childNodes if not __class__.is_skipped(node)]:
                yield child
            yield from DataElementGenerator(child)

    @staticmethod
    def is_skipped(elem):
        return elem.nodeName in ["#text", "a"] or "hidden" in elem.getAttribute("class")

    @staticmethod
    def get_text(elem):
        if not elem.childNodes:
            return elem.nodeValue
        return "".join([__class__.get_text(e).strip() for e in elem.childNodes])

def analyze_table(xmlstr, mode):
    if mode == "key-value-pairs":
        return analyze_key_value_table(xmlstr=xmlstr)
    elif mode == "row-column-table":
        return analyze_row_column_table(xmlstr=xmlstr)

    raise(ValueError("Invalid mode."))

def analyze_key_value_table(xmlstr):
    data = {}
    xml_data = xml.dom.minidom.parseString(xmlstr).documentElement
    tb_title = None
    tb_header = None
    tb_data = None
    for elem in DataElementGenerator(xml_data):
        if elem.getAttribute("class") == "tb_title":
            tb_title = DataElementGenerator.get_text(elem)
            data[tb_title] = {}
        elif elem.tagName == "th":
            tb_header = DataElementGenerator.get_text(elem).strip()
        elif elem.tagName == "td" and tb_header:
            tb_data = DataElementGenerator.get_text(elem).strip()
            data[tb_title][tb_header] = tb_data
            tb_header = None
            tb_data = None

    return data

def analyze_row_column_table(xmlstr):
    data = {}
    xml_data = xml.dom.minidom.parseString(xmlstr).documentElement
    tb_title = None
    for elem in DataElementGenerator(xml_data):
        if elem.getAttribute("class") == "tb_title":
            tb_title = DataElementGenerator.get_text(elem)
            data[tb_title] = {}
            index = 0
            columns = []
            is_index_incremented = False
        elif elem.tagName == "th":
            column = DataElementGenerator.get_text(elem).strip()
            if column in columns:
                continue

            columns.append(column)
            data[tb_title][columns[-1]] = []
            if len(columns) > 1 and is_index_incremented:
                index = (index - 1) % (len(columns) - 1)
                index = (index + 1) % len(columns)
                is_index_incremented = False

        elif elem.tagName == "td" and columns:
            data[tb_title][columns[index]].append(DataElementGenerator.get_text(elem).strip())
            index = (index + 1) % len(columns)
            is_index_incremented = True

    return data

def run_driver(license_no):
    driver = get_driver(license_year=110, license_cat="建造執照", license_no=license_no)
    tables = get_all_tables(driver)
    driver.quit()
    return tables

def main(argv):
    del argv

    if FLAGS.license_year is None \
        or FLAGS.license_cat is None \
        or FLAGS.license_no is None \
        or FLAGS.output_dir is None:
        raise(ValueError(
            "The parameters need to be provided, please use --help for more details."))

    driver = get_driver(
        license_year=FLAGS.license_year,
        license_cat=FLAGS.license_cat,
        license_no=FLAGS.license_no)
    tables = get_all_tables(driver)
    driver.quit()

    ANALYSIS = [
        ("基本資料", "key-value-pairs"),
        ("執照基本資料", "key-value-pairs"),
        ("起造人資料", "key-value-pairs"),
        ("起造人變更", "row-column-table"),
        ("設計人資料", "key-value-pairs"),
        ("監造人資料", "key-value-pairs"),
        ("承造人資料", "key-value-pairs"),
        ("地號資料", "row-column-table"),
        ("樓層概要資料", "row-column-table"),
        ("相關執照", "key-value-pairs"),
    ]

    SUB_FOLDERS = [
        "xml",
        "json",
        "csv"
    ]

    for folder in [os.path.join(FLAGS.output_dir, rel_path) for rel_path in SUB_FOLDERS]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for analysis, table in zip(ANALYSIS, tables):
        title, analysis_mode = analysis
        output_path = os.path.join(FLAGS.output_dir, "xml", title)
        with open(f"{output_path}.xml", "w") as f:
            f.write(table)

        print(f"Processing '{title}'...")
        output_path = os.path.join(FLAGS.output_dir, "json", title)
        json_data = analyze_table(table, analysis_mode)
        with open(f"{output_path}.json", "w") as f:
            f.write(json.dumps(json_data, indent=2, ensure_ascii=False))

        output_path = os.path.join(FLAGS.output_dir, "csv", title)
        with open(f"{output_path}.csv", "w") as f:
            for table_name, table_data in json_data.items():
                if analysis_mode == "key-value-pairs":
                    table_data = {k: [v] for k, v in table_data.items()}
                f.write(f"{table_name}\n")
                f.write(pd.DataFrame.from_dict(table_data).to_csv(index=False))
                f.write("\n" * 2)


if __name__ == "__main__":
    app.run(main)

