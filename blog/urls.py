from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path(
        "post/<str:year>/<str:month>/<str:day>/<str:slug>/",
        views.BlogDetailView.as_view(),
        name="post_list",
    ),
    path("posts/", views.BlogPostListView.as_view(), name="post_list"),
    path("posts/top/<int:count>/", views.GetTopPost.as_view(), name="top_posts"),
    path("post/images/", views.UploadBlogImages.as_view(), name="images"),
    path(
        "post/create/<str:category>/",
        views.CreateBlogPostView.as_view(),
        name="create_post",
    ),
    path(
        "create_comment/<str:year>/<str:month>/<str:day>/<str:slug>/",
        views.CreatePostCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "create_comment/<str:year>/<str:month>/<str:day>/<str:slug>/<str:parent_id>/",
        views.CreatePostCommentView.as_view(),
        name="create_reply",
    ),
    path(
        "post/<str:year>/<str:month>/<str:day>/<str:post_slug>/comments/",
        views.PostCommentListView.as_view(),
        name="post_comments",
    ),
    path(
        "post/<str:parent_id>/replies/",
        views.CommentRepliesListView.as_view(),
        name="comment_replies",
    ),
    path("posts/views/", views.GetPostViews.as_view(), name="post_views"),
    path(
        "post/views/update/<int:post_id>/",
        views.IncreasePostViews.as_view(),
        name="update_views",
    ),
]
