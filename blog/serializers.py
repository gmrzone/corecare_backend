from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import PostImage, Post
from api.serializers import TimeSince, EmployeeCategorySerializer
from account.serializers import UserSerializer
class BlogImagesSerializer(ModelSerializer):

    class Meta:
        model= PostImage
        fields = "__all__"




class PostSerializer(ModelSerializer):

    category = EmployeeCategorySerializer(many=False, read_only=True)
    created = TimeSince(read_only=True)
    author = UserSerializer(many=False, read_only=True)
    date_slug = SerializerMethodField(method_name="get_date_slug")
    class Meta:
        model = Post
        fields = ('author', 'category', 'title', 'slug', 'photo', 'body', 'created', "date_slug")

    def get_date_slug(self, obj):
        return {
            "year": obj.created.year,
            "month": obj.created.month,
            "day": obj.created.day
        }


