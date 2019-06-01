import sys
sys.path.insert(0, '/Users/joshuakim/PycharmProjects/Math_Tools')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# excel_file = "pearson_correlations_between_two_categories.xlsx"
excel_file = "multiple_correlations_of_ranks_on_two_categories.xlsx"
data = pd.read_excel(excel_file)

# data["Independent Variable"] = data["Independent Variable Data Type"].map(str) + data["Independent Variable Data Category"]
# data["Dependent Variable"] = data["Dependent Variable Data Type"].map(str) + data["Dependent Variable Data Category"]
# data_pivoted = data.pivot(index = "Independent Variable", columns = "Dependent Variable", values = "Pearson Correlation")
data["Variable 1"] = data["Variable 1 Data Type"].map(str) + data["Variable 1 Data Category"]
data["Variable 2"] = data["Variable 2 Data Type"].map(str) + data["Variable 2 Data Category"]
data_pivoted = data.pivot(index="Variable 1", columns="Variable 2", values="Multiple Correlation")

plt.figure(figsize=(40, 40))
sns.heatmap(data_pivoted, fmt="g", cmap='viridis')
# plt.show()
plt.savefig('kbo_heatmap_2d_rank.png')
