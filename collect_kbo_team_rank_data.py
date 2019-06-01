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


def collect_kbo_team_rank_data(years, is_separate=False):
    # Note: in year 1999 and 2000, the league is separated into 2 - Dream League and Magic League

    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", chrome_options=options)
    url = "https://www.koreabaseball.com/TeamRank/TeamRank.aspx"
    driver.get(url)

    if not is_separate:
        for year in years:
            # redirect to specified year
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlYear']/option[@value='" + str(
                                                    year) + "']")))
            element.click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH,
                                                                             "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlYear']/option[@selected='selected']"),
                                                                            str(year)))
            page = driver.page_source

            bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4

            # parsing data from the table
            header_row_1 = bs_obj.find_all('table')[0].find('thead').find('tr').find_all('th')
            header_row_2 = bs_obj.find_all('table')[1].find('thead').find('tr').find_all('th')
            body_rows_1 = bs_obj.find_all('table')[0].find('tbody').find_all('tr')
            body_rows_2 = bs_obj.find_all('table')[1].find('tbody').find_all('tr')

            headings_1 = []
            headings_2 = []

            for heading in header_row_1:
                headings_1.append(heading.get_text())

            for heading in header_row_2:
                headings_2.append(heading.get_text())

            body_1 = []
            body_2 = []

            for row in body_rows_1:
                cells = row.find_all('td')
                row_temp = []
                for i in range(len(cells)):
                    row_temp.append(cells[i].get_text())
                body_1.append(row_temp)

            for row in body_rows_2:
                cells = row.find_all('td')
                row_temp = []
                for i in range(len(cells)):
                    row_temp.append(cells[i].get_text())
                body_2.append(row_temp)

            # create a workbook and add a worksheet
            excel_file_name_1 = "kbo_team_rank_data_" + str(year) + ".xlsx"
            excel_file_name_2 = "kbo_team_relative_rank_data_" + str(year) + ".xlsx"
            workbook_1 = xlsxwriter.Workbook(excel_file_name_1)
            worksheet_1 = workbook_1.add_worksheet()
            workbook_2 = xlsxwriter.Workbook(excel_file_name_2)
            worksheet_2 = workbook_2.add_worksheet()

            # write the first table to workbook_1
            row = 0
            for i in range(len(headings_1)):
                worksheet_1.write(row, i, format_num_data(headings_1[i]))
            row += 1
            for i in range(len(body_1)):
                for j in range(len(body_1[i])):
                    worksheet_1.write(row + i, j, format_num_data(body_1[i][j]))

            # write the second table to workbook_2
            row = 0
            for i in range(len(headings_2)):
                worksheet_2.write(row, i, format_num_data(headings_2[i]))
            row += 1
            for i in range(len(body_2)):
                for j in range(len(body_2[i])):
                    worksheet_2.write(row + i, j, format_num_data(body_2[i][j]))

            workbook_1.close()
            workbook_2.close()
            print(excel_file_name_1, excel_file_name_2)

    elif is_separate:
        for year in years:
            # redirect to specified year
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlYear']/option[@value='" + str(
                                                    year) + "']")))
            element.click()
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH,
                                                                             "//select[@name='ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlYear']/option[@selected='selected']"),
                                                                            str(year)))
            page = driver.page_source

            bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4

            # parsing data from the table
            header_row_1 = bs_obj.find_all('table')[0].find('thead').find('tr').find_all('th')
            header_row_2 = bs_obj.find_all('table')[1].find('thead').find('tr').find_all('th')
            header_row_3 = bs_obj.find_all('table')[2].find('thead').find('tr').find_all('th')
            body_rows_1 = bs_obj.find_all('table')[0].find('tbody').find_all('tr')
            body_rows_2 = bs_obj.find_all('table')[1].find('tbody').find_all('tr')
            body_rows_3 = bs_obj.find_all('table')[2].find('tbody').find_all('tr')

            headings_1 = []
            headings_2 = []
            headings_3 = []

            for heading in header_row_1:
                headings_1.append(heading.get_text())

            for heading in header_row_2:
                headings_2.append(heading.get_text())

            for heading in header_row_3:
                headings_3.append(heading.get_text())

            body_1 = []
            body_2 = []
            body_3 = []

            for row in body_rows_1:
                cells = row.find_all('td')
                row_temp = []
                for i in range(len(cells)):
                    row_temp.append(cells[i].get_text())
                body_1.append(row_temp)

            for row in body_rows_2:
                cells = row.find_all('td')
                row_temp = []
                for i in range(len(cells)):
                    row_temp.append(cells[i].get_text())
                body_2.append(row_temp)

            for row in body_rows_3:
                cells = row.find_all('td')
                row_temp = []
                for i in range(len(cells)):
                    row_temp.append(cells[i].get_text())
                body_3.append(row_temp)

            # create a workbook and add a worksheet
            excel_file_name_1 = "kbo_team_rank_data_" + str(year) + "_dream.xlsx"
            excel_file_name_2 = "kbo_team_rank_data_" + str(year) + "_magic.xlsx"
            excel_file_name_3 = "kbo_team_relative_rank_data_" + str(year) + ".xlsx"
            workbook_1 = xlsxwriter.Workbook(excel_file_name_1)
            worksheet_1 = workbook_1.add_worksheet()
            workbook_2 = xlsxwriter.Workbook(excel_file_name_2)
            worksheet_2 = workbook_2.add_worksheet()
            workbook_3 = xlsxwriter.Workbook(excel_file_name_3)
            worksheet_3 = workbook_3.add_worksheet()

            # write the first table to workbook_1
            row = 0
            for i in range(len(headings_1)):
                worksheet_1.write(row, i, format_num_data(headings_1[i]))
            row += 1
            for i in range(len(body_1)):
                for j in range(len(body_1[i])):
                    worksheet_1.write(row + i, j, format_num_data(body_1[i][j]))

            # write the second table to workbook_2
            row = 0
            for i in range(len(headings_2)):
                worksheet_2.write(row, i, format_num_data(headings_2[i]))
            row += 1
            for i in range(len(body_2)):
                for j in range(len(body_2[i])):
                    worksheet_2.write(row + i, j, format_num_data(body_2[i][j]))

            # write the second table to workbook_3
            row = 0
            for i in range(len(headings_3)):
                worksheet_3.write(row, i, format_num_data(headings_3[i]))
            row += 1
            for i in range(len(body_3)):
                for j in range(len(body_3[i])):
                    worksheet_3.write(row + i, j, format_num_data(body_3[i][j]))

            workbook_1.close()
            workbook_2.close()
            workbook_3.close()
            print(excel_file_name_1, excel_file_name_2, excel_file_name_3)

    driver.quit()    # quit the driver


if __name__ == '__main__':
    data_types = ['Hitter/Basic1', 'Hitter/Basic2', 'Pitcher/Basic1', 'Pitcher/Basic2', 'Defense/Basic', 'Runner/Basic']
    series_types = [0]
    years_1 = [1982+i for i in range(17)]
    years_2 = [1999, 2000]
    years_3 = [2001+i for i in range(18)]
#    collect_kbo_team_rank_data(years_1)
    collect_kbo_team_rank_data(years_2, True)
#    collect_kbo_team_rank_data(years_3)
