from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects as Project, FundingShares as Share


class FundingProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'nftId', 'startTime', 'endTime', 'token', 'buyPrice', 'sellPrice', 'gasPrice']


class FundingProjectsSerializerAdmin(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UserFundingSharesSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = ['id', 'fundingProject', 'share']
