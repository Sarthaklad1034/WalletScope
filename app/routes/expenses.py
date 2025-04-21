from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Expense
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from datetime import datetime

expenses = Blueprint('expenses', __name__)

class ExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save')

class DeleteExpenseForm(FlaskForm):
    """Empty form just for CSRF protection"""
    submit = SubmitField('Delete')


@expenses.route("/expenses", methods=['GET', 'POST'])
@login_required
def expense_list():
    form = ExpenseForm()
    delete_form = DeleteExpenseForm()

    # Set category choices based on the predefined list from the original code
    form.category_id.choices = [
        (1, 'Housing'),
        (2, 'Transportation'),
        (3, 'Food'),
        (4, 'Utilities'),
        (5, 'Insurance'),
        (6, 'Healthcare'),
        (7, 'Entertainment'),
        (8, 'Personal'),
        (9, 'Education'),
        (10, 'Savings'),
        (11, 'Other')
    ]

    if form.validate_on_submit():
        expense = Expense(
            date=form.date.data,
            amount=form.amount.data,
            category=dict(form.category_id.choices).get(form.category_id.data),
            description=form.description.data,
            author=current_user
        )
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been added!', 'success')
        return redirect(url_for('expenses.expense_list'))

    # Set default date to today
    if request.method == 'GET':
        form.date.data = datetime.now().date()

    # Get filter parameter
    filter_category = request.args.get('filter', 'all')

    # Get expenses with filter
    query = Expense.query.filter_by(user_id=current_user.id)

    # Apply category filter if not 'all'
    if filter_category != 'all' and filter_category.isdigit():
        category_id = int(filter_category)
        category_name = dict(form.category_id.choices).get(category_id)
        if category_name:
            query = query.filter_by(category=category_name)

    # Order by date descending
    user_expenses = query.order_by(Expense.date.desc()).all()

    # Calculate total amount of filtered expenses
    total_amount = sum(expense.amount for expense in user_expenses) if user_expenses else 0

    # Create a simple pagination object for template compatibility
    class Pagination:
        def __init__(self, items, page=1, per_page=10):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = len(items)

        @property
        def pages(self):
            return max(1, (self.total + self.per_page - 1) // self.per_page)

        @property
        def has_prev(self):
            return self.page > 1

        @property
        def has_next(self):
            return self.page < self.pages

        @property
        def prev_num(self):
            return self.page - 1 if self.has_prev else None

        @property
        def next_num(self):
            return self.page + 1 if self.has_next else None

        def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
            """Iterates over the page numbers in the pagination."""
            last = 0
            for num in range(1, self.pages + 1):
                if num <= left_edge or \
                        (num > self.page - left_current - 1 and num < self.page + right_current) or \
                        num > self.pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

    # Get page parameter
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Create simple pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_expenses = user_expenses[start:end] if user_expenses else []
    pagination = Pagination(user_expenses, page, per_page)

    return render_template('expenses.html',
        title='Expenses',
        form=form,
        delete_form=delete_form,
        expenses=paginated_expenses,
        pagination=pagination,
        total_amount=total_amount,
        categories=[{'id': k, 'name': v, 'color': '#6c757d'} for k, v in form.category_id.choices])

@expenses.route("/expenses/add", methods=['POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    
    # Set category choices based on the predefined list
    form.category_id.choices = [
        (1, 'Housing'),
        (2, 'Transportation'),
        (3, 'Food'),
        (4, 'Utilities'),
        (5, 'Insurance'),
        (6, 'Healthcare'),
        (7, 'Entertainment'),
        (8, 'Personal'),
        (9, 'Education'),
        (10, 'Savings'),
        (11, 'Other')
    ]
    
    if form.validate_on_submit():
        expense = Expense(
            date=form.date.data,
            amount=form.amount.data,
            category=dict(form.category_id.choices).get(form.category_id.data),
            description=form.description.data,
            author=current_user
        )
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been added!', 'success')
    
    return redirect(url_for('expenses.expense_list'))

@expenses.route("/expenses/<int:expense_id>/edit", methods=['POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if the expense belongs to the current user
    if expense.author != current_user:
        flash('You do not have permission to update this expense.', 'danger')
        return redirect(url_for('expenses.expense_list'))
    
    form = ExpenseForm()
    
    # Set category choices
    form.category_id.choices = [
        (1, 'Housing'),
        (2, 'Transportation'),
        (3, 'Food'),
        (4, 'Utilities'),
        (5, 'Insurance'),
        (6, 'Healthcare'),
        (7, 'Entertainment'),
        (8, 'Personal'),
        (9, 'Education'),
        (10, 'Savings'),
        (11, 'Other')
    ]
    
    if form.validate_on_submit():
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.category = dict(form.category_id.choices).get(form.category_id.data)
        expense.description = form.description.data
        db.session.commit()
        flash('Your expense has been updated!', 'success')
    
    return redirect(url_for('expenses.expense_list'))

@expenses.route("/expenses/<int:expense_id>/update", methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if the expense belongs to the current user
    if expense.author != current_user:
        flash('You do not have permission to update this expense.', 'danger')
        return redirect(url_for('expenses.expense_list'))
    
    form = ExpenseForm()
    
    # Set category choices
    form.category_id.choices = [
        (1, 'Housing'),
        (2, 'Transportation'),
        (3, 'Food'),
        (4, 'Utilities'),
        (5, 'Insurance'),
        (6, 'Healthcare'),
        (7, 'Entertainment'),
        (8, 'Personal'),
        (9, 'Education'),
        (10, 'Savings'),
        (11, 'Other')
    ]
    
    if form.validate_on_submit():
        expense.date = form.date.data
        expense.amount = form.amount.data
        expense.category = dict(form.category_id.choices).get(form.category_id.data)
        expense.description = form.description.data
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('expenses.expense_list'))
    
    elif request.method == 'GET':
        form.date.data = expense.date
        form.amount.data = expense.amount
        # Find the key for the category value
        for key, value in form.category_id.choices:
            if value == expense.category:
                form.category_id.data = key
                break
        form.description.data = expense.description
    
    return render_template('update_expense.html', title='Update Expense', form=form, expense=expense)

@expenses.route("/expenses/<int:expense_id>/delete", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    delete_form = DeleteExpenseForm()
    
    if not delete_form.validate_on_submit():
        flash('CSRF token is invalid. Please try again.', 'danger')
        return redirect(url_for('expenses.expense_list'))
    
    if expense.author != current_user:
        flash('You do not have permission to delete this expense.', 'danger')
        return redirect(url_for('expenses.expense_list'))
    
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('expenses.expense_list'))