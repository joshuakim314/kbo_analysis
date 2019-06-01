import sys
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

from matrix import *
from statistics_tools import *
import xlrd
import xlsxwriter
from analyze_kbo_team_data import *


category_dict = {
    'hitter1': ['AVG', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'TB', 'RBI', 'SAC', 'SF'],
    'hitter2': ['AVG', 'BB', 'IBB', 'HBP', 'SO', 'GDP', 'SLG', 'OBP', 'OPS', 'MH', 'RISP', 'PH-BA'],
    'pitcher1': ['ERA', 'G', 'W', 'L', 'SV', 'HLD', 'WPCT', 'IP', 'H', 'HR', 'BB', 'HBP', 'SO', 'R', 'ER', 'WHIP'],
    'pitcher2': ['ERA', 'CG', 'SHO', 'QS', 'BSV', 'TBF', 'NP', 'AVG', '2B', '3B', 'SAC', 'SF', 'IBB', 'WP', 'BK'],
    'defense': ['G', 'E', 'PKO', 'PO', 'A', 'DP', 'FPCT', 'PB', 'SB', 'CS', 'CS%'],
    'runner': ['G', 'SBA', 'SB', 'CS', 'SB%', 'OOB', 'PKO']
}
category_element_list = []
for key in category_dict:
    for elem in category_dict[key]:
        category_element_list.append([key, elem])

workbook = xlsxwriter.Workbook("pearson_correlations_between_two_categories.xlsx")
worksheet = workbook.add_worksheet()
row_excel = 0

worksheet.write(row_excel, 0, "Independent Variable Data Type")
worksheet.write(row_excel, 1, "Independent Variable Data Category")
worksheet.write(row_excel, 2, "Dependent Variable Data Type")
worksheet.write(row_excel, 3, "Dependent Variable Data Category")
worksheet.write(row_excel, 4, "Constant Coefficient")
worksheet.write(row_excel, 5, "Variable Coefficient")
worksheet.write(row_excel, 6, "Pearson Correlation")
row_excel += 1

years = [2001 + i for i in range(18)]

# these for-loop statements do not allow duplicates
# for i in range(len(category_element_list) - 1):
#     for j in range(len(category_element_list) - i - 1):
#         categories = [category_element_list[i], category_element_list[i + j + 1]]

for i in range(len(category_element_list)):
    for j in range(len(category_element_list)):
        categories = [category_element_list[i], category_element_list[j]]
        coeffs, correl = compare_two_categories(years, categories)
        #########################
        # ONLY FOR TESTING PURPOSE
        print("Coefficients of Linear Fit: ", coeffs)
        print("Pearson Correlation: ", correl)
        # REMOVE THIS LATER
        #########################
        worksheet.write(row_excel, 0, categories[0][0])
        worksheet.write(row_excel, 1, categories[0][1])
        worksheet.write(row_excel, 2, categories[1][0])
        worksheet.write(row_excel, 3, categories[1][1])
        worksheet.write(row_excel, 4, coeffs[0])
        worksheet.write(row_excel, 5, coeffs[1])
        worksheet.write(row_excel, 6, correl)
        row_excel += 1

workbook.close()
