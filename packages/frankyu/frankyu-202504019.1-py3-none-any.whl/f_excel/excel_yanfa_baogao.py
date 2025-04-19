#!/usr/bin/env python
# coding: utf-8
# 脚本起始行，指定解释器为 python 并且设置编码为 utf-8

import os  # 导入 os 模块，用於文件和目錄操作
import win32com.client  # 导入 win32com.client 模块，用於與 Windows 應用程式（如 Excel）交互
import datetime  # 导入 datetime 模块，用於更方便地處理日期

def convert_formula_to_value(sheet, cell_range):
    """
    將指定工作表的單元格範圍內的公式轉換為值。

    Args:
        sheet: Excel 工作表物件。
        cell_range: 要處理的單元格範圍字串 (例如 "B2" 或 "B5:Z100")。
    """
    try:  # 使用 try...except 塊捕獲可能發生的異常
        range_obj = sheet.Range(cell_range)  # 獲取指定的單元格範圍物件
        range_obj.Value = range_obj.Value  # 將範圍內的值賦值給自身，從而去除公式
        return True  # 返回 True 表示處理成功
    except Exception as e:  # 捕獲所有異常
        print(f'處理工作表 "{sheet.Name}" 的範圍 "{cell_range}" 時出錯: {e}')  # 打印詳細錯誤信息
        return False  # 返回 False 表示處理失敗

def process_excel_formulas(filepath, target_sheet_name="報告", formula_ranges=None):
    """
    去除 Excel 文件中特定单元格区域的公式，将其转换为值。

    Args:
        filepath: Excel 文件完整路径。
        target_sheet_name: 要處理的工作表名稱，默認為 "報告"。
        formula_ranges: 包含要轉換公式為值的單元格範圍列表，默認為 ["B2", "B5:Z100"]。

    Returns:
        True 如果處理成功，False 如果處理失敗。
    """
    if not os.path.exists(filepath):  # 檢查文件是否存在
        print(f'文件不存在: {filepath}')  # 打印文件不存在的消息
        return False  # 返回 False 表示處理失敗

    excel_app = None  # 初始化 Excel 應用程式物件為 None
    workbook = None  # 初始化 Excel 工作簿物件為 None
    if formula_ranges is None:  # 如果沒有提供 formula_ranges，則使用默認值
        formula_ranges = ["B2", "B5:Z100"]  # 定義要轉換公式為值的默認單元格範圍

    try:  # 使用 try...except...finally 塊處理可能發生的異常並確保資源釋放
        excel_app = win32com.client.Dispatch('Excel.Application')  # 創建 Excel 應用程式物件
        excel_app.Visible = False  # 設置 Excel 應用程式不可見
        workbook = excel_app.Workbooks.Open(filepath)  # 打開指定的 Excel 文件
        excel_app.DisplayAlerts = False  # 禁用 Excel 的警告提示
        sheet = workbook.Worksheets(target_sheet_name)  # 獲取指定名稱的工作表

        for cell_range in formula_ranges:  # 遍歷需要處理的單元格範圍
            if not convert_formula_to_value(sheet, cell_range):  # 調用函數將公式轉換為值
                return False  # 如果轉換失敗，則返回 False

        workbook.Save()  # 保存工作簿
        print(f'{workbook.Name} quCuLianJie OK')  # 打印處理成功的消息
        return True  # 返回 True 表示處理成功

    except Exception as e:  # 捕獲所有異常
        print(f'處理文件 {filepath} 的公式時出錯: {e}')  # 打印詳細錯誤信息
        return False  # 返回 False 表示處理失敗
    finally:  # 無論是否發生異常，都執行以下代碼
        if workbook:  # 如果工作簿物件存在
            workbook.Close(False)  # 關閉工作簿，不保存更改（因為之前已經保存了）
        if excel_app:  # 如果 Excel 應用程式物件存在
            excel_app.Quit()  # 退出 Excel 應用程式

