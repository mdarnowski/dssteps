from models.alchemy import Step


class StepFactory:
    @staticmethod
    def create_step(step_type):
        for subclass in Step.__subclasses__():
            if subclass.__mapper_args__['polymorphic_identity'] == step_type:
                step = subclass()
                return step
        raise ValueError(f"Invalid step type: {step_type}.")
