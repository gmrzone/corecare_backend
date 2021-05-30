from api.models import EmployeeCategory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import BlogImagesSerializer, PostSerializer
from django.middleware.csrf import get_token

from .models import Post
# Create your views here.

@api_view(['GETs'])
def test(request):
    return Response({'main': "Afzal"})


class UploadBlogImages(CreateAPIView):
    serializer_class = BlogImagesSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=user)
            image_url = request.META['HTTP_HOST'] + instance.upload.url
            start = "https://" if request.is_secure() else "http://"
            data = {
            "url": start + image_url
            }
        else:
            data = {"error": {
            "message": "Serializer Error"
        }}
        get_token(request)
        return Response(data)

class CreateBlogPostView(CreateAPIView):
    serializer_class = PostSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def post(self, request, category,  *args, **kwargs):
        user = request.user
        if not category == "others":
            category = get_object_or_404(EmployeeCategory, slug=category)
        else:
            category= None
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category, author=user)
            data = {'status': 'success', 'message': "Post Created Sucessfully"}
            H_status = status.HTTP_200_OK
        else:
            data = {'status': 'error', 'message': "Error"}
            H_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=H_status)


class BlogPostListView(ListAPIView):
    serializer_class = PostSerializer
    http_method_names = ['get']
    permission_classes = [AllowAny]
    

    def get_queryset(self):
        query = Post.objects.all().select_related('author', 'category')
        return query

class BlogDetailView(APIView):
    
    http_method_names = ['get']
    permission_classes = [AllowAny]
    year = None
    month = None    
    day = None
    slug = None

    def dispatch(self, request,year, month, day, slug, *args, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.slug = slug
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        query = Post.objects.select_related('author', 'category').get(created__year=self.year, created__month=self.month, created__day=self.day, slug=self.slug)
        serializer = PostSerializer(query)
        return Response(serializer.data)


