from myfundingprojectsshares.serializers import FundingSharesSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from mywallet.walletfunction import wfunction
from mydatabase.models import FundingShares,FundingProjects

class FundingSharesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = FundingSharesSerializer

    def get_queryset(self):  # added string
        return super().get_queryset().filter(userData=User.objects.get(id=self.request.user.id))

    def create(self, request, *args, **kwargs):
        sharesdata = request.data
        fundingProjectId = sharesdata['fundingProject']
        share = sharesdata['share']
        fundingProject= FundingProjects.objects.get(id=fundingProjectId)
        if not wfunction().walletCanUse(request.user.id,fundingProject.token,share):
            pass
        
        new_shares = FundingShares.objects.create(userData=User.objects.get(id=request.user.id),
                                                    hands=1,
                                                    fundingProject= fundingProject,
                                                    enabled=True,
                                                    hands=1,
                                                    share=share)
        new_shares.save()




