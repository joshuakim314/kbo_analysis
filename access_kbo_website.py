import sys
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

from matrix import *
from statistics_tools import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BSoup
from time import sleep

import xlsxwriter
import xlrd
import pandas as pd

from format_kbo_data import *


team_id_dict = {'삼성': 'SS', '두산': 'OB', 'SK': 'SK', 'NC': 'NC', '키움': 'WO', '넥센': 'WO', '히어로즈': 'WO', '우리': 'WO', '현대': 'HD', 'KIA': 'HT', 'LG': 'LG', '롯데': 'LT', '한화': 'HH', 'KT': 'KT'}


def login_kbo_home(username, password):

    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", chrome_options=options)

    url = "https://www.koreabaseball.com/Member/Login.aspx"

    driver.get(url)

    # login
    username_field = driver.find_element_by_id("cphContents_cphContents_cphContents_txtUserId").send_keys(username)
    password_field = driver.find_element_by_id("cphContents_cphContents_cphContents_txtPassWord").send_keys(password)
    login_button = driver.find_element_by_id("cphContents_cphContents_cphContents_btnLogin")
    login_button.click()
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.ID, ""))

    # link = driver.find_element_by_link_text('Details')

    # sleep for some time to complete ajax load of the table
    page = driver.page_source


def collect_live_game_text(year, series=0, start_row=0):

    excel_file_loc = "/Volumes/Samsung_T5/KBO_Data/Games/Regular Season Games/KBO Schedule Regular Season/kbo_schedule_" + str(year)
    if series == 0:
        excel_file_loc += "_regular_season.xlsx"
    elif series == 1:
        excel_file_loc += "_pre_season.xlsx"
    elif series == 4:
        excel_file_loc += "_wildcard.xlsx"
    elif series == 3:
        excel_file_loc += "_semi_playoffs.xlsx"
    elif series == 5:
        excel_file_loc += "_playoffs.xlsx"
    elif series == 7:
        excel_file_loc += "_korean_series.xlsx"
    else:
        print("incorrect series type data input")
        return False

    # open Workbook
    workbook = xlrd.open_workbook(excel_file_loc)
    worksheet = workbook.sheet_by_index(0)
    num_row_temp = worksheet.nrows - 1

    url_list = []
    for i in range(start_row, num_row_temp):
        date_id = int(worksheet.cell_value(i + 1, 1))
        away_id = worksheet.cell_value(i + 1, 7)
        home_id = worksheet.cell_value(i + 1, 8)
        url_temp = "https://www.koreabaseball.com/Game/LiveText.aspx?leagueId=1&seriesId=" + str(series) + "&gameId=" + str(date_id) + str(away_id) + str(home_id) + str(series) + "&gyear=" + str(year)
        url_list.append(url_temp)

    for url in url_list:
        # set a headless browser
        # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # instantiate a Chrome web driver
        driver = webdriver.Chrome("/Applications/chromedriver", options=options)

        driver.get(url)
        print(url)

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "all")))
            element.click()
            sleep(5)  # sleep for some time to complete ajax load of the table
        except Exception:
            continue  # cancelled game

        page = driver.page_source
        bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4

        # parsing data from the table
        live_text_spans = bs_obj.find_all('div')[0].find_all('div')[-1].find_all('span')
        live_text_list = []
        for span in live_text_spans:
            text_formatted = format_live_text_string(span.get_text())
            if type(text_formatted) is list:
                live_text_list.extend(text_formatted)
            else:
                live_text_list.append(text_formatted)

        text_file_loc = "/Volumes/Samsung_T5/KBO_Data/Games/Regular Season Games/KBO " + str(year)
        if series == 0:
            text_file_loc += " Regular Season Live Text/"
        elif series == 1:
            text_file_loc += " Pre Season Live Text/"
        elif series == 4:
            text_file_loc += " Wildcard Live Text/"
        elif series == 3:
            text_file_loc += " Semi Playoffs Live Text/"
        elif series == 5:
            text_file_loc += " Playoffs Live Text/"
        elif series == 7:
            text_file_loc += " Korean Series Live Text/"
        else:
            print("incorrect series type data input")
            return False
        text_file_loc += url.split('=')[3].split('&')[0] + ".txt"
        text_file = open(text_file_loc, "w")
        for line in live_text_list:
            text_file.writelines(line + '\n')
        text_file.close()

        driver.quit()


