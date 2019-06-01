from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
import glob
import os
import shutil
import pandas as pd
from bs4 import BeautifulSoup as BSoup


def collect_kbo_player_data(player_type, page_type, custom_id_list=None):
    # TODO: implement the feature to change years from the dropdown box
    # player_type can be: "Hitter" or "Pitcher"
    # page_type can be: "Basic", "Total", "Daily", "Game", or "Situation"
    id_list = custom_id_list
    if custom_id_list is None:
        id_list = get_player_id_list("kbo_id_list.csv")

    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", options=options)

    for id in id_list:
        print(id)
        url = "https://www.koreabaseball.com/Record/Player/" + player_type + "Detail/" + page_type + ".aspx?playerId=" + str(id)
        driver.get(url)

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/div[2]/div[2]/div/table')))
        page = driver.page_source
        bs_obj = BSoup(page, 'html.parser')  # instantiate Beautiful Soup 4

        if page_type == "Total":
            # parsing data from the table
            header_row = bs_obj.find_all('table')[0].find('thead').find('tr').find_all('th')
            body_rows = bs_obj.find_all('table')[0].find('tbody').find_all('tr')
            if player_type == "Hitter":
                footer_row = bs_obj.find_all('table')[0].find('tfoot').find('tr').find_all('th')
            elif player_type == "Pitcher":
                footer_row = bs_obj.find_all('table')[0].find('tfoot').find_all('tr')[1].find_all('th')

            headings = []
            footings = ['']

            for heading in header_row:
                headings.append(heading.get_text())

            for footing in footer_row:
                footings.append(footing.get_text())

            if footings[-1] == '':
                continue

            body = []
            for tr in body_rows:
                td = tr.find_all('td')
                row = [cell.text for cell in td]
                body.append(row)

            body.append(footings)

            df = pd.DataFrame(body, columns=headings)
            csv_file = "/Volumes/Samsung_T5/KBO_Data/Players/" + str(id) + "/" + str(id) + "_" + player_type.lower() + "_" + page_type.lower() + "_regular_season.csv"
            df.to_csv(csv_file, index=False)
            print(csv_file)

        if page_type == "Situation":
            tables = bs_obj.find_all('table')  # 0: "주자상황별", 1: "볼카운트별", 2: "이닝별", 3: "타순별", 4: "타자/투수유형별", 5: "아웃카운트별"
            situation_index = -1
            for table in tables:
                situation_index += 1
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

                if body == [["기록이 없습니다."]]:
                    continue

                situation_string = ""
                if situation_index == 0:
                    situation_string = "주자상황별"
                elif situation_index == 1:
                    situation_string = "볼카운트별"
                elif situation_index == 2:
                    situation_string = "이닝별"
                elif situation_index == 3:
                    situation_string = "타순별"
                elif situation_index == 4:
                    if player_type == "Hitter":
                        situation_string = "투수유형별"
                    elif player_type == "Pitcher":
                        situation_string = "타자유형별"
                elif situation_index == 5:
                    situation_string = "아웃카운트별"

                df = pd.DataFrame(body, columns=headings)
                csv_file = "/Volumes/Samsung_T5/KBO_Data/Players/" + str(id) + "/" + str(id) + "_" + page_type + "/" + str(id) + "_" + player_type.lower() + "_" + situation_string + "_2019_regular_season.csv"
                df.to_csv(csv_file, index=False)
                print(csv_file)


def generate_player_folders(parent_path, folder_type=False):
    id_list = get_player_id_list("kbo_id_list.csv")

    # define the access rights
    access_rights = 0o755  # read and write by the owner, read only by the rest

    for id in id_list:
        if not folder_type:
            path = parent_path + "/" + str(id)
        else:
            path = parent_path + "/" + str(id) + "/" + str(id) + "_" + folder_type
        try:
            os.makedirs(path, access_rights)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)


def remove_player_folders(parent_path, folder_type=False):
    id_list = get_player_id_list("kbo_id_list.csv")

    for id in id_list:
        if not folder_type:
            path = parent_path + "/" + str(id) + "/" + str(id)
        else:
            path = parent_path + "/" + str(id) + "/" + str(id) + "/" + folder_type
        try:
            shutil.rmtree(path)
        except Exception:
            print("Removal of the directory %s failed" % path)


def remove_csv_file(parent_path=None):
    id_list = get_player_id_list("kbo_id_list.csv")
    for id in id_list:
        path = "/Volumes/Samsung_T5/KBO_Data/Players/" + str(id) + "/" + str(id) + "_Situation/" + str(id) + "_" + "타자유형별" + "_2019_regular_season.csv"
        try:
            os.remove(path)
        except Exception:
            print("Not found: " + path)
        else:
            print("Successfully created the directory %s" % path)


def convert_excel_to_csv(excel_file, in_main_dir=True):
    csv_file = excel_file.replace(".xlsx", '.csv')
    if in_main_dir:
        csv_file = csv_file.split('/')[-1]
    pd.read_excel(excel_file).to_csv(csv_file, index=False)


def rename_file_name(parent_path=None):
    id_list = get_player_id_list("kbo_id_list.csv")[1000:2000]
    situation_list = ["주자상황별", "볼카운트별", "이닝별", "타순별", "투수유형별", "아웃카운트별"]
    for id in id_list:
        for situation_string in situation_list:
            old_path = "/Volumes/Samsung_T5/KBO_Data/Players/" + str(id) + "/" + str(id) + "_Situation/" + str(id) + "_" + situation_string + "_2019_regular_season.csv"
            new_path = "/Volumes/Samsung_T5/KBO_Data/Players/" + str(id) + "/" + str(id) + "_Situation/" + str(id) + "_hitter_" + situation_string + "_2019_regular_season.csv"
            try:
                os.rename(old_path, new_path)
                print("Found: " + old_path)
            except Exception:
                print("Not found: " + old_path)
    # os.chdir(parent_path)
    # glob_paths = glob.glob('*/')
    # paths = [path[:-1] for path in glob_paths]
    # for path in paths:
    #     old_path = parent_path + "/" + path + "/" + path + "hitter_total_regular_season.csv"
    #     new_path = parent_path + "/" + path + "/" + path + "_hitter_total_regular_season.csv"
    #     try:
    #         os.rename(old_path, new_path)
    #         print("Found: " + old_path)
    #     except Exception:
    #         print("Not found: " + old_path)


def merge_player_id_lists():
    # always remove the resultant excel file before running this function
    # the resultant file has a similar name as the other files
    all_data = pd.DataFrame()
    os.chdir("KBO ID Lists")
    for f in glob.glob("kbo_id_list*.xlsx"):
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True, sort=False)
    all_data = all_data.sort_values("ID", ascending=True)
    all_data.to_excel("kbo_id_list.xlsx", encoding='utf-8', index=False)


def get_player_id_list(file_name='kbo_id_list.csv'):
    df = pd.read_csv(file_name)
    id_list = df['ID'].tolist()
    return id_list


def update_player_info(player_id, player_type, file_name='kbo_id_list.csv'):
    df = pd.read_csv(file_name)

    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", options=options)

    url = "https://www.koreabaseball.com/Record/Player/" + str(player_type) + "/Basic.aspx?playerId=" + str(player_id)
    driver.get(url)

    # 0: player_id, 1: player_name, 2: player_team, 3: player_number, 4: player_birthday, 5: position, 6: player_body
    # 7: player_career, 8: player_payment, 9: player_salary, 10: player_draft, 11: player_join, 12: url_type
    player_info = [player_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    player_name_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "cphContents_cphContents_cphContents_playerProfile_lblName")))

    player_name = player_name_element.text
    if player_name == "":
        print("Not Found")
        return False

    print(player_name)

    player_info[1] = player_name
    player_info[2] = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/h4').text
    player_info[3] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblBackNo").text
    player_info[4] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblBirthday").text
    player_info[5] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblPosition").text
    player_info[6] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
    player_info[7] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblCareer").text
    player_info[8] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblPayment").text
    player_info[9] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblSalary").text
    player_info[10] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblDraft").text
    player_info[11] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblJoinInfo").text

    error_string = ""
    index = df[df['ID'] == player_id].index.item()
    print(index)
    print(df.iloc[index])

    df.iat[index, 1] = player_info[1]

    df.iat[index, 2] = player_info[2]
    if player_info[2] == '':
        error_string += "Team (2): " + str(player_info[2]) + "   "

    try:
        df.iat[index, 3] = int(player_info[3].replace('No.', ''))
    except Exception:
        error_string += "Number (3): " + str(player_info[3]) + "   "

    try:
        player_birthday = player_info[4].split()
        df.iat[index, 4] = int(player_birthday[0].replace('년', ''))
        df.iat[index, 5] = int(player_birthday[1].replace('월', ''))
        df.iat[index, 6] = int(player_birthday[2].replace('일', ''))
    except Exception:
        error_string += "Birthday (4, 5, 6): " + str(player_info[4]) + "   "

    try:
        player_position = player_info[5].split('(')
        player_position[1] = player_position[1].replace(')', '')
        detailed_position = player_position[0]
        if detailed_position == '투수':
            detailed_position = 'Pitcher'
        elif detailed_position == '포수':
            detailed_position = 'Catcher'
        elif detailed_position == '내야수':
            detailed_position = 'Infielder'
        elif detailed_position == '외야수':
            detailed_position = 'Outfielder'
        pitching_hand = player_position[1][:2]
        is_underhand = False
        if pitching_hand == '우투':
            pitching_hand = 'Right'
        elif pitching_hand == '좌투':
            pitching_hand = 'Left'
        elif pitching_hand == '우언':
            pitching_hand = 'Right'
            is_underhand = True
        elif pitching_hand == '좌언':
            pitching_hand = 'Left'
            is_underhand = True
        batting_hand = player_position[1][2:]
        if batting_hand == '우타':
            batting_hand = 'Right'
        elif batting_hand == '좌타':
            batting_hand = 'Left'
        df.iat[index, 7] = detailed_position
        df.iat[index, 8] = pitching_hand
        df.iat[index, 9] = is_underhand
        df.iat[index, 10] = batting_hand
    except Exception:
        error_string += "Position (7, 8, 9, 10): " + str(player_info[5]) + "   "

    try:
        height_weight = player_info[6].split('/')
        df.iat[index, 11] = int(height_weight[0].replace('cm', ''))
        df.iat[index, 12] = int(height_weight[1].replace('kg', ''))
    except Exception:
        error_string += "Body (11, 12): " + str(player_info[6]) + "   "

    df.iat[index, 13] = player_info[7]

    try:
        if player_info[8][-1:] == '엔':
            df.iat[index, 14] = int(player_info[8].replace('엔', ''))
            df.iat[index, 15] = player_info[8][-1:]
        elif player_info[8][-3:] == '만달러':
            df.iat[index, 14] = int(player_info[8].replace('만달러', ''))
            df.iat[index, 15] = player_info[8][-3:]
        else:
            df.iat[index, 14] = int(player_info[8].replace('만원', '').replace('달러', ''))
            df.iat[index, 15] = player_info[8][-2:]
    except Exception:
        error_string += "Contract Payment (14, 15): " + str(player_info[8]) + "   "

    try:
        df.iat[index, 16] = int(player_info[9].replace('만원', '').replace('달러', ''))
        df.iat[index, 17] = player_info[9][-2:]
    except Exception:
        error_string += "Salary (16, 17): " + str(player_info[9]) + "   "

    try:
        player_draft = player_info[10].split()
        draft_detail = ""
        for text in player_draft[2:]:
            draft_detail += text + " "
        draft_detail = draft_detail[:-1]
        df.iat[index, 18] = int(player_draft[0])
        df.iat[index, 19] = player_draft[1]
        df.iat[index, 20] = draft_detail
    except Exception:
        error_string += "Draft (18, 19, 20): " + str(player_info[10]) + "   "

    try:
        df.iat[index, 21] = int(player_info[11][:2])
        df.iat[index, 22] = player_info[11][2:]
    except Exception:
        error_string += "Join (21, 22): " + str(player_info[11]) + "   "

    df.iat[index, 23] = error_string

    print(df.iloc[index])

    df.to_csv(file_name, encoding='utf-8', index=False)


def collect_player_id(player_type):
    # set a headless browser
    # remove the next 2 lines and 'chrome_options' parameter in driver signature to have the web driver pop up
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    workbook = xlsxwriter.Workbook("kbo_id_list_7.xlsx")
    worksheet = workbook.add_worksheet()

    row = 0
    worksheet.write(row, 0, "ID")
    worksheet.write(row, 1, "Name")
    worksheet.write(row, 2, "Team")
    worksheet.write(row, 3, "Number")
    worksheet.write(row, 4, "Birth Year")
    worksheet.write(row, 5, "Birth Month")
    worksheet.write(row, 6, "Birth Day")
    worksheet.write(row, 7, "Position")
    worksheet.write(row, 8, "Pitching Hand")
    worksheet.write(row, 9, "Underhand")
    worksheet.write(row, 10, "Batting Hand")
    worksheet.write(row, 11, "Height (cm)")
    worksheet.write(row, 12, "Weight (kg)")
    worksheet.write(row, 13, "Career")
    worksheet.write(row, 14, "Contract Payment")
    worksheet.write(row, 15, "Payment Unit")
    worksheet.write(row, 16, "Salary")
    worksheet.write(row, 17, "Salary Unit")
    worksheet.write(row, 18, "Draft Year")
    worksheet.write(row, 19, "Draft Team")
    worksheet.write(row, 20, "Draft Detail")
    worksheet.write(row, 21, "Joined Year")
    worksheet.write(row, 22, "Joined Team")
    worksheet.write(row, 23, "Data Errors")

    # instantiate a Chrome web driver
    driver = webdriver.Chrome("/Applications/chromedriver", options=options)

    # index_list = [40001, 40002, 40003, 40004, 40005, 40006, 40007]
    # index_list.extend(list(range(49573, 50000)))

    # index_list = get_player_id_list("kbo_pitcher_id_list_33.xlsx")

    # no players found between 0 and 9999
    for player_id in range(70000, 80000):
        print(player_id)
        url = "https://www.koreabaseball.com/Record/Player/" + str(player_type) + "/Basic.aspx?playerId=" + str(player_id)
        driver.get(url)

        # 0: player_id, 1: player_name, 2: player_team, 3: player_number, 4: player_birthday, 5: position, 6: player_body
        # 7: player_career, 8: player_payment, 9: player_salary, 10: player_draft, 11: player_join, 12: url_type
        player_info = [player_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        player_name_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "cphContents_cphContents_cphContents_playerProfile_lblName")))

        player_name = player_name_element.text
        if player_name == "":
            print("Not Found")
            continue
        print(player_name)
        player_info[1] = player_name
        player_info[2] = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/h4').text
        player_info[3] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblBackNo").text
        player_info[4] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblBirthday").text
        player_info[5] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblPosition").text
        player_info[6] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblHeightWeight").text
        player_info[7] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblCareer").text
        player_info[8] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblPayment").text
        player_info[9] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblSalary").text
        player_info[10] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblDraft").text
        player_info[11] = driver.find_element_by_id("cphContents_cphContents_cphContents_playerProfile_lblJoinInfo").text
        player_info[12] = player_type

        # write to individual excel file

        row += 1
        print(row)

        error_string = ""

        worksheet.write(row, 0, player_info[0])
        worksheet.write(row, 1, player_info[1])

        try:
            worksheet.write(row, 2, player_info[2])
        except Exception:
            error_string += "Team (2): " + str(player_info[2]) + "   "

        try:
            worksheet.write(row, 3, int(player_info[3].replace('No.', '')))
        except Exception:
            error_string += "Number (3): " + str(player_info[3]) + "   "

        try:
            player_birthday = player_info[4].split()
            worksheet.write(row, 4 + 0, int(player_birthday[0].replace('년', '')))
            worksheet.write(row, 4 + 1, int(player_birthday[1].replace('월', '')))
            worksheet.write(row, 4 + 2, int(player_birthday[2].replace('일', '')))
        except Exception:
            error_string += "Birthday (4, 5, 6): " + str(player_info[4]) + "   "

        try:
            player_position = player_info[5].split('(')
            player_position[1] = player_position[1].replace(')', '')
            detailed_position = player_position[0]
            if detailed_position == '투수':
                detailed_position = 'Pitcher'
            elif detailed_position == '포수':
                detailed_position = 'Catcher'
            elif detailed_position == '내야수':
                detailed_position = 'Infielder'
            elif detailed_position == '외야수':
                detailed_position = 'Outfielder'
            pitching_hand = player_position[1][:2]
            is_underhand = False
            if pitching_hand == '우투':
                pitching_hand = 'Right'
            elif pitching_hand == '좌투':
                pitching_hand = 'Left'
            elif pitching_hand == '우언':
                pitching_hand = 'Right'
                is_underhand = True
            elif pitching_hand == '좌언':
                pitching_hand = 'Left'
                is_underhand = True
            batting_hand = player_position[1][2:]
            if batting_hand == '우타':
                batting_hand = 'Right'
            elif batting_hand == '좌타':
                batting_hand = 'Left'
            worksheet.write(row, 5 + 2 + 0, detailed_position)
            worksheet.write(row, 5 + 2 + 1, pitching_hand)
            worksheet.write(row, 5 + 2 + 2, is_underhand)
            worksheet.write(row, 5 + 2 + 3, batting_hand)
        except Exception:
            error_string += "Position (7, 8, 9, 10): " + str(player_info[5]) + "   "

        try:
            height_weight = player_info[6].split('/')
            worksheet.write(row, 6 + 5 + 0, int(height_weight[0].replace('cm', '')))
            worksheet.write(row, 6 + 5 + 1, int(height_weight[1].replace('kg', '')))
        except Exception:
            error_string += "Body (11, 12): " + str(player_info[6]) + "   "

        worksheet.write(row, 7 + 2 + 3 + 1, player_info[7])

        try:
            if player_info[8][-1:] == '엔':
                worksheet.write(row, 8 + 6 + 0, int(player_info[8].replace('엔', '')))
                worksheet.write(row, 8 + 6 + 1, player_info[8][-1:])
            elif player_info[8][-3:] == '만달러':
                worksheet.write(row, 8 + 6 + 0, int(player_info[8].replace('만달러', '')))
                worksheet.write(row, 8 + 6 + 1, player_info[8][-3:])
            else:
                worksheet.write(row, 8 + 6 + 0, int(player_info[8].replace('만원', '').replace('달러', '')))
                worksheet.write(row, 8 + 6 + 1, player_info[8][-2:])
        except Exception:
            error_string += "Contract Payment (14, 15): " + str(player_info[8]) + "   "

        try:
            worksheet.write(row, 9 + 7 + 0, int(player_info[9].replace('만원', '').replace('달러', '')))
            worksheet.write(row, 9 + 7 + 1, player_info[9][-2:])
        except Exception:
            error_string += "Salary (16, 17): " + str(player_info[9]) + "   "

        try:
            player_draft = player_info[10].split()
            draft_detail = ""
            for text in player_draft[2:]:
                draft_detail += text + " "
            draft_detail = draft_detail[:-1]
            worksheet.write(row, 10 + 8 + 0, int(player_draft[0]))
            worksheet.write(row, 10 + 8 + 1, player_draft[1])
            worksheet.write(row, 10 + 8 + 2, draft_detail)
        except Exception:
            error_string += "Draft (18, 19, 20): " + str(player_info[10]) + "   "

        try:
            worksheet.write(row, 11 + 10 + 0, int(player_info[11][:2]))
            worksheet.write(row, 11 + 10 + 1, player_info[11][2:])
        except Exception:
            error_string += "Join (21, 22): " + str(player_info[11]) + "   "

        worksheet.write(row, 23, error_string)

    workbook.close()
    driver.quit()


if __name__ == '__main__':
    # PitcherDetail, HitterDetail, Retire
    # player_type = "HitterDetail"
    # collect_player_id(player_type)
    # merge_player_id_lists()
    # convert_excel_to_csv("/Users/joshuakim/PycharmProjects/KBO_Analysis/KBO ID Lists/kbo_id_list.xlsx")
    # generate_player_folders("/Volumes/Samsung_T5/KBO_Data/Players", "Situation")
    # collect_kbo_player_data("Hitter", "Situation")
    # rename_file_name()
    # remove_player_folders("/Volumes/Samsung_T5/KBO_Data/Players")
    # remove_csv_file()
    update_player_info(65827, "HitterDetail")
    update_player_info(61743, "HitterDetail")
    update_player_info(62802, "HitterDetail")
