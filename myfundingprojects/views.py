from mydatabase.models import  FundingProjects ,LikeLists,FundingShares,Wallet
from django.contrib.auth.models import User
from myfundingprojects.serializers import FundingProjectsSerializer2,FundingProjectsSerializer3 ,FundingProjectsSerializer4,UserLikeListsSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from myapi.response import *
from myapi.message import *
import datetime
import pytz
from mywallet.walletfunction import wfunction


class FundingProjectsViewSet2(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return FundingProjectsSerializer2
        elif self.action == 'update':
            return FundingProjectsSerializer3
        elif self.action == 'retrieve':
            return FundingProjectsSerializer4
        elif self.action == 'like':
            return UserLikeListsSerializer
        return FundingProjectsSerializer2

    def get_queryset(self):  # added string
        if self.action == 'list':
            return FundingProjects.objects.filter(enabled=True)
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


    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'like':
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
                gasPrice=0.001,
                stopPrice=data['stopPrice'],
                lowest_share=data['lowest_share'],
                status=1)
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
            if 'lowest_share' in data:
                update_funding.lowest_share = data['lowest_share']
            if 'stopPrice' in data:
                update_funding.stopPrice = data['stopPrice']
            
            
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


        update_funding = update_fundingf[0]

        tzUTC = pytz.utc
        dt1 = update_funding.create_time
        dtnow = datetime.datetime.now(tzUTC)
        dt = dtnow-dt1
        dtdays=dt.days
        if dtdays >= 2:
            return err(Msg.Err.FundingProject.create)
        update_funding.enabled=False
        
        # userFundingShare=FundingShares.objects.filter(fundingProject=update_funding,enabled=True,hands=1)
        # userData = User.objects.filter(userFunding=update_funding)
        # fsplus = userFundingShare.filter(userData=userData)
        # fshare = FundingShares.objects.filter(userData__in=userData,hands=1,enabled=True,fundingProject=update_funding)

        fshare = FundingShares.objects.filter(hands=1,enabled=True,fundingProject=update_funding)

        for e in fshare:
            wfunction().walletChange(e.userData.pk,update_funding.token,e.share)


        # Wallet.objects.filter(token=update_funding.token,userData=userData).update(amount=F('amount')+F('fshare__share'))
        

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

                       


