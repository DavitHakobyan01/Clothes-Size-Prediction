from flask import Blueprint, render_template, request
from prediction_functions import *
import datetime
from csv import writer

RUNNING_IP = '127.0.0.1'

views = Blueprint(__name__, 'views')


@views.route("/")
def home():

    the_time = datetime.datetime.now()
    the_time = the_time.replace(second=0, microsecond=0)
    ip_addr = request.remote_addr

    if ip_addr != RUNNING_IP:
        with open(r'.\website_data\visitors.csv', 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([the_time, ip_addr])

    return render_template("input.html", ad_image="main-banner.png", title="Input Form")


@views.route('/', methods=["POST"])
def button():
    if request.method == "POST":
        if request.form['submit_button'] == 'Submit':

            genders = {'on': 'Արական', 'off': 'Իգական'}

            age = float(request.form['age'])
            gender = genders[request.form['gender']]
            height = float(request.form['height'])
            weight = float(request.form['weight'])

            predictions = predict_clothes_sizes(gender, age, height, weight)

            shoe_sizes, shoe_sizes_prob = list(predictions['Shoe'].keys()), list(predictions['Shoe'].values())
            jeans_sizes, jeans_sizes_prob = list(predictions['Jeans'].keys()), list(predictions['Jeans'].values())
            shirt_sizes, shirt_sizes_prob = list(predictions['Shirt'].keys()), list(predictions['Shirt'].values())

            return render_template('prediction.html',
                                   shoe_sizes=shoe_sizes,
                                   shoe_sizes_prob=shoe_sizes_prob,
                                   jeans_sizes=jeans_sizes,
                                   jeans_sizes_prob=jeans_sizes_prob,
                                   shirt_sizes=shirt_sizes,
                                   shirt_sizes_prob=shirt_sizes_prob,
                                   ad_image="main-banner.png",
                                   title="Your Sizes")

