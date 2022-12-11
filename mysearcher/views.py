from mysearcher.serializers import SearcherSerializer
from mydatabase.models import FundingProjects
from django.contrib.auth.models import User

import requests
import json
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
                    fundraiser = User.objects.get(username__contains=parm)  # find fundraiser

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
                        'fundraiser': User.objects.filter(id=p.fundraiser_id).values('username')
                    }
                        for p in raiser_project
                    ]
                })
            except Exception as e:
                print(e)
                return notfound(Msg.NotFound.project)
        else:
            return err(Msg.Err.FundingProject.search,status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False)
    def opensea(self, request):
        data = request.query_params
        ca = data.get('address')
        tid = data.get('token_id')

        if (ca is not None) and (len(ca) == 42):
            if tid is not None:
                #taddr = "0x3ad7ad283dab53511abdc5ff9f95a35f735e48f2"
                # url = "https://testnets-api.opensea.io/api/v1/assets?token_ids="+tid+"&asset_contract_address="+taddr+"&order_direction=desc&offset=0&limit=50&include_orders=false"

                url = "https://testnets-api.opensea.io/api/v1/assets?token_ids="+tid+"&asset_contract_address=" + ca \
                      + "&order_direction=desc&offset=0&limit=5&include_orders=false"
            else:
                url = "https://testnets-api.opensea.io/api/v1/assets?asset_contract_address=" + ca \
                      + "&order_direction=desc&offset=0&limit=5&include_orders=false"

                response = requests.get(url)
                process = response.json()  # dict
                process = process["assets"]  # list

                return success({
                    "assets": [{
                        "id": p["id"],
                        "num_sales": p["num_sales"],
                        "image_url": p["image_url"],
                        "image_preview_url": p["image_preview_url"],
                        "image_thumbnail_url": p["image_thumbnail_url"],
                        "image_original_url": p["image_original_url"],
                        "animation_url": p["animation_url"],
                        "animation_url": p["animation_url"],
                        "name": p["name"],
                        "description": p["description"],
                        "external_link": p["external_link"],
                        "asset_contract": p["asset_contract"],
                        "permalink": p["permalink"],
                        "token_metadata": p["token_metadata"],
                        "last_sale": p["last_sale"],
                        "top_bid": p["top_bid"],
                        "listing_date": p["listing_date"],
                        "supports_wyvern": p["supports_wyvern"],
                        "rarity_data": p["rarity_data"],
                        "transfer_fee": p["transfer_fee"],
                        "transfer_fee_payment_token": p["transfer_fee_payment_token"],
                        "token_id": p["token_id"]

                    }
                        for p in process
                    ]

                })
        else:
            return err(Msg.Err.OpenSea.address)
