from rest_framework.serializers import ModelSerializer
from .models import PostImage


class BlogImagesSerializer(ModelSerializer):

    class Meta:
        model= PostImage
        fields = "__all__"
