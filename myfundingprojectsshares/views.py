from myfundingprojectsshares.serializers import FundingSharesSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from mywallet.walletfunction import wfunction
from mydatabase.models import FundingShares,FundingProjects
from rest_framework import status
from rest_framework.response import Response

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
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
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

            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)





