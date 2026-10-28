"""
Support Feedback Analyzer
Author: Abbas Beigy
Description: Reads support ticket text files, extracts phone numbers and emails using RegEx,
performs basic rule-based sentiment analysis, builds a pandas DataFrame, and exports the report to CSV.
"""

from glob import glob
import re
import pandas as pd


def extract_contact_info(text):
    """استخراج شماره موبایل و ایمیل با استفاده از عبارات باقاعده (RegEx)"""
    # الگوی شماره موبایل (پشتیبانی از ارقام فارسی و انگلیسی)
    phone_pattern = r"[0۰][9۹][0-9۰-۹]{7,9}"
    phones = re.findall(phone_pattern, text)

    # الگوی ایمیل
    email_pattern = r"[\w.-]+@[\w.-]+\.\w+"
    emails = re.findall(email_pattern, text)

    return phones, emails


def detect_sentiment(text):
    """تحلیل احساسات مبتنی بر کلمات کلیدی (Rule-based Sentiment Analysis)"""
    good_list = ["خوب", "عالی", "راضی", "ممنون", "تشکر", "فوق‌العاده", "متشکرم"]
    bad_list = ["بد", "ناراضی", "افتضاح", "مشکل", "خراب", "کند", "ضعیف"]

    # شمارش کلمات مثبت و منفی در متن
    good_count = sum(1 for word in good_list if word in text)
    bad_count = sum(1 for word in bad_list if word in text)

    if good_count > bad_count:
        return "رضایتمندی"
    elif bad_count > good_count:
        return "نارضایتی"
    else:
        return "معمولی"


def main():
    # ۱. جستجوی فایل‌های متنی تیکت‌ها با glob
    file_list = glob("support_logs/*.txt")  # مسیر پوشه حاوی تیکت‌ها

    if not file_list:
        print("هیچ فایلی در مسیر مورد نظر پیدا نشد!")
        return

    coment_list = []

    # ۲. پیمایش و خواندن فایل‌ها
    for item in file_list:
        with open(item, "r", encoding="utf-8") as f:
            new_content = f.read()

        # استخراج اطلاعات تماس
        phones, emails = extract_contact_info(new_content)

        # تحلیل احساسات تیکت
        status = detect_sentiment(new_content)

        # ساخت دیکشنری داده‌های هر تیکت
        row_data = {
            "file_name": item,
            "raw_text": new_content,
            "phones": phones,
            "emails": emails,
            "status": status,
        }
        coment_list.append(row_data)

    # ۳. تبدیل به DataFrame در پانداس
    df_coment = pd.DataFrame(coment_list)

    print("--- پیش‌نمایش دیتافریم تیکت‌ها ---")
    display(df_coment)

    # ۴. محاسبه بسامد وضعیت‌ها (آمار احساسات)
    print('\n--- توزیع فراوانی وضعیت تیکت‌ها ---')
    print(df_coment["status"].value_counts())

    # ۵. خروجی گرفتن به فایل CSV با انکودینگ استاندارد فارسی
    output_filename = "support_report.csv"
    df_coment.to_csv(output_filename, index=False, encoding="utf-8-sig")
    print(f"\nگزارش نهایی با موفقیت در فایل {output_filename} ذخیره شد.")


if __name__ == "__main__":
    main()
