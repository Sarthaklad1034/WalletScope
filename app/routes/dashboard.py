# dashboard.py - Updated version

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import Expense, Budget
from datetime import datetime, timedelta
from sqlalchemy import func, extract
import calendar
import json

dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/")
@dashboard.route("/dashboard")
@login_required
def home():
    # Get current date information
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Get current month budget and expenses
    current_month_budget = Budget.query.filter_by(
        user_id=current_user.id,
        month=current_month,
        year=current_year
    ).first()

    current_month_start = datetime(current_year, current_month, 1)
    current_month_end = datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])

    current_month_expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.date.between(current_month_start, current_month_end)
    ).all()

    current_month_total = sum(expense.amount for expense in current_month_expenses)

    # Get previous month budget and expenses for comparison
    prev_month_date = current_date - timedelta(days=current_date.day)
    prev_month = prev_month_date.month
    prev_year = prev_month_date.year

    prev_month_start = datetime(prev_year, prev_month, 1)
    prev_month_end = datetime(prev_year, prev_month, calendar.monthrange(prev_year, prev_month)[1])

    prev_month_expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.date.between(prev_month_start, prev_month_end)
    ).all()

    prev_month_total = sum(expense.amount for expense in prev_month_expenses)

    # Calculate budget stats
    budget_amount = current_month_budget.budget_amount if current_month_budget else 0
    budget_remaining = budget_amount - current_month_total if budget_amount > 0 else 0
    budget_percentage = (current_month_total / budget_amount * 100) if budget_amount > 0 else 0

    # Calculate percentage changes from previous month
    expense_change_pct = (
                (current_month_total - prev_month_total) / prev_month_total * 100) if prev_month_total > 0 else 0

    # Get previous month's budget for balance comparison
    prev_month_budget = Budget.query.filter_by(
        user_id=current_user.id,
        month=prev_month,
        year=prev_year
    ).first()

    prev_budget_amount = prev_month_budget.budget_amount if prev_month_budget else 0
    prev_balance = prev_budget_amount - prev_month_total if prev_budget_amount > 0 else 0
    current_balance = budget_amount - current_month_total if budget_amount > 0 else 0

    balance_change_pct = ((current_balance - prev_balance) / prev_balance * 100) if prev_balance > 0 else 0

    # Calculate savings rate (remaining budget as percentage of total budget)
    savings_rate = (budget_remaining / budget_amount * 100) if budget_amount > 0 else 0
    prev_savings_rate = (
                (prev_budget_amount - prev_month_total) / prev_budget_amount * 100) if prev_budget_amount > 0 else 0
    savings_rate_change = savings_rate - prev_savings_rate

    # Prepare expense categories for pie chart
    categories = {}
    for expense in current_month_expenses:
        if expense.category in categories:
            categories[expense.category] += expense.amount
        else:
            categories[expense.category] = expense.amount

    pie_data = {
        'labels': list(categories.keys()),
        'datasets': [{
            'data': list(categories.values()),
            'backgroundColor': [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#8AC249', '#EA526F', '#25CED1', '#FCEADE', '#FF8A5B'
            ],
            'hoverBackgroundColor': [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#8AC249', '#EA526F', '#25CED1', '#FCEADE', '#FF8A5B'
            ]
        }]
    }

    # Prepare monthly expense trend for line chart
    expenses_by_month = []
    budget_by_month = []

    for month in range(1, 13):
        # Get expenses for this month
        month_start = datetime(current_year, month, 1)
        month_end = datetime(current_year, month, calendar.monthrange(current_year, month)[1])

        month_expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            Expense.date.between(month_start, month_end)
        ).all()

        month_total = sum(expense.amount for expense in month_expenses)
        expenses_by_month.append(month_total)

        # Get budget for this month
        month_budget = Budget.query.filter_by(
            user_id=current_user.id,
            month=month,
            year=current_year
        ).first()

        budget_amount = month_budget.budget_amount if month_budget else 0
        budget_by_month.append(budget_amount)

    line_data = {
        'labels': [calendar.month_abbr[month] for month in range(1, 13)],
        'datasets': [
            {
                'label': 'Monthly Expenses',
                'data': expenses_by_month,
                'fill': False,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1
            },
            {
                'label': 'Monthly Budget',
                'data': budget_by_month,
                'fill': False,
                'borderColor': 'rgb(255, 99, 132)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'tension': 0.1,
                'borderDash': [5, 5]
            }
        ]
    }

    return render_template(
        'dashboard.html',
        title='Dashboard',
        total_expenses=current_month_total,
        budget_amount=budget_amount,
        budget_remaining=budget_remaining,
        budget_percentage=budget_percentage,
        balance=current_balance,
        savings_rate=savings_rate,
        expense_change_pct=expense_change_pct,
        balance_change_pct=balance_change_pct,
        savings_rate_change=savings_rate_change,
        pie_data=json.dumps(pie_data),
        line_data=json.dumps(line_data)
    )