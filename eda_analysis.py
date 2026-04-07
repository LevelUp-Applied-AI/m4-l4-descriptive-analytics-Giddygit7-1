"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def load_and_profile(filepath):
    """Load the dataset and generate a data profile report."""
    student_data = pd.read_csv(filepath)
    os.makedirs('output', exist_ok=True)
    
    nulls = student_data.isnull().sum()
    null_ratio = (nulls / len(student_data)) * 100
    
    with open('output/data_profile.txt', 'w') as f:
        f.write("Student Performance Data Profile\n")
        f.write(f"Rows/Cols: {student_data.shape}\n\n")
        f.write("Column Types:\n")
        f.write(str(student_data.dtypes) + "\n\n")
        f.write("Missing Values:\n")
        f.write(str(nulls) + "\n\n")
        f.write("Missing Percentage:\n")
        f.write(str(null_ratio.round(2)) + "%\n\n")
        f.write("Stats Summary:\n")
        f.write(str(student_data.describe()) + "\n")

    # Clean data: Impute commute with median, drop study hour nulls
    student_data['commute_minutes'] = student_data['commute_minutes'].fillna(student_data['commute_minutes'].median())
    student_data = student_data.dropna(subset=['study_hours_weekly'])
    return student_data

def plot_distributions(data_frame):
    """Create distribution plots for key numeric variables."""
    plt.figure(figsize=(8, 6))
    # Using data_frame to match the function argument
    sns.histplot(data_frame['gpa'], kde=True, color='skyblue') 
    plt.title('GPA Histogram')
    plt.savefig('output/gpa_distribution.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='department', y='gpa', data=data_frame)
    plt.title('GPA by Department')
    plt.savefig('output/gpa_by_department.png')
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.histplot(data_frame['attendance_pct'], kde=True, color='green')
    plt.title('Attendance Rate Distribution')
    plt.savefig('output/attendance_distribution.png')
    plt.close()

def plot_correlations(data_frame):
    """Analyze and visualize relationships between numeric variables."""
    numeric_cols = data_frame.select_dtypes(include=[np.number])
    corr_matrix = numeric_cols.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig('output/correlation_heatmap.png')
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='study_hours_weekly', y='gpa', data=data_frame)
    plt.title('Study Hours vs GPA')
    plt.savefig('output/scatter_study_gpa.png')
    plt.close()

def run_hypothesis_tests(data_frame):
    """Run statistical tests to validate observed patterns."""
    test_results = {}
    
    with_intern = data_frame[data_frame['has_internship'] == 'Yes']['gpa']
    no_intern = data_frame[data_frame['has_internship'] == 'No']['gpa']
    
    t_val, p_val = stats.ttest_ind(with_intern, no_intern)
    
    # Calculate Cohen's d (Effect Size)
    m_diff = with_intern.mean() - no_intern.mean()
    std_p = np.sqrt((with_intern.std()**2 + no_intern.std()**2) / 2)
    d_effect = m_diff / std_p
    
    test_results['internship_ttest'] = (t_val, p_val, d_effect)
    
    # Chi-Square test
    cross_tab = pd.crosstab(data_frame['scholarship'], data_frame['department'])
    chi_val, chi_p, d_f, exp = stats.chi2_contingency(cross_tab)
    test_results['scholarship_chi2'] = (chi_val, chi_p, d_f)
    
    print(f"Internship T-Test: t={t_val:.4f}, p={p_val:.4e}")
    print(f"Effect Size (Cohen's d): {d_effect:.2f}")
    print(f"Scholarship Chi2: chi2={chi_val:.4f}, p={chi_p:.4e}")
    return test_results

def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)
    my_students = load_and_profile('data/student_performance.csv')
    plot_distributions(my_students)
    plot_correlations(my_students)
    run_hypothesis_tests(my_students)
    print("\nLab 4 complete. Files saved in the output/ folder.")

if __name__ == "__main__":
    main()