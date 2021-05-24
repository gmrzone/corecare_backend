from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('blog/posts/', views.test, name="post_list"),
]