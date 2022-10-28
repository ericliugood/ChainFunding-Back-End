from rest_framework.serializers import ModelSerializer
from mydatabase.models import  FundingShares as Share 

class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['fundingProject', 'share']