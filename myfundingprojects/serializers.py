from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects as Project, FundingShares as Share ,SoldPrices


class FundingProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice']


class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['fundingProject', 'share']

class SoldPricesSerializer(ModelSerializer):
    class Meta:
        model = SoldPrices
        fields = ['fundingShares', 'price']
