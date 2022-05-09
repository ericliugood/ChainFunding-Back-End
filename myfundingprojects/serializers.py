from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects,LikeLists,FundingShares


class FundingProjectsSerializer(ModelSerializer):
    
    class Meta:
        model=FundingProjects
        fields = ['id','nftId','startTime','endTime','token','buyPrice','sellPrice','gasPrice']


class UserLikeListsSerializer(ModelSerializer):
    
    class Meta:
        model=LikeLists
        fields = ['id','fundingProject']

class UserFundingSharesSerializer(ModelSerializer):
    
    class Meta:
        model=FundingShares
        fields = ['id','fundingProject','share']