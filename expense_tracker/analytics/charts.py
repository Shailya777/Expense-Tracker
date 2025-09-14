import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Ensuring That Directory Named "outputs" exists for Saving Charts:
if not os.path.exists('outputs'):
    os.makedirs('outputs')

def plot_monthly_trend(trend_df: pd.DataFrame, user_id: int) -> str:
    """
     Generates and saves a bar chart for the monthly expense trend.

    :param trend_df: DataFrame from reports.monthly_expense_trend.
    :param user_id: The user's ID for unique filenames.

    :return: The file path where the chart was saved.
    """
    if trend_df.empty:
        return 'No Data Available to Plot.'

    plt.figure(figsize = (10,6))
    sns.barplot(data= trend_df, x = 'month', y = 'Total Expense', palette= 'viridis')
    plt.title('Monthly Expense Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Spent')
    plt.xticks(rotation= 45)
    plt.tight_layout()

    filename = f'outputs/user_{user_id}_monthly_trend_{datetime.now().strftime('%Y%m%d%H%M%S')}.png'
    plt.savefig(filename)
    plt.close()
    return filename


def plot_category_breakdown(category_df: pd.DataFrame, user_id: int) -> str:
    """
    Generates and saves a pie chart for the expense category breakdown.

    :param category_df: DataFrame from reports.category_breakdown.
    :param user_id: The user's ID for unique filenames.

    :return: The file path where the chart was saved.
    """

    if category_df.empty:
        return 'No Data Available to Plot.'

    plt.figure(figsize = (12,8))
    plt.pie(category_df['Total Expense'], labels= category_df['category_name'], autopct= '%1.1f%%', startangle= 140)
    plt.title('Expense Breakdown By Category')
    plt.axis('equal')

    filename = f'outputs/user_{user_id}_category_breakdown_{datetime.now().strftime('%Y%m%d%H%M%S')}.png'
    plt.savefig(filename)
    plt.close()
    return filename


def plot_budget_vs_actual(comparison_df: pd.DataFrame, user_id: int, year: int, month: int) -> str:
    """
    Generates and saves a grouped bar chart for budget vs. actual spending.

    :param comparison_df: DataFrame from reports.budget_vs_actual.
    :param user_id: The user's ID for unique filenames.
    :param year: The year for the chart title.
    :param month: The month for the chart title.

    :return: The file path where the chart was saved.
    """

    if comparison_df.empty:
        return 'No Budget Data Available to Plot.'

    df_melted = comparison_df.melt(id_vars= 'Category', value_vars= ['Budget', 'Actual'], var_name= 'Type', value_name= 'Amount')

    plt.figure(figsize= (14,8))
    sns.barplot(data= df_melted, x = 'Category', y = 'Amount', hue= 'Type', palette= 'Set2')
    plt.title(f'Budget vs Actual Spending for {year}-{month:02d}')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation= 45, ha= 'right')
    plt.tight_layout()

    filename = f'outputs/user_{user_id}_udget_vs_actual_{year}_{month:02d}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png'
    plt.savefig(filename)
    plt.close()
    return filename