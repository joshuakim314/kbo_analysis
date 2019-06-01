from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
import glob
import os
import time
import shutil
import pandas as pd
from bs4 import BeautifulSoup as BSoup


def collect_kbo_team_roster(years=[2019]):
    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", options=options)
    url = "https://www.koreabaseball.com/Player/Register.aspx"
    driver.get(url)
    while True:
        raw_date = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cphContents_cphContents_cphContents_lblGameDate"]'))).text
        date_formatted = [int(x) for x in raw_date.split('(')[0].split('.')]
        date_string = raw_date.split('(')[0].replace('.', '')
        year = date_formatted[0]
        month = date_formatted[1]
        date = date_formatted[2]
        print(date_string)

        # terminating condition
        if year < min(years):
            break
        if year == 2010 and month == 2:
            break

        skip_page = False
        if year not in years:
            skip_page = True
        else:
            if month in [1, 2, 11, 12]:
                skip_page = True
            # change the dates for every year
            elif month == 9:
                if date > 6:
                    skip_page = True
            elif month == 3:
                if date < 24:
                    skip_page = True

        if skip_page:
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cphContents_cphContents_cphContents_btnPreDate"]')))
            element.click()
            time.sleep(5)  # change the wait time if not sufficient
            continue

        previous_team_name = ""
        for i in range(1, 11):
            while True:
                team_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[1]/ul/li[' + str(i) + ']/a')))
                team_element.click()
                team_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div[1]/ul/li[' + str(i) + ']/a/span'))).text
                if team_name == '키움' and year < 2019:
                    team_name = '넥센'
                if team_name == 'KT' and year < 2015:
                    continue
                if team_name == 'NC' and year < 2013:
                    continue
                if team_name != previous_team_name:
                    previous_team_name = team_name
                    break
                print("Team did not change.")

            page = driver.page_source
            bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4
            tables = bs_obj.find_all('table')  # 0: "감독", 1: "코치", 2: "투수", 3: "포수", 4: "내야수", 5: "외야수, 6: "등록", 7: "말소"
            table_index = -1

            for table in tables:
                table_index += 1
                # parsing data from the table
                header_row = table.find('thead').find('tr').find_all('th')
                body_rows = table.find('tbody').find_all('tr')

                headings = []
                for heading in header_row:
                    headings.append(heading.get_text())

                body = []
                for tr in body_rows:
                    td = tr.find_all('td')
                    row = [cell.text for cell in td]
                    body.append(row)

                if "당일 1군" in body[0][0] and "없습니다." in body[0][0]:
                    continue

                table_string = ""
                if table_index == 0:
                    table_string = "감독"
                elif table_index == 1:
                    table_string = "코치"
                elif table_index == 2:
                    table_string = "투수"
                elif table_index == 3:
                    table_string = "포수"
                elif table_index == 4:
                    table_string = "내야수"
                elif table_index == 5:
                    table_string = "외야수"
                elif table_index == 6:
                    table_string = "등록"
                elif table_index == 7:
                    table_string = "말소"

                # define the access rights
                access_rights = 0o755  # read and write by the owner, read only by the rest
                path = "/Volumes/Samsung_T5/KBO_Data/Team Rosters/" + str(year) + "/" + team_name + "/" + team_name + "_" + date_string
                if not os.path.exists(path):
                    os.makedirs(path, access_rights)
                else:
                    print("Already exists:", path)

                df = pd.DataFrame(body, columns=headings)
                csv_file = "/Volumes/Samsung_T5/KBO_Data/Team Rosters/" + str(year) + "/" + team_name + "/" + team_name + "_" + date_string + "/" + team_name + "_" + date_string + "_" + table_string + "_roster.csv"
                df.to_csv(csv_file, index=False)
                print(csv_file)

            time.sleep(3)

        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cphContents_cphContents_cphContents_btnPreDate"]')))
        element.click()
        time.sleep(5)  # change the wait time if not sufficient

    return True


if __name__ == '__main__':
    collect_kbo_team_roster(years=[2017, 2018])
