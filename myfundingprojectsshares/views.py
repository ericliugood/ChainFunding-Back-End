from myfundingprojectsshares.serializers import FundingSharesSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from mywallet.walletfunction import wfunction
from mydatabase.models import FundingShares,FundingProjects
from rest_framework import status
from rest_framework.response import Response
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
            print(share)
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

            
        





