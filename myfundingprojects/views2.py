from mydatabase.models import  FundingProjects ,LikeLists
from django.contrib.auth.models import User
from myfundingprojects.serializers import FundingProjectsSerializer2,FundingProjectsSerializer3 ,UserLikeListsSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from myapi.response import *
from myapi.message import *
import datetime
import pytz

class FundingProjectsViewSet2(viewsets.ModelViewSet):

    def get_queryset(self):  # added string
        if self.action == 'list':
            return FundingProjects.objects.all()
        elif self.action == 'update':
            return FundingProjects.objects.filter(fundraiser=User.objects.get(id=self.request.user.id))
        elif self.action == 'retrieve':
            return FundingProjects.objects.all()
        elif self.action == 'create':
            return FundingProjects.objects.filter(fundraiser=User.objects.get(id=self.request.user.id))
        elif self.action == 'like' and self.request.method == 'POST':
            return LikeLists.objects.filter(userData=User.objects.get(id=self.request.user.id))
        elif self.action == 'like' and self.request.method == 'GET':
            return LikeLists.objects.filter(userData=User.objects.get(id=self.request.user.id))
        elif self.action == 'like' and self.request.method == 'DELETE':
            return LikeLists.objects.filter(userData=User.objects.get(id=self.request.user.id))


# return FundingProjects.objects.filter(fundingshares__userData_id=UserDatas.objects.get(id=self.request.user.id))
    def get_serializer_class(self):
        if self.action == 'create':
            return FundingProjectsSerializer2
        elif self.action == 'update':
            return FundingProjectsSerializer3
        elif self.action == 'retrieve':
            return FundingProjectsSerializer2
        elif self.action == 'like':
            return UserLikeListsSerializer
        return FundingProjectsSerializer2

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'like':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        return[]

        
    def create(self, request, *args, **kwargs):
        data = request.data

        try:
            new_funding = FundingProjects.objects.create(
                fundraiser=User.objects.get(id=self.request.user.id),
                nftId=data['nftId'],
                nftContractAddress=data['nftContractAddress'],
                nftName=data['nftName'],
                startTime=data['startTime'],
                endTime=data['endTime'],
                token=data['token'],
                buyPrice=data['buyPrice'],
                sellPrice=data['sellPrice'],
                gasPrice=data['gasPrice'])
            new_funding.save()
            serializer_new_funding = FundingProjectsSerializer2(new_funding)
            return Response(serializer_new_funding.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return err(Msg.Err.FundingProject.create)

    def update(self, request, pk=None):
        update_fundingf = FundingProjects.objects.filter(id=pk,fundraiser=User.objects.get(id=self.request.user.id))
        if not update_fundingf.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)


        data = request.data
        
        try:
            update_funding = FundingProjects.objects.get(id=pk)

            tzUTC = pytz.utc
            dt1 = update_funding.create_time
            dtnow = datetime.datetime.now(tzUTC)
            dt = dtnow-dt1
            dtdays=dt.days
            if dtdays >= 2:
                return err(Msg.Err.FundingProject.create)

            if 'endTime' in data:
                update_funding.endTime = data['endTime']
            if 'buyPrice' in data:
                update_funding.buyPrice = data['buyPrice']
            if 'sellPrice' in data:
                update_funding.sellPrice = data['sellPrice']
            
            update_funding.save()
            serializer_new_funding = FundingProjectsSerializer2(update_funding)
            return Response(serializer_new_funding.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return err(Msg.Err.FundingProject.create)

    def destroy(self, request, pk=None):
        update_fundingf = FundingProjects.objects.filter(id=pk,fundraiser=User.objects.get(id=self.request.user.id))
        if not update_fundingf.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)


        update_funding = FundingProjects.objects.get(id=pk)

        tzUTC = pytz.utc
        dt1 = update_funding.create_time
        dtnow = datetime.datetime.now(tzUTC)
        dt = dtnow-dt1
        dtdays=dt.days
        if dtdays >= 2:
            return err(Msg.Err.FundingProject.create)
        update_funding.enabled=False
        update_funding.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
                        

    def partial_update(self, request):
        pass



    @action(detail=True, methods=['POST', 'DELETE','GET'])
    def like(self, request, pk=None):
        if request.method == 'POST':
            try:
                new_like=LikeLists.objects.create(userData=User.objects.get(id=self.request.user.id),fundingProject=FundingProjects.objects.get(id=pk))
                new_like.save()
                return Response({'like': 'true'},status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return err(Msg.Err.FundingProject.create)
        elif request.method == 'DELETE':
            try:
                new_like=LikeLists.objects.get(userData=User.objects.get(id=self.request.user.id),fundingProject=FundingProjects.objects.get(id=pk))
                new_like.delete()
                return Response({'like': 'false'},status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return err(Msg.Err.FundingProject.create)
        elif request.method == 'GET': 
            try:
                new_like=LikeLists.objects.get(userData=User.objects.get(id=self.request.user.id),fundingProject=FundingProjects.objects.get(id=pk))
                new_like_serilizars = UserLikeListsSerializer(new_like)
                return Response(new_like_serilizars,status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return err(Msg.Err.FundingProject.create)

                       


