import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/donation-creation', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            input_donor = Donor.select().where(
                Donor.name == request.form['name']).get()
            donation = Donation(
                donor=input_donor.id, value=request.form['amount'])
            donation.save()
        except Donor.DoesNotExist:
            # No Donor matches request name
            return render_template('donation-creation.jinja2', error='Donor not found, please check spelling')

        return redirect(url_for('all'))

    return render_template('donation-creation.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
