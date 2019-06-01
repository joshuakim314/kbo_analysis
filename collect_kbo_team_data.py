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
import pandas as pd

from format_kbo_data import *


def collect_kbo_team_data(years, series_types, data_types):
    # parameters
    # year varies between 2001 and current
    # series varies between 0: Regular Season, 1: Preseason, 4: Wildcard Game, 3: Semi-playoffs, 5: Playoffs, and 7: Korean Series
    # data_type varies between 'Hitter/Basic1', 'Hitter/Basic2', 'Pitcher/Basic1', 'Pitcher/Basic2', 'Defense/Basic', and 'Runner/Basic'

    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", chrome_options=options)

    for data_type in data_types:
        url = "https://www.koreabaseball.com/Record/Team/"+str(data_type)+".aspx"
        for series in series_types:
            for year in years:
                driver.get(url)

                # redirect to specified year
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeason$ddlSeason']/option[@value='" + str(
                                                        year) + "']")))
                element.click()
                WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH,
                                                                                 "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeason$ddlSeason']/option[@selected='selected']"),
                                                                                str(year)))

                # redirect to specified series
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeries$ddlSeries']/option[@value='" + str(
                                                        series) + "']")))
                element.click()
                # WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH,
                #                                                                  "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlSeries$ddlSeries']/option[@selected='selected']"),
                #                                                                 str(series)))

                sleep(10)
                # sleep for some time to complete ajax load of the table
                page = driver.page_source

                bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4

                # parsing data from the table
                header_row = bs_obj.find_all('table')[0].find('thead').find('tr').find_all('th')
                body_rows = bs_obj.find_all('table')[0].find('tbody').find_all('tr')
                footer_row = bs_obj.find_all('table')[0].find('tfoot').find('tr').find_all('td')

                headings = []
                footings = [None]

                for heading in header_row:
                    headings.append(heading.get_text())

                for footing in footer_row:
                    footings.append(footing.get_text())

                body = []

                for row in body_rows:
                    cells = row.find_all('td')
                    row_temp = []
                    for i in range(len(cells)):
                        row_temp.append(cells[i].get_text())
                    body.append(row_temp)

                # create a workbook and add a worksheet
                data_type_name = str(data_type).split('/')[0].lower()
                data_type_num = str(data_type)[-1]
                if data_type_num == '1' or data_type_num == '2':
                    data_type_name += data_type_num
                excel_file_name = "kbo_team_"+data_type_name+"_data_"+str(year)
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
                for i in range(len(headings)):
                    worksheet.write(row, i, format_num_data(headings[i]))
                row += 1
                for i in range(len(body)):
                    for j in range(len(body[i])):
                        worksheet.write(row + i, j, format_num_data(body[i][j]))
                row += len(body)
                for i in range(len(footings)):
                    if footings[i] == None:
                        continue
                    worksheet.write(row, i, format_num_data(footings[i]))
                workbook.close()
                print(headings)
                print(body)
                print(footings)
                print(excel_file_name)

    driver.quit()    # quit the driver


if __name__ == '__main__':
    data_types = ['Hitter/Basic1', 'Hitter/Basic2', 'Pitcher/Basic1', 'Pitcher/Basic2', 'Defense/Basic', 'Runner/Basic']
    series_types = [0]
    years = [2001+i for i in range(18)]
    collect_kbo_team_data(years, series_types, data_types)
