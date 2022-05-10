from rest_framework.serializers import ModelSerializer
from mydatabase.models import FundingProjects,FundingShares


class FundingProjectsSerializer(ModelSerializer):
    
    class Meta:
        model=FundingProjects
        fields = ['id','nftId','startTime','endTime','token','buyPrice','sellPrice','gasPrice']




class UserFundingSharesSerializer(ModelSerializer):
    
    class Meta:
        model=FundingShares
        fields = ['id','fundingProject','share']