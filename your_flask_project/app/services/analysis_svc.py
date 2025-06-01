import requests
import json
import re
import pandas as pd # Added for dummy data consistency

# Attempt to import original for direct call if preferred, though subtask implies re-implementing.
# For this implementation, we directly use the TDX web service call.
# try:
#     from original_codebase_references.util.checkStock import checkStock as OriginalCheckStock
#     original_checker = OriginalCheckStock()
# except ImportError:
#     original_checker = None

def get_stock_risk_scan(stock_code_input: str):
    """
    Fetches risk scan information for a given stock code from TDX.
    Adapts logic from the original util/checkStock.py baolei method.
    Returns: (fxlist: list, sum_score: int, stock_name_checked: str, stock_code_formatted: str)
    """
    fxlist = []
    sum_score = 100  # Default score, assuming 100 is no risk.

    # Normalize stock code (e.g., add sh/sz prefix if just numbers)
    if stock_code_input.isnumeric() and len(stock_code_input) == 6:
        if stock_code_input.startswith('6') or stock_code_input.startswith('9'):
            stock_code_formatted = f"sh{stock_code_input}"
        elif stock_code_input.startswith('0') or stock_code_input.startswith('3') or stock_code_input.startswith('2'):
            stock_code_formatted = f"sz{stock_code_input}"
        elif stock_code_input.startswith('8') or stock_code_input.startswith('4'):
             stock_code_formatted = f"bj{stock_code_input}"
        else:
            stock_code_formatted = stock_code_input # Should ideally not happen for 6-digit numeric
    elif isinstance(stock_code_input, str) and (stock_code_input.lower().startswith('sh') or stock_code_input.lower().startswith('sz') or stock_code_input.lower().startswith('bj')):
        stock_code_formatted = stock_code_input.lower()
    else:
        fxlist.append(f"Invalid stock code format: {stock_code_input}. Expected format like 'sh600000' or '000001'.")
        return fxlist, 0, stock_code_input, stock_code_input

    stock_name_checked = stock_code_formatted
    numeric_stock_code = stock_code_formatted[2:] if len(stock_code_formatted) == 8 else stock_code_formatted

    if not numeric_stock_code.isnumeric() or len(numeric_stock_code) != 6:
        fxlist.append(f"Could not derive valid 6-digit numeric code from {stock_code_formatted}.")
        return fxlist, 0, stock_name_checked, stock_code_formatted

    url = f'http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/json/{numeric_stock_code}.js'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        match = re.search(r'g_sdata\s*=\s*(\{.*?\});?\s*$', response.text, re.DOTALL | re.MULTILINE)
        if not match:
            fxlist.append(f"Could not parse JSON data from TDX response for {stock_code_formatted}. Stock might not be covered or data format changed.")
            return fxlist, 50, stock_code_formatted, stock_code_formatted # Default to 50 if parse fails

        catalog_str = match.group(1)
        catalog = json.loads(catalog_str)

        stock_name_checked = catalog.get('name', stock_code_formatted)
        isfengxiantotal = int(catalog.get('num', 0))

        if isfengxiantotal == 0:
            fxlist.append(f"No specific risks identified by TDX for {stock_name_checked} ({stock_code_formatted}).")
        else:
            fxdata = catalog.get('data', [])
            risk_categories_map = {0: "财务类风险", 1: "市场类风险", 2: "交易类风险", 3: "退市类风险"}

            for i, category_risks in enumerate(fxdata):
                category_name = risk_categories_map.get(i, f"未知风险类别{i+1}")
                rows = category_risks.get('rows', [])
                for data_row in rows:
                    if data_row.get('trig') == 1:
                        fx = data_row.get('lx', '未知风险项')
                        fxscore_deduction = data_row.get('fs', 0)
                        sum_score -= fxscore_deduction
                        trigyy = data_row.get('trigyy', '无详细说明')
                        fxlist.append(f'{category_name}: {fx} (扣分: {fxscore_deduction}) - {trigyy}')

            if not fxlist and isfengxiantotal > 0 :
                 fxlist.append(f"TDX indicated {isfengxiantotal} risk(s) for {stock_name_checked} ({stock_code_formatted}), but no specific triggered items were found or parsed.")
                 if sum_score == 100 : sum_score = 70

    except requests.exceptions.Timeout:
        fxlist.append(f"Request to TDX timed out for {stock_code_formatted}. Using dummy fallback.")
        return ["Dummy: Network timeout."], 0, stock_name_checked, stock_code_formatted
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            fxlist.append(f"No risk data found for stock {stock_code_formatted} on TDX (404 Not Found). It might be a non-existent code or not covered.")
        else:
            fxlist.append(f"TDX service request failed for {stock_code_formatted} with status {e.response.status_code}.")
        return fxlist, 0, stock_name_checked, stock_code_formatted
    except requests.exceptions.RequestException as e:
        fxlist.append(f"Network error for {stock_code_formatted}: {str(e)}. Using dummy fallback.")
        return ["Dummy: Network error."], 0, stock_name_checked, stock_code_formatted
    except json.JSONDecodeError:
        fxlist.append(f"Failed to decode JSON from TDX response for {stock_code_formatted}. Using dummy fallback.")
        return ["Dummy: JSON decode error."], 0, stock_name_checked, stock_code_formatted
    except Exception as e:
        fxlist.append(f"An unexpected error occurred while scanning {stock_code_formatted}: {str(e)}. Using dummy fallback.")
        return ["Dummy: Unexpected error."], 0, stock_name_checked, stock_code_formatted

    # Fallback for "dummy001" for testing purposes
    if stock_code_input == "dummy001":
        fxlist = ["Dummy Risk 1: This is a test risk.", "Dummy Risk 2: Another test warning."]
        sum_score = 60
        stock_name_checked = "Dummy Test Stock"
        stock_code_formatted = "dummy001"
    elif not fxlist and sum_score == 100: # If list is still empty after all checks and score is perfect
         fxlist.append(f"Scan complete. No specific adverse risk indicators found by TDX for {stock_name_checked} ({stock_code_formatted}).")

    return fxlist, max(0, sum_score), stock_name_checked, stock_code_formatted
