from django.apps import AppConfig


class FoodFinderAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "food_finder_app"

    def ready(self):
        import food_finder_app.signals