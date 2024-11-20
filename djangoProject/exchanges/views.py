from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests

@api_view(['GET'])
def exchange_list(request):

    # API 요청
    response = requests.get(
        f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01"
    ).json()

    return Response(response)
