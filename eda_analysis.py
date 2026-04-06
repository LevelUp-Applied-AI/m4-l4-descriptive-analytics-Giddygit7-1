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
    """Load the dataset and generate a data profile report.

    Args:
        filepath: path to the CSV file (e.g., 'data/student_performance.csv')

    Returns:
        DataFrame: the loaded dataset

    Side effects:
        Saves a text profile to output/data_profile.txt containing:
        - Shape (rows, columns)
        - Data types for each column
        - Missing value counts per column
        - Descriptive statistics for numeric columns
    """
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

    student_data['commute_minutes'] = student_data['commute_minutes'].fillna(student_data['commute_minutes'].median())
    student_data = student_data.dropna(subset=['study_hours_weekly'])
    return student_data


def plot_distributions(data_frame):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    """
    plt.figure(figsize=(8, 6))
    # Make sure this says 'data_frame' to match the line above
    sns.histplot(data_frame['gpa'], kde=True, color='skyblue') 
    plt.title('GPA Histogram')
    plt.savefig('output/gpa_distribution.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    # Make sure this also says 'data_frame'
    sns.boxplot(x='department', y='gpa', data=data_frame)
    plt.title('GPA by Department')
    plt.savefig('output/gpa_by_department.png')
    plt.close()


def plot_correlations(data_frame):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """
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
    """Run statistical tests to validate observed patterns.

    Args:
        data_frame: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """
    test_results = {}
    
    with_intern = data_frame[data_frame['has_internship'] == 'Yes']['gpa']
    no_intern = data_frame[data_frame['has_internship'] == 'No']['gpa']
    
    t_val, p_val = stats.ttest_ind(with_intern, no_intern)
    
    m_diff = with_intern.mean() - no_intern.mean()
    std_p = np.sqrt((with_intern.std()**2 + no_intern.std()**2) / 2)
    d_effect = m_diff / std_p
    
    test_results['internship_ttest'] = (t_val, p_val, d_effect)
    
    cross_tab = pd.crosstab(data_frame['scholarship'], data_frame['department'])
    chi_val, chi_p, d_f, exp = stats.chi2_contingency(cross_tab)
    test_results['scholarship_chi2'] = (chi_val, chi_p, d_f)
    
    print(f"Internship T-Test: t={t_val:.4f}, p={p_val:.4e}")
    print(f"Scholarship Chi2: chi2={chi_val:.4f}, p={chi_p:.4e}")
    return test_results


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)
    my_students = load_and_profile('data/student_performance.csv')
    plot_distributions(my_students)
    plot_correlations(my_students)
    run_hypothesis_tests(my_students)
    print("Lab 4 complete. Files saved.")


if __name__ == "__main__":
    main()
