from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from .serializers import BlogImagesSerializer
from django.middleware.csrf import get_token
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