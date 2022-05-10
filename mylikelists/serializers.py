from rest_framework.serializers import ModelSerializer
from mydatabase.models import LikeLists


class UserLikeListsSerializer(ModelSerializer):
    
    class Meta:
        model=LikeLists
        fields = ['id','fundingProject']