import io
import logging
import uuid

import pandas as pd
from flask import Blueprint, redirect, url_for, render_template, session, request
from markupsafe import Markup
from factory.step_factory import StepFactory
from models.alchemy import Step, db
from services.login import login
from models.steps_list import StepsList
from services.dataset_service import DatasetService

dataset_controller_blueprint = Blueprint('dataset_controller', __name__)
dataset_service = DatasetService()


@dataset_controller_blueprint.route('/add_steps/<int:dataset_id>', methods=['GET', 'POST'])
def add_steps(dataset_id):
    steps_list = StepsList(dataset_id)
    df = dataset_service.get_dataset_dataframe(dataset_id)
    if request.method == 'POST':
        step_type = request.form['type']
        step = StepFactory.create_step(step_type)

        # Save the step to the database so it gets an ID.
        db.session.add(step)
        db.session.commit()

        steps_list.append(step)

        # Update the code below
        return redirect(url_for('dataset_controller.add_steps', dataset_id=dataset_id, _anchor=f'plot_{step.id}'))

    step_types = get_step_types()
    steps = Step.query.filter_by(dataset_id=dataset_id).all()  # Fetch all steps associated with the dataset
    return render_template('add_steps.html', dataset_id=dataset_id, step_types=step_types, steps=steps)  # Pass the steps to the template


@dataset_controller_blueprint.route('/get_plot/<int:step_id>', methods=['GET'])
def get_plot(step_id):
    step = Step.query.get(step_id)

    df = dataset_service.get_dataset_dataframe(step.dataset_id)
    logging.debug(f'Loaded DataFrame with shape {df.shape} for step {step_id}')

    plot_html = step.plot(df)
    logging.debug(f'Generated plot HTML with length {len(plot_html)} for step {step_id}')

    return Markup(plot_html)


@dataset_controller_blueprint.route('/dataset', methods=['POST'])
def add_dataset():
    url = session.get('url', None)
    if url is None:
        return redirect(url_for('home'))
    # create a new user for each session
    user_id = str(uuid.uuid4())
    login(user_id)
    ds = dataset_service.add_dataset(user_id, url)
    return redirect(url_for('dataset_controller.add_steps', dataset_id=ds.id))


def get_step_types():
    return [subclass.__mapper_args__['polymorphic_identity'] for subclass in Step.__subclasses__()]
