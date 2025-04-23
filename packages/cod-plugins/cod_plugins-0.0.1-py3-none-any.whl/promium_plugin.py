import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import zipfile
from datetime import datetime
import numpy as np

import json
import pandas
import xlwt
import requests

from cod_plugin import CODPlugin
import pandas as pd
import pyodbc


class PromiumPlugin(CODPlugin):

    def __init__(self, zip_input_path, output_folder, api_url=None, cookies=None, logger=None, **kwargs):
        super(PromiumPlugin, self).__init__(zip_input_path, output_folder, api_url, cookies, logger=logger)

        self.config = {
        # Database connection parameters
        'server': '192.168.1.22,1433',
        # database = 'element_TEST'
        'database': 'element',
        'username': 'ElementTestUser',
        'password': 'Chem@8529'
        }
        self.config = self._deep_merge_dicts(self.config, kwargs)

        # Create a connection to the SQL Server database
        connection_string = (
            f'DRIVER=ODBC Driver 17 for SQL Server;'
            f'SERVER={self.config["server"]};'
            f'DATABASE={self.config["database"]};'
            f'UID={self.config["username"]};'
            f'PWD={self.config["password"]}'
        )
        self.sql_conn = pyodbc.connect(connection_string)



    def run(self):

        self.read_json_file()
        self.parse_cod_data()
        self.get_promium_data()
        self.generate_results()
        self.dump_xls_results()


    def parse_cod_data(self):

        batch_nums = set()
        sequence_nums = set()

        # get the sequence num
        for analysis in self.analyses:
            analysis_name = analysis['name']
            analysis_type = analysis['content']['type']

            if analysis_type == 'calibration':
                continue

            if 'cal' in analysis['name'] or 'blank' in analysis['name']:
                pass
            elif analysis_name.startswith('b'):
                batch_num = analysis_name.split('-')[0].upper()
                batch_nums.add(batch_num)
                pass
            elif analysis_name.startswith('s'):
                sequence_num = analysis_name.split('-')[0].upper()
                sequence_nums.add(sequence_num)
                pass
            elif analysis_name.startswith('2'):
                pass
            else:
                self.logger.warning(f'Unexpected analysis name {analysis_name}')

        sequence_nums = list(sequence_nums)
        batch_nums = list(batch_nums)
        if len(sequence_nums) == 0:
            raise Exception('No sequence number found')
        elif len(sequence_nums) > 1:
            self.logger.warning(f'Unexpected sequence nums {sequence_nums})')
        #assert len(sequence_nums) == 1, f'Unexpected sequence nums {sequence_nums}'
        self.sequence_num = max(sequence_nums)

        if len(batch_nums) == 0:
            self.logger.warning(f'Unexpected batch nums {sequence_nums}')
        
        self.batch_num = batch_nums

        pass

    def get_promium_data(self):

        # SQL SELECT query
        global_sql_query = f"""SELECT SE.Wrk + '-' + SE.Sample AS labnumber, SE.Analysis, LY.Analyte, LY.AnalyteOrder As AnalyteOrder, SE.AnaOrder AS AnalysisOrder, '' AS Analyzed, '' AS InitialResult, '' AS ResultType, '' AS MDL, '' AS LOD, '' AS MRL, '' AS LR, '' AS MinMRL, '' AS MinPRL, '' AS RT, '' AS RESP, 
                          '' AS MDA, '' AS UNC, '' AS EDL, '' AS EMPC, '' AS RES, LM.InitialUnits, '' AS Dilution, '' AS Analyst, '' AS Instrument, '' AS FileID, SE.Batch, SE.AnaBatch, '' AS AnalyteInfo1, '' AS AnalyteInfo2, '' AS AnalyteInfo3, '' AS AnalyteInfo4, 
                          '' AS AnalyteInfo5, '' AS AnalyteInfo6, '' AS AnalyteInfo7, '' AS AnalyteInfo8, '' AS AnalyteInfo9, '' AS AnalyteInfo10
        FROM     dbo.ANALYSISMATRIX AS LM INNER JOIN
                          dbo.ANALYSISANALYTE AS LY ON LM.Analysis = LY.Analysis AND LM.Matrix = LY.Matrix INNER JOIN
                          dbo.SAMPLEEXTRACTION AS SE ON LM.Analysis = SE.Analysis INNER JOIN
                          dbo.BATCH AS B ON LM.Matrix = B.Matrix AND LY.Matrix = B.Matrix AND SE.Matrix = B.Matrix AND SE.AnaBatch = B.Batch INNER JOIN
                          dbo.BATCHANALYSIS AS BL ON LM.Analysis = BL.Analysis AND SE.Analysis = BL.Analysis AND SE.AnaBatch = BL.Batch AND B.Batch = BL.Batch
        WHERE  B.Batch = '{self.sequence_num}'
        UNION
        SELECT QE.Batch + '-' + QE.QCSample AS Labnumber, BL.Analysis, LY.Analyte, LY.AnalyteOrder AS Analyteorder, QE.AnaOrder AS AnalysisOrder, '' AS Analyzed, '' AS InitialResult,  '' AS ResultType, '' AS MDL, '' AS LOD, '' AS MRL, '' AS LR, '' AS MinMRL, '' AS MinPRL, '' AS RT, 
                          '' AS RESP, '' AS MDA, '' AS UNC, '' AS EDL, '' AS EMPC, '' AS RES, LM.InitialUnits, '' AS Dilution, '' AS Analyst, '' AS Instrument, '' AS FileID, QE.Batch, QE.AnaBatch, '' AS AnalyteInfo1, '' AS AnalyteInfo2, '' AS AnalyteInfo3, '' AS AnalyteInfo4, 
                          '' AS AnalyteInfo5, '' AS AnalyteInfo6, '' AS AnalyteInfo7, '' AS AnalyteInfo8, '' AS AnalyteInfo9, '' AS AnalyteInfo10
        FROM     dbo.BATCH AS B INNER JOIN
                          dbo.BATCHANALYSIS AS BL ON B.Batch = BL.Batch INNER JOIN
                          dbo.QCEXTRACTION AS QE ON B.Batch = QE.AnaBatch AND BL.Batch = QE.AnaBatch INNER JOIN
                          dbo.ANALYSISMATRIX AS LM ON B.Matrix = LM.Matrix AND BL.Analysis = LM.Analysis INNER JOIN
                          dbo.ANALYSISANALYTE AS LY ON B.Matrix = LY.Matrix AND LM.Analysis = LY.Analysis AND LM.Matrix = LY.Matrix AND BL.Analysis = LY.Analysis
        WHERE  B.Batch = '{self.sequence_num}'
        """

        samples_sql_query = """
        Select Distinct SE.Wrk + '-' + SE.Sample As LabNumber, SE.Analysis, LY.Analyte, LY.AnalyteOrder As AnalyteOrder, SE.AnaOrder As AnalysisOrder, '' As Analyzed,
          '' As InitialResult, '' As ResultType, '' As MDL, '' As LOD, '' As MRL, '' As LR,  '' As MinMRL, '' As MinPRL, '' As RT, '' As RESP, '' As MDA, '' As UNC,
          '' As EDL, '' As EMPC, '' As RES, LM.InitialUnits, '' As Dilution,  'IDA' As Analyst, '' As Instrument, '' As FileID, SE.Batch, SE.AnaBatch,
          '' As AnalyteInfo1, '' As AnalyteInfo2, '' As AnalyteInfo3,  '' As AnalyteInfo4, '' As AnalyteInfo5, '' As AnalyteInfo6,  '' As AnalyteInfo7, '' As AnalyteInfo8, '' As AnalyteInfo9,  '' As AnalyteInfo10
        From dbo.ANALYSISMATRIX As LM Inner Join
          dbo.ANALYSISANALYTE As LY On LM.Analysis = LY.Analysis And LM.Matrix = LY.Matrix Inner Join
          dbo.SAMPLEEXTRACTION As SE On LM.Analysis = SE.Analysis And LY.Matrix = SE.Matrix And LM.Matrix = SE.Matrix Inner Join
          dbo.BATCH As B On LM.Matrix = B.Matrix And LY.Matrix = B.Matrix And SE.Matrix = B.Matrix And SE.Matrix = B.Matrix And SE.Batch = B.Batch
        Where SE.Batch =  '{}'
                """

        qc_sql_query = """
        SELECT QE.Batch + '-' + QE.QCSample AS LabNumber, BL.Analysis, LY.Analyte, LY.AnalyteOrder AS AnalyteOrder, QE.AnaOrder AS AnalysisOrder, '' AS Analyzed, '' AS InitialResult,  '' AS ResultType, '' AS MDL, '' AS LOD, '' AS MRL, '' AS LR, '' AS MinMRL, '' AS MinPRL, '' AS RT,
                          '' AS RESP, '' AS MDA, '' AS UNC, '' AS EDL, '' AS EMPC, '' AS RES, LM.InitialUnits, '' AS Dilution, 'IDA' AS Analyst, '' AS Instrument, '' AS FileID, QE.Batch, QE.AnaBatch, '' AS AnalyteInfo1, '' AS AnalyteInfo2, '' AS AnalyteInfo3, '' AS AnalyteInfo4,
                          '' AS AnalyteInfo5, '' AS AnalyteInfo6, '' AS AnalyteInfo7, '' AS AnalyteInfo8, '' AS AnalyteInfo9, '' AS AnalyteInfo10
        FROM     dbo.BATCH AS B INNER JOIN
                          dbo.BATCHANALYSIS AS BL ON B.Batch = BL.Batch INNER JOIN
                          dbo.QCEXTRACTION AS QE ON B.Batch = QE.Batch AND BL.Batch = QE.Batch INNER JOIN
                          dbo.ANALYSISMATRIX AS LM ON B.Matrix = LM.Matrix AND BL.Analysis = LM.Analysis INNER JOIN
                          dbo.ANALYSISANALYTE AS LY ON B.Matrix = LY.Matrix AND LM.Analysis = LY.Analysis AND LM.Matrix = LY.Matrix AND BL.Analysis = LY.Analysis
        WHERE  B.Batch = '{}'
                """

        seq_sql_query = f"""
        SELECT QE.Batch + '-' + QE.QCSample AS LabNumber, BL.Analysis, LY.Analyte, LY.AnalyteOrder AS AnalyteOrder, QE.AnaOrder AS AnalysisOrder, '' AS Analyzed, '' AS InitialResult,  '' AS ResultType, '' AS MDL, '' AS LOD, '' AS MRL, '' AS LR, '' AS MinMRL, '' AS MinPRL, '' AS RT, 
                          '' AS RESP, '' AS MDA, '' AS UNC, '' AS EDL, '' AS EMPC, '' AS RES, LM.InitialUnits, '' AS Dilution, 'IDA' AS Analyst, B.Instrument AS Instrument, '' AS FileID, QE.Batch, QE.AnaBatch, '' AS AnalyteInfo1, '' AS AnalyteInfo2, '' AS AnalyteInfo3, '' AS AnalyteInfo4, 
                          '' AS AnalyteInfo5, '' AS AnalyteInfo6, '' AS AnalyteInfo7, '' AS AnalyteInfo8, '' AS AnalyteInfo9, '' AS AnalyteInfo10
        FROM     dbo.BATCH AS B INNER JOIN
                          dbo.BATCHANALYSIS AS BL ON B.Batch = BL.Batch INNER JOIN
                          dbo.QCEXTRACTION AS QE ON B.atch = QE.AnaBatch AND BL.Batch = QE.AnaBatch INNER JOIN
                          dbo.ANALYSISMATRIX AS LM ON B.Matrix = LM.Matrix AND BL.Analysis = LM.Analysis INNER JOIN
                          dbo.ANALYSISANALYTE AS LY ON B.Matrix = LY.Matrix AND LM.Analysis = LY.Analysis AND LM.Matrix = LY.Matrix AND BL.Analysis = LY.Analysis
        WHERE  B.Batch = '{self.sequence_num}'
                """

        dfs = []

        for batch_num in self.batch_num:
            batch_sample_df = pd.read_sql(samples_sql_query.format(batch_num), self.sql_conn)
            dfs.append(batch_sample_df)

        seq_df = pd.read_sql(seq_sql_query, self.sql_conn)
        dfs.append(seq_df)

        if seq_df.empty:
            for batch_num in self.batch_num:
                batch_qc_df = pd.read_sql(qc_sql_query.format(batch_num), self.sql_conn)
                dfs.append(batch_qc_df)

        # Execute the SQL query
        self.df = pandas.concat(dfs, ignore_index=True)

        # Assign the current date to a new column
        self.df['Analyzed'] = datetime.now().strftime("%m/%d/%y %H:%M")
        self.df['Analyst'] = 'IDA'

        # Assign the instrument
        if not seq_df.empty:
            instrument = max(seq_df['Instrument'])
            self.df['Instrument'] = instrument
        
        # Fill nan in  AnalysisOrder if possibleB
        order_lab_dict = {}

        for index, row in self.df.iterrows():
            analysis_order = row['AnalysisOrder']
            lab_number = row['LabNumber']
            
            if pd.notna(analysis_order):
                if analysis_order not in order_lab_dict:
                    order_lab_dict[analysis_order] = set()
                order_lab_dict[analysis_order].add(lab_number)

        lab_order_dict = {lab_number: num_order for num_order, lab_numbers in order_lab_dict.items() for lab_number in lab_numbers}

        for index, row in self.df.iterrows():
            lab_number = row['LabNumber']
            if pd.isna(row['AnalysisOrder']) and lab_number in lab_order_dict:
                self.df.at[index, 'AnalysisOrder'] = lab_order_dict[lab_number]


    def generate_results(self):

        results = []

        for analysis in self.analyses:

            # if analysis['content']['type'] not in ['sample', 'mbd', 'blank']:
            #     continue

            uas = [ua for ua in self.unitary_analyses if ua['content']['analysis']['id'] == analysis['_id']]
            part_results = []
            for ua in uas:
                if ua['content']['validation'] == '1':
                    report = True
                elif ua['content']['validation'] == '0' and ua['content']['classification'] == 'detected':
                    # report = True # we report also the auto detections
                    report = False
                elif analysis['content']['type'] != 'sample':
                    # report = True # we report also the auto detections
                    report = False
                else:
                    # report = True # we report everything
                    report = False

                # we use analysis to avoid incoherences in cse of renaming
                lab_number = analysis['name']
                # we get the initial filename to be used for generating PDFs
                filename = analysis['content']['file'].split('/')[-1].replace('.json', '')
                analyte = ua['name']
                main_channel = ua['content']['channels'][str(ua['content']['main_channel'])]
                if report and 'peak' in main_channel:
                    rt = main_channel['peak']['time']
                    response = main_channel['peak']['area']
                    concentration = main_channel['concentration'] if 'concentration' in main_channel else None
                else:
                    rt = None
                    response = None
                    concentration = None

                infos = {
                    'LabNumber': lab_number.upper(),
                    'Analyte': analyte.lower(),
                    'RT': np.round(rt, 2) if rt is not None else rt,
                    'RESP': np.round(response, 0) if response is not None else response,
                    'InitialResult': np.round(concentration, 2) if concentration is not None else concentration,
                    'FileID': filename.upper(),
                    'Dilution': analysis['content']['formula_infos']['facteur_dilution'] if 'formula_infos' in analysis['content'] and analysis['content']['formula_infos']['facteur_dilution'] != 1 else None
                }

                results.append(infos)
                part_results.append(infos)

                pass

            part_result_df = pandas.DataFrame(part_results)
            pass

        result_df = pandas.DataFrame(results)

        # Remove duplicates based on columns 'LabNumber', 'Analyte'
        result_df = result_df.drop_duplicates(subset=['LabNumber', 'Analyte'])
        self.df = self.df.drop_duplicates(subset=['LabNumber', 'Analyte', 'Analysis'])

        # Remove rows where column A contains the substring 'TUN'
        self.df = self.df[~self.df['LabNumber'].str.contains('TUN')]

        # Merging df1 and df2 based on LabNumber and Analyte
        self.df['Analyte'] = self.df['Analyte'].str.lower()
        self.df = pd.merge(self.df, result_df, on=['LabNumber', 'Analyte'], how='outer', suffixes=('_df1', '_df2'))

        # Step 2: Combine the common columns and drop the extra columns
        for key in ['RT', 'RESP', 'InitialResult', 'FileID', 'Dilution']:
            key_df1 = key + '_df1'
            key_df2 = key + '_df2'
            self.df[key] = self.df[key_df2].combine_first(self.df[key_df1])
            self.df[key].where(self.df[key].notna(), None)
            self.df = self.df.drop([key_df1, key_df2], axis=1)

        # Step 3: remove the lines not coming from SQL
        self.df = self.df.dropna(subset=['Analysis'])

        # Step 3.2: remove the lines not showing in the batch
        self.df = self.df[self.df['FileID'] != '']

        # Step4: reorder columns
        ordered_columns = ['LabNumber', 'Analysis', 'Analyte', 'AnalyteOrder', 'AnalysisOrder',
                           'Analyzed', 'InitialResult', 'InitialUnits', 'ResultType', 'RT', 'RESP', 'MDL', 'LOD', 'MRL', 'LR', 'MinMRL',
                           'MinPRL', 'MDA', 'UNC', 'EDL', 'EMPC', 'RES', 'Dilution',
                           'Analyst', 'Instrument', 'FileID', 'Batch', 'AnaBatch',
                           'AnalyteInfo1', 'AnalyteInfo2', 'AnalyteInfo3', 'AnalyteInfo4', 'AnalyteInfo5',
                           'AnalyteInfo6', 'AnalyteInfo7', 'AnalyteInfo8', 'AnalyteInfo9', 'AnalyteInfo10']
        self.df = self.df[ordered_columns]

        # Step 4: order everything according to the LIMS
        self.df = self.df.sort_values(by=['AnalysisOrder', 'AnalyteOrder'])
        pass

    def get_analysi_details(self, analysis):

        if analysis['content']['type'] == 'sample':

            pass

        pass

    def generate_before_modification_report(self) -> None:
        """
        Generate report before modification.
        """
        pass

    def generate_after_modification_report(self) -> None:
        """
        Generate report after modification.
        """

        self.run()

    def generate_report(self) -> None:
        """
        Generate report.
        """

        pass

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

    def _validateconfig(self):
        self.logger.debug("Validating config...")
        if self.config.get("zip_input_path"):
            self.logger.debug("    Validating zip_input_path...")
            path = self.config.get("zip_input_path")
            if not os.path.isfile(path):
                raise Exception(f'{path} is not a readable archive')
            if not path.endswith('.bson') and not path.endswith('.zip'):
                self.logger.debug("    Validating is the file is a readable archive")
                raise Exception(f'Path {path} is not a readable archive (.zip or .bson)')
            if path.endswith('.zip'):
                self.logger.debug("    Validating the zip file content")
                zip_file = zipfile.ZipFile(path,'r')
                infos = zip_file.infolist()
                bson_paths = [x.filename for x in infos if x.filename.endswith('.bson')]
                if len(bson_paths) > 1:
                    raise Exception(f'Archive {path} is ambiguous, several Bson files found : {", ".join(bson_paths)}')
                elif len(bson_paths) == 0:
                    raise Exception(f'Archive {path} does not contain a Bson file')
        else:
            raise Exception('No zip_input_path provided')

    def read_json_file(self):
        self.logger.debug("Reading JSON file...")

        # zip_file = zipfile.ZipFile(self.zip_input_path,'r')
        # infos = zip_file.infolist()
        # bson_paths = [x.filename for x in infos if x.filename.endswith('.bson')]
        

        # with zip_file.open(bson_paths[0]) as file:
        #     bson_str = file.read()
        with zipfile.ZipFile(self.zip_input_path, "r") as zip_file:
            infos = zip_file.infolist()
            json_paths = [x.filename for x in infos if x.filename.endswith(".json")]
            if not json_paths:
                raise ValueError(f"No JSON file found in the ZIP archive: {self.zip_input_path}")
            if len(json_paths) > 1:
                self.logger.warning("Multiple JSON files found in the ZIP archive. Using the first one.")
            with zip_file.open(json_paths[0]) as file:
                json_bytes = file.read()
        # Use bson.decode_all to deserialize BSON data from the file
        json_data = json.loads(json_bytes.decode("utf-8"))

        self.data = json_data

        for key in ['batch', 'analysis', 'unitary_analysis', 'unitary_calibration']:
            assert key in self.data, f'Missing {key} in COD archive {self.zip_input_path}'

        self.batch = self.data['batch']
        name_analyses = {}
        
        self.analyses = []
        ## Transform analyses name (removing 000_ pattern at the start of the name)
        for analysis in self.data['analysis']:
            ## Cleanup the analysis name if needed, remove 001_ at the beginning and remove _d20/_d@20 at the end
            ## This allow us to get the correct name in Elements (LIMS).
            name = re.sub(r'^\d+_', '', analysis['name'])
            name = re.sub(r'_d.*\d+$', '', name)
            analysis['name'] = name
            type = analysis['content']['type']
            
            ## Remove analyses hidden by the user in the interface, the tag off_visibility is here when its the case.
            if not 'off_visibility' in analysis['tags']:
                if name in name_analyses:
                    existing_type = name_analyses[name]['content']['type']
                    ## If the analysis name is not unique we prioritize the one which is not of the type other
                    if existing_type == 'other' and type != 'other':
                        name_analyses[name] = analysis
                else:
                    name_analyses[name] = analysis
        
        self.analyses = list(name_analyses.values())
        self.unitary_analyses = self.data['unitary_analysis']
        self.unitary_calibrations = self.data['unitary_calibration']
        self.logs = self.data['log'] if 'log' in self.data else []

        assert self.batch != None

    def dump_xls_results(self):
        batch_name = self.batch['name']

        path = os.path.join(self.ouptut_folder, f'promium_export_{batch_name}.xls')
        #self.df.to_excel(path, sheet_name='DETable', index=False)

        # Create an xlwt workbook and worksheet
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('DETable')

        # Write the column headers
        for col_num, column_title in enumerate(self.df.columns):
            worksheet.write(0, col_num, column_title)

        # Write the data
        for row_num, row in enumerate(self.df.iterrows()):
            for col_num, cell_value in enumerate(row[1]):
                if isinstance(cell_value, str):
                    cell_value = cell_value.replace('\r', '\r\n')  # Replace CR par CRLF
                worksheet.write(row_num + 1, col_num, cell_value)
        # for row_num, row in enumerate(self.df.iterrows()):
        #     for col_num, cell_value in enumerate(row[1]):
        #         worksheet.write(row_num + 1, col_num, cell_value)

        # Save the workbook
        workbook.save(path)
        self.add_success_flag(path)
        self.send_mail_notification(path)
    
    def add_success_flag(self, path):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        batch_id = self.batch['_id']
        
        url = f'{self.api_url}/batch/{batch_id}/flag'
        
        data = {
            "action": "create",
            "flag": {
                "title": "Result Excel file",
                "reason": f"The result Excel file has been generated at {path} {date_str}"
            }
        }
        
        response = requests.put(url, json=data, cookies=self.cookies, verify=False)
        
        if response.status_code == 200:
            self.logger.info("Flag has been added to the batch {batch_id} with success.")
        else:
            self.logger.warning("Error when trying to add a flag to the batch {batch_id} ", response.status_code)
    
    def send_mail_notification(self, path):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        SMTP_SERVER = "owa.lcgportal.net"
        SMTP_PORT = 587
        
        sender_email = "test.test@test.com"
        receiver_emails = ["test.test@test.com", "test.test@test.com"]

        PASSWORD = "test"
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)
        message["Subject"] = "[NOTIF] COD Excel Promium file created"
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, PASSWORD)
        
        body = f"The result Excel file has been generated at {path} {date_str}"
        message.attach(MIMEText(body, "plain"))
        
        text = message.as_string()
        for receiver_email in receiver_emails:
            server.sendmail(sender_email, receiver_email, text)

        server.quit()