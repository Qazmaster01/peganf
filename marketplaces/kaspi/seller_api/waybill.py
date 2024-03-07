import requests

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.api_key import services
from utils.kaspi import get_kaspi_http_headers
from apps.request_for_shipment import services as rq_services


class WaybillAPI(APIView):
    """Получить ссылку на скачивание маркировки."""

    def post(self, request, pk):
        try:
            rq = rq_services.get_rq_by_id(pk)
            token = services.get_kaspi_token_by_user(rq.user.id)
            r = requests.get(url=rq.kaspi_self, headers=get_kaspi_http_headers(token))
            if 'data' in r.json():
                waybill = r.json()['data']['attributes']['kaspiDelivery']['waybill']
                if waybill:
                    return Response(waybill, status=200)
                raise Exception('Маркировка еще не сформирована.')
            raise Exception(r.json())

        except Exception as e:
            return Response({"status": "error", "data": str(e)}, status=500)
