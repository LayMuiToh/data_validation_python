import pandas 
from openpyxl import load_workbook
import configparser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_item_in_list(list, row):  
  for item in list:
    if (item == row):
      return True
  return False    

def validate_machine(type, fn):
  xls_file = pandas.ExcelFile(fn)
  parser = configparser.ConfigParser()
  parser.read(r'./datafile/config')
  master_sheet = parser.get(type, 'master_sheet')
  new_sheet = parser.get(type, 'new_sheet')
  conf_sheet = parser.get(type, 'config_sheet')
  master_serial_number = parser.get(type, 'master_serial_number')
  
  master_sheet_attr = pandas.read_excel(xls_file, sheet_name=master_sheet)
  master_sheet_entire = pandas.read_excel(xls_file, sheet_name=master_sheet,header=[0])
  config_sheet = pandas.read_excel(xls_file, sheet_name=conf_sheet)

  # Create a empty dictionary to store data validation for serial number
  sn_dict = {}

  # Machine xxx 
  # For each row with Serial Number at master sheet (Master_HEX), 
  # check against the configuration sheet (Master_Data)
    for (index_master,row_master) in master_sheet_attr.iterrows():
      logging.info(row_master)
      for (index_conf,row_conf) in config_sheet.iterrows():
            complete_config = "True"
            break
      sn_dict[(row_master[master_serial_number])] = complete_config  
  
  # For each row in the master sheet, loop through the sn_dict where the value of 
  # each Serial Number's key will be the result of the Data Validation's column   
  for (index_master_entire,row_master_entire) in master_sheet_entire.iterrows():
    if (row_master_entire[master_serial_number] == master_serial_number):
      row_master_entire['Data Validation'] = 'Data Validation'
      continue
    is_valid = False 
    for (key,value) in sn_dict.items():
      if (row_master_entire[master_serial_number] == key):
        is_valid = value
        break
    master_sheet_entire.loc[index_master_entire, 'Data Validation'] = is_valid
    
  # To print to the log file  
  for (index_master_entire,row_master_entire) in master_sheet_entire.iterrows():
    logging.info(str(index_master_entire) + ':' + 
    str(row_master_entire[master_serial_number]) + ' ' + 
    str(row_master_entire['Data Validation']))
  
  # To write a entire master sheet to the new_sheet with the Data Validation column
  writer = pandas.ExcelWriter(fn, engine='openpyxl')
  writer.book = load_workbook(fn)
  writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
  master_sheet_entire.to_excel(writer, sheet_name=new_sheet,index=False)
  writer.save()
