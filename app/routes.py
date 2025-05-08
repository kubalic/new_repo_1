from flask import render_template, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm, AddPlantForm, AddCategoryForm
from app.models import User, Plant, PlantCategory
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from datetime import timedelta

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or email already in use.', 'danger')
            return render_template('register.html', form=form)

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Account created!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('register.html', form=form)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

@routes.route('/add-plant', methods=['GET', 'POST'])
@login_required
def add_plant():
    form = AddPlantForm()
    form.category_id.choices = [(c.id, c.name) for c in PlantCategory.query.all()]
    if form.validate_on_submit():
        category = PlantCategory.query.get(form.category_id.data)
        next_watering = form.last_watering.data + timedelta(days=category.watering_interval)
        new_plant = Plant(
            nickname=form.nickname.data,
            last_watering=form.last_watering.data,
            next_watering=next_watering,
            user_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(new_plant)
        db.session.commit()
        flash('Plant added!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('add_plant.html', form=form)

@routes.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = PlantCategory(
            name=form.name.data,
            latin_name=form.latin_name.data,
            watering_interval=int(form.watering_interval.data)
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('add_category.html', form=form)
