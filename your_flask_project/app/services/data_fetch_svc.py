import pandas as pd
import akshare as ak
import requests
import re
import time # For CLS News timestamp

# Attempt to import the custom akShareUnit
try:
    from original_codebase_references.util.akShare_unit import akShareUnit
    ak_unit_instance = akShareUnit()
    print("Successfully imported akShareUnit from original_codebase_references.")
except ImportError:
    print("Warning: original_codebase_references.util.akShare_unit not found or akShareUnit class not found. Using dummy akShareUnit and direct akshare calls.")
    ak_unit_instance = None
    class DummyAkShareUnit:
        def _create_dummy_df(self, columns, num_rows=5, prefix="dummy"):
            data = {}
            for col_info in columns:
                col_name = col_info if isinstance(col_info, str) else col_info[0]
                if col_name == '代码': data[col_name] = [f'{prefix}{i:03d}' for i in range(1, num_rows + 1)]
                elif col_name == '名称': data[col_name] = [f'Dummy {prefix.capitalize()} {i}' for i in range(1, num_rows + 1)]
                elif '最新价' in col_name: data[col_name] = [100.0 + i for i in range(1, num_rows + 1)]
                elif '涨跌幅' in col_name: data[col_name] = [0.05 * i for i in range(1, num_rows + 1)]
                elif '成交量' in col_name: data[col_name] = [1000 * i for i in range(1, num_rows + 1)]
                elif '成交额' in col_name: data[col_name] = [100000 * i for i in range(1, num_rows + 1)]
                elif '总市值' in col_name: data[col_name] = [1E9 + i*1E7 for i in range(1, num_rows + 1)]
                elif '主力净流入-净额' in col_name: data[col_name] = [50000 * i for i in range(1,num_rows+1)]
                elif '超大单净流入-净额' in col_name: data[col_name] = [20000 * i for i in range(1,num_rows+1)]
                elif '板块名称' in col_name: data[col_name] = [f'Sector {i}' for i in range(1,num_rows+1)]
                elif '领涨股' in col_name and '代码' not in col_name and '涨跌幅' not in col_name : data[col_name] = [f'LeadStock{i}' for i in range(1,num_rows+1)]
                elif '封单资金' in col_name: data[col_name] = [1000000 * i for i in range(1, num_rows+1)]
                elif '涨停天数' in col_name: data[col_name] = [i for i in range(1, num_rows+1)]
                # For CLS News dummy
                elif col_name == '时间': data[col_name] = [pd.Timestamp.now() - pd.Timedelta(minutes=i*10) for i in range(num_rows)]
                elif col_name == '内容': data[col_name] = [f'This is dummy news content for item {i}. Something important happened.' for i in range(num_rows)]
                elif col_name == '快讯ID': data[col_name] = [1000+i for i in range(num_rows)]
                elif col_name == '资讯类型': data[col_name] = [0 for _ in range(num_rows)]


                else: data[col_name] = [f'val{i}' for i in range(1, num_rows + 1)]
            return pd.DataFrame(data)

        def get_stock_info_a_code_name(self): return self._create_dummy_df(['code', 'name'], 50, "A")
        def get_bank_CurrentQuotes(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌额', '涨跌幅', '昨收', '今开', '最高', '最低', '成交量', '成交额'], 5, "DomIdx")
        def get_etf_spot_list_em(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅'], 5, "ETF")
        def get_convertible_bond_list_em(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅', '正股代码', '正股名称'], 5, "CBond")
        def get_us_stock_list_em(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅', '成交额', '总市值'], 5, "US")
        def get_hk_stock_list_em(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅', '成交额'], 5, "HK")
        def get_chinese_concept_stock_list_em(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅', '总市值'], 5, "USZH")
        def get_chinext_spot_list(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅'], 5, "CY")
        def get_sme_spot_list(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅'], 5, "ZX")
        def get_star_market_spot_list(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅'], 5, "KCB")
        def get_bse_spot_list(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅'], 5, "BJ")

        def get_large_orders_data_dummy(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅', '主力净流入-净额', '超大单净流入-净额'], 50, "LO")
        def get_sector_monitor_data_dummy(self): return self._create_dummy_df(['板块名称', '涨跌幅', '总市值', '领涨股', '领涨股代码', '领涨股-涨跌幅'], 20, "Sector")
        def get_concept_sectors_data_dummy(self): return self._create_dummy_df(['板块名称', '涨跌幅', '总市值', '领涨股', '领涨股代码', '领涨股-涨跌幅'], 20, "Concept")
        def get_stock_quotes_general_dummy(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨跌幅', '成交额', '总市值'], 50, "Quote")
        def get_limit_up_stocks_dummy(self): return self._create_dummy_df(['代码', '名称', '最新价', '涨停价', '成交额', '流通市值', '封单资金', '涨停天数', '所属行业'], 15, "LimitUp")
        def get_cls_news_dummy(self): # For ak.cls_telegraph_news()
            # Expected columns: '时间', '内容', '快讯ID', '资讯类型', '标签', '重要性', '个股代码', '个股名称', '板块代码', '板块名称'
            print("DummyAkShareUnit: Returning sample CLS news data.")
            return self._create_dummy_df(['时间', '内容', '快讯ID', '资讯类型'], 25, "CLS")


    ak_unit_instance = DummyAkShareUnit()

def _paginate_dataframe(df: pd.DataFrame, page: int, per_page: int):
    if df is None or df.empty: return pd.DataFrame(), 0, 1
    total_items = len(df)
    total_pages = (total_items + per_page - 1) // per_page if per_page > 0 else 1
    start = (page - 1) * per_page
    end = start + per_page
    paginated_df = df.iloc[start:end]
    return paginated_df, total_items, total_pages

def _fetch_data_with_fallback(ak_method_name_custom_or_direct_func, page, per_page, *args, **kwargs):
    is_method_name = isinstance(ak_method_name_custom_or_direct_func, str)
    if is_method_name: dummy_method_name = ak_method_name_custom_or_direct_func
    elif hasattr(ak_method_name_custom_or_direct_func, '__name__'): dummy_method_name = f"{ak_method_name_custom_or_direct_func.__name__}_dummy"
    else: dummy_method_name = "generic_dummy_method"
    try:
        df = None
        if is_method_name and ak_unit_instance and hasattr(ak_unit_instance, ak_method_name_custom_or_direct_func) and not isinstance(ak_unit_instance, DummyAkShareUnit):
            df = getattr(ak_unit_instance, ak_method_name_custom_or_direct_func)(*args, **kwargs)
        elif not is_method_name:
             print(f"Using direct akshare call ak.{ak_method_name_custom_or_direct_func.__name__}.")
             df = ak_method_name_custom_or_direct_func(*args, **kwargs)
        elif isinstance(ak_unit_instance, DummyAkShareUnit) and hasattr(ak_unit_instance, ak_method_name_custom_or_direct_func):
            print(f"Using dummy method DummyAkShareUnit.{ak_method_name_custom_or_direct_func}.")
            df = getattr(ak_unit_instance, ak_method_name_custom_or_direct_func)(*args, **kwargs)
        else: raise ValueError(f"No valid real or dummy function for {ak_method_name_custom_or_direct_func}")
        paginated_df, total_items, total_pages = _paginate_dataframe(df, page, per_page)
        return paginated_df, total_items, total_pages, page
    except Exception as e:
        print(f"Error fetching data for {str(ak_method_name_custom_or_direct_func)}: {e}. Using dummy data as fallback.")
        if hasattr(DummyAkShareUnit(), dummy_method_name): df_dummy = getattr(DummyAkShareUnit(), dummy_method_name)()
        elif is_method_name and hasattr(DummyAkShareUnit(), ak_method_name_custom_or_direct_func): df_dummy = getattr(DummyAkShareUnit(), ak_method_name_custom_or_direct_func)()
        else: print(f"Could not find specific dummy method {dummy_method_name}, returning empty DataFrame."); df_dummy = pd.DataFrame()
        paginated_df, total_items, total_pages = _paginate_dataframe(df_dummy, page, per_page)
        return paginated_df, total_items, total_pages, page

# --- Stock Lists & Quotes ---
def get_a_share_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_stock_info_a_code_name', ak.stock_info_a_code_name, page, per_page)
def get_us_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_us_stock_list_em', ak.stock_us_spot_em, page, per_page)
def get_hk_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_hk_stock_list_em', ak.stock_hk_spot_em, page, per_page)
def get_chinese_concept_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_chinese_concept_stock_list_em', ak.stock_us_zh_spot, page, per_page)
def get_chinext_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_chinext_spot_list', ak.stock_cy_spot, page, per_page)
def get_sme_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_sme_spot_list', ak.stock_zx_spot, page, per_page)
def get_star_market_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_star_market_spot_list', ak.stock_kcb_spot, page, per_page)
def get_bse_stock_list(page=1, per_page=30): return _fetch_data_with_fallback('get_bse_spot_list', ak.stock_bj_a_spot_em, page, per_page)
def get_stock_quotes_general(page=1, per_page=50, stock_codes=None):
    if stock_codes:
         symbols_str = ",".join(stock_codes) if isinstance(stock_codes, list) else stock_codes
         return _fetch_data_with_fallback(ak.stock_zh_a_spot_em, page, per_page, symbols=symbols_str)
    return _fetch_data_with_fallback('get_stock_quotes_general_dummy', ak.stock_zh_a_spot_em, page, per_page)

# --- Indices & Bonds ---
def get_domestic_indices(page=1, per_page=30): return _fetch_data_with_fallback('get_bank_CurrentQuotes', ak.stock_zh_index_spot, page, per_page)
def get_global_indices(page=1, per_page=30): return _fetch_data_with_fallback(ak.index_world_spot_sina, page, per_page)
def get_global_bond_list(page=1, per_page=30): return _fetch_data_with_fallback(ak.bond_world_index_current, page, per_page)

# --- ETFs & Convertible Bonds ---
def get_etf_spot_list(page=1, per_page=30): return _fetch_data_with_fallback('get_etf_spot_list_em', ak.fund_etf_spot_em, page, per_page)
def get_convertible_bond_list(page=1, per_page=30): return _fetch_data_with_fallback('get_convertible_bond_list_em', ak.bond_zh_cov_spot, page, per_page)

# --- Monitoring Center Data ---
def get_large_orders_data(page=1, per_page=30): return _fetch_data_with_fallback('get_large_orders_data_dummy', lambda: ak.stock_individual_fund_flow_rank(indicator="今日"), page, per_page)
def get_leading_stocks_data():
    tdx_url = "http://page.tdx.com.cn:7615/TQLEX?Entry=CWServ.cfg_fx_ygzl"; payload = {"Params": ["ygts"]}; headers = {'Content-Type': 'application/json'}
    leading_stocks_info = []; dummy_return = [{'code_full': 'dummy001', 'name': 'Dummy Lead', 'price': '10.0', 'chg_pct': '1.0%'}]
    try:
        response_tdx = requests.post(tdx_url, json=payload, headers=headers, timeout=3); response_tdx.raise_for_status(); tdx_data = response_tdx.json()
        if not tdx_data.get("Success", False) or not tdx_data.get("ResultSets"): return "龙头股数据获取失败(TDX)。"
        stock_codes_to_fetch = [f"{'sh' if row[1] == '1' else 'sz'}{row[0]}" for row in tdx_data["ResultSets"][0]["Content"]]
        if not stock_codes_to_fetch: return "没有获取到龙头股代码。"
        response_sina = requests.get(f"https://hq.sinajs.cn/?list={','.join(stock_codes_to_fetch)}", timeout=3); response_sina.raise_for_status()
        raw_data_lines = response_sina.text.split(';');
        for line in raw_data_lines:
            if not line.strip(): continue
            match = re.search(r'var hq_str_(\w+)="([^"]+)"', line)
            if match:
                full_code, data_str = match.group(1), match.group(2); parts = data_str.split(',')
                if len(parts) > 3:
                    price, prev_close = float(parts[3]), float(parts[2])
                    chg_pct = f"{( (price - prev_close) / prev_close * 100) if prev_close != 0 else 0 :.2f}%" if price != 0 and prev_close != 0 else "N/A"
                    leading_stocks_info.append({'code_full': full_code, 'code': full_code[2:], 'name': parts[0],'open': parts[1],'prev_close': parts[2],'price': parts[3],'high': parts[4],'low': parts[5],'volume': parts[8],'amount': parts[9],'chg_pct': chg_pct})
        return leading_stocks_info if leading_stocks_info else "获取龙头股行情失败(Sina)。"
    except requests.exceptions.RequestException as e: print(f"Net err: {e}"); return dummy_return
    except Exception as e: print(f"Proc err: {e}"); return dummy_return
def get_sector_monitor_data(page=1, per_page=30): return _fetch_data_with_fallback('get_sector_monitor_data_dummy', ak.stock_board_industry_spot_em, page, per_page)
def get_concept_sectors_data(page=1, per_page=30): return _fetch_data_with_fallback('get_concept_sectors_data_dummy', ak.stock_board_concept_spot_em, page, per_page)
def get_ranked_stock_fundflow(page=1, per_page=50): return _fetch_data_with_fallback('get_large_orders_data_dummy', lambda: ak.stock_individual_fund_flow_rank(indicator="今日"), page, per_page)
def get_limit_up_stocks(page=1, per_page=50): return _fetch_data_with_fallback('get_limit_up_stocks_dummy', ak.stock_zt_pool_em, page, per_page)

# --- News ---
def get_cls_news(page=1, per_page=20):
    # ak.cls_telegraph_news() returns a DataFrame with columns: '电报内容', '快讯ID', '快讯等级', '快讯来源', '快讯时间', '标签', '相关股票代码', '相关股票名称', '相关板块代码', '相关板块名称'
    # We can rename them for consistency if needed. For now, use original names.
    # The API itself doesn't support pagination directly, it gets latest. We paginate its output.
    return _fetch_data_with_fallback('get_cls_news_dummy', ak.cls_telegraph_news, page, per_page)
