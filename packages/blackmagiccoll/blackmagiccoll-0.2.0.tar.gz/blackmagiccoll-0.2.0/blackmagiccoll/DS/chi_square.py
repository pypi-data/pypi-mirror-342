import pandas as pd
from scipy.stats import chi2_contingency

aptitude = [85, 65, 50, 68, 87, 74, 65, 96, 68, 94, 73, 84, 85, 87, 91]
jobprof = [70, 90, 80, 89, 88, 86, 78, 67, 86, 90, 92, 94, 99, 93, 87]

df = pd.DataFrame({'aptitude': aptitude, 'jobprof': jobprof})

df['aptitude_cat'] = pd.qcut(df['aptitude'], q=3, labels=['Low', 'Medium', 'High'])
df['jobprof_cat'] = pd.qcut(df['jobprof'], q=3, labels=['Low', 'Medium', 'High'])

contingency_table = pd.crosstab(df['aptitude_cat'], df['jobprof_cat'])

chi2, p, dof, expected = chi2_contingency(contingency_table)

print("Contingency Table:\n", contingency_table)
print("\nChi-Square Statistic:", chi2)
print("Degrees of Freedom:", dof)
print("P-Value:", p)
if p>0.05:
    print("Null hypothesis is rejucted.")
else:
    print("Accept null hypothesis.")
