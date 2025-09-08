import seaborn as sns
import matplotlib.pyplot as plt

def plot_monthly_expense_trend(monthly, output_path):
    plt.figure(figsize = (8,4))
    sns.barplot(x = monthly.index, y = monthly.values, color = 'skyblue')
    plt.title('Monthly Expense Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Spent')
    plt.tight_layout()
    plt.savefig(output_path)
    return output_path

def plot_category_breakdown(breakdown, output_path):
    plt.figure(figsize = (8,5))
    sns.barplot(x = breakdown.index, y = breakdown.values)
    plt.title('Expense By Category')
    plt.xlabel('Category')
    plt.ylabel('Total Spent')
    plt.tight_layout()
    plt.savefig(output_path)
    return output_path

def plot_budget_vs_actual(budget_actual, output_path):
    plt.figure(figsize= (9,5))
    ax = sns.barplot(x = 'category', y = 'budget', data= budget_actual, color= 'green', label = 'Budget')
    sns.barplot(x = 'category', y = 'amount_actual', data= budget_actual, color= 'red', label= 'Actual')
    ax.legend()
    plt.title('Budget vs Actual Expense')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.tight_layout()
    plt.savefig(output_path)
    return output_path