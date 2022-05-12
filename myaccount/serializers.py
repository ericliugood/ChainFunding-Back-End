from rest_framework.serializers import ModelSerializer
from mydatabase.models import UserDatas


class AccountSerializer(ModelSerializer):
    class Meta:
        model=UserDatas
        fields = ['usernameAccount', 'emailAccount']