def delete_other_sheets(filepath, target_sheet_name="報告"):
    """
    删除 Excel 文件中除了指定工作表之外的所有其他工作表。

    Args:
        filepath: Excel 文件完整路径。
        target_sheet_name: 要保留的工作表名稱，默認為 "報告"。

    Returns:
        True 如果處理成功，False 如果處理失敗。
    """
    if not os.path.exists(filepath):  # 檢查文件是否存在
        print(f'文件不存在: {filepath}')  # 打印文件不存在的消息
        return False  # 返回 False 表示處理失敗

    excel_app = None  # 初始化 Excel 應用程式物件為 None
    workbook = None  # 初始化 Excel 工作簿物件為 None
    try:  # 使用 try...except...finally 塊處理可能發生的異常並確保資源釋放
        excel_app = win32com.client.Dispatch('Excel.Application')  # 創建 Excel 應用程式物件
        excel_app.Visible = False  # 設置 Excel 應用程式不可見
        workbook = excel_app.Workbooks.Open(filepath)  # 打開指定的 Excel 文件
        excel_app.DisplayAlerts = False  # 禁用 Excel 的警告提示

        sheets_to_delete = []  # 初始化一個列表，用於存儲需要刪除的工作表
        for sheet in workbook.Worksheets:  # 遍歷工作簿中的所有工作表
            if sheet.Name != target_sheet_name:  # 如果工作表名稱不是目標名稱
                sheets_to_delete.append(sheet)  # 將該工作表添加到待刪除列表中

        # 逆序删除，避免索引问题
        for sheet in reversed(sheets_to_delete):  # 逆序遍歷待刪除的工作表列表
            print(f'正在刪除工作表: {sheet.Name}')  # 打印正在刪除的工作表名稱
            sheet.Delete()  # 刪除工作表

        workbook.Save()  # 保存工作簿
        print(f'{workbook.Name} canCuSheet OK')  # 打印處理成功的消息
        return True  # 返回 True 表示處理成功

    except Exception as e:  # 捕獲所有異常
        print(f'處理文件 {filepath} 的工作表時出錯: {e}')  # 打印詳細錯誤信息
        return False  # 返回 False 表示處理失敗
    finally:  # 無論是否發生異常，都執行以下代碼
        if workbook:  # 如果工作簿物件存在
            workbook.Close(False)  # 關閉工作簿，不保存更改
        if excel_app:  # 如果 Excel 應用程式物件存在
            excel_app.Quit()  # 退出 Excel 應用程式

def find_excel_files(pathroot, file_extension=".xlsx"):
    """
    遍历指定根目录下的所有文件夹和文件，并将所有指定扩展名的文件的完整路径添加到列表中返回。

    Args:
        pathroot: 根目录路径。
        file_extension: 要查找的文件扩展名，默认为 ".xlsx"。

    Returns:
        包含所有指定扩展名文件完整路径的列表。
    """
    file_list = []  # 初始化一個空列表，用於存儲文件路徑
    for root_dir, _, files in os.walk(pathroot):  # 使用 os.walk 遍歷目錄樹
        for file in files:  # 遍歷當前目錄下的所有文件
            if file.endswith(file_extension):  # 如果文件名以指定的擴展名結尾
                file_path = os.path.join(root_dir, file)  # 創建文件的完整路徑
                file_list.append(file_path)  # 將文件路徑添加到列表中
    return file_list  # 返回包含所有找到的 Excel 文件路徑的列表

