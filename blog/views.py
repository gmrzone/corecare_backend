from typing import Dict

from django.db.models import Case, When
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import EmployeeCategory
from cart.utils import r

from .models import Comment, Post
from .pagination import PostListPagination
from .serializers import (BlogImagesSerializer, CommentSerializer,
                          PostSerializer)


class UploadBlogImages(CreateAPIView):
    serializer_class = BlogImagesSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=user)
            image_url = request.META["HTTP_HOST"] + instance.upload.url
            start = "https://" if request.is_secure() else "http://"
            data = {"url": start + image_url}
        else:
            data = {"error": {"message": "Serializer Error"}}
        get_token(request)
        return Response(data)


class CreateBlogPostView(CreateAPIView):
    serializer_class = PostSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, category, *args, **kwargs):
        user = request.user
        if not category == "others":
            category = get_object_or_404(EmployeeCategory, slug=category)
        else:
            category = None
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category, author=user)
            data = {"status": "success", "message": "Post Created Sucessfully"}
            H_status = status.HTTP_200_OK
        else:
            data = {"status": "error", "message": "Error"}
            H_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=H_status)


class BlogPostListView(ListAPIView):
    serializer_class = PostSerializer
    http_method_names = ["get"]
    permission_classes = [AllowAny]
    category = None
    pagination_class = PostListPagination
    pagination_class.page_size = 9

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get("category")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.category:
            query = Post.objects.filter(category__slug=self.category).select_related(
                "author", "category"
            )
        else:
            query = Post.objects.all().select_related("author", "category")
        return query

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")

        if page:
            return super().get(request, *args, **kwargs)
        else:
            query = self.get_queryset()
            serializer = self.serializer_class(query, many=True)
            return Response(serializer.data)


# class BlogPostListView(APIView):
#     http_method_names = ['get']
#     permission_classes = [AllowAny]

#     def get(self, request):


class BlogDetailView(APIView):

    http_method_names = ["get"]
    permission_classes = [AllowAny]
    year = None
    month = None
    day = None
    slug = None

    def dispatch(self, request, year, month, day, slug, *args, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        query = Post.objects.select_related("author", "category").get(
            created__year=self.year,
            created__month=self.month,
            created__day=self.day,
            slug=self.slug,
        )
        # r.zincrby("top_posts", 1, query.id)
        serializer = PostSerializer(query)
        return Response(serializer.data)


class GetTopPost(APIView):
    http_method_names = ["get"]
    permission_classes = [AllowAny]
    count = None

    def dispatch(self, request, count, *args, **kwargs):
        self.count = count
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        top_posts_r = r.zrange("top_posts", 0, -1, desc=True)
        if top_posts_r and len(top_posts_r) > 3:
            top_posts_r = (
                top_posts_r[0 : self.count]
                if self.count < len(top_posts_r)
                else top_posts_r
            )
            preserve_ids = Case(
                *[When(id=id, then=index) for index, id in enumerate(top_posts_r)]
            )
            posts = (
                Post.objects.filter(id__in=top_posts_r)
                .select_related("author", "category")
                .order_by(preserve_ids)
            )
        else:
            posts = Post.objects.all().select_related("author", "category")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CreatePostCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def post(self, request, year, month, day, slug, parent_id=None, *args, **kwargs):
        parent = None if not parent_id else get_object_or_404(Comment, pk=parent_id)
        user = request.user if request.user.is_authenticated else None
        post = get_object_or_404(
            Post, created__year=year, created__month=month, created__day=day, slug=slug
        )
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            instance = serializer.save(user=user, post=post, parent=parent)
            serializer_data = self.serializer_class(instance).data
            response = Response(
                {
                    "status": "ok",
                    "message": "Comment Created Sucessfully.",
                    "data": serializer_data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            response = Response(
                {
                    "status": "error",
                    "message": "Please Make sure to fill all required fields",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return response


class PostCommentListView(ListAPIView):
    serializer_class = CommentSerializer
    http_method_names = ["get"]
    permission_classes = [AllowAny]
    year = None
    month = None
    day = None
    post_slug = None

    def dispatch(self, request, year, month, day, post_slug, *args, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.post_slug = post_slug
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = (
            Comment.objects.filter(
                post__created__year=self.year,
                post__created__month=self.month,
                post__created__day=self.day,
                post__slug=self.post_slug,
                parent=None,
            )
            .select_related("user")
            .prefetch_related("replies")
        )
        return query


class CommentRepliesListView(ListAPIView):
    serializer_class = CommentSerializer
    http_method_names = ["get"]
    permission_classes = [AllowAny]
    parent_id = None

    def dispatch(self, request, parent_id, *args, **kwargs):
        self.parent_id = parent_id
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = (
            Comment.objects.filter(parent__id=self.parent_id)
            .select_related("user")
            .prefetch_related("replies")
        )
        return query


class GetPostViews(APIView):
    http_method_names = ["get"]

    def get(self, request):
        post_views = r.zrange(
            "top_posts", 0, -1, desc=True, withscores=True, score_cast_func=int
        )
        if post_views:
            post_views = {
                key.decode() if isinstance(key, bytes) else key: value
                for key, value in post_views
            }
        else:
            post_views = {}
        return Response(post_views)


class IncreasePostViews(APIView):
    http_method_names = ["get"]
    post_id = None

    def dispatch(self, request, post_id, *args, **kwargs):
        self.post_id = post_id
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        r.zincrby("top_posts", 1, self.post_id)
        return Response({"status": "ok"})
