# Student Performance Analysis Report
**Hashemite Technical University**

## 1. Dataset Description
- **Data Shape:** The initial dataset contained 2,000 student records.
- **Data Quality:** I handled missing values in `commute_minutes` using median imputation. For `study_hours_weekly`, I dropped the rows with missing data (about 5%) to keep the analysis accurate.
- **Observations:** The GPA distribution is left-skewed, meaning the majority of students are performing well (clustering between 2.5 and 3.5).

## 2. Key Distribution Findings
- **GPA by Department:** Looking at `gpa_by_department.png`, student performance is fairly consistent across different majors, though some departments have slightly more outliers on the lower end.
- **Weekly Study Time:** Most students report studying between 15 and 20 hours per week.
- **Attendance Rates:** High attendance (over 80%) is common at HTU, as shown in `attendance_distribution.png`.

## 3. Notable Correlations
- **Main Relationship:** The strongest relationship found was between `study_hours_weekly` and `gpa`. 
- **Finding:** There is a clear positive correlation here. As study hours increase, GPA generally tends to rise as well, which is shown in `scatter_study_gpa.png`.

## 4. Hypothesis Test Results
### Hypothesis 1: Internship Status vs. GPA
- **Test Type:** Independent Samples T-Test
- **Results:** t = 13.5644, p = 3.6848e-40, d = 0.6898
- **Interpretation:** This result is **statistically significant**. Students who have internships maintain a significantly higher GPA than those who do not. The effect size (0.69) is medium-to-large, suggesting this is a very important factor for student success.

### Hypothesis 2: Scholarship vs. Department
- **Test Type:** Chi-Square Test
- **Results:** chi2 = 13.9486, p = 0.3040
- **Interpretation:** This result is **not significant**. There is no strong evidence to suggest that certain scholarships are concentrated in specific departments; they seem to be distributed fairly evenly.

## 5. Actionable Recommendations
1. **Promote Internships:** Since internships have a strong link to higher GPAs, the university should help more students find placement opportunities.
2. **Study Support:** Because study hours are tied to grades, the university could offer workshops on time management to help students maximize their weekly study hours.
3. **Departmental Parity:** Since GPA and scholarships are consistent across departments, the university should continue its current balanced resource allocation.