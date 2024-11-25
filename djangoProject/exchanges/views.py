from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import ExchangeRate

@api_view(['GET'])
def exchange_list(request):
    try:
        # 1. API 요청
        response = requests.get(
            f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01"
        )
        response.raise_for_status()
        data = response.json()

        # 2. 데이터 출력 (디버깅 용도)
        for item in data:
            print(item)  # 데이터가 예상과 다른 경우 확인 가능

        # 3. 데이터 저장
        for item in data:
            try:
                ExchangeRate.objects.update_or_create(
                    cur_unit=item["cur_unit"],  # 통화 코드로 중복 방지
                    defaults={
                        "cur_nm": item["cur_nm"],
                        "ttb": float(item["ttb"].replace(",", "")) if item["ttb"] else None,
                        "tts": float(item["tts"].replace(",", "")) if item["tts"] else None,
                        "deal_bas_r": float(item["deal_bas_r"].replace(",", "")) if item["deal_bas_r"] else None,
                        "bkpr": float(item["bkpr"].replace(",", "")) if item["bkpr"] else None,
                    },
                )
            except Exception as e:
                print(f"데이터 저장 실패: {item} -> {str(e)}")
                continue  # 저장 실패 시 다음 데이터로 넘어감

        # 4. 저장된 데이터를 반환
        return Response(data)

    except requests.exceptions.RequestException as e:
        return Response({"error": f"API 요청 실패: {str(e)}"}, status=500)

    except Exception as e:
        return Response({"error": f"서버 내부 오류: {str(e)}"}, status=500)
