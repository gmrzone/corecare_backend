from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('blog/post/<str:year>/<str:month>/<str:day>/<str:slug>/', views.BlogDetailView.as_view(), name="post_list"),
    path('blog/posts/', views.BlogPostListView.as_view(), name="post_list"),
    path('blog/post/images/', views.UploadBlogImages.as_view(), name="images"),
    path('blog/post/create/<str:category>/', views.CreateBlogPostView.as_view(), name="create_post"),
    path('blog/create_comment/<str:year>/<str:month>/<str:day>/<str:slug>/', views.CreatePostCommentView.as_view(), name="create_comment"),
    path('blog/create_comment/<str:year>/<str:month>/<str:day>/<str:slug>/<str:parent_id>/', views.CreatePostCommentView.as_view(), name="create_reply"),
    path('blog/post/<str:year>/<str:month>/<str:day>/<str:post_slug>/comments/', views.PostCommentListView.as_view(), name="post_comments"),
    path('blog/post/<str:parent_id>/replies/', views.CommentRepliesListView.as_view(), name="comment_replies")
]