from flask import render_template, redirect, url_for, flash, request
from app.forms import RegisterForm, LoginForm, AddPlantForm, AddCategoryForm, UpdateProfileForm
from app.models import User, Plant, PlantCategory
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Blueprint
from datetime import timedelta
import os

# Create a Blueprint for routing
routes = Blueprint('routes', __name__)

# Home page
@routes.route('/')
def index():
    user_plants = Plant.query.all()
    return render_template('index.html', user_plants=user_plants)

# Search for another user by username
@routes.route('/search-user')
@login_required
def search_user():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for('routes.index'))
    return redirect(url_for('routes.view_user', username=user.username))


# User registration
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

# User login
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

# User logout
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

# Add a new plant
@routes.route('/add-plant', methods=['GET', 'POST'])
@login_required
def add_plant():
    form = AddPlantForm()
    form.latin_name.choices = [(c.latin_name, c.name) for c in PlantCategory.query.all()]

    if form.validate_on_submit():
        category = PlantCategory.query.get(form.latin_name.data)
        next_watering = form.last_watering.data + timedelta(days=category.watering_interval)

        # Handle uploaded photo
        photo = form.photo.data
        photo_filename = None
        if photo:
            filename = secure_filename(photo.filename)
            upload_path = os.path.join('app/static/uploads', filename)
            photo.save(upload_path)
            photo_filename = filename

        new_plant = Plant(
            plant_name=form.nickname.data,
            last_watering=form.last_watering.data,
            next_watering=next_watering,
            photo_path=photo_filename,
            username=current_user.username,
            latin_name=form.latin_name.data,
            description=form.description.data
        )
        db.session.add(new_plant)
        db.session.commit()
        flash('Plant added!', 'success')
        return redirect(url_for('routes.index'))

    return render_template('add_plant.html', form=form)

# Add a new plant category
@routes.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm()

    if form.validate_on_submit():
        # Check if latin_name already exists in DB
        existing = PlantCategory.query.filter_by(latin_name=form.latin_name.data).first()
        if existing:
            flash("❌ Error: Plant with this Latin name already exists.", "danger")
            return render_template('add_category.html', form=form)

        # Create and add new category
        category = PlantCategory(
            name=form.name.data,
            latin_name=form.latin_name.data,
            watering_interval=int(form.watering_interval.data),
            info=form.info.data
        )
        db.session.add(category)
        db.session.commit()
        flash('✅ Category added successfully!', 'success')
        return redirect(url_for('routes.index'))

    return render_template('add_category.html', form=form)


# User profile: shows logged-in user's plants
@routes.route('/profile')
@login_required
def profile():
    plants = Plant.query.filter_by(username=current_user.username).all()
    return render_template('profile.html', plants=plants)

# View another user's profile (read-only)
@routes.route('/user/<username>')
@login_required
def view_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('public_profile.html', user=user, plants=user.plants)


# Edit profile description
@routes.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm(description=current_user.description)
    if form.validate_on_submit():
        current_user.description = form.description.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('routes.profile'))
    return render_template('edit_profile.html', form=form)

# Delete a plant
@routes.route('/delete-plant/<int:plant_id>', methods=['POST'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    if plant.username != current_user.username:
        flash("You don't have permission to delete this plant.", "danger")
        return redirect(url_for('routes.profile'))

    db.session.delete(plant)
    db.session.commit()
    flash('Plant deleted.', 'info')
    return redirect(url_for('routes.profile'))
