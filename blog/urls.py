from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('blog/post/<str:year>/<str:month>/<str:day>/<str:slug>/', views.BlogDetailView.as_view(), name="post_list"),
    path('blog/posts/', views.BlogPostListView.as_view(), name="post_list"),
    path('blog/post/images/', views.UploadBlogImages.as_view(), name="images"),
    path('blog/post/create/<str:category>/', views.CreateBlogPostView.as_view(), name="create_post"),
]