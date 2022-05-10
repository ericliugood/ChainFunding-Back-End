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

        nftid = data.get('nftid')
        fundraiser = data.get('fundraiser')

        if fundraiser is not None:  # find project from raiser
            fundraiser = UserDatas.objects.get(usernameAccount=fundraiser)  # find fundraiser
            raiser_project = FundingProjects.objects.filter(fundraiser_id=fundraiser.id)  # find project by raiser
            return success({
                'project': [{
                        'id': p.nftId,
                        'startTime': p.startTime,
                        'endTime': p.endTime,
                        'token': p.token,
                        'butPrice': p.buyPrice,
                        'sellPrice': p.sellPrice,
                        'gasPrice': p.gasPrice,
                        'fundraiser': fundraiser.usernameAccount
                     }
                    for p in raiser_project
                ]
            })
        elif nftid is not None:  # find project from nftid
            nft_project = FundingProjects.objects.filter(nftId=nftid)  # find project by nft id
            return success({
                'project': [{
                        'id': p.nftId,
                        'startTime': p.startTime,
                        'endTime': p.endTime,
                        'token': p.token,
                        'butPrice': p.buyPrice,
                        'sellPrice': p.sellPrice,
                        'gasPrice': p.gasPrice
                    }
                    for p in nft_project
                ]
            })
        else:  # list all project
            project = FundingProjects.objects.all()
            return success({
                'project': [{
                        'id': p.nftId,
                        'startTime': p.startTime,
                        'endTime': p.endTime,
                        'token': p.token,
                        'butPrice': p.buyPrice,
                        'sellPrice': p.sellPrice,
                        'gasPrice': p.gasPrice
                    }
                    for p in project
                ]
            })
