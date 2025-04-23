import datetime
import json
import os
import re
import shutil
import tempfile
import time
import zipfile
from os.path import join as joinpath

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import Bbox
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Table, TableStyle, XPreformatted)

from cod_plugin import CODPlugin


class PDFGenerator(CODPlugin):
    graph_format = {
        "figsizex": 10,
        "figsizey": 8,
        "fontsize": 2,
        "width": 220,
        "height": 180
    }

    ascii_table_format = {
        "tablefmt": "pipe",
        "styles": "BodyText",
        "fontName": "Courier",
        "fontSize": 7,
        "wordWrap": "CJK"
    }

    graph_title_format = {
        "tablefmt": "pipe",
        "styles": "BodyText",
        "fontName": "Courier",
        "fontSize": 9,
        "wordWrap": "CJK"
    }

    main_header_format = {
        "styles": "Heading1",
        "fontName": "Courier",
        "fontSize": 10,
        "wordWrap": "CJK"
    }

    header_format = {
        "styles": "BodyText",
        "fontName": "Courier",
        "fontSize": 7,
        "wordWrap": "CJK"
    }

    graph_header_format = {
        "styles": "BodyText",
        "fontName": "Courier",
        "fontSize": 7,
        "wordWrap": "CJK"
    }

    Table_Style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add grid lines
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),  # Use monospace font
        ('FONTSIZE', (0, 0), (-1, -1), 7),  # Adjust font size as needed
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('SET_ROWHEIGHTS', (0, 0), (-1, -1), [1])
    ])

    date_pdf = datetime.datetime.now()
    suffix_pdf = date_pdf.strftime("%Y.%m.%d.%H.%M.%S")

    def __init__(self, zip_input_path, output_folder, api_url=None, cookies=None, logger=None, **kwargs):
        super(PDFGenerator, self).__init__(zip_input_path, output_folder, api_url, cookies, logger=logger, **kwargs)

        self.data = None
        self.batchid = None
        self.batchname = None
        self.folder_path = None
        self.png_folder = None
        self.local_path = tempfile.TemporaryDirectory().name

        self.forced_output_location = kwargs.get("forced_output_location", None)
        self.special_atl = kwargs.get("special_atl", False)
        self.new_pdfs = []
        
        self.config = {}
        self.config["graph_format"] = self.graph_format
        self.config["ascii_table_format"] = self.ascii_table_format
        self.config["header_format"] = self.header_format
        self.config["zip_input_path"] = zip_input_path
        self.config["output_folder"] = output_folder
        self.config["suffix_pdf"] = self.suffix_pdf
        self.config["Table_Style"] = self.Table_Style
        self.config["graph_title_format"] = self.graph_title_format
        self.config["graph_header_format"] = self.graph_header_format
        self.config["main_header_format"] = self.main_header_format

        self.config["url"] = "https://agricod.fujitsu-systems-europe.com/"
        self.config["title_text"] = "Fujitsu Systems Europe - Chromatography on Demand"
        self.config["graph_selection_mode"] = "validation"
        self.config["ascii_table_headers"] = ["*", "Name", "Validation", "ISTD", 'RT', 'Quantitative', 'Qualifier', 'Area', 'Dev RT', 'Conc.(µg/l)', 'Link']
        self.config = self._deep_merge_dicts(self.config, kwargs)

        self._sanitize_config()

        self.table = {}

    def generate_before_modification_report(self):
        self.config["title_text"] = "Advanced Technology Laboratories - Quality Environmental Testing"
        self.config['url'] = "https://agricod.fujitsu-systems-europe.com/"

        self.config["graph_selection_mode"] = "classification"
        self.config["ascii_table_headers"] = ["*", "Name", "Classification", "ISTD", 'RT', 'Quantitative', 'Qualifier', 'Area', 'Dev RT', 'Conc.(µg/l)', 'Link']

        self.config["folder_path"] = os.path.join(self.ouptut_folder, 'pdfs')
        self.config["pdf_name"] = ""
        self.config["suffix_pdf"] = ""
        self.config["only_one_pdf"] = False

        self.logger.info("Start PDF creation process (call before)")
        self.generate_report()
        self.logger.info("End PDF creation process (call before)")

    def generate_after_modification_report(self):
        self.config["title_text"] = "Advanced Technology Laboratories - Quality Environmental Testing"
        self.config['url'] = "https://agricod.fujitsu-systems-europe.com/"

        self.config["graph_selection_mode"] = "validation"
        self.config["ascii_table_headers"] = ["*", "Name", "Validation", "ISTD", 'RT', 'Quantitative', 'Qualifier', 'Area', 'Dev RT', 'Conc.(µg/l)', 'Link']

        self.config["folder_path"] = os.path.join(self.ouptut_folder, 'pdfs')
        self.config["pdf_name"] = ""
        self.config["suffix_pdf"] = ""

        self.config["only_one_pdf"] = False

        self.logger.info("Start PDF creation process")
        self.generate_report()
        self.logger.info("End PDF creation process")

    def generate_report(self):
        t0 = time.time()
        self.logger.info(f"Generate pdfs for {self.zip_input_path}")
        self.logger.debug("CONFIG:", self.config)

        try:
            self._validate_data()
        except Exception as e:
            self.logger.error(e)

        try:
            self.data = self.read_json_file()
        except Exception as e:
            self.logger.exception("An error occurred while reading the JSON file: ")

        try:
            self.set_data()
        except Exception as e:
            self.logger.exception("An error occurred while setting data: ")

        try:
            self.set_folder_path()
        except Exception as e:
            self.logger.exception("An error occurred while setting folder path: ")

        try:
            emptylinestyle = self.set_empty_line_style()
            emptyline = self.set_empty_line(emptylinestyle)
            mainheaderstyle = self.set_main_header_style()
            headerstyle = self.set_header_style()
            graphstitlestyle = self.set_graphs_title_style()
            graphsheaderstyle = self.set_graphs_header_style()

            elements_all = []
            for analysis_result in self.table.values():
                try:
                    analysis_name = analysis_result[0]["Analysis_Name"]

                    self.logger.info(f"  Start generate elements for analysis: {analysis_name}")
                    t1 = time.time()
                    elements = []
                    counter = 0
                    for molecule in analysis_result:
                        if counter == 0:
                            elements = self.set_main_header(elements, emptyline, mainheaderstyle)
                            elements = self.set_header(molecule, emptyline, headerstyle, elements)
                            elements = self.set_ascii_table(analysis_result, elements)
                            counter += 1

                        if self._should_display_graph(molecule):
                            if counter == 1:
                                elements = self.set_graphs_title(emptyline, graphstitlestyle, elements)

                            counter, elements = self.set_graphs(molecule, counter, graphsheaderstyle, elements)

                    if 'only_one_pdf' not in self.config or not self.config['only_one_pdf']:
                        if len(analysis_result) > 0:
                            _pdf_name = self.config.get("pdf_name", None)
                            if len(analysis_result) > 1 and _pdf_name:
                                # check pdf name & number analyzes
                                self.logger.warning(f'Cannot force pdf name to {_pdf_name} for multiple analyzes')
                                pdfpath = self.set_pdf_path(batch_name=self.batchname, analysis_name=analysis_name,
                                                            suffix=self.config["suffix_pdf"], pdf_name=None)
                            else:
                                pdfpath = self.set_pdf_path(batch_name=self.batchname, analysis_name=analysis_name,
                                                            suffix=self.config["suffix_pdf"], pdf_name=_pdf_name)

                            self.write_pdf(pdfpath, elements)
                    else:
                        if len(elements_all) > 0:
                            # Add page break between 2 analyzes
                            elements_all.append(PageBreak())

                        elements_all.extend(elements)
                except Exception as e:
                    self.logger.exception("An error occurred while creating elements for " + molecule["Analysis_Name"])

                self.logger.info(f"  End generate elements (time={time.time() - t1:.0f}s)")
        except Exception as e:
            self.logger.exception(f"An error occurred during generate report with {self.zip_input_path} in {self.folder_path}")

        if 'only_one_pdf' in self.config and self.config['only_one_pdf']:
            try:
                pdfpath = self.set_pdf_path(batch_name=self.batchname, analysis_name=None,
                                            suffix=self.config["suffix_pdf"],
                                            pdf_name=self.config.get("pdf_name", None))
                self.write_pdf(pdfpath, elements_all)
            except Exception as e:
                self.logger.exception(f"An error occurred while write pdf local temporary: {self.local_path}")

        try:
            if self.special_atl and self.config["graph_selection_mode"] == "validation":
                self.copy_pdfs_atl()
            self.cleanup(tmp_dir=True)
        except Exception as e:
            self.logger.exception(f"An error occurred while cleanup the local temporary: {self.local_path}")

        self.logger.info(f"End generate pdf (time={time.time() - t0:.0f}) for {self.zip_input_path}")

    def _sanitize_config(self):
        if 'url' in self.config and not self.config['url'].endswith("/"):
            self.config['url'] += "/"

    def _should_display_graph(self, molecule):
        if self.config['graph_selection_mode'] == 'classification':
            return molecule["Classification"] == "Detected" or molecule["Classification"] == "Suspected"
        else:
            return molecule["Validation"] == "Detected" or molecule["Validation"] == "Relaunch"

    def _should_display_line_table(self, ua):
        if ua["analysis_type"] != "sample":
            return False

        if self.config['graph_selection_mode'] == 'classification':
            return "classification" in ua and (ua["classification"] == "detected" or ua["classification"] == "suspected")
        else:
            # Case of validated: 1-> "Detected", 2 -> "Not Detected", 3-> "Relaunch"
            return "validation" in ua and (ua["validation"] == "1" or ua["validation"] == "2" or ua["validation"] == "3")

    def _deep_merge_dicts(self, dict1, dict2):
        """
        Deep merge two dictionaries.

        Args:
            dict1 (dict): First dictionary.
            dict2 (dict): Second dictionary.

        Returns:
            dict: Merged dictionary.
        """
        merged_dict = dict1.copy()
        for key, value in dict2.items():
            if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
                merged_dict[key] = self._deep_merge_dicts(merged_dict[key], value)
            else:
                merged_dict[key] = value
        return merged_dict

    def _validate_data(self):
        t = time.time()
        self.logger.info("  Start validating data file...")
        if self.config.get("zip_input_path"):
            self.logger.debug("    Validating zip_input_path...")
            path = self.config.get("zip_input_path")
            if not os.path.isfile(path):
                raise ValueError(f'{path} is not a readable archive')
            if not path.endswith('.json') and not path.endswith('.zip'):
                self.logger.debug("    Validating is the file is a readable archive")
                raise ValueError(f'Path {path} is not a readable archive (.zip or .json)')
            if path.endswith('.zip'):
                self.logger.debug("    Validating the zip file content")
                zip_file = zipfile.ZipFile(path, 'r')
                infos = zip_file.infolist()
                json_paths = [x.filename for x in infos if x.filename.endswith('.json')]
                if len(json_paths) > 1:
                    raise ValueError(f'Archive {path} is ambiguous, several json files found : {", ".join(json_paths)}')
                elif len(json_paths) == 0:
                    raise ValueError(f'Archive {path} does not contain a json file')
        else:
            raise ValueError('No zip_input_path provided')

        self.logger.info(f"  End validating data file (time={time.time()- t:.0f}s)")

    def read_json_file(self):
        """Reads a JSON file from the specified path,
        supporting both .json files and .zip archives."""
        t = time.time()
        self.logger.info("  Start reading input file...")

        input_path = self.config.get("zip_input_path")

        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if input_path.endswith(".json"):
            with open(input_path, "rb") as file:
                json_bytes = file.read()

        elif input_path.endswith(".zip"):
            with zipfile.ZipFile(input_path, "r") as zip_file:
                infos = zip_file.infolist()
                json_paths = [x.filename for x in infos if x.filename.endswith(".json")]

                if not json_paths:
                    raise ValueError(f"No JSON file found in the ZIP archive: {input_path}")
                if len(json_paths) > 1:
                    self.logger.warning("Multiple JSON files found in the ZIP archive. Using the first one.")

                with zip_file.open(json_paths[0]) as file:
                    json_bytes = file.read()

        else:
            raise ValueError(f"Unsupported file type: {input_path}. Expected a .json or .zip file.")

        try:
            json_data = json.loads(json_bytes.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON content: {e}")

        self.logger.info(f"  End reading input file (time={time.time() - t:.0f}s)")

        return json_data

    def set_data(self):
        t = time.time()
        self.logger.info("  Start set data...")

        # clear table
        self.table = {}

        defaultvalue = "-"
        moleculehyperlink = "-"
        moleculegraphsecond_channel_y = "-"
        self.batchid = self.data["batch"]["_id"]
        self.batchname = self.data["batch"]["name"]
        for ua in self.data.get("unitary_analysis"):
            # if ua["content"]["analysis_type"] == "sample":
            if self._should_display_line_table(ua["content"]):
                self.logger.debug("Set classification...")
                analysis_id = ua["content"]["analysis"]["id"]
                moleculehyperlink = f'<a href="{self.config["url"]}?{self.batchid}/analysis/{analysis_id}/ua={ua["_id"]}"><font color="blue"><u>{"Link"}</u></font></a>'

                match ua["content"]["validation"]:
                    case "0":
                        validation = defaultvalue
                    case "1":
                        validation = "Detected"
                    case "2":
                        validation = "Not Detected"
                    case "3":
                        validation = "Relaunch"
                    case _:
                        validation = "None"

                match ua["content"]["classification"]:
                    case "suspected":
                        classification = "Suspected"
                    case "detected":
                        classification = "Detected"
                    case "excluded":
                        classification = "Excluded"
                    case "ok":
                        classification = "OK"
                    case "ko":
                        classification = "KO"
                    case _:
                        classification = "None"

                match ua["content"]["istd"]:
                    case "True":
                        istd = "*"
                    case _:
                        istd = ""
                self.logger.debug("Set main channel...")
                main_channel = str(ua["content"]["main_channel"])
                self.logger.debug("Set second channel...")
                channels_dict = ua['content']['channels']
                for key in map(str, range(1, 6)):
                    if key in channels_dict and key != main_channel:
                        second_channel = key
                        moleculegraphsecond_channel_y = ua["content"]["channels"][second_channel].get("ampl", None)
                        break
                    else:
                        second_channel = main_channel
                if main_channel is None:
                    raise Exception('Couldnt find any main channel')

                # Calibration data for calibration graphs
                for uc in self.data.get("unitary_calibration"):
                    graph2points = None
                    calibrationformula = None
                    calibrationtype = None
                    calibrationweighing = None
                    calibrationzeropolicy = None
                    moleculegraph2_y = None
                    moleculegraph2_x = None
                    moleculegraph2 = None
                    if ua["name"] == uc["name"]:
                        main_channel_cal = str(uc["content"]["main_channel"])
                        if "graph" in uc["content"]:
                            moleculegraph2_x = uc["content"]["graph"].get("concentration_line", None)
                        if "graph" in uc["content"]["channels"][main_channel_cal]:
                            moleculegraph2_y = uc["content"]["channels"][main_channel_cal]["graph"].get("area_line", None)
                            if moleculegraph2_y is not None and moleculegraph2_x is not None:
                                moleculegraph2 = len(moleculegraph2_x) == len(moleculegraph2_y)
                                calibrationweighing = uc["content"]["channels"][main_channel_cal].get("interpolation", {}).get("weights_policy", None)
                                calibrationzeropolicy = uc["content"]["channels"][main_channel_cal].get("interpolation", {}).get("zero_policy", None)
                                match uc["content"]["channels"][main_channel_cal].get("interpolation", {}).get("type", None):
                                    case "linear":
                                        calibrationtype = "linear"
                                        graph2points = uc["content"]["channels"][main_channel_cal]["graph"].get("points", None)
                                        params = uc["content"]["channels"][main_channel_cal].get("interpolation", {}).get("params", None)
                                        if params is not None:
                                            calibrationformula = f"{round(params[0], 5)} x + {round(params[1], 5)}"
                                    case "quadra":
                                        calibrationtype = "quadratic"
                                        graph2points = uc["content"]["channels"][main_channel_cal]["graph"].get("points", None)
                                        params = uc["content"]["channels"][main_channel_cal].get("interpolation", {}).get("params", None)
                                        if params is not None:
                                            calibrationformula = f"{round(params[0], 5)} x2 + {round(params[1], 3)} x + {round(params[2], 5)}"
                            else:
                                moleculegraph2 = 0
                        break

                # Concentration/Area point for calibration graph
                ua_graph_points = None
                if main_channel in ua["content"]["channels"] and \
                        "concentration" in ua["content"]["channels"][main_channel] and \
                        "peak" in ua["content"]["channels"][main_channel] and \
                        "area" in ua["content"]["channels"][main_channel]["peak"]:
                    ua_graph_points = ua["content"]["channels"][main_channel]["concentration"], ua["content"]["channels"][main_channel]["peak"]["area"]

                self.logger.debug("Set temporary table...")
                _temptable = {
                    "*": ua["content"]["molecule"]["event"],
                    "Name": ua["name"],
                    "Name_graph": ua["name"],
                    "Analysis_Name": ua["content"]["analysis"]["name"],
                    "Compound_ID": ua["_id"],
                    "Batch_Name": ua["content"]["batch"]["name"],
                    "Validation": validation,
                    "Classification": classification,
                    "ISTD": istd,
                    "Dev RT": round(ua["content"]["channels"][main_channel].get("dev_rt", defaultvalue), 2) \
                        if ua["content"]["channels"][main_channel].get("dev_rt", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "Conc.(µg/l)": round(ua["content"]["channels"][main_channel].get("concentration", defaultvalue), 3) \
                        if ua["content"]["channels"][main_channel].get("concentration", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "mainchannel": main_channel,
                    "secondchannel": second_channel,
                    "create_date": datetime.datetime.fromtimestamp(ua["creationDate"]),
                    "moleculegraph_x": ua["content"]["time"],
                    "moleculegraph_y": ua["content"]["channels"][main_channel]["ampl"],
                    "moleculegraphsecond_channel_y": moleculegraphsecond_channel_y,
                    "moleculegraph2_y": moleculegraph2_y,
                    "moleculegraph2_x": moleculegraph2_x,
                    "RT": round(ua["content"]["channels"][main_channel].get("peak", {}).get("time", defaultvalue), 2) \
                        if ua["content"]["channels"][main_channel].get("peak", {}).get("time", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "Quantitative": ua["content"]["channels"][main_channel]["q1"],
                    "Qualifier": ua["content"]["channels"][second_channel]["q1"],
                    "Area": int(ua["content"]["channels"][main_channel].get("peak", {}).get("area", defaultvalue)) \
                        if ua["content"]["channels"][main_channel].get("peak", {}).get("area", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "calibrationformula": calibrationformula,
                    "moleculegraph2": moleculegraph2,
                    "graph2points": graph2points,
                    "graph2uapoint": ua_graph_points,
                    "calibrationtype": calibrationtype,
                    "calibrationweighing": calibrationweighing,
                    "calibrationzeropolicy": calibrationzeropolicy,
                    "Analysis_ID": analysis_id,
                    "Link": moleculehyperlink,
                    "RT_Graph": ua["content"]["channels"][main_channel].get("rt_calib", defaultvalue) \
                        if ua["content"]["channels"][main_channel].get("rt_calib", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "AreaGraphleftx": ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("left", {}).get("x", defaultvalue) \
                        if ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("left", {}).get("x", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "AreaGraphlefty": ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("left", {}).get("y", defaultvalue) \
                        if ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("left", {}).get("y", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "AreaGraphrightx": ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("right", {}).get("x", defaultvalue) \
                        if ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("right", {}).get("x", defaultvalue) != defaultvalue \
                        else defaultvalue,
                    "AreaGraphrighty": ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("right", {}).get("y", defaultvalue) \
                        if ua["content"]["channels"][main_channel].get("peak", {}).get("base", {}).get("right", {}).get("y", defaultvalue) != defaultvalue \
                        else defaultvalue,
                }
                if analysis_id not in self.table:
                    self.table[analysis_id] = []
                self.table[analysis_id].append(_temptable)
        self.logger.info(f"  End set data (time={time.time()- t:.0f}s)")

    def set_folder_path(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        if "folder_path" in self.config and self.config["folder_path"]:
            self.folder_path = self.config["folder_path"]
        else:
            ## Only build a complex folder path if None was given
            year = now.strftime("%Y")
            month = now.strftime("%m")
            self.folder_path = os.path.join(self.config["output_folder"], year, month, self.batchname)

        os.makedirs(self.folder_path, exist_ok=True)

        self.png_folder = os.path.join(self.local_path, "pngs_" + timestamp)

    def set_pdf_path(self, batch_name: str = None, analysis_name: str = None, suffix: str = None, pdf_name: str = None):
        assert batch_name or pdf_name
        try:
            if not os.path.exists(self.png_folder):
                os.makedirs(self.png_folder, exist_ok=True)
        except Exception as e:
            self.logger.error("Failed to setup png folder: " + str(e))

        if not pdf_name:
            pdf_name = batch_name
            if analysis_name:
                pdf_name += f'-{analysis_name}'

        if suffix:
            pdf_name += f'-{suffix}'

        pdf_name += '.pdf'

        return joinpath(self.folder_path, pdf_name)

    def set_header_style(self):
        styles = getSampleStyleSheet()
        preformatted_style = styles[self.config["header_format"]["styles"]]
        preformatted_style.fontName = self.config["header_format"]["fontName"]
        preformatted_style.fontSize = self.config["header_format"]["fontSize"]
        preformatted_style.wordWrap = self.config["header_format"]["wordWrap"]

        centered_style = ParagraphStyle(
            "centered",
            parent=preformatted_style,
            alignment=1  # 0=left, 1=center, 2=right
        )

        return centered_style

    def set_header(self, molecule, emptyline, headerstyle, elements):
        self.logger.debug("Set header...")

        header_text = f'<b>Report creation date:</b> {self.date_pdf.strftime("%Y-%m-%d %H:%M:%S")}\n' \
                      f'<b>Batch Name:</b> {molecule["Batch_Name"]}\n' \
                      f'<b>Analysis name:</b> <a href="{self.config["url"]}?{self.batchid}/analysis/{molecule["Analysis_ID"]}"><font color="blue"><u>{molecule["Analysis_Name"]}</u></font></a>\n' \
                      f'<b>Batch creation date:</b> {molecule["create_date"]}\n'
        # "create_date": datetime.datetime.fromtimestamp(data["creationDate"]),

        header = XPreformatted(header_text, headerstyle)

        elements.append(header)

        elements.append(emptyline)

        return elements
        # return header

    def set_ascii_table(self, analysis, elements):
        self.logger.debug("Set ascii table...")
        df = pd.DataFrame(analysis, columns=self.config["ascii_table_headers"])
        # Convert DataFrame to list of lists
        data = df.values.tolist()

        # Add headers to the data
        data.insert(0, self.config["ascii_table_headers"])

        styles = getSampleStyleSheet()
        preformatted_style = styles[self.config["ascii_table_format"]["styles"]]
        preformatted_style.fontName = self.config["ascii_table_format"]["fontName"]
        preformatted_style.fontSize = self.config["ascii_table_format"]["fontSize"]
        preformatted_style.wordWrap = self.config["ascii_table_format"]["wordWrap"]

        # Convert any cell that contains a hyperlink into a Paragraph
        for i in range(len(data)):
            for j in range(len(data[i])):
                if isinstance(data[i][j], str) and "<a href=" in data[i][j]:
                    data[i][j] = Paragraph(data[i][j], styles["BodyText"])

        asciitable = Table(data, style=self.config["Table_Style"], rowHeights=(5 * mm))

        elements.append(asciitable)

        elements.append(PageBreak())

        return elements

        # return asciitable

    def set_graphs_header_style(self):
        styles = getSampleStyleSheet()
        preformatted_style = styles[self.config["graph_header_format"]["styles"]]
        preformatted_style.fontName = self.config["graph_header_format"]["fontName"]  # Use built-in 'Courier' font
        preformatted_style.fontSize = self.config["graph_header_format"]["fontSize"]  # Reduce font size
        preformatted_style.wordWrap = self.config["graph_header_format"]["wordWrap"]

        centered_style = ParagraphStyle(
            "centered",
            parent=preformatted_style,
            alignment=1  # 0=left, 1=center, 2=right
        )
        return centered_style

    def set_graphs(self, molecule, counter, graphsheaderstyle, elements):
        self.logger.debug("Set graphs...")
        pngfilesubfolderpath = joinpath(self.png_folder, f"{counter}")
        # Check if the directory exists
        if not os.path.exists(pngfilesubfolderpath):
            # Create the directory if it doesn't exist
            os.makedirs(pngfilesubfolderpath, exist_ok=True)

        if molecule["moleculegraph_x"] is not None and molecule["moleculegraph_y"] is not None:
            fig, ax1 = plt.subplots(figsize=(self.config["graph_format"]["figsizex"], self.config["graph_format"]["figsizey"]))

            # Chromatograph
            ax1.plot(molecule["moleculegraph_x"], molecule["moleculegraph_y"], label='Channel ' + molecule["mainchannel"], color='b')

            if molecule["AreaGraphleftx"] != "-" and molecule["AreaGraphlefty"] != "-" and \
                    molecule["AreaGraphrightx"] != "-" and molecule["AreaGraphrighty"] != "-":
                # Choose two points (x1, y1) and (x2, y2) between which you want to shade the area
                x1 = molecule["AreaGraphleftx"]
                y1 = molecule["AreaGraphlefty"]
                x2 = molecule["AreaGraphrightx"]
                y2 = molecule["AreaGraphrighty"]
                # Find the indices corresponding to x1 and x2
                idx1 = np.argmax(np.array(molecule["moleculegraph_x"]) >= x1)
                idx2 = np.argmax(np.array(molecule["moleculegraph_x"]) >= x2)
                # Create a polygon representing the shaded area
                polygon_x = np.concatenate([[x1], np.array(molecule["moleculegraph_x"][idx1:idx2]), [x2]])
                polygon_y = np.concatenate([[y1], np.array(molecule["moleculegraph_y"][idx1:idx2]), [y2]])
                # Fill the polygon with a light gray color
                ax1.fill(polygon_x, polygon_y, color='orange', alpha=1)
                ax1.scatter([molecule["AreaGraphleftx"], molecule["AreaGraphrightx"]],
                            [molecule["AreaGraphleftx"], molecule["AreaGraphrighty"]], color='black')
                ax1.fill_betweenx([molecule["AreaGraphlefty"], molecule["AreaGraphrighty"]], molecule["AreaGraphleftx"],
                                  molecule["AreaGraphrightx"], color='orange', alpha=1)

            if len(molecule["moleculegraphsecond_channel_y"]) == len(molecule["moleculegraph_x"]):
                ax1.plot(molecule["moleculegraph_x"], molecule["moleculegraphsecond_channel_y"], label='Channel ' + molecule["secondchannel"], color='r')

            if molecule["RT_Graph"] != "-":
                ax1.axvline(x=molecule["RT_Graph"], color='g', linestyle='--', label='RT=' + str(round(molecule["RT_Graph"], 3)))

            ax1.set_xlabel('Time')

            ## To sanitize molecule name
            if molecule["Name"].startswith("__"):
                molecule["Name"] = molecule["Name"][2:]

            ax1.legend()

            # Adjust the values based on your needs
            left, bottom, right, top = 0, 0, 10, 7.15  # Adjust these values
            custom_bbox = Bbox.from_bounds(left, bottom, right, top)

            image_graph = joinpath(pngfilesubfolderpath, f"{counter}.png")
            plt.savefig(image_graph, bbox_inches=custom_bbox, pad_inches=0.1)
            plt.close()
            counter += 1
            fig, ax2 = plt.subplots(figsize=(self.config["graph_format"]["figsizex"], self.config["graph_format"]["figsizey"]))
            if molecule["moleculegraph2_x"] is not None and molecule["moleculegraph2_y"] is not None and \
                    (molecule["graph2points"] is not None or molecule["graph2uapoint"] is not None):
                ax2.plot(molecule["moleculegraph2_x"], molecule["moleculegraph2_y"], color='r')
                if molecule["graph2points"] is not None:
                    for point_coords_key, point_coords_value in molecule["graph2points"].items():
                        if type(point_coords_value) is float:
                            ax2.scatter(point_coords_key, point_coords_value, marker='o', color='b')
                        else:
                            ax2.scatter(point_coords_value[1], point_coords_value[0], marker='o', color='b')
                if molecule["graph2uapoint"] is not None:
                    x = molecule["graph2uapoint"][0]
                    y = molecule["graph2uapoint"][1]
                    ax2.scatter(x, y, marker='x', color='r', label=f'({x}, {y})')
                    ax2.axvline(x, ymin=0.0, ymax=y, color='red', linestyle='--', label=f'Point sur x={x}')
                    ax2.axhline(y, xmin=0.0, xmax=x, color='red', linestyle='--', label=f'Point sur y={y}')
                    ax2.text(x, y, f'({x:.2f}, {y:.2f})', color='black', ha='left', va='bottom')
            else:
                self.logger.error(f'\t  No calibration for {molecule["Name"]} in {molecule["Analysis_Name"]}')

            image_graph = joinpath(pngfilesubfolderpath, f"{counter}.png")
            plt.savefig(image_graph, bbox_inches=custom_bbox, pad_inches=0.1)
            plt.close()

        self.logger.debug("Set header graphs...")

        header_text = (
            f'<a href="{self.config["url"]}?{self.batchid}/analysis/{molecule["Analysis_ID"]}/ua={molecule["Compound_ID"]}"><u><font color="{colors.blue}">{str(molecule["Name"])}</font></u></a> \n '
            f'<b>Area:</b> {str(molecule["Area"])} <b>Quantitative:</b> {str(molecule["Quantitative"])} <b>Conc.(µg/l):</b> {str(molecule["Conc.(µg/l)"])}\n'
            f'<b>Formula:</b> {str(molecule["calibrationformula"])} <b>Curve Fit:</b> {str(molecule["calibrationtype"])} <b>Weighing:</b> {str(molecule["calibrationweighing"])} <b>Zero Policy:</b> {str(molecule["calibrationzeropolicy"])}\n'
        )

        header_graph = XPreformatted(header_text, graphsheaderstyle)

        elements.append(header_graph)

        files = os.listdir(pngfilesubfolderpath)
        # Filter out non-png files
        png_files = [f for f in files if f.endswith('.png')]
        # Sort the files so they're in the correct order
        png_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
        # Create Image objects for each png file
        images = [Image(joinpath(pngfilesubfolderpath, f), width=self.config["graph_format"]["width"],
                        height=self.config["graph_format"]["height"]) for f in png_files]
        # Create a list of lists (table data) for the images
        data = [images[i:i + 2] for i in range(0, len(images), 2)]
        # Create a table with the images
        graphtable = Table(data)

        elements.append(graphtable)

        if counter % 6 == 0:
            elements.append(PageBreak())
        counter += 1

        return counter, elements

    def set_graphs_title_style(self):
        # Retrieve the default sample styles for document elements
        styles = getSampleStyleSheet()
        # Access the style for the graph title formatting from the sample styles
        preformatted_style = styles[self.config["graph_title_format"]["styles"]]
        # Set the font name to a specified value (e.g., 'Courier')
        preformatted_style.fontName = self.config["graph_title_format"]["fontName"]
        # Adjust the font size based on the specified configuration
        preformatted_style.fontSize = self.config["graph_title_format"]["fontSize"]
        # Set word wrap behavior based on the configuration
        preformatted_style.wordWrap = self.config["graph_title_format"]["wordWrap"]
        # Define a new style for centered text based on the preformatted style
        centered_style = ParagraphStyle(
            "centered",
            parent=preformatted_style,
            alignment=1  # 0=left, 1=center, 2=right
        )
        # Return the customized style for centered graph titles
        return centered_style

    def set_graphs_title(self, emptyline, graphtitlestyle, elements):
        # Create a preformatted element for the graph title with specified content and style
        graphtitle = XPreformatted("\nCompound Graphs\n", graphtitlestyle)
        # Add the graph title element to the document's list of elements
        elements.append(graphtitle)
        # Add an empty line element to the document's list of elements
        # elements.append(emptyline)

        return elements

    def set_empty_line_style(self):
        # Retrieve the default sample styles for document elements
        styles = getSampleStyleSheet()
        # Access the style for the graph title formatting from the sample styles
        preformatted_style = styles[self.config["graph_title_format"]["styles"]]
        # Set the font name to a specified value (e.g., 'Courier')
        preformatted_style.fontName = self.config["graph_title_format"]["fontName"]
        # Adjust the font size based on the specified configuration
        preformatted_style.fontSize = self.config["graph_title_format"]["fontSize"]
        # Set word wrap behavior based on the configuration
        preformatted_style.wordWrap = self.config["graph_title_format"]["wordWrap"]
        # Return the customized style for graph titles
        return preformatted_style

    def set_empty_line(self, emptylinestyle):
        # Return a preformatted element containing a non-breaking space and a newline
        # The element is created using XPreformatted with specified content and style
        return XPreformatted("&nbsp;\n", emptylinestyle)

    def set_main_header_style(self):
        styles = getSampleStyleSheet()
        preformatted_style = styles[self.config["main_header_format"]["styles"]]
        preformatted_style.fontName = self.config["main_header_format"]["fontName"]  # Use built-in 'Courier' font
        preformatted_style.fontSize = self.config["main_header_format"]["fontSize"]
        preformatted_style.wordWrap = self.config["main_header_format"]["wordWrap"]

        centered_style = ParagraphStyle(
            "centered",
            parent=preformatted_style,
            alignment=1  # 0=left, 1=center, 2=right
        )

        return centered_style

    def set_main_header(self, elements, emptyline, mainheaderstyle):
        title = XPreformatted(self.config["title_text"], mainheaderstyle)
        # Create a table with the title as the only cell
        table_data = [[title]]
        table = Table(table_data)

        # Add a border to the table
        table.setStyle([
            ('BOX', (0, 0), (-1, -1), 1, 'black'),
            ('BACKGROUND', (0, 0), (-1, -1), 'lightgrey'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ])

        elements.append(table)

        elements.append(emptyline)

        return elements

    def write_pdf(self, pdfpath, elements):
        t = time.time()
        self.logger.info(f"\t * start writing pdf: {pdfpath } ...")
        # Check if there are elements in the document and if the third-to-last element is a PageBreak
        if len(elements) > 0 and isinstance(elements[-1], PageBreak):
            # Remove the last element from the document (excluding the PageBreak)
            elements = elements[:-1]
        
        ## Special args to force a new output location
        # if self.forced_output_location:
        #     pdfpath = self.forced_output_location + os.path.basename(pdfpath)
        
        # Create a SimpleDocTemplate with specified parameters
        doc = SimpleDocTemplate(pdfpath, pagesize=letter, topMargin=0)
        # Build the document using elements, specifying functions for first page and later pages
        self.new_pdfs.append(pdfpath)
        doc.build(elements, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
        self.logger.info(f"\t * end writing (time={time.time() - t:.0f}s)")
        # Perform cleanup operations
        self.cleanup()

        # Return the path to the generated PDF file
        return pdfpath

    def copy_pdfs_atl(self):
        sequences = []
        for analyse in self.data.get("analysis"):
            match = re.match(r'^(s\d+[a-z0-9]*)-ccv\d+', analyse['name'], re.IGNORECASE)
            if match:
                sequences.append(match.group(1))

        ## Move and change pdf name to the special SEQUENCE folder of ATL
        for sequence in sequences:
            for index, pdf_path in enumerate(self.new_pdfs, start=1):
                if len(self.new_pdfs) == 1:
                    new_name = f"{sequence}.pdf"
                else:
                    new_name = f"{sequence}_ADD{index}.pdf"
                
                self.forced_output_location = self.forced_output_location.replace("\\\\", "\\")
                destination = os.path.join(self.forced_output_location, new_name)
                shutil.copy2(pdf_path, destination)

    def cleanup(self, tmp_dir:bool = False):
        """Clean up temporary folders and files"""
        self.logger.info(f"\t * start cleanup ... ")
        t2 = time.time()
        if tmp_dir and os.path.exists(self.local_path):
            shutil.rmtree(self.local_path)
            self.logger.info(f"\t * end cleanup (time={time.time() - t2:.0f}s, path={self.local_path})")
        elif os.path.exists(self.png_folder):
            shutil.rmtree(self.png_folder)
            self.logger.info(f"\t * end cleanup (time={time.time() - t2:.0f}s, path={self.png_folder})")

    def add_page_number(self, canvas, doc):
        """
        Add the page number
        """
        page_num = canvas.getPageNumber()
        text = "Page %s" % page_num
        # Save the current font
        original_font = canvas._fontname, canvas._fontsize
        # Set the new font (Courier, 10 points)
        canvas.setFont("Courier", 6)
        # Draw the text with the new font
        canvas.drawRightString(210 * mm, 3 * mm, text)
        # Draw a line on top of the text
        canvas.line(10 * mm, 6 * mm, 200 * mm, 6 * mm)
        # Restore the original font
        canvas.setFont(*original_font)


if __name__ == "__main__":
    _zip_input_path = "C:\\Users\\ROMDHANES\\Downloads\\batch_656f59480455154ec43cdf39_dump.zip"
    _zip_input_path = "C:\\Users\\ROMDHANES\\Downloads\\batch_655223636d8ce93b5c9af7be_dump (4).zip"
    _zip_input_path = "C:\\Users\\ROMDHANES\\Downloads\\batch_659f26d10465562b4aeae020_dump.zip"

    _output_folder = "C:\\Users\\ROMDHANES\\Downloads\\pdf\\ATL"

    pdf_generator = PDFGenerator(zip_input_path=_zip_input_path, output_folder=_output_folder)
    pdf_generator.generate_before_modification_report()
    pdf_generator.generate_after_modification_report()