def rename_excel_file(excelpath, new_file_prefix="品质检测报告"):
    """
    根据 Excel 文件的路径信息，按照特定规则重命名 Excel 文件。

    Args:
        excelpath: Excel 文件完整路径。
        new_file_prefix: 新文件名的前缀，默认为 "品质检测报告"。

    Returns:
        True 如果重命名成功，False 如果重命名失败。
    """
    month_dict = {  # 定義月份數字到英文縮寫的映射字典
        8: "Aug", 7: "Jul", 1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    path_parts = excelpath.split("\\")  # 將文件路徑按反斜杠分割成列表
    if len(path_parts) < 2:  # 檢查路徑是否包含足夠的信息
        print(f'文件路徑格式不正確: {excelpath}')  # 打印路徑格式錯誤的消息
        return False  # 返回 False 表示重命名失敗

    folder_name = path_parts[-2]  # 獲取文件所在的上級文件夾名稱
    file_name_with_extension = path_parts[-1]  # 獲取包含擴展名的文件名

    try:  # 使用 try...except 塊處理可能發生的異常
        month_year_str = folder_name  # 假設文件夾名稱是 "年.月" 的格式
        year_str_2digit = month_year_str.split(".")[0]  # 從文件夾名稱中提取年份（兩位數字）
        month_str_2digit = month_year_str.split(".")[1]  # 從文件夾名稱中提取月份（兩位數字）
        month_int = int(month_str_2digit)  # 將月份字符串轉換為整數
        month_abbr = month_dict.get(month_int)  # 從字典中獲取月份的英文縮寫
        if not month_abbr:  # 如果無法識別月份
            print(f'無法識別的月份: {month_str_2digit}，文件: {excelpath}')  # 打印無法識別的月份消息
            return False  # 返回 False 表示重命名失敗

        file_name_without_extension = file_name_with_extension.split(".")[0]  # 去除文件擴展名的文件名
        folder_path = os.path.dirname(excelpath)  # 獲取文件所在的目錄路徑
        new_file_name_without_extension = (  # 創建新的文件名（不包含擴展名）
            f"{new_file_prefix}{file_name_without_extension}-20{year_str_2digit}-{month_abbr}"
        )
        new_file_name = new_file_name_without_extension + ".xlsx"  # 創建包含擴展名的新文件名
        new_file_path = os.path.join(folder_path, new_file_name)  # 創建新的完整文件路徑

        os.rename(excelpath, new_file_path)  # 重命名文件
        print(f'{new_file_path} 重命名成功。')  # 打印重命名成功的消息
        return True  # 返回 True 表示重命名成功

    except (ValueError, IndexError) as e:  # 捕獲值錯誤或索引錯誤
        print(f'解析文件路徑或文件名時出錯: {e}，文件: {excelpath}')  # 打印解析錯誤信息
        return False  # 返回 False 表示重命名失敗
    except FileExistsError:  # 捕獲文件已存在的錯誤
        print(f'文件已存在，無法重命名: {new_file_path}')  # 打印文件已存在無法重命名的消息
        return False  # 返回 False 表示重命名失敗
    except Exception as e:  # 捕獲所有其他異常
        print(f'重命名文件 {excelpath} 出錯: {e}')  # 打印重命名文件出錯的消息
        return False  # 返回 False 表示重命名失敗

def should_rename(filepath, renamed_keyword="品质"):
    """
    检查文件是否需要重命名。如果文件名中包含指定的关键字，则认为已重命名。

    Args:
        filepath: Excel 文件完整路径。
        renamed_keyword: 用于判断文件是否已重命名的关键字，默认为 "品质"。

    Returns:
        True 如果文件已重命名或重命名成功，False 如果文件不存在或重命名失败。
    """
    if not os.path.exists(filepath):  # 檢查文件是否存在
        print(f'文件不存在: {filepath}')  # 打印文件不存在的消息
        return False  # 返回 False

    if renamed_keyword in os.path.basename(filepath):  # 檢查文件名是否包含指定的關鍵字
        print(f'{filepath} 已经完成,无需转化')  # 打印文件已完成無需轉化的消息
        return True  # 返回 True 表示已處理
    else:  # 如果文件名不包含指定的關鍵字
        return rename_excel_file(filepath)  # 調用 rename_excel_file 函數進行重命名

def process_excel_files(root_path_list, target_filename_length=len(r"2024RD05.xlsx"),
                       target_sheet_name="報告", formula_cell_ranges=None,
                       renamed_check_keyword="品质", new_file_prefix="品质检测报告"):
    """
    遍历指定根目录列表下的所有 Excel 文件，并根据文件名进行处理。

    Args:
        root_path_list: 根目录路径列表。
        target_filename_length: 需要處理的文件名的長度，默認為 len("2024RD05.xlsx")。
        target_sheet_name: 要處理的工作表名稱，默認為 "報告"。
        formula_cell_ranges: 包含要轉換公式為值的單元格範圍列表，默認為 ["B2", "B5:Z100"]。
        renamed_check_keyword: 用于判断文件是否已重命名的关键字，默认为 "品质"。
        new_file_prefix: 新文件名的前缀，默认为 "品质检测报告"。
    """
    for root_path in root_path_list:  # 遍歷根目錄路徑列表
        print(f'正在處理目錄: {root_path}')  # 打印正在處理的目錄
        file_list = find_excel_files(root_path)  # 獲取當前目錄下的所有 Excel 文件列表
        if not file_list:  # 如果當前目錄沒有 Excel 文件
            print(f'目錄 {root_path} 中沒有找到 Excel 文件')  # 打印未找到文件的消息
            continue  # 跳過當前目錄，處理下一個目錄

        for file_path in file_list:  # 遍歷文件列表
            if len(os.path.basename(file_path)) == target_filename_length:  # 篩選文件名長度符合條件的文件
                print(f'處理文件: {file_path}')  # 打印正在處理的文件路徑
                if process_excel_formulas(  # 調用 process_excel_formulas 函數處理公式
                    file_path,
                    target_sheet_name=target_sheet_name,
                    formula_ranges=formula_cell_ranges
                ):
                    if delete_other_sheets(file_path, target_sheet_name=target_sheet_name):  # 調用 delete_other_sheets 函數刪除其他工作表
                        should_rename(file_path, renamed_keyword=renamed_check_keyword)  # 調用 should_rename 函數判斷是否需要重命名
                        print(f'{file_path} 處理完成')  # 打印文件處理完成提示
                    else:  # 如果 delete_other_sheets 處理失敗
                        print(f'{file_path} delete_other_sheets 處理失敗')  # 打印 delete_other_sheets 失敗提示
                else:  # 如果 process_excel_formulas 處理失敗
                    print(f'{file_path} process_excel_formulas 處理失敗')  # 打印 process_excel_formulas 失敗提示
                print(" over")  # 打印 " over" 表示當前文件處理的子步驟完成
            else:  # 如果文件名長度不符合條件
                print(f'跳過文件: {file_path}, 文件名格式不符合條件')  # 打印跳過處理的文件提示
        print(f'目錄 {root_path} 處理完成')  # 打印目錄處理完成提示
    print("all over")  # 所有目錄處理完成提示

if __name__ == "__main__":  # main 函數入口
    # 示例根目录路径列表，请根据实际情况修改为你要处理的 Excel 文件所在的根目录
    root_directories = [
        r"C:\Users\frank_yu\Downloads\sc26\1348",  # 示例目录1，请替换为实际目录
        r"D:\新增資料夾\中间数据"    # 示例目录2，请替换为实际目录
        # 可以添加更多根目录路径
    ]

    # 定義需要處理的工作表名稱
    report_sheet = "報告"
    # 定義需要去除公式的單元格範圍
    formula_cells = ["B2", "B5:Z100"]
    # 定義判斷文件是否已重命名的關鍵字
    renamed_keyword_check = "品质"
    # 定義新的文件名的前綴
    new_report_prefix = "品质检测报告"
    # 定義需要處理的文件名的長度
    target_filename_len = len(r"2024RD05.xlsx")

    print("开始处理 Excel 文件...")  # 打印程序開始運行提示
    process_excel_files(  # 調用文件處理函數，批量處理指定目錄下的 Excel 文件
        root_directories,
        target_filename_length=target_filename_len,
        target_sheet_name=report_sheet,
        formula_cell_ranges=formula_cells,
        renamed_check_keyword=renamed_keyword_check,
        new_file_prefix=new_report_prefix
    )
    print("所有 Excel 文件处理完成。")  # 打印程序結束運行提示
    print("over")  # 打印 "over"，作為腳本結束的標記