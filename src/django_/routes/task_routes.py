from django.urls import path
from view.task_views import (
    TaskViews as T,
)


urlpatterns = [
    path("", T.NoParametersView.as_view()),
    path("<str:id>/", T.WithParametersView.as_view()),
]
