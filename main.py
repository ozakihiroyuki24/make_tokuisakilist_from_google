# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 20:24:52 2020

@author: ozakihiroyuki24
"""


from selenium import webdriver
import csv
import re


def search_no_in_desc(word, desc_text, tel_no_local_in_desc):

    # 引数wordをDescriptionから探す
    if word in desc_text.upper():
        word_for_regular = word+".+"
        try:
            tel_text = re.search(
                r"%s" % word_for_regular, desc_text.upper(), flags=re.DOTALL)
            tel_text_2 = tel_text.group(0) if tel_text else None
            tel_text_3 = re.search(r'[0-9]+-[0-9]+-\d{4}', tel_text_2)
            tel_no_local_in_desc = tel_text_3.group(0) if tel_text_3 else None
            # print(tel_no_in_desc)
        except:
            tel_no_local_in_desc = ""

    return tel_no_local_in_desc


def search_no_in_page(word, page_source_txt, tel_no_local_in_page):

    # 引数wordをページ内から探す
    if word in page_source_txt.upper():
        word_for_regular = word+".+"
        try:
            tel_text = re.search(
                r"%s" % word_for_regular, page_source_txt.upper(), flags=re.DOTALL)
            tel_text_2 = tel_text.group(0) if tel_text else None
            tel_text_3 = re.search(r'[0-9]+-[0-9]+-\d{4}', tel_text_2)
            tel_no_local_in_page = tel_text_3.group(0) if tel_text_3 else None
        except:
            tel_no_local_in_page = ""

    return tel_no_local_in_page


def search_mail_in_desc(word, desc_text, email_local_in_desc):

    # 引数wordをDescriptionから探す
    if word in desc_text.upper():
        word_for_regular = word+".+"
        try:
            tel_text = re.search(
                r"%s" % word_for_regular, desc_text.upper(), flags=re.DOTALL)
            tel_text_2 = tel_text.group(0) if tel_text else None
            tel_text_3 = re.search(
                r"[^\s]+@[^\s]+", tel_text_2)
            email_local_in_desc = tel_text_3.group(0) if tel_text_3 else None
        except:
            email_local_in_desc = ""

    return email_local_in_desc


def search_mail_in_page(word, page_source_txt, email_local_in_page):

    # 引数wordをページ内から探す
    if word in page_source_txt.upper():
        word_for_regular = word+".+"
        try:
            tel_text = re.search(
                r"%s" % word_for_regular, page_source_txt.upper(), flags=re.DOTALL)
            tel_text_2 = tel_text.group(0) if tel_text else None
            tel_text_3 = re.search(
                r"[^\s]+@[^\s]+", tel_text_2)
            email_local_in_page = tel_text_3.group(0) if tel_text_3 else None
        except:
            email_local_in_page = ""

    return email_local_in_page


def get_data_in_each_pages(page_number):

    div_num = 1

    while div_num < 20:
        basic_xpath = "/html/body/div[6]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div["+str(
            div_num)

        title_xpath = basic_xpath+"]/div/div[1]/a/h3"
        title_url_xpath = basic_xpath+"]/div/div[1]/a"
        desc_xpath = basic_xpath+"]/div/div[2]/div"

        try:
            driver.find_element_by_xpath(title_xpath).text
        except:
            break

        title_text = driver.find_element_by_xpath(title_xpath).text
        title_url_link = driver.find_element_by_xpath(
            title_url_xpath).get_attribute("href")
        desc_text = driver.find_element_by_xpath(desc_xpath).text
        driver.get(title_url_link)
        page_source_txt = driver.page_source

        file_name = str(page_number) + "_" + str(div_num) + ".txt"
        with open(file_name, 'w', encoding='CP932', errors='replace') as sourcefile:
            print(page_source_txt, file=sourcefile)

        driver.back()

        tel_no_local_in_desc = ""
        tel_no_local_in_page = ""
        fax_no_local_in_desc = ""
        fax_no_local_in_page = ""
        email_local_in_desc = ""
        email_local_in_page = ""

        tel_no_local_in_desc = search_no_in_desc(
            "TEL", desc_text, tel_no_local_in_desc)
        tel_no_local_in_page = search_no_in_page(
            "TEL", page_source_txt, tel_no_local_in_page)
        fax_no_local_in_desc = search_no_in_desc(
            "FAX", desc_text, tel_no_local_in_desc)
        fax_no_local_in_page = search_no_in_page(
            "FAX", page_source_txt, tel_no_local_in_page)
        email_local_in_desc = search_mail_in_desc(
            "E-MAIL", desc_text, email_local_in_desc)
        email_local_in_page = search_mail_in_page(
            "E-MAIL", page_source_txt, email_local_in_page)

        result_array = [file_name, title_text, tel_no_local_in_desc, tel_no_local_in_page,
                        fax_no_local_in_desc, fax_no_local_in_page, email_local_in_desc, email_local_in_page, desc_text, title_url_link]

        with open('nichiyouhin_tokuisaki_list.csv', 'a', encoding='CP932', errors='replace', newline="") as tsvfile:
            writer = csv.writer(tsvfile, delimiter="\t")
            writer.writerow(result_array)

        div_num = div_num + 1


def access_each_pages():

    page_url = "https://google.com"

    driver.get(page_url)
    google_searchbox_xpath = "/html/body/div/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input"
    #検索キーワードの入力
    search_word = "日用品 卸売業者　企業概要　電話番号 filetype:html"
    driver.find_element_by_xpath(google_searchbox_xpath).send_keys(search_word)
    google_search_button_xpath = "/html/body/div/div[3]/form/div[2]/div[1]/div[3]/center/input[1]"
    driver.find_element_by_xpath(google_search_button_xpath).click()

    #最大20ページ目までクロール
    for page_num in range(3, 20):
        
        if page_num > 8:
            page_num_button = 8
        else:
            page_num_button = page_num

        get_data_in_each_pages(page_num)
        google_search_next_page_button_xpath_base = "/html/body/div[6]/div[2]/div[9]/div[1]/div[2]/div/div[5]/div[2]/span[1]/div/table/tbody/tr/td["+str(
            page_num_button)+"]/a"
        driver.find_element_by_xpath(
            google_search_next_page_button_xpath_base).click()


if __name__ == "__main__":

    driver = webdriver.Chrome("c:/driver/chromedriver.exe")
    driver.delete_all_cookies()

    header_array = ["file_no", "title", "tel_no",
                    "fax_no", "e-mail", "description", "url"]

    with open('nichiyouhin_tokuisaki_list.csv', 'w', encoding='CP932', errors='replace', newline="") as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t", lineterminator="\n")
        writer.writerow(header_array)

    access_each_pages()

    driver.close()
