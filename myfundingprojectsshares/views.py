from myfundingprojectsshares.serializers import FundingSharesSerializer,FundingSharesSoldSerializer,FundingSharesSoldSerializer2,FundingSharesSoldedSerializer
from rest_framework import viewsets
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from mywallet.walletfunction import wfunction
from mydatabase.models import FundingShares,FundingProjects,SharesSold,SharesSolded,TransferLogsUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from myapi.message import *
import datetime
import pytz

class FundingSharesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = FundingSharesSerializer

    def get_queryset(self):  # added string
        return FundingShares.objects.filter(userData=User.objects.get(id=self.request.user.id),enabled=True)

    def create(self, request, *args, **kwargs):
        sharesdata = request.data
        try:
            old_share=0
            fundingProjectId = sharesdata['fundingProject']
            share = sharesdata['share']
            
            fundingProject= FundingProjects.objects.get(id=fundingProjectId)
            if not (fundingProject.status == 1 and fundingProject.enabled == True):
                return Response(Msg.Err.Shares.shares_not_enabled,status=status.HTTP_406_NOT_ACCEPTABLE)
            shares_sold_sum = FundingShares.objects.filter(hands=1,enabled=True,fundingProject=fundingProject).aggregate(share=Sum('share'))['share'] or 0
            shares_sold_can_buy = fundingProject.buyPrice - shares_sold_sum
            if (((share < fundingProject.buyPrice * fundingProject.lowest_share) or
            ((share < fundingProject.buyPrice * fundingProject.lowest_share) and 
              (share != shares_sold_can_buy))) or (share > shares_sold_can_buy)):
                return Response(Msg.Err.Shares.create_share_not_filter,status=status.HTTP_406_NOT_ACCEPTABLE)

            
            if not wfunction().walletCanUse(request.user.id,fundingProject.token,share):
                return Response(Msg.Err.Shares.create_money_not_enough,status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if FundingShares.objects.filter(userData=User.objects.get(id=request.user.id),
                                                    hands=1,
                                                    fundingProject= fundingProject,
                                                    enabled=True).exists():

                old_shares = FundingShares.objects.get(userData=User.objects.get(id=request.user.id),
                                                    fundingProject= fundingProject,
                                                    enabled=True)
                old_share=old_shares.share
                old_shares.enabled = False

                old_shares.save()
                


        

            new_shares = FundingShares.objects.create(userData=User.objects.get(id=request.user.id),
                                                    hands=1,
                                                    fundingProject= fundingProject,
                                                    enabled=True,
                                                    share=share+old_share)
            new_shares.save()

            sharesub = share * (-1)

            wfunction().walletChange(request.user.id,fundingProject.token,sharesub)

            shares_sold_sum = FundingShares.objects.filter(hands=1,enabled=True,fundingProject=fundingProject).aggregate(share=Sum('share'))['share'] or 0

            if shares_sold_sum >= fundingProject.buyPrice:
                fundingProject.status=2
                fundingProject.save()

            return Response(FundingSharesSerializer(new_shares).data,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        pass
    def partial_update(self, request):
        pass

    def destroy(self, request, pk=None):
        try:
            qset = self.get_queryset()
            qset = qset.filter(hands=1,id=pk)
            
            if not qset.exists():
                return Response(Msg.Err.Shares.not_found_shares,status=status.HTTP_404_NOT_FOUND)
            
            q=qset[0]
            fundingProject= q.fundingProject
            tzUTC = pytz.utc
            dt1 = q.create_time
            dtnow = datetime.datetime.now(tzUTC)
            dt = dtnow-dt1
            dtdays=dt.days
            if dtdays >= 2:
                return Response(Msg.Err.Shares.delete_share_not_enough,status=status.HTTP_406_NOT_ACCEPTABLE)
            q.enabled=False
            wfunction().walletChange(request.user.id,fundingProject.token,q.share)
            q.save()

            

            return Response(Msg.Sucess.delete_sucess,status=status.HTTP_204_NO_CONTENT)

            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

            
        
class FundingSharesSoldViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return FundingSharesSoldSerializer
        elif self.action == 'update':
            return FundingSharesSoldSerializer
        elif self.action == 'retrieve':
            return FundingSharesSoldSerializer2
        elif self.action == 'buy':
            return FundingSharesSoldedSerializer

        return FundingSharesSoldSerializer2

    def get_queryset(self):  # added string
        if self.action == 'destroy':
            SharesSold.objects.filter(userData=User.objects.get(id=self.request.user.id),enabled=True)
        elif self.action == 'create':
            SharesSold.objects.filter(userData=User.objects.get(id=self.request.user.id),enabled=True)
        elif self.action == 'buy':
            SharesSolded.objects.filter(userBuy=User.objects.get(id=self.request.user.id))
        return SharesSold.objects.filter(enabled=True)

        

    def create(self, request, *args, **kwargs):
        sharessolddata = request.data
        

        fundingProjectId = sharessolddata['fundingProject']
        share = sharessolddata['share']
        token = sharessolddata['token']
        price = sharessolddata['price']
        fundingProject= FundingProjects.objects.get(id=fundingProjectId)
        myfdshares=FundingShares.objects.filter(userData=User.objects.get(id=request.user.id),
                                                    
                                                    fundingProject= fundingProject,
                                                    enabled=True)
        if not (fundingProject.status == 2 and fundingProject.enabled == True):
            return Response(Msg.Err.Shares.create_money_not_enough,status=status.HTTP_406_NOT_ACCEPTABLE)

        if not myfdshares.exists():
            return Response(Msg.Err.Shares.create_money_not_enough,status=status.HTTP_406_NOT_ACCEPTABLE)
        old_shares=myfdshares[0]
        if not old_shares.share >= share:
            return Response(Msg.Err.Shares.create_money_not_enough,status=status.HTTP_406_NOT_ACCEPTABLE)
        new_shares_sold = SharesSold.objects.create(userData=User.objects.get(id=self.request.user.id),
                                                    fundingProject=fundingProject,
                                                    share=share,
                                                    token=token,
                                                    price=price,
                                                    enabled=True    )
        new_shares_sold.save()

        if old_shares.share - share > 0:

            new_shares = FundingShares.objects.create(userData=User.objects.get(id=request.user.id),
                                                    hands=2,
                                                    fundingProject= fundingProject,
                                                    enabled=True,
                                                    share=old_shares.share - share)
            new_shares.save()                                
        old_shares.enabled=False
        old_shares.save()





    def destroy(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass
    def partial_update(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def buy(self, request):
        sharesdata = request.data
        try:
            old_share=0
            sharesSoldId = sharesdata['sharesSold']
            share = sharesdata['share']
            
            sharesSold= SharesSold.objects.get(id=sharesSoldId)
            price = (share/sharesSold.share)*sharesSold.price
            if not wfunction().walletCanUse(request.user.id,sharesSold.token,price):
                return Response(Msg.Err.Shares.create_money_not_enough,status=status.HTTP_406_NOT_ACCEPTABLE)
            
            
            if FundingShares.objects.filter(userData=User.objects.get(id=request.user.id),
                                                   
                                                    fundingProject= sharesSold.fundingProject,
                                                    enabled=True).exists():

                old_shares = FundingShares.objects.get(userData=User.objects.get(id=request.user.id),
                                                    fundingProject= sharesSold.fundingProject,
                                                    enabled=True)
                old_share=old_shares.share
                old_shares.enabled = False

                old_shares.save()
                


        

            new_shares = FundingShares.objects.create(userData=User.objects.get(id=request.user.id),
                                                    hands=2,
                                                    fundingProject= sharesSold.fundingProject,
                                                    enabled=True,
                                                    share=share+old_share)
            new_shares.save()

            pricesub = price * (-1)

            new_shares_solded = SharesSolded.objects.create(sharesSold=sharesSold,
                                                            userBuy=User.objects.get(id=request.user.id),
                                                            share=share)
            
            new_shares_solded.save()

            wfunction().walletChange(request.user.id,sharesSold.token,pricesub)
            wfunction().walletChange(sharesSold.userData.pk,sharesSold.token,price)
            

            new_transferlog = TransferLogsUser.objects.create(fromUserData=User.objects.get(id=request.user.id),
                                                              toUserData=User.objects.get(id=sharesSold.userData.pk),
                                                              amount=price,
                                                              token=sharesSold.token
                                                                )
            

            new_transferlog.save()



            return Response(FundingSharesSerializer(new_shares).data,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)







