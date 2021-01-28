from django.apps import AppConfig


class LearningMgtConfig(AppConfig):
    name = 'learning_mgt'

    def ready(self):
        import learning_mgt.signals