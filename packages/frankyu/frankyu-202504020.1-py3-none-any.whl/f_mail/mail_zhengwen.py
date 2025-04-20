import pythoncom
import win32com.client
from datetime import datetime
import os

def initialize_outlook():
    """
    初始化 Outlook 应用程序并获取 MAPI 命名空间。
    """
    try:
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        mapi = outlook.GetNamespace("MAPI")
        return mapi
    except pythoncom.com_error as e:
        print(f"COM 错误: {e}")
        return None
    except Exception as e:
        print(f"初始化 Outlook 时发生其他错误: {str(e)}")
        return None

def find_outlook_account(mapi, account_email):
    """
    根据邮箱地址查找 Outlook 账户。
    """
    if mapi:
        for account in mapi.Accounts:
            if account.SmtpAddress.lower() == account_email.lower():
                return account
        print(f"未找到邮箱账户: {account_email}")
    return None

def get_folder_by_name(account, folder_name):
    """
    根据账户和文件夹名称获取 Outlook 文件夹对象。
    """
    if account:
        try:
            if folder_name == "Inbox":
                return account.DeliveryStore.GetDefaultFolder(6)
            elif folder_name == "Sent Items":
                return account.DeliveryStore.GetDefaultFolder(5)
            else:
                try:
                    folder = account.DeliveryStore.Folders(folder_name)
                    print(f"成功找到文件夹: {folder.Name}")
                    return folder
                except Exception as e:
                    print(f"未找到指定文件夹 '{folder_name}': {str(e)}")
                    return None
        except Exception as e:
            print(f"获取文件夹时出错: {str(e)}")
            return None
    return None

def get_emails(folder):
    """
    从指定的 Outlook 文件夹获取邮件列表并按接收时间排序。
    """
    if folder:
        try:
            items = folder.Items
            items.Sort("[ReceivedTime]", True)
            return items
        except Exception as e:
            print(f"获取邮件列表时出错: {str(e)}")
            return None
    return None

def print_email_info(email, folder_name, index):
    """
    打印单封邮件的信息，包括主题、发件人/收件人、接收时间、正文前三行和附件名称。
    """
    print(f"邮件 {index}:")
    try:
        print(f"  主题: {email.Subject}")
    except AttributeError:
        print("  主题: 无法获取")

    if folder_name == "Sent Items":
        try:
            print(f"  收件人: {email.To}")
        except AttributeError:
            try:
                print(f"  发件人 (尝试 Sender): {email.Sender}")
            except AttributeError:
                try:
                    print(f"  发件人 (尝试 SenderName): {email.SenderName}")
                except AttributeError:
                    print("  无法获取发件人/收件人信息")
    else:
        try:
            print(f"  发件人: {email.SenderName}")
        except AttributeError:
            try:
                print(f"  发件人 (尝试 Sender): {email.Sender}")
            except AttributeError:
                print("  无法获取发件人信息")

    try:
        print(f"  接收时间: {email.ReceivedTime}")
    except AttributeError:
        print("  接收时间: 无法获取")

    try:
        body = email.Body
        body_lines = body.splitlines()
        print("  正文前三行:")
        for i, line in enumerate(body_lines[:3]):
            print(f"    {line}")
            if i == 2:
                break
        if not body_lines:
            print("    (正文为空)")
        elif len(body_lines) < 3:
            print("    (正文不足三行)")
    except AttributeError:
        print("  正文: 无法获取")

    try:
        attachments = email.Attachments
        if attachments.Count > 0:
            print("  附件:")
            for attachment in attachments:
                print(f"    - {attachment.FileName}")
        else:
            print("  附件: 无")
    except AttributeError:
        print("  附件: 无法获取")

def print_emails_in_folder(folder_name, emails):
    """
    打印指定文件夹中的所有邮件信息。
    """
    if emails:
        print(f"\n成功获取到 {len(emails)} 封来自 '{folder_name}' 的邮件！")
        for idx, email in enumerate(emails):
            print_email_info(email, folder_name, idx + 1)
    else:
        print(f"未获取到 '{folder_name}' 中的邮件或发生错误。")

def main():
    account_email = "Frank_Yu@prime3c.com"

    mapi = initialize_outlook()
    if mapi:
        print("\n所有账户：")
        for account in mapi.Accounts:
            print(f"  - 账户名称: {account.DisplayName}")
            print(f"    邮箱地址: {account.SmtpAddress}")
            print(f"    邮箱路径: {account.DeliveryStore.DisplayName}")

        account = find_outlook_account(mapi, account_email)
        if account:
            # 获取收件箱邮件
            inbox_folder = get_folder_by_name(account, "Inbox")
            inbox_emails = get_emails(inbox_folder)
            print_emails_in_folder("收件箱", inbox_emails)

            # 获取已发送邮件
            sent_folder = get_folder_by_name(account, "Sent Items")
            sent_emails = get_emails(sent_folder)
            print_emails_in_folder("已发送邮件", sent_emails)

    pythoncom.CoUninitialize()

if __name__ == "__main__":
    main()