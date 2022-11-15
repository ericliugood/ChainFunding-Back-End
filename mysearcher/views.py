from mysearcher.serializers import SearcherSerializer
from mydatabase.models import FundingProjects, UserDatas

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from myapi.response import *
from myapi.message import *


class SearcherViewSet(ModelViewSet):
    queryset = FundingProjects.objects.all()
    serializer_class = SearcherSerializer

    @action(detail=False)
    def project(self, request):  # project nft user
        data = request.query_params
        parm = data.get('parm')

        if parm is not None:  # find project from raiser
            try:
                try:
                    fundraiser = UserDatas.objects.get(usernameAccount__contains=parm)  # find fundraiser

                    raiser_project = FundingProjects.objects.filter(
                        Q(fundraiser_id=fundraiser.id) | Q(nftName__contains=parm) | Q(nftContractAddress__contains=parm)
                    )  # find project by raiser, nftname, nftid, nftaddr
                except ObjectDoesNotExist:
                    raiser_project = FundingProjects.objects.filter(
                        Q(nftName__contains=parm) | Q(nftContractAddress__contains=parm)
                    )  # find project by nftname, nftid, nftaddr

                return success({
                    'project': [{
                        'nftId': p.nftId,
                        'nftContractAddress': p.nftContractAddress,
                        'nftName': p.nftName,
                        'startTime': p.startTime,
                        'endTime': p.endTime,
                        'token': p.token,
                        'butPrice': p.buyPrice,
                        'sellPrice': p.sellPrice,
                        'gasPrice': p.gasPrice,
                        'fundraiser': UserDatas.objects.filter(id=p.fundraiser_id).values('usernameAccount')
                    }
                        for p in raiser_project
                    ]
                })
            except Exception as e:
                print(e)
                return notfound(Msg.NotFound.project)
        else:
            return err(Msg.Err.FundingProject.search)
        # elif nftid is not None:  # find project from nftid
        #     try:
        #         nft_project = FundingProjects.objects.filter(nftId=nftid)  # find project by nft id
        #         return success({
        #             'project': [{
        #                 'nftid': p.nftId,
        #                 'startTime': p.startTime,
        #                 'endTime': p.endTime,
        #                 'token': p.token,
        #                 'butPrice': p.buyPrice,
        #                 'sellPrice': p.sellPrice,
        #                 'gasPrice': p.gasPrice
        #             }
        #                 for p in nft_project
        #             ]
        #         })
        #     except Exception as e:
        #         print(e)
        #         return notfound(Msg.NotFound.project)
        # else:  # list all project
        #     try:
        #         project = FundingProjects.objects.all()
        #         return success({
        #             'project': [{
        #                 'nftid': p.nftId,
        #                 'startTime': p.startTime,
        #                 'endTime': p.endTime,
        #                 'token': p.token,
        #                 'butPrice': p.buyPrice,
        #                 'sellPrice': p.sellPrice,
        #                 'gasPrice': p.gasPrice
        #             }
        #                 for p in project
        #             ]
        #         })
        #     except Exception as e:
        #         print(e)
        #         return notfound(Msg.NotFound.project)

    @action(detail=False)
    def opensea(self, request):
        data = request.query_params
        nftid = data.get('nftid')
