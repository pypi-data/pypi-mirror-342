# 导入 win32com.client 模块，
# 用于与 Microsoft Office 应用程序进行交互
import win32com.client as win32
# 导入 string 模块，
# 该模块包含一些常用的字符串常量
import string
# 导入 datetime 模块，
# 用于处理日期和时间
from datetime import datetime

# 定义函数 create_excel_application，
# 用于创建并返回 Excel 应用程序对象
def create_excel_application():
    """
    创建并返回 Excel 应用程序对象。

    返回:
        excel_app: Excel 应用程序对象，
                   允许与 Excel 进行交互。
    """
    # 使用 win32.Dispatch 连接到 Excel 应用程序
    excel_app = win32.Dispatch("Excel.Application")
    # 禁用所有警告弹窗（如覆盖文件、公式错误等）
    excel_app.DisplayAlerts = False   # 关闭警告提示
    # 设置 Excel 应用程序的可见性，
    # 1 表示显示 Excel 窗口，
    # 0 表示在后台运行
    excel_app.Visible = 1
    # 返回创建的 Excel 应用程序对象
    return excel_app


# 定义函数 create_new_workbook，
# 接收 Excel 应用程序对象，
# 创建并返回一个新的工作簿对象
def create_new_workbook(app):
    """
    接收 Excel 应用程序对象，
    创建并返回一个新的工作簿对象。

    参数:
        app: Excel 应用程序对象，
             用于创建新的工作簿。

    返回:
        workbook: 新创建的工作簿对象。
    """
    # 使用应用程序对象的 Workbooks.Add() 方法
    # 创建一个新的工作簿
    workbook = app.Workbooks.Add()
    # 返回新创建的工作簿对象
    return workbook


# 定义函数 generate_timestamped_filename，
# 生成并返回包含指定基础文件名
# 和当前时间戳的文件名
def generate_timestamped_filename(base_filename="字母表"):
    """
    生成并返回包含指定基础文件名
    和当前时间戳的文件名。

    参数:
        base_filename: 基础文件名，默认为“字母表”。

    返回:
        filename: 生成的文件名，
                  格式为“基础文件名_时间戳.xlsx”。
    """
    # 获取当前的日期和时间
    now = datetime.now()
    # 将当前的日期和时间格式化为指定的字符串格式
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # 使用 f-string 创建包含基础文件名和时间戳的文件名
    filename = f"{base_filename}_{timestamp}.xlsx"
    # 返回生成的文件名
    return filename


# 定义函数 save_excel_file，
# 接收工作簿对象和文件路径，
# 保存 Excel 文件并关闭工作簿
def save_excel_file(workbook, filepath):
    """
    接收工作簿对象和文件路径，
    保存 Excel 文件并关闭工作簿。

    参数:
        workbook: 要保存的工作簿对象。
        filepath: 保存文件的完整路径，包括文件名。
    """
    # 使用工作簿对象的 SaveAs() 方法
    # 将工作簿保存到指定的文件路径
    workbook.SaveAs(filepath)
    # workbook.Close()  # 可选：关闭工作簿


# 定义函数 write_alphabet_to_excel，
# 接收工作表对象，
# 将字母表写入 A1:A26 单元格
def write_alphabet_to_excel(worksheet):
    """
    接收工作表对象，
    将字母表写入 A1:A26 单元格。

    参数:
        worksheet: 要写入字母表的工作表对象。
    """
    # 创建一个包含大写字母表的列表，
    # 每个字母都在一个子列表中
    alphabet = [[letter] for letter in string.ascii_uppercase]
    # 使用工作表对象的 Range() 方法选择 A1:A26 单元格，
    # 并将字母表写入这些单元格
    worksheet.Range("A1:A26").Value = alphabet


# 定义函数 add_comments_to_rows，
# 接收工作表对象，
# 在 B1:B26 单元格中添加注释“Alphabet Letter”
def add_comments_to_rows(worksheet):
    """
    接收工作表对象，
    在 B1:B26 单元格中添加注释“Alphabet Letter”。

    参数:
        worksheet: 要添加注释的工作表对象。
    """
    # 循环遍历从 1 到 26 的数字，
    # 代表 Excel 的行号
    for i in range(1, 27):
        # 使用工作表对象的 Cells() 方法选择要添加注释的单元格，
        # 这里是第 i 行的第 2 列（B 列）
        cell_to_comment = worksheet.Cells(i, 2)
        # 使用单元格对象的 AddComment() 方法添加注释，
        # 注释内容为 "Alphabet Letter"
        cell_to_comment.AddComment("Alphabet Letter")


# 定义函数 main，作为脚本的主函数，
# 负责协调其他函数的执行
def main():
    """
    脚本的主函数，
    负责协调其他函数的执行。

    该函数创建 Excel 应用程序，
    生成新的工作簿，
    写入字母表，
    并保存文件。
    """
    # 调用 create_excel_application() 函数
    # 创建 Excel 应用程序对象
    excel_app = create_excel_application()

    # 调用 create_new_workbook() 函数，
    # 传入 Excel 应用程序对象，
    # 创建一个新的工作簿对象
    workbook = create_new_workbook(excel_app)

    # 获取活动工作表
    worksheet = workbook.ActiveSheet

    # 调用 write_alphabet_to_excel() 函数，
    # 将字母表写入活动工作表
    write_alphabet_to_excel(worksheet)

    # add_comments_to_rows(worksheet)  # 可选：添加注释

    # 调用 generate_timestamped_filename() 函数
    # 生成带有时间戳的文件名
    filename = generate_timestamped_filename()

    # 定义保存文件的目录
    save_directory = r"T:\xls\\"

    # 构建完整的文件路径
    filepath = save_directory + filename

    # 调用 save_excel_file() 函数，
    # 保存工作簿到指定的文件路径
    save_excel_file(workbook, filepath)

    #excel_app.Quit()  # 可选：退出 Excel 应用程序

    # 打印一条消息，
    # 指示文件已成功创建并保存到哪个路径
    print(f"Excel 文件已成功创建并保存到：{filepath}")


# 判断当前模块是否作为主程序运行
if __name__ == "__main__":
    # 如果是，则调用 main() 函数开始执行脚本
    main()