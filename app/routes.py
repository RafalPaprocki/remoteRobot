from flask import render_template, flash, redirect, url_for, request
from app import app


@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route('/robot-config')
def robot_config():
    return render_template('robotConfig.html')


@app.route('/robot-routes')
def robot_routes():
    return render_template('robotRoutes.html')


@app.route('/data-preview')
def data_preview():
    return render_template('dataPreview.html')

