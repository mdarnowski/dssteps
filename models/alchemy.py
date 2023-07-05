import plotly
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, LargeBinary, Text, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objects as go

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True)
    datasets = db.relationship("Dataset", back_populates="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = db.relationship("User", back_populates="datasets")
    url = Column(String(500), nullable=False)
    data = Column(LargeBinary, nullable=False)

    steps = db.relationship("Step", back_populates="dataset")


class Step(db.Model):
    __tablename__ = 'step'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    dataset_id = Column(Integer, ForeignKey('dataset.id'))
    dataset = db.relationship("Dataset", back_populates="steps")

    next_step_id = Column(Integer, ForeignKey('step.id'))
    prev_step_id = Column(Integer, ForeignKey('step.id'))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'step'
    }

    def plot(self, df):
        raise NotImplementedError


class PreviewStep(Step):
    __mapper_args__ = {
        'polymorphic_identity': 'Preview',
    }

    def plot(self, df):
        if df.empty:
            raise ValueError("The dataframe is empty. Cannot display table.")

        # Create a Plotly Table
        table = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df[col].head(25).values for col in df.columns],
                       fill_color='lavender',
                       align='left'))
        ])

        table_html = plotly.offline.plot(table, output_type='div')

        return table_html
