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

    return render_template("index.html")


@views.route('/', methods=["GET", "POST"])
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
                                   shoe_size_1=shoe_sizes[0],
                                   shoe_size_2=shoe_sizes[1],
                                   shoe_size_3=shoe_sizes[2],
                                   shoe_size_prob_1=shoe_sizes_prob[0],
                                   shoe_size_prob_2=shoe_sizes_prob[1],
                                   shoe_size_prob_3=shoe_sizes_prob[2],
                                   jeans_size_1=jeans_sizes[0],
                                   jeans_size_2=jeans_sizes[1],
                                   jeans_size_3=jeans_sizes[2],
                                   jeans_size_prob_1=jeans_sizes_prob[0],
                                   jeans_size_prob_2=jeans_sizes_prob[1],
                                   jeans_size_prob_3=jeans_sizes_prob[2],
                                   shirt_size_1=shirt_sizes[0],
                                   shirt_size_2=shirt_sizes[1],
                                   shirt_size_3=shirt_sizes[2],
                                   shirt_size_prob_1=shirt_sizes_prob[0],
                                   shirt_size_prob_2=shirt_sizes_prob[1],
                                   shirt_size_prob_3=shirt_sizes_prob[2])

