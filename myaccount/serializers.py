from rest_framework.serializers import ModelSerializer
from mydatabase.models import UserDatas


class UserSeeSerializer(ModelSerializer):
    class Meta:
        model=UserDatas
        fields = ['usernameAccount', 'emailAccount', 'evaluation']