from rest_framework.serializers import ModelSerializer
from mydatabase.models import Notice


class NoticeSerializer(ModelSerializer):
    
    class Meta:
        model=Notice
        fields = ['id','notice','read']
