from rest_framework.serializers import ModelSerializer
from mydatabase.models import  FundingShares as Share ,SharesSold

class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['id','fundingProject', 'share']

class FundingSharesSoldSerializer(ModelSerializer):
    class Meta:
        model = SharesSold
        fields = ['id','fundingProject', 'share','price','token']