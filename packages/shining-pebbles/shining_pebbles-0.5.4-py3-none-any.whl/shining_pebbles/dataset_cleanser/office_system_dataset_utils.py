import numpy as np
import pandas as pd

def parse_commaed_number(number_str):
    if isinstance(number_str, (int, float)):
        return number_str
    else:
        return float(number_str.replace(',', ''))
   
def force_int(number):
    if isinstance(number, float) and number.is_integer():
        return int(number)
    return number

def transform_fund_code_float_to_string(fund_code):    
    if pd.isna(fund_code):
        return None    
    if isinstance(fund_code, float):
        fund_code = str(int(fund_code)).replace('.0', '').zfill(6)
    elif isinstance(fund_code, int):
        fund_code = str(fund_code).zfill(6)
    elif isinstance(fund_code, str):
        fund_code = fund_code.replace('.0', '').zfill(6)
    elif isinstance(fund_code, np.number):
        fund_code = str(int(fund_code)).replace('.0', '').zfill(6)
    return fund_code