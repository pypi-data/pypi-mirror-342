import pythoncom
# 导入 pythoncom 模块，用于处理 COM (Component Object Model) 对象
import win32com.client
# 导入 win32com.client 模块，用于与 Windows 应用程序（如 Outlook）进行交互
from datetime import datetime
# 导入 datetime 模块，用于处理日期和时间（虽然当前代码中未使用）
import os
# 导入 os 模块，用于处理操作系统相关的功能（虽然当前代码中未使用）

def initialize_outlook():
    """
    初始化 Outlook 应用程序并获取 MAPI 命名空间。

    此函数尝试连接到 Outlook 应用程序，并返回 MAPI
    (Messaging Application Programming Interface) 命名空间对象。
    MAPI 允许程序访问 Outlook 的数据。

    参数:
        无

    返回值:
        mapi: Outlook 的 MAPI 命名空间对象，如果初始化成功。
              None，如果初始化失败（例如，Outlook 未安装或发生 COM 错误）。

    变量:
        pythoncom: 用于处理 COM 对象的模块。
        win32com.client: 用于创建和调度 COM 对象的模块。
        outlook: 代表 Outlook 应用程序的 COM 对象。
        mapi: 代表 Outlook 的 MAPI 命名空间的 COM 对象。
        e: 捕获到的异常对象，用于打印错误信息。
    """
    try:
        pythoncom.CoInitialize()
        # 初始化 COM 库，这是使用 win32com 的必要步骤
        outlook = win32com.client.Dispatch("Outlook.Application")
        # 创建 Outlook 应用程序的 COM 对象
        mapi = outlook.GetNamespace("MAPI")
        # 获取 Outlook 的 MAPI 命名空间
        return mapi
        # 返回 MAPI 命名空间对象
    except pythoncom.com_error as e:
        # 捕获 COM 错误
        print(f"COM 错误: {e}")
        # 打印 COM 错误信息
        return None
        # 返回 None 表示初始化失败
    except Exception as e:
        # 捕获其他类型的异常
        print(f"初始化 Outlook 时发生其他错误: {str(e)}")
        # 打印其他错误信息
        return None
        # 返回 None 表示初始化失败

def find_outlook_account(mapi, account_email):
    """
    根据邮箱地址查找 Outlook 账户。

    此函数遍历 Outlook 的所有账户，并查找与提供的邮箱地址匹配的账户。

    参数:
        mapi: Outlook 的 MAPI 命名空间对象。
        account_email: 要查找的邮箱账户的电子邮件地址（字符串）。

    返回值:
        account: 匹配的 Outlook 账户对象，如果找到。
                 None，如果没有找到匹配的账户或 mapi 为 None。

    变量:
        mapi: Outlook 的 MAPI 命名空间对象。
        account_email: 要查找的邮箱账户的电子邮件地址。
        account: 当前遍历到的 Outlook 账户对象。
    """
    if mapi:
        # 检查 MAPI 命名空间是否已成功获取
        for account in mapi.Accounts:
            # 遍历 MAPI 中的所有账户
            if account.SmtpAddress.lower() == account_email.lower():
                # 将账户的 SMTP 地址转换为小写并与提供的邮箱地址进行比较（忽略大小写）
                return account
                # 如果找到匹配的账户，则返回该账户对象
        print(f"未找到邮箱账户: {account_email}")
        # 如果遍历完所有账户后没有找到匹配项，则打印未找到的消息
    return None
    # 如果 mapi 为 None 或没有找到匹配的账户，则返回 None

def get_folder_by_name(account, folder_name):
    """
    根据账户和文件夹名称获取 Outlook 文件夹对象。

    此函数根据提供的账户对象和文件夹名称，返回对应的 Outlook 文件夹对象。
    它处理了 "Inbox"（收件箱）和 "Sent Items"（已发送邮件）的特殊情况，
    并允许通过名称获取其他文件夹。

    参数:
        account: Outlook 账户对象。
        folder_name: 要获取的文件夹的名称（字符串），例如 "Inbox" 或 "Sent Items"。

    返回值:
        folder: 对应的 Outlook 文件夹对象，如果找到。
                None，如果没有找到匹配的文件夹或账户为 None。

    变量:
        account: Outlook 账户对象。
        folder_name: 要获取的文件夹的名称。
        folder: 获取到的 Outlook 文件夹对象。
        e: 捕获到的异常对象，用于打印错误信息。
    """
    if account:
        # 检查账户对象是否有效
        try:
            if folder_name == "Inbox":
                # 如果文件夹名称是 "Inbox"
                return account.DeliveryStore.GetDefaultFolder(6)
                # 返回默认的收件箱文件夹（编号 6）
            elif folder_name == "Sent Items":
                # 如果文件夹名称是 "Sent Items"
                return account.DeliveryStore.GetDefaultFolder(5)
                # 返回默认的已发送邮件文件夹（编号 5）
            else:
                # 如果是其他文件夹名称
                try:
                    folder = account.DeliveryStore.Folders(folder_name)
                    # 尝试通过名称获取文件夹
                    print(f"成功找到文件夹: {folder.Name}")
                    # 打印成功找到的文件夹名称
                    return folder
                    # 返回找到的文件夹对象
                except Exception as e:
                    # 捕获获取特定名称文件夹时可能发生的异常
                    print(f"未找到指定文件夹 '{folder_name}': {str(e)}")
                    # 打印未找到文件夹的错误信息
                    return None
                    # 返回 None 表示未找到
        except Exception as e:
            # 捕获获取默认文件夹或通过名称获取文件夹时可能发生的异常
            print(f"获取文件夹时出错: {str(e)}")
            # 打印获取文件夹时发生的错误信息
            return None
            # 返回 None 表示获取失败
    return None
    # 如果账户对象为 None，则返回 None

def get_emails(folder):
    """
    从指定的 Outlook 文件夹获取邮件列表并按接收时间排序。

    此函数接收一个 Outlook 文件夹对象，并返回该文件夹中所有邮件的集合，
    邮件列表会按照接收时间降序排列（最新的邮件在前面）。

    参数:
        folder: Outlook 文件夹对象。

    返回值:
        items: 包含邮件的集合对象，如果获取成功。
               None，如果获取失败或文件夹为 None。

    变量:
        folder: Outlook 文件夹对象。
        items: 包含邮件的集合对象。
        e: 捕获到的异常对象，用于打印错误信息。
    """
    if folder:
        # 检查文件夹对象是否有效
        try:
            items = folder.Items
            # 获取文件夹中的所有项目（包括邮件）
            items.Sort("[ReceivedTime]", True)
            # 对项目按接收时间进行排序，True 表示降序（最新的在前）
            return items
            # 返回排序后的邮件集合
        except Exception as e:
            # 捕获获取邮件列表时可能发生的异常
            print(f"获取邮件列表时出错: {str(e)}")
            # 打印错误信息
            return None
            # 返回 None 表示获取失败
    return None
    # 如果文件夹对象为 None，则返回 None

def print_email_info(email, folder_name, index):
    """
    打印单封邮件的信息。

    此函数接收一个邮件对象、所在的文件夹名称和邮件的索引，
    然后打印邮件的主题、发件人/收件人（根据文件夹类型判断）和接收时间。
    函数包含错误处理，以应对某些属性可能不存在的情况。

    参数:
        email: Outlook 邮件对象。
        folder_name: 邮件所在的文件夹名称（字符串），用于判断是收件箱还是已发送邮件。
        index: 邮件在列表中的索引（整数）。

    返回值:
        无

    变量:
        email: Outlook 邮件对象。
        folder_name: 邮件所在的文件夹名称。
        index: 邮件在列表中的索引。
    """
    print(f"邮件 {index}:")
    # 打印邮件的索引
    try:
        print(f"  主题: {email.Subject}")
        # 尝试打印邮件的主题
    except AttributeError:
        # 如果 Subject 属性不存在，则捕获 AttributeError
        print("  主题: 无法获取")
        # 打印无法获取主题的消息

    if folder_name == "Sent Items":
        # 如果是已发送邮件
        try:
            print(f"  收件人: {email.To}")
            # 尝试打印收件人信息
        except AttributeError:
            # 如果 To 属性不存在
            try:
                print(f"  发件人 (尝试 Sender): {email.Sender}")
                # 尝试打印发件人信息 (Sender 属性)
            except AttributeError:
                # 如果 Sender 属性也不存在
                try:
                    print(f"  发件人 (尝试 SenderName): {email.SenderName}")
                    # 尝试打印发件人名称 (SenderName 属性)
                except AttributeError:
                    # 如果 SenderName 属性也不存在
                    print("  无法获取发件人/收件人信息")
                    # 打印无法获取发件人/收件人信息的消息
    else:
        # 如果是收件箱或其他文件夹
        try:
            print(f"  发件人: {email.SenderName}")
            # 尝试打印发件人名称
        except AttributeError:
            # 如果 SenderName 属性不存在
            try:
                print(f"  发件人 (尝试 Sender): {email.Sender}")
                # 尝试打印发件人信息 (Sender 属性)
            except AttributeError:
                # 如果 Sender 属性也不存在
                print("  无法获取发件人信息")
                # 打印无法获取发件人信息的消息

    try:
        print(f"  接收时间: {email.ReceivedTime}")
        # 尝试打印接收时间
    except AttributeError:
        # 如果 ReceivedTime 属性不存在
        print("  接收时间: 无法获取")
        # 打印无法获取接收时间的消息

def print_emails_in_folder(folder_name, emails):
    """
    打印指定文件夹中的所有邮件信息。

    此函数接收文件夹名称和邮件列表，然后遍历邮件列表，
    并为每封邮件调用 print_email_info 函数来打印详细信息。

    参数:
        folder_name: 邮件所在的文件夹名称（字符串）。
        emails: 包含 Outlook 邮件对象的集合。

    返回值:
        无

    变量:
        folder_name: 邮件所在的文件夹名称.
        emails: 包含 Outlook 邮件对象的集合.
        idx: 循环索引，用于记录邮件的序号.
        email: 当前遍历到的 Outlook 邮件对象.
    """
    if emails:
        # 检查邮件列表是否为空
        print(f"\n成功获取到 {len(emails)} 封来自 '{folder_name}' 的邮件！")
        # 打印成功获取的邮件数量和文件夹名称
        for idx, email in enumerate(emails):
            # 遍历邮件列表，同时获取索引
            print_email_info(email, folder_name, idx + 1)
            # 调用 print_email_info 函数打印每封邮件的详细信息
    else:
        # 如果邮件列表为空或为 None
        print(f"未获取到 '{folder_name}' 中的邮件或发生错误。")
        # 打印未获取到邮件或发生错误的消息

def main():
    """
    主函数，用于获取指定邮箱账户的收件箱和已发送邮件信息并打印。

    此函数首先初始化 Outlook，然后查找指定的账户，
    接着获取该账户的收件箱和已发送邮件，并分别打印这些邮件的信息。

    参数:
        无

    返回值:
        无

    变量:
        account_email: 要访问的 Outlook 账户的电子邮件地址。
        mapi: Outlook 的 MAPI 命名空间对象。
        account: 找到的 Outlook 账户对象。
        inbox_folder: 收件箱文件夹对象。
        inbox_emails: 收件箱中的邮件列表。
        sent_folder: 已发送邮件文件夹对象。
        sent_emails: 已发送邮件中的邮件列表。
    """
    account_email = "Frank_Yu@prime3c.com"
    # 设置要访问的 Outlook 账户的电子邮件地址

    mapi = initialize_outlook()
    # 初始化 Outlook 并获取 MAPI 命名空间
    if mapi:
        # 如果 MAPI 初始化成功
        print("\n所有账户：")
        # 打印所有可用的 Outlook 账户信息
        for account in mapi.Accounts:
            print(f"  - 账户名称: {account.DisplayName}")
            print(f"    邮箱地址: {account.SmtpAddress}")
            print(f"    邮箱路径: {account.DeliveryStore.DisplayName}")

        account = find_outlook_account(mapi, account_email)
        # 根据邮箱地址查找 Outlook 账户
        if account:
            # 如果找到了指定的账户
            # 获取收件箱邮件
            inbox_folder = get_folder_by_name(account, "Inbox")
            # 获取收件箱文件夹对象
            inbox_emails = get_emails(inbox_folder)
            # 获取收件箱中的邮件列表
            print_emails_in_folder("收件箱", inbox_emails)
            # 打印收件箱中的邮件信息

            # 获取已发送邮件
            sent_folder = get_folder_by_name(account, "Sent Items")
            # 获取已发送邮件文件夹对象
            sent_emails = get_emails(sent_folder)
            # 获取已发送邮件中的邮件列表
            print_emails_in_folder("已发送邮件", sent_emails)
            # 打印已发送邮件中的邮件信息

    pythoncom.CoUninitialize()
    # 取消初始化 COM 库，释放资源

if __name__ == "__main__":
    main()
    # 当脚本直接运行时，调用 main 函数