from tabulate import tabulate
import argparse
from services.transaction_service import TransactionService
from services.budget_service import BudgetService
from analytics.reports import ReportGenerator
from analytics.charts import plot_monthly_expense_trend, plot_category_breakdown, plot_budget_vs_actual
from utils.validators import validate_email, validate_date, validate_amount

def print_table(data, headers):
    print(tabulate(data, headers= headers, tablefmt= 'grid'))

def notify(message):
    print(f'\n==> {message}\n')

def parse_args():
    parser = argparse.ArgumentParser(description= 'Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest= 'command')

    add_txn = subparsers.add_parser('add_txn')
    add_txn.add_argument('--account_id', type= int, required= True)
    add_txn.add_argument('--category_id', type= int, required= True)
    add_txn.add_argument('--merchant_id', type= int, required= True)
    add_txn.add_argument('--amount', type= str, required= True)
    add_txn.add_argument('--date', type= str, required= True)
    add_txn.add_argument('--description', type= str, required= True)
    add_txn.add_argument('--txn_type', choices= ['expense', 'income'], required= True)

    view_budget = subparsers.add_parser('view budget')
    view_budget.add_argument('--user_id', type= int, required= True)

    analyze = subparsers.add_parser('analyze')
    analyze.add_argument('--user_id', type= int, required= True)
    analyze.add_argument('--type', choices= ['monthly', 'category', 'budget_vs_actual'], required= True)
    analyze.add_argument('--month',type= int, default= None)

    return parser.parse_args()

def handle_command(args, config):
    txn_service = TransactionService(config)
    budget_service = BudgetService(config)
    report_gen = ReportGenerator(config)

    if args.command == 'add_txn':
        amount = validate_amount(args.amount)
        date = validate_date(args.date)
        txn_data = {
            'transaction_id' : None,
            'account_id' : args.account_id,
            'category_id' : args.category_id,
            'merchant_id' : args.merchant_id,
            'amount' : amount,
            'transaction_date' : date,
            'transaction_desc' : args.description,
            'transaction_type' : args.txn_type
        }
        txn_service.add_transaction(txn_data)
        notify('Transaction Added Successfully.')

    elif args.command == 'view_budget':
        budgets = budget_service.get_budgets(args.user_id)
        print_table(budgets, headers= ['Budget ID', 'User ID', 'Category', 'Amount', 'Month', 'Year'])

    elif args.command == 'analyze':
        if args.type == 'monthly':
            monthly = report_gen.monthly_expense_trend(args.user_id)
            path = plot_monthly_expense_trend(monthly, 'outputs/monthly_trend.png')
            notify(f'Monthly Expense Trend Chart Saved to {path}')

        elif args.type == 'category':
            breakdown = report_gen.category_breakdown(args.user_id, args.month)
            path = plot_category_breakdown(breakdown, 'outputs/category_breakdown.png')
            notify(f'Category Breakdown Chart Saved to {path}')

        elif args.type == 'budget_vs_actual':
            if not args.month:
                notify('Month is Required for Budget vs Actual Analysis.')
                return

            budget_actual = report_gen.budget_vs_actual(args.user_id, args.month)
            path = plot_budget_vs_actual(budget_actual, 'outputs/budget_vs_actual.png')
            notify(f'Budget vs Actual Chart Saved to {path}')