import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.api_key import services
from utils.kaspi import get_kaspi_http_headers


class KaspiOrdersByCodeAPI(APIView):
    """Получение состава заказа по коду."""

    def get(self, request):
        try:
            if not request.user:
                return Response({"error": "Пользователь не найдено"}, status=400)

            token = services.get_kaspi_token_by_user(request.user)
            codes = request.data.get('code')
            if not codes:
                return Response({"error": "Код заказа не найдено"}, status=400)

            url = f"https://kaspi.kz/shop/api/v2/orders?filter[orders][code]={codes}"
            r = requests.get(url=url, headers=get_kaspi_http_headers(token))
            if r.status_code == 200:
                data = r.json().get("data")
                if data:
                    return Response(data, status=200)
                else:
                    return Response({"error": "Нет данных в ответе от Каспий"}, status=500)
            else:
                return Response({"error": "Ошибка при запросе к Каспий", "data": r.content}, status=r.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


