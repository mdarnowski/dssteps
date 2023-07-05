
from models.alchemy import Step, db
from services.dataset_service import DatasetService

dss = DatasetService()


class StepsList:
    def __init__(self, dataset_id):
        self.tail = None
        self.head = None
        self.dataset_id = dataset_id
        self.load_from_db()

    def load_from_db(self):
        steps = Step.query.filter_by(dataset_id=self.dataset_id).order_by(Step.id).all()
        self.head = steps[0] if steps else None
        self.tail = steps[-1] if steps else None

    def append(self, step):
        step.dataset_id = self.dataset_id

        if self.tail:
            step.prev_step_id = self.tail.id
            self.tail.next_step_id = step.id
            db.session.commit()

        db.session.add(step)
        db.session.commit()

        self.tail = step
