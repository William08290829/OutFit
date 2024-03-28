import locale
from datetime import datetime, timedelta

def format_date(input_date):
    # 設置地區為中文
    locale.setlocale(locale.LC_TIME, 'zh_TW.UTF-8')
    
    # 將字符串轉換為日期對象
    
    # 格式化日期
    formatted_date = input_date.strftime("%#m/%d")
    weekday =  input_date.strftime("%A")
    
    return formatted_date, weekday

def get_future_date(days_offset):
    today = datetime.now().date()
    future_date = today + timedelta(days=days_offset)
    return future_date

def get_date_by_code(code):
    code_to_offset = {'d1': 1, 'd2': 2, 'd3': 3, 'd4': 4}

    if code in code_to_offset:
        days_offset = code_to_offset[code]
        return get_future_date(days_offset)
    else:
        return None  # 如果 code 不是有效的值，可以根據實際需求返回適當的值

def get_date_num_by_code(code):
    code_to_offset = {'d1': 1, 'd2': 2, 'd3': 3, 'd4': 4}
    
    if code in code_to_offset:
        date_num = code_to_offset[code]
        return date_num
    
    return None