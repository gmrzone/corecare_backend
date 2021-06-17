from rest_framework.serializers import ModelSerializer
from account.models import CustomUser
from api.serializers import TimeSince

class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)


    class Meta:

        model = CustomUser
        fields = ('id','number', 'username', 'email', 'last_login', 'first_name', 'last_name', 'date_joined')