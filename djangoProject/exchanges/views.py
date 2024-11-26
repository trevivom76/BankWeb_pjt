from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.conf import settings
import requests
from datetime import date

@api_view(['GET'])
def exchange_list(request):
    today = date.today()

    response = requests.get(
        f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01"
    ).json()

    updated_count = 0
    created_count = 0

    for exchange_data in response:
        cur_unit = exchange_data['cur_unit']
        
        existing_data = ExchangeRate.objects.filter(cur_unit=cur_unit, date_fetched=today).first()

        if existing_data:
            continue
        else:
            latest_data = ExchangeRate.objects.filter(cur_unit=cur_unit).order_by('-date_fetched').first()

            if latest_data and latest_data.date_fetched < today:
                serializer = ExchangeSerializer(latest_data, data=exchange_data)
                if serializer.is_valid():
                    serializer.save()
                    updated_count += 1
            else:
                serializer = ExchangeSerializer(data=exchange_data)
                if serializer.is_valid():
                    serializer.save()
                    created_count += 1

    return Response({
        "message": f"Updated {updated_count} records, Created {created_count} new records.",
        "data": response
    })