from scipy import stats

scores = [72, 88, 64, 74, 67, 79, 85, 75, 89, 77]
hypothesized_mean = 70

t_statistic, p_value = stats.ttest_1samp(scores, hypothesized_mean)

print("T-Statistic:", t_statistic)
print("P-Value:", p_value)
