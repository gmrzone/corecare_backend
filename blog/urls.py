from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('blog/posts/', views.BlogPostListView.as_view(), name="post_list"),
    path('blog/posts/images/', views.UploadBlogImages.as_view(), name="images"),
    path('blog/posts/create/<str:category>/', views.CreateBlogPostView.as_view(), name="create_post"),
]