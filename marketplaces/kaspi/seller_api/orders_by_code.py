import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.api_key import services
from utils.kaspi import get_kaspi_http_headers

class KaspiOrdersByCodeAPI(APIView):
    def get(self, request):
        token = services.get_kaspi_token_by_user(request.user)
        url = f"https://kaspi.kz/shop/api/v2/orders?filter[orders][code]={request.data.get('code')}"
        response = requests.get(url=url, headers=get_kaspi_http_headers(token))
        return Response(response.json() if "data" in response.json() else {"error": "Неправильный запрос на каспи", "data": response.content}, status=201 if "data" in response.json() else 500)


