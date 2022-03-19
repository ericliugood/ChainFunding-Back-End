from rest_framework.serializers import ModelSerializer
from database.models import UserDatas

class AccountSerializer(ModelSerializer):
    class Meta:
        model=UserDatas
        fields = '__all__'