from rest_framework.serializers import ModelSerializer
from account.models import CustomUser
from api.serializers import TimeSince

class UserSerializerAdministrator(ModelSerializer):

    last_login = TimeSince(read_only=True)
    date_joined = TimeSince(read_only=True)


    class Meta:

        model = CustomUser
        fields = ('id','number', 'username', 'email', 'last_login', 'first_name', 'last_name',"address_1", "address_2", "city", "state", "pincode", "verified",'is_employee', 'is_active', 'is_verified_employee', 'date_joined')