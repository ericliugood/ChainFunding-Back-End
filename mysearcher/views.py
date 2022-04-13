from mysearcher.serializers import SearcherSerializer
from mydatabase.models import FundingProjects
from mydatabase.models import UserDatas

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from myapi.response import *
from myapi.message import *

# Create your views here.


class SearcherViewSet(ModelViewSet):
    queryset = FundingProjects.objects.all()
    serializer_class = SearcherSerializer

    @action(detail=False)
    def project(self, request):  # project nft user
        data = request.query_params

        nid = data.get('nftid')
        project = FundingProjects.objects.filter(nftId=nid)
        fundraiser = UserDatas.objects.get(usernameAccount=project.first().fundraiser)
        if project.exists():
            return success({
                'nftid': project.first().nftId,
                'startTime': project.first().startTime,
                'endTime': project.first().endTime,
                'token': project.first().token,
                'butPrice': project.first().buyPrice,
                'sellPrice': project.first().sellPrice,
                'gasPrice': project.first().gasPrice,
                'fundraiser': fundraiser.usernameAccount
            })
        else:
            return notfound(Msg.NotFound.project)
