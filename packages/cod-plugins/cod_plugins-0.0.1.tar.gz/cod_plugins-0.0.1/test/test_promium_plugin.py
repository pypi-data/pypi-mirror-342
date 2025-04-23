import os
from datetime import datetime

import pandas as pd
import pyodbc
import pytest

from promium_plugin import PromiumPlugin


@pytest.fixture(scope='module')
def result_dir():

    # prepare the result directory
    today = datetime.now()
    result_dir = os.path.abspath('./results/atl/' + today.strftime('%Y%m%d_%H%M%S'))
    os.makedirs(result_dir, exist_ok=True)

    return result_dir

def test_simple_run(result_dir):
    # zip_path = "/data/ATL/tests/batch_6707eb771325df4a5cd53545_dump.zip"
    zip_path = "/data/ATL/tests/promium_tests/batch_679a3aaadc64cd3f4e12eb07_dump.zip"

    plugin = PromiumPlugin(zip_input_path=zip_path, output_folder = result_dir)
    plugin.run()

def test_simple_run_prod(result_dir):
    zip_path = '/nas/shared/Data/ATL_global/MS-05 (8260 SOIL)/batch_659a929f0465562b4ae61948_dump.zip'
    # zip_path = '/nas/shared/Data/ATL_global/MS-05 (8260 SOIL)/batch_8260_soil_08-01-24_S3K0514.zip'
    # zip_path = '/nas/shared/Data/ATL_global/MS-05 (8260 SOIL)/batch_8260_soil_12-01-24_S4K0416.zip'
    zip_path = '/nas/shared/Data/ATL_global/MS-05 (8260 SOIL)/batch_8260_soil_29-01-24_S4A0540.zip'
    plugin = PromiumPlugin(zip_input_path=zip_path, output_folder = result_dir)
    plugin.run()


def test_get_MDL(result_dir):

    req = '''Select Distinct Y.Analysis, Y.Matrix, Y.Analyte, Y.AnalyteOrder,  Y.MDL, Y.LOD, Y.MRL, L.Tinitial, L.Tfinal, L.InitialUnits,
      L.Units, UI.Factor As Inifactor, UF.Factor as FinFactor,
    (Y.MDL/ UF.Factor)*(Tinitial / tFinal) * UI.Factor as InstMDL
    From ANALYSISMATRIX L Inner Join
      ANALYSISANALYTE Y On L.Analysis = Y.Analysis And L.Matrix = Y.Matrix
      Inner Join
      UNITS As UI On UI.Units = L.InitialUnits Left Join
      UNITS UF On L.Units = UF.Units
    Where MDL <> ''
    Order By Y.Analysis, Y.Matrix, Y.Analyte
    '''

    req = '''Select Distinct Y.Analysis, Y.Matrix, Y.Analyte, Y.AnalyteOrder,  Y.MDL, Y.LOD, Y.MRL, L.Tinitial, L.Tfinal, L.InitialUnits,
      L.Units, UI.Factor As Inifactor, UF.Factor as FinFactor,
    (Y.MDL/ UF.Factor)*(Tinitial / tFinal) * UI.Factor as InstMDL
    From ANALYSISMATRIX L Inner Join
      ANALYSISANALYTE Y On L.Analysis = Y.Analysis And L.Matrix = Y.Matrix
      Inner Join
      UNITS As UI On UI.Units = L.InitialUnits Left Join
      UNITS UF On L.Units = UF.Units
    Where Y.Analysis = '8260' and Y.Matrix = 'Soil'
    Order By Y.Analysis, Y.Matrix, Y.AnalyteOrder
    '''


    config = {
        # Database connection parameters
        'server': '192.168.1.22,1433',
        # database = 'element_TEST'
        'database': 'element',
        'username': 'ElementTestUser',
        'password': 'Chem@8529'
    }

    # Create a connection to the SQL Server database
    connection_string = (
        f'DRIVER=ODBC Driver 17 for SQL Server;'
        f'SERVER={config["server"]};'
        f'DATABASE={config["database"]};'
        f'UID={config["username"]};'
        f'PWD={config["password"]}'
    )
    sql_conn = pyodbc.connect(connection_string)
    df = pd.read_sql(req, sql_conn)

    path = os.path.join(result_dir, f'ATL_MDLs.xls')
    df.to_excel(path, index=False)
    pass