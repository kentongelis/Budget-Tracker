from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
from dotenv import load_dotenv
import os
import openai


from app.main.forms import PostForm, PaycheckForm, UpdatePlanForm, CategoryForm, AIForm
from app.models import User, Post, Plan, Category

from app.extensions import app, bcrypt, db

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/budget', methods = ['GET', 'POST'])
@login_required
def budget():
    form1 = PaycheckForm()
    form2 = UpdatePlanForm()
    
    if form1.validate_on_submit():
        amount = form1.amount.data
        print(amount)
        current_user.paycheck = amount
        print(current_user.paycheck)
        print(current_user.plan)
        if current_user.plan == Plan.normal:
            print('yes')
            saved_money = int(amount) * 0.2
        elif current_user.plan == Plan.extreme:
            saved_money = int(amount) * 0.4
        elif current_user.plan == Plan.lenient:
            saved_money = int(amount) * 0.1
            
        current_user.savings = int(current_user.savings) + saved_money
            
        db.session.commit()
        flash('New paycheck has been submitted')
        return redirect(url_for('main.budget'))
    
    if form2.validate_on_submit():
        current_user.plan = form2.new_plan.data
        db.session.commit()
        flash('Your plan has been udpated')
        return redirect(url_for('main.budget'))
    
    paycheck = current_user.paycheck
    post_paycheck = f'${int(paycheck):,d}'
    savings = current_user.savings
    savings = f'${int(savings):,d}'
    
    print(paycheck)
    if str(paycheck) == '0.0':
        saved_money = 0
        needs=0
        self_money=0
        
    print(current_user.plan)

    if current_user.plan == Plan.normal:
        saved_money = int(paycheck) * 0.2
    elif current_user.plan == Plan.extreme:
        saved_money = int(paycheck) * 0.4
    elif current_user.plan == Plan.lenient:
        saved_money = int(paycheck) * 0.1
    saved_money = f'${int(saved_money):,d}'
    
    if current_user.plan == Plan.normal:
        needs = int(paycheck) * 0.5
    else:
        needs = int(paycheck) * 0.4
    needs = f'${int(needs):,d}'
    
    if current_user.plan == Plan.normal:
        self_money = int(paycheck) * 0.3
    elif current_user.plan == Plan.extreme:
        self_money = int(paycheck) * 0.2
    elif current_user.plan == Plan.lenient:
        self_money = int(paycheck) * 0.5
    self_money = f'${int(self_money):,d}'
    
    name = current_user.name.split(' ')
    
    print(paycheck)
    context = {
        'og' : str(paycheck),
        'paycheck' : post_paycheck,
        'saved' : saved_money,
        'needs' : needs,
        'self_money' : self_money,
        'name' : name[0],
        'form1' : form1,
        'form2' : form2,
        'savings': savings
    }
        
    return render_template('budget.html', **context)

@main.route('/category', methods=["GET", "POST"])
@login_required
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_cat = Category(
            title = form.title.data
        )
        
        db.session.add(new_cat)
        db.session.commit()
        flash('New category was created')
        return redirect(url_for('main.category'))
    return render_template('category.html', form = form)

@main.route('/tips')
@login_required
def tips():
    all_cats = Category.query.all()
    return render_template('tips.html', cats = all_cats)

@main.route('/tips/<cat_id>', methods=["GET", "POST"])
@login_required
def tip_page(cat_id):
    category = Category.query.get(cat_id)
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            data = form.data.data,
            date = date.today(),
            user_id = current_user.id,
            category_id = cat_id
        )
        
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.tip_page', cat_id = category.id))
    return render_template('cat_detail.html', category=category, form = form)

openai.api_key = os.getenv("OPENAIKEY")

@app.route("/ai", methods=['POST', 'GET']) 
def ai(): 
    form = AIForm()
    if request.method == "POST":
        question = request.form.get("question")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=question,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return render_template('ai.html', result=response.choices[0].text, form=form)
    return render_template("ai.html", form=form)
