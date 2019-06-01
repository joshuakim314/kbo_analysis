import sys
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

from matrix import *
from statistics_tools import *
import xlrd
import xlsxwriter
from analyze_kbo_team_data import *


# num_category = 3

category_dict = {
    'hitter1': ['AVG', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'TB', 'RBI', 'SAC', 'SF'],
    'hitter2': ['AVG', 'BB', 'IBB', 'HBP', 'SO', 'GDP', 'SLG', 'OBP', 'OPS', 'MH', 'RISP', 'PH-BA'],
    'pitcher1': ['ERA', 'G', 'W', 'L', 'SV', 'HLD', 'WPCT', 'IP', 'H', 'HR', 'BB', 'HBP', 'SO', 'R', 'ER', 'WHIP'],
    'pitcher2': ['ERA', 'CG', 'SHO', 'QS', 'BSV', 'TBF', 'NP', 'AVG', '2B', '3B', 'SAC', 'SF', 'IBB', 'WP', 'BK'],
    'defense': ['G', 'E', 'PKO', 'PO', 'A', 'DP', 'FPCT', 'PB', 'SB', 'CS', 'CS%'],
    'runner': ['G', 'SBA', 'SB', 'CS', 'SB%', 'OOB', 'PKO']
}
category_element_list = []

# # category_element_list generator for all data types
# for key in category_dict:
#     for elem in category_dict[key]:
#         category_element_list.append([key, elem])

# # category_element_list generator for hitter types
# for elem in category_dict['hitter1']:
#     category_element_list.append(['hitter1', elem])
# for elem in category_dict['hitter2'][1:]:    # [1:] to avoid any duplicates
#     category_element_list.append(['hitter2', elem])

# # category_element_list generator for pitcher types
# for elem in category_dict['pitcher1']:
#     category_element_list.append(['pitcher1', elem])
# for elem in category_dict['pitcher2'][1:]:    # [1:] to avoid any duplicates
#     category_element_list.append(['pitcher2', elem])

# for elem in category_dict['defense']:
#     category_element_list.append(['defense', elem])

for elem in category_dict['runner']:
    category_element_list.append(['runner', elem])

# workbook = xlsxwriter.Workbook("multiple_correlations_of_ranks_on_two_categories.xlsx")
# workbook = xlsxwriter.Workbook("multiple_correlations_of_ranks_on_three_hitter_categories.xlsx")
# workbook = xlsxwriter.Workbook("multiple_correlations_of_ranks_on_three_pitcher_categories.xlsx")
# workbook = xlsxwriter.Workbook("multiple_correlations_of_ranks_on_three_defense_categories.xlsx")
workbook = xlsxwriter.Workbook("multiple_correlations_of_ranks_on_three_runner_categories.xlsx")
worksheet = workbook.add_worksheet()
row_excel = 0

worksheet.write(row_excel, 0, "Variable 1 Data Category")
worksheet.write(row_excel, 1, "Variable 2 Data Category")
worksheet.write(row_excel, 2, "Variable 3 Data Category")
worksheet.write(row_excel, 3, "Constant Coefficient")
worksheet.write(row_excel, 4, "Variable 1 Coefficient")
worksheet.write(row_excel, 5, "Variable 2 Coefficient")
worksheet.write(row_excel, 6, "Variable 3 Coefficient")
worksheet.write(row_excel, 7, "Multiple Correlation")
row_excel += 1

years = [2001 + i for i in range(18)]

# this is for two categories
# for i in range(len(category_element_list)):
#     for j in range(len(category_element_list)):
#         categories = [category_element_list[i], category_element_list[j]]
#         coeffs, correl = [False, False, False], 0
#         try:
#             coeffs, correl = analyze_team_data(years, categories)
#         except:
#             pass
#         #########################
#         # ONLY FOR TESTING PURPOSE
#         print("Coefficients of Linear Fit: ", coeffs)
#         print("Multiple Correlation: ", correl)
#         # REMOVE THIS LATER
#         #########################
#         worksheet.write(row_excel, 0, categories[0][0])
#         worksheet.write(row_excel, 1, categories[0][1])
#         worksheet.write(row_excel, 2, categories[1][0])
#         worksheet.write(row_excel, 3, categories[1][1])
#         worksheet.write(row_excel, 4, coeffs[0])
#         worksheet.write(row_excel, 5, coeffs[1])
#         worksheet.write(row_excel, 6, coeffs[2])
#         worksheet.write(row_excel, 7, correl)
#         row_excel += 1

# this is for three categories
for i in range(len(category_element_list)):
    for j in range(len(category_element_list)):
        for k in range(len(category_element_list)):
            categories = [category_element_list[i], category_element_list[j], category_element_list[k]]
            default_false_list = [False, False, False, False]
            coeffs, correl = default_false_list, 0
            try:
                coeffs, correl = analyze_team_data(years, categories)
                if not coeffs:
                    coeffs, correl = default_false_list, 0
            except:
                pass
            #########################
            # ONLY FOR TESTING PURPOSE
            print("Coefficients of Linear Fit: ", coeffs)
            print("Multiple Correlation: ", correl)
            # REMOVE THIS LATER
            #########################
            worksheet.write(row_excel, 0, categories[0][1])
            worksheet.write(row_excel, 1, categories[1][1])
            worksheet.write(row_excel, 2, categories[2][1])
            worksheet.write(row_excel, 3, coeffs[0])
            worksheet.write(row_excel, 4, coeffs[1])
            worksheet.write(row_excel, 5, coeffs[2])
            worksheet.write(row_excel, 6, coeffs[3])
            worksheet.write(row_excel, 7, correl)
            row_excel += 1

workbook.close()
