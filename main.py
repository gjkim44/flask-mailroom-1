import os
from login import app
from flask import render_template, request, redirect, url_for, flash
from form import RegistrationForm, LoginForm, CreateForm, SingleUserForm
from model import Donation, Donor
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required

app.secret_key = os.environ.get('SECRET_KEY').encode()
bcrypt = Bcrypt(app)


@app.route('/')
@app.route('/home')
def home():
    return redirect(url_for('all_donation'))


@app.route('/donations')
def all_donation():
    message = request.args.get('user')
    if message:
        donor = Donor.select().where(Donor.name == message).get()
        donations = Donation.select().where(Donation.donor == donor)
        name = donor.name.title()
    else:
        donations = Donation.select()
        name = "All"
    return render_template('donations.jinja2', title='show all', name=name, donations=donations)


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        flash(f'Thank you for your donation of {form.donation.data}.', 'success')
        user = Donor.select().where(Donor.username == current_user.username).get()
        Donation(value=form.donation.data, donor=user).save()
        return redirect(url_for('all_donation'))
    return render_template('create_new.jinja2', title='create', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_donation'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_donor = Donor(username=form.username.data, name=form.name.data, password=hashed_pass)
        new_donor.save()
        flash(f'Account created for {form.name.data}!, you can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.jinja2', title='register', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_donation'))
    form = LoginForm()
    if form.validate_on_submit():
        username = Donor.select().where(Donor.username == form.username.data)
        if username and bcrypt.check_password_hash(username.get().password, form.password.data):
            flash(f'You have been logged in', 'success')
            login_user(username.get(), remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('all_donation'))
        else:
            flash(f'Login Unsuccessful, Please check username and password', 'danger')
            return render_template('login.jinja2', title='login', form=form)
    return render_template('login.jinja2', title='login', form=form)


@app.route('/single_user', methods=['POST', 'GET'])
def single_user():
    form = SingleUserForm()
    if form.validate_on_submit():
        username = Donor.select().where(Donor.name == form.name.data)
        if username:
            return redirect(url_for('all_donation', user=form.name.data))
        else:
            flash(f'User does not exist!', 'danger')
    return render_template('single.jinja2', tittle='single_user', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('all_donation'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)