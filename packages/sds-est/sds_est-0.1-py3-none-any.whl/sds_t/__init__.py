import numpy as np
from scipy import stats

# Test scores before and after remedial lectures
test1 = np.array([85, 68, 67, 84, 98, 60, 94, 80, 94, 98, 95, 80, 85, 87, 75])
test2 = np.array([70, 90, 80, 89, 88, 86, 78, 87, 90, 86, 92, 94, 99, 93, 86])

# Print Null and Alternative Hypothesis
print("Null Hypothesis (H0): There is no significant difference in the mean test scores before and after the remedial lectures.")
print("Alternative Hypothesis (H1): There is a significant difference in the mean test scores before and after the remedial lectures.")

# Perform paired t-test
t_statistic, p_value = stats.ttest_rel(test1, test2)

# Print the results
print("\nT-statistic:", t_statistic)
print("P-value:", p_value)

# Step 5: Conclusion based on the p-value
alpha = 0.05  # significance level

if p_value < alpha:
    print("\nConclusion: Reject the null hypothesis")
    print("There is a significant difference in the test scores before and after the remedial lectures.")
    print("The remedial lectures seem to have improved the students' performance.")
else:
    print("\nConclusion: Fail to reject the null hypothesis.")
    print("There is no significant difference in the test scores before and after the remedial lectures.")
    print("The remedial lectures did not have a significant impact on the students' performance.")
