from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models import Budget, Expense
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime
import calendar

budget = Blueprint('budget', __name__)

class BudgetForm(FlaskForm):
    month = SelectField('Month', validators=[DataRequired()], choices=[
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    ], coerce=int)
    year = SelectField('Year', validators=[DataRequired()], coerce=int)
    budget_amount = FloatField('Budget Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Set Budget')

@budget.route("/budget", methods=['GET', 'POST'])
@login_required
def budget_management():
    # Setup the form with current year and the next 5 years
    current_year = datetime.now().year
    form = BudgetForm()
    form.year.choices = [(year, str(year)) for year in range(current_year - 1, current_year + 6)]
    
    if form.validate_on_submit():
        # Check if budget already exists for this month and year
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            month=form.month.data,
            year=form.year.data
        ).first()
        
        if existing_budget:
            existing_budget.budget_amount = form.budget_amount.data
            db.session.commit()
            flash('Your budget has been updated!', 'success')
        else:
            budget_entry = Budget(
                user_id=current_user.id,
                month=form.month.data,
                year=form.year.data,
                budget_amount=form.budget_amount.data
            )
            db.session.add(budget_entry)
            db.session.commit()
            flash('Your budget has been set!', 'success')
        
        return redirect(url_for('budget.budget_management'))
    
    # Set default month and year to current
    if request.method == 'GET':
        form.month.data = datetime.now().month
        form.year.data = current_year
    
    # Get all budgets for the current user
    user_budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.year.desc(), Budget.month.desc()).all()
    
    # Calculate expenses for each budget
    budget_stats = []
    for budget_entry in user_budgets:
        expenses = Expense.query.filter(
            Expense.user_id == current_user.id,
            Expense.date.between(
                f"{budget_entry.year}-{budget_entry.month:02d}-01", 
                f"{budget_entry.year}-{budget_entry.month:02d}-{calendar.monthrange(budget_entry.year, budget_entry.month)[1]}"
            )
        ).all()
        
        total_expenses = sum(expense.amount for expense in expenses)
        remaining = budget_entry.budget_amount - total_expenses
        percentage_used = (total_expenses / budget_entry.budget_amount * 100) if budget_entry.budget_amount > 0 else 0
        
        budget_stats.append({
            'id': budget_entry.id,
            'month': calendar.month_name[budget_entry.month],
            'year': budget_entry.year,
            'budget_amount': budget_entry.budget_amount,
            'total_expenses': total_expenses,
            'remaining': remaining,
            'percentage_used': percentage_used
        })
    
    return render_template('budget.html', title='Budget Management', form=form, budget_stats=budget_stats)

@budget.route("/budget/<int:budget_id>/delete", methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget_entry = Budget.query.get_or_404(budget_id)
    
    if budget_entry.user_id != current_user.id:
        flash('You do not have permission to delete this budget.', 'danger')
        return redirect(url_for('budget.budget_management'))
    
    db.session.delete(budget_entry)
    db.session.commit()
    flash('Your budget has been deleted!', 'success')
    return redirect(url_for('budget.budget_management'))