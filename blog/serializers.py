from rest_framework.serializers import ModelSerializer, SerializerMethodField

from account.serializers import UserSerializer
from api.serializers import EmployeeCategorySerializer, ReviewUser, TimeSince

from .models import Comment, Post, PostImage


class BlogImagesSerializer(ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class PostSerializer(ModelSerializer):

    category = EmployeeCategorySerializer(many=False, read_only=True)
    created = TimeSince(read_only=True)
    author = UserSerializer(many=False, read_only=True)
    date_slug = SerializerMethodField(method_name="get_date_slug")
    photo = SerializerMethodField(method_name="get_blog_photo")

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "category",
            "title",
            "slug",
            "photo",
            "body",
            "created",
            "date_slug",
        )

    def get_date_slug(self, obj):
        created_date = obj.created
        return {
            "year": str(created_date.year),
            "month": str(created_date.month),
            "day": str(created_date.day),
        }

    def get_blog_photo(self, obj):
        return obj.photo.url


# class ReplySerializer(ModelSerializer):
#     created = TimeSince(read_only=True)
#     user = ReviewUser(many=False, read_only=True)

#     class Meta:
#         model = Comment
#         fields = ('id', 'user', 'name', 'email', "comment", 'created')


class CommentSerializer(ModelSerializer):
    created = TimeSince(read_only=True)
    user = ReviewUser(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "parent",
            "user",
            "name",
            "email",
            "replies",
            "comment",
            "created",
        )
