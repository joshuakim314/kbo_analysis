import sys
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

from matrix import *
from statistics_tools import *
import xlsxwriter
from analyze_kbo_team_data import *


def dot_product(A, B):
    if len(A) != len(B):
        return False
    return sum(C[0]*C[1] for C in zip(A, B))


num_years = 9
teams = ['삼성', '두산', 'SK', 'NC', '넥센', 'KIA', 'LG', '롯데', '한화', 'KT']
if num_years > 4:
    teams = ['삼성', '두산', 'SK', 'NC', '넥센', 'KIA', 'LG', '롯데', '한화']
if num_years > 6:
    teams = ['삼성', '두산', 'SK', '넥센', 'KIA', 'LG', '롯데', '한화']
coeffs, correl = analyze_rank_data_wrt_time(num_years)
rank_history = format_rank_data()

workbook = xlsxwriter.Workbook("time_analysis_of_rank_data_with_past_" + str(num_years) + "_years.xlsx")
worksheet = workbook.add_worksheet()

row_excel = 0
worksheet.write(row_excel, 0, "Number of Years Used")
worksheet.write(row_excel, 1, "Constant Coefficient")
for i in range(num_years):
    worksheet.write(row_excel, i + 2, "Coefficient for " + str(num_years-i) + " Year(s) Ago")
worksheet.write(row_excel, num_years + 2, "Multiple Correlation")

row_excel = 1
worksheet.write(row_excel, 0, num_years)
for i in range(num_years + 1):
    worksheet.write(row_excel, i + 1, coeffs[i])
worksheet.write(row_excel, num_years + 2, correl)

row_excel = 3
worksheet.write(row_excel, 0, "Team")
worksheet.write(row_excel, 1, "Prediction")
for i in range(num_years):
    worksheet.write(row_excel, i + 2, "Winning % from " + str(num_years-i) + " Year(s) Ago")

row_excel = 4
for team in teams:
    worksheet.write(row_excel, 0, team)
    past_ranks = [rank_history[team][i - num_years] for i in range(num_years)]
    print(team, past_ranks)
    prediction = coeffs[0] + dot_product(past_ranks, coeffs[1:])
    worksheet.write(row_excel, 1, prediction)
    for i in range(num_years):
        worksheet.write(row_excel, i + 2, past_ranks[i])
    row_excel += 1

if num_years > 6:
    worksheet.write(row_excel, 0, 'NC')
    past_ranks_NC = rank_history['NC'][-6:]
    coeffs_NC, correl_NC = analyze_rank_data_wrt_time(6)
    prediction = coeffs_NC[0] + dot_product(past_ranks_NC, coeffs_NC[1:])
    worksheet.write(row_excel, 1, prediction)
    for i in range(6):
        worksheet.write(row_excel, num_years - 4 + i, past_ranks_NC[i])
    row_excel += 1

if num_years > 4:
    worksheet.write(row_excel, 0, 'KT')
    past_ranks_KT = rank_history['KT'][-4:]
    coeffs_KT, correl_KT = analyze_rank_data_wrt_time(4)
    prediction = coeffs_KT[0] + dot_product(past_ranks_KT, coeffs_KT[1:])
    worksheet.write(row_excel, 1, prediction)
    for i in range(4):
        worksheet.write(row_excel, num_years - 2 + i, past_ranks_KT[i])
    row_excel += 1

workbook.close()
