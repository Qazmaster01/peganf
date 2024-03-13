import requests

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.api_key import services
from apps.good import services as good_services
from apps.request_for_shipment import services as rq_services
from utils.kaspi import get_kaspi_http_headers


class OrderApprovedByMerchantAPI(APIView):
    """Подтверждение заказа."""

    def post(self, request):
        related_link = request.data.get('related_link')
        if related_link:
            token = services.get_kaspi_token_by_user(request.user)
            r1 = requests.get(url=request.data.get('related_link'), headers=get_kaspi_http_headers(token))
            if "data" in r1.json():
                for i in r1.json()["data"]:
                    r2 = requests.get(
                        url=i["relationships"]["product"]["links"]["related"],
                        headers=get_kaspi_http_headers(token)
                    )
                    quantity = i["attributes"]["quantity"]
                    if "data" in r2.json():
                        r3 = requests.get(
                            url=r2.json()["data"]["relationships"]["merchantProduct"]["links"]["related"],
                            headers=get_kaspi_http_headers(token)
                        )
                        if "data" in r3.json():
                            vendor_code = r3.json()["data"]["attributes"]["code"]
                            url = "https://kaspi.kz/shop/api/v2/orders"
                            body = {
                                "data":
                                    {
                                        "type": "orders",
                                        "id": request.data.get('id'),
                                        "attributes": {
                                            "code": request.data.get('code'),
                                            "status": "ACCEPTED_BY_MERCHANT"
                                        }
                                    }
                            }
                            r = requests.post(url=url, json=body, headers=get_kaspi_http_headers(token))
                            if "data" in r.json():
                                query_data = {
                                    "user": request.user,
                                    "resource": "kaspi",
                                    "posting_number": request.data.get("id"),
                                    "status": "awaiting_packaging"
                                }
                                rq_services.create(query_data)
                                good_services.remove_by_vendor_code(vendor_code, quantity)
                                return Response(r.json(), status=201)
                            return self.kaspi_request_error(r)
                        return self.kaspi_request_error(r3)
                    return self.kaspi_request_error(r2)
            return self.kaspi_request_error(r1)
        else:
            return Response({"error": "Ссылка на товар отсутствует"}, status=400)

    def kaspi_request_error(self, response):
        return Response({"error": "Неправильный запрос на каспи", "data": response.json()}, status=500)