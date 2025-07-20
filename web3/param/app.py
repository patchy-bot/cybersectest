from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField
from wtforms.validators import NumberRange
from models import User, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-secure-random-secret'

class TransferForm(FlaskForm):
    amount = IntegerField('Amount', validators=[NumberRange(min=1)])

@app.route('/login', methods=['GET','POST'])
def login():
    # Implement login logic
    pass

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = TransferForm()
    if form.validate_on_submit():
        user = User.query.get(session['user_id'])
        amt = form.amount.data
        if user.balance >= amt:
            user.balance -= amt
            db.session.commit()
            flash('Transfer successful')
        else:
            flash('Insufficient funds')
        return redirect(url_for('transfer'))
    return render_template('transfer.html', form=form)

if __name__ == '__main__':
    app.run()