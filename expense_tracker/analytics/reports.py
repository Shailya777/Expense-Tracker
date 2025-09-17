import pandas as pd
from typing import List

from pandas.core.ops import comparison_op

from expense_tracker.services.budget_service import BudgetService

def monthly_expense_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
     Calculates the total monthly expense trend from transaction data.

    :param df: DataFrame with transaction data.

    :return: A DataFrame indexed by month with total expenses.
    """

    expenses_df = df[df['transaction_type'] == 'expense'].copy()

    if expenses_df.empty:
        return pd.DataFrame(columns= ['Total Expense'])

    expenses_df['month'] = expenses_df['transaction_date'].dt.to_period('M')
    monthly_trend = expenses_df.groupby('month')['amount'].sum().reset_index()
    monthly_trend.rename(columns = {'amount': 'Total Expense'}, inplace= True)
    monthly_trend['month'] = monthly_trend['month'].astype(str)
    return monthly_trend

def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the breakdown of expenses by category.

    :param df: DataFrame with transaction data.

    :return: A DataFrame with total expense amount for each category.
    """

    expenses_df = df[df['transaction_type'] == 'expense']

    if expenses_df.empty:
        return pd.DataFrame(columns=['Total Expense'])

    breakdown = expenses_df.groupby('category_name')['amount'].sum().reset_index()
    breakdown.rename(columns = {'amount': 'Total Expense'}, inplace= True)
    return breakdown.sort_values(by= 'Total Expense', ascending= False)

def top_merchants(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Identifies the top N merchants by total spending.

    :param df: DataFrame with transaction data.
    :param n: The number of top merchants to return. Defaults to 5.

    :return: A DataFrame with the top N merchants and their total spending.
    """

    expenses_df = df[df['transaction_type'] == 'expense']

    if expenses_df.empty or 'merchant_name' not in expenses_df.columns:
        return pd.DataFrame(columns=['Total Expense'])

    top = expenses_df.groupby('merchant_name')['amount'].sum().reset_index()
    top.rename(columns = {'amount':'Total Expense'}, inplace= True)
    return top.nlargest(n, 'Total Expense')

def budget_vs_actual(user_id: int, year: int, month: int, transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compares budgeted amounts vs actual spending for a given month.

    :param user_id: The ID of the user.
    :param year: The year of the analysis period.
    :param month: The month of the analysis period.
    :param transactions_df: DataFrame of the user's transactions.

    :return: A DataFrame comparing Budget, Actual, and Variance for each category.
    """

    # 1. Get Budget Data:
    budgets_raw: List[dict] = BudgetService.get_budgets_for_period(user_id, year, month)

    if not budgets_raw:
        return pd.DataFrame(columns=['Category', 'Budget', 'Actual','Variance'])

    budgets_df = pd.DataFrame(budgets_raw)
    budgets_df.rename(columns= {'category_name': 'Category', 'amount': 'Budget'}, inplace= True)

    # 2. Calculate Actual Spending For The Month:
    start_date = pd.Timestamp(year= year, month= month, day= 1)
    end_date = start_date + pd.offsets.MonthEnd(1)

    mask = (transactions_df['transaction_date'] >= start_date) & (transactions_df['transaction_date'] <= end_date) & (transactions_df['transaction_type'] == 'expense')

    actual_df = transactions_df.loc[mask]

    if actual_df.empty:
        actual_summary = pd.DataFrame(columns=['Category', 'Actual'])
    else:
        actual_summary = actual_df.groupby('category_name')['amount'].sum().reset_index()
        actual_summary.rename(columns = {'category_name': 'Category', 'amount':'Actual'}, inplace= True)

    # 3. Merging Budgets vs Actual Data:
    comparison_df = pd.merge(budgets_df, actual_summary, on= 'Category', how= 'left')
    comparison_df['Actual'] = comparison_df['Actual'].fillna(0)
    comparison_df['variance'] = comparison_df['Budget'] = comparison_df['Actual']

    return comparison_df[['Category', 'Budget', 'Actual', 'Variance']]