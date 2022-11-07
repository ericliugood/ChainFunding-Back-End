from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects as Project, FundingShares as Share ,SharesSold ,LikeLists


class FundingProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice']

class FundingProjectsSerializer2(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice']


class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['fundingProject', 'share']

class SoldPricesSerializer(ModelSerializer):
    class Meta:
        model = SharesSold
        fields = ['fundingShares', 'price']

class UserLikeListsSerializer(ModelSerializer):
    
    class Meta:
        model=LikeLists
        fields = ['fundingProject']
