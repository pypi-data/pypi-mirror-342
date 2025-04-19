import scipy.stats as stats

# Time taken by employees in Group-I (Experience: 0-1 year)
group1 = [85, 95, 100, 80, 90, 97, 104, 95, 88, 92, 94, 99]

# Time taken by employees in Group-II (Experience: 1-2 years)
group2 = [83, 85, 96, 92, 100, 104, 94, 95, 88, 90, 93, 94]

print("Hypotheses:")
print("Null Hypothesis (H₀): There is no significant difference in the mean time taken between Group-I and Group-II.")
print("Alternative Hypothesis (H₁): There is a significant difference in the mean time taken between Group-I and Group-II.\n")

# Perform the Two-Sample T-Test
t_statistic, p_value = stats.ttest_ind(group1, group2)

# Print results
print("T-statistic:", t_statistic)
print("P-value:", p_value)

# Set significance level (alpha)
alpha = 0.05
print("Alpha value is" , alpha)

# Interpret the result
if p_value < alpha:
    print("\nalpha value is less than p value")
    print("\nReject the null hypothesis: There is a significant difference in the mean time taken between the two groups.")
else:
    print("\nFail to reject the null hypothesis: There is no significant difference in the mean time taken between the two groups.")
