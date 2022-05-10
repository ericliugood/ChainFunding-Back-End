from mydatabase.models import UserDatas,FundingProjects,LikeLists
from mylikelists.serializers import UserLikeListsSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated



class UserLikeListsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]

    serializer_class = UserLikeListsSerializer
    queryset = LikeLists.objects.all()

    def get_queryset(self):                                            # added string
        return super().get_queryset().filter(userData=UserDatas.objects.get(id=self.request.user.id))
    
    def create(self, request, *args, **kwargs):
        userLikeListsdata=request.data
        
        try:
                new_userLikeLists = LikeLists.objects.create(
                userData=UserDatas.objects.get(id=self.request.user.id),
                fundingProject=FundingProjects.objects.get(id=userLikeListsdata['fundingProject']) )
                new_userLikeLists.save()
                return Response(status=status.HTTP_201_CREATED) 
        except:
                return Response(status=status.HTTP_400_BAD_REQUEST) 