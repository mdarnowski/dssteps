
from models.alchemy import Step, db
from services.dataset_service import DatasetService

dss = DatasetService()


class StepsList:
    def __init__(self, dataset_id):
        self.steps = None
        self.dataset_id = dataset_id
        self.load_from_db()

    def load_from_db(self):
        steps = Step.query.filter_by(dataset_id=self.dataset_id).order_by(Step.id).all()
        self.steps = {step.id: step for step in steps}

    def append(self, step, after_step_id=None):
        step.dataset_id = self.dataset_id
        if after_step_id:
            previous_step = self.steps[after_step_id]
            step.prev_step_id = previous_step.id
            step.next_step_id = previous_step.next_step_id
            if previous_step.next_step_id:
                next_step = self.steps[previous_step.next_step_id]
                next_step.prev_step_id = step.id
            previous_step.next_step_id = step.id
        else:
            if self.steps:
                last_step = max(self.steps.values(), key=lambda step: step.id)
                last_step.next_step_id = step.id
                step.prev_step_id = last_step.id

        db.session.add(step)
        db.session.commit()
        self.steps[step.id] = step
