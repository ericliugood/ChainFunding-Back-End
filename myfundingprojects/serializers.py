from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects as Project, FundingShares as Share


class FundingProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['nftId', 'nftContractAddress', 'nftName', 'startTime', 'endTime', 'token', 'buyPrice',
                  'sellPrice', 'gasPrice']


class FundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['fundingProject', 'share']

# class FundingProjectsSerializerAdmin(ModelSerializer):
#     class Meta:
#         model = Project
#         fields = '__all__'
