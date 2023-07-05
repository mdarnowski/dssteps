from flask import request, session, redirect, url_for, render_template
import logging

from controllers.dataset_controller import add_dataset
from factory.app_factory import create_app

logging.basicConfig(filename='app.log', level=logging.DEBUG)
app = create_app()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['url'] = request.form['url']
        return add_dataset()
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