def collect_game_schedule(year, series=0):

    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", options=options)

    url = "https://www.koreabaseball.com/Schedule/Schedule.aspx?seriesId=0"
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@id='ddlYear']/option[@value='" + str(year) + "']")))
    element.click()
    sleep(5)  # sleep for some time to complete ajax load of the table

    page = driver.page_source

    bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4

    # parsing data from the table
    # header_row = bs_obj.find_all('table')[0].find('thead').find('tr').find_all('th')
    body_rows = bs_obj.find_all('table')[0].find('tbody').find_all('tr')

    # headings = []
    body = []

    # for heading in header_row:
    #     headings.append(heading.get_text())

    day = ""
    for row in body_rows:
        cells = row.find_all('td')
        row_temp = []
        rowspan = cells[0].get('rowspan')
        extra_row = 1
        if rowspan is not None:
            extra_row = 0
            day = cells[0].get_text()  # day
        row_temp.append(day)
        day_num = str(year) + str(day.split("(")[0].replace(".", ""))
        row_temp.append(day_num)  # numerical day
        row_temp.append(cells[1 - extra_row].get_text())  # time

        team_names_table = cells[2 - extra_row].find_all('span')
        team_names_table_len = len(team_names_table)
        away_team_name = ""
        home_team_name = ""
        if team_names_table_len == 3:
            away_team_name = team_names_table[0].get_text()
            row_temp.append(away_team_name)  # away team name
            row_temp.append('')
            row_temp.append('')
            home_team_name = team_names_table[2].get_text()
            row_temp.append(home_team_name)  # home team name
        else:
            away_team_name = team_names_table[0].get_text()
            row_temp.append(away_team_name)  # away team name
            row_temp.append(team_names_table[1].get_text())  # away team score
            row_temp.append(team_names_table[3].get_text())  # home team score
            home_team_name = team_names_table[4].get_text()
            row_temp.append(home_team_name)  # home team name

        row_temp.append(team_id_dict[away_team_name])  # away team id
        row_temp.append(team_id_dict[home_team_name])  # home team id

        row_temp.append(cells[5 - extra_row].get_text())  # TV
        row_temp.append(cells[6 - extra_row].get_text())  # radio
        row_temp.append(cells[7 - extra_row].get_text())  # stadium
        row_temp.append(cells[8 - extra_row].get_text())  # note

        row_temp.append(int(series))  # series id

        body.append(row_temp)
        print(row)
        print(row_temp)

    excel_file_name = "/Volumes/Samsung_T5/KBO_Data/Games/Regular Season Games/KBO Schedule Regular Season/kbo_schedule_" + str(year)
    if series == 0:
        excel_file_name += "_regular_season.xlsx"
    elif series == 1:
        excel_file_name += "_pre_season.xlsx"
    elif series == 4:
        excel_file_name += "_wildcard.xlsx"
    elif series == 3:
        excel_file_name += "_semi_playoffs.xlsx"
    elif series == 5:
        excel_file_name += "_playoffs.xlsx"
    elif series == 7:
        excel_file_name += "_korean_series.xlsx"
    else:
        print("incorrect series type data input")
        return False
    workbook = xlsxwriter.Workbook(excel_file_name)
    worksheet = workbook.add_worksheet()

    # write to individual excel file
    row = 0
    worksheet.write(row, 0, "Date")
    worksheet.write(row, 1, "Date ID")
    worksheet.write(row, 2, "Start Time")
    worksheet.write(row, 3, "Away Team")
    worksheet.write(row, 4, "Away Score")
    worksheet.write(row, 5, "Home Score")
    worksheet.write(row, 6, "Home Team")
    worksheet.write(row, 7, "Away ID")
    worksheet.write(row, 8, "Home ID")
    worksheet.write(row, 9, "TV")
    worksheet.write(row, 10, "Radio")
    worksheet.write(row, 11, "Stadium")
    worksheet.write(row, 12, "Note")
    worksheet.write(row, 13, "Series ID")

    row += 1
    for i in range(len(body)):
        for j in range(len(body[i])):
            worksheet.write(row + i, j, format_num_data(body[i][j]))

    workbook.close()
    driver.quit()


def update_schedule_and_live_texts(year, series=0, start_row=0):
    # collect_game_schedule(year)
    collect_live_game_text(year, series, start_row)


def format_live_text_string(live_text):
    text_formatted = live_text.replace("\n                        ", '').replace("\n", '')
    # 39 '-'s
    if len(text_formatted) >= 39:
        if "---------------------------------------" in text_formatted:
            text_temp = text_formatted.split("---------------------------------------")[0]
            text_formatted = [text_temp, "---------------------------------------"]
    return text_formatted


if __name__ == "__main__":
    # collect_live_game_text(2018)
    # login_kbo_home('gbkim0907', 'Ks9415842!')
    # for year in range(2001, 2019):
    #     collect_game_schedule(year)
    # collect_game_schedule(2019)
    update_schedule_and_live_texts(2019, series=0, start_row=161)
