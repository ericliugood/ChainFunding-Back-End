from mydatabase.models import UserDatas,FundingProjects
from myfundingprojects.serializers import FundingProjectsSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated

class FundingProjectsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    serializer_class = FundingProjectsSerializer
    queryset = FundingProjects.objects.all()

    def get_queryset(self):                                            # added string
        return super().get_queryset().filter(fundraiser=UserDatas.objects.get(id=self.request.user.id))
    def create(self, request, *args, **kwargs):
        fundingProjectsdata=request.data
        
        try:
                new_fundingProjects = FundingProjects.objects.create(
                fundraiser=UserDatas.objects.get(id=self.request.user.id),
                nftId=fundingProjectsdata['nftId'],
                startTime=fundingProjectsdata['startTime'],
                endTime=fundingProjectsdata['endTime'],
                token=fundingProjectsdata['token'],
                buyPrice=fundingProjectsdata['buyPrice'] ,
                sellPrice=fundingProjectsdata['sellPrice'] ,
                gasPrice=fundingProjectsdata['gasPrice'] )
                new_fundingProjects.save()
                return Response(status=status.HTTP_201_CREATED) 
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 

