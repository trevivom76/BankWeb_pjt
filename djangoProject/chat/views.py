# import json
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from deposits.models import *
# from deposits.serializers import *
# from rest_framework.decorators import api_view

# # openai.api_key = settings.OPENAI_API_KEY

# from openai import OpenAI

# client = OpenAI(
#     api_key=settings.OPENAI_API_KEY
# )

# # def exchange_list():
# #     response = requests.get(
# #         f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01"
# #     )
# #     if response.status_code == 200:
# #         try:
# #             return response.json()
# #         except ValueError:
# #             return {"error": "Invalid JSON response"}
# #     return {"error": f"API request failed with status code {response.status_code}"}


# # def search_banks_by_location(query):
# #     headers = {
# #         'Authorization': f'KakaoAK {settings.KAKAO_API_KEY}'
# #     }
# #     params = {
# #         'query': query,
# #         'category_group_code': 'BK9',  # 은행 카테고리 코드
# #         'size': 5  # 최대 5개의 결과 반환
# #     }
# #     url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
# #     response = requests.get(url, headers=headers, params=params)
    
# #     if response.status_code == 200:
# #         return response.json().get('documents', [])
# #     else:
# #         return []


# @api_view(['POST'])
# @csrf_exempt
# def chatbot_response(request):
#     if request.method == "POST":
#         try:
#             # 사용자 입력 받기
#             data = json.loads(request.body)
#             user_message = data.get("message", "")
#             # query = data.get("query", "서울 강남구")  # 예: 기본 검색 지역

#             # DB에서 예적금 데이터 가져오기
#             savings_data = Saving.objects.all()
#             deposit_data = Deposit.objects.all()
#             saving_serializer = SavingSerializer(savings_data, many=True)
#             deposit_serializer = DepositSerializer(deposit_data, many=True)

#             # 외부 API 데이터 가져오기
#             # exchange_rates = exchange_list()
#             # kakao_map_results = search_banks_by_location(query)
#             # 직렬화된 데이터 생성
#             deposit_json = json.dumps(deposit_serializer.data, ensure_ascii=False, indent=2)
#             saving_json = json.dumps(saving_serializer.data, ensure_ascii=False, indent=2)
#             # exchange_json = json.dumps(exchange_rates, ensure_ascii=False, indent=2)
#             # kakao_map_json = json.dumps(kakao_map_results, ensure_ascii=False, indent=2)

#             # 프롬프트 생성
#             BASE_PROMPT = f"""
#             당신은 BBK 금융 서비스의 챗봇 "핀"입니다. 😆  
#             사용자에게 금융 관련 도움을 제공합니다. 아래의 주요 서비스를 처리하세요:

#             1️⃣ **예적금 상품 추천**
#             - 사용자에게 목표 금액과 저축 기간을 요청하세요.  
#             - 입력된 조건에 맞는 금융 상품을 추천하세요.  
#             - 추천 가능한 상품이 없으면 조건 변경을 제안하세요.
#             예금 데이터:
#             {deposit_json}

#             적금 데이터:
#             {saving_json}

#             2️⃣ **주변 은행 위치 찾기**
#             - 지역 이름 또는 현재 위치를 요청하세요.  
#             - ATM만, 특정 은행 등의 조건을 추가로 요청하세요.  
#             - 조건에 맞는 결과를 반환하며 지도 링크를 제공합니다.
            
#             아래는 '{query}' 지역에서 검색된 은행입니다:
            

#             3️⃣ **환율 계산기**
#             - 기준 통화(예: USD), 계산 방식(송금 보낼 때/받을 때), 환전 금액을 요청하세요.  
#             - 실시간 환율 데이터를 기반으로 계산 결과를 제공합니다.
            
#             실시간 환율 데이터:
            

#             4️⃣ **금융 상품 비교**  
#             - 사용자가 선택한 상품의 금리, 조건 등을 비교하세요.

#             중간중간 효과적인 이모티콘을 사용해 사용자에게 부드러운 인상으로 다가가주세요.
#             모든 응답은 친절하고 명확하게 제공하며, 사용자가 챗봇을 효과적으로 이용할 수 있도록 도와주세요.
#             """
            
#             # chat_completion = client.chat.completions.create(
#             #     model="gpt-4-turbo",  # 원하는 모델 이름
#             #     messages=[{"role": "user", "content": "Hello world"}]
#             # )
            
#             # # GPT 응답 가져오기
#             # chatbot_message = chat_completion["choices"][0]["message"]["content"].strip()

#             # # 응답 반환
#             # return JsonResponse({"response": chatbot_message})
            
#             chat_completion = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[
#                     {"role": "system", "content": BASE_PROMPT},
#                     {"role": "user", "content": user_message},
#                 ],
#             )
            
#             # GPT 응답 가져오기
#             chatbot_message = chat_completion["choices"][0]["message"]["content"].strip()

#             # 응답 반환
#             return JsonResponse({"response": chatbot_message})
        
#         except Exception as e:
#             # 오류 처리
#             return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

#     return JsonResponse({"error": "올바른 요청 방식이 아닙니다. POST 요청을 사용하세요."}, status=405)



from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import openai
import json


@csrf_exempt
@api_view(['POST'])
def chatbot_response(request):
    try:
        print(1)    
        # 요청 데이터 파싱
        data = json.loads(request.body)
        user_message = data.get("message", "")

        print(user_message)
        if not user_message:
            return JsonResponse({"error": "메시지가 비어 있습니다."}, status=400)
        print(2)

        openai.api_key = settings.OPENAI_API_KEY
        
        # OpenAI API 호출
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 은행의 금융 전문가 챗봇입니다."},
                {"role": "user", "content": "예금 서비스가 무엇인지 설명해줘."},
            ]
        )
        print(3)

        chatbot_message = completion["choices"][0]["message"]["content"]
        return JsonResponse({"response": chatbot_message})
    except json.JSONDecodeError:
        return JsonResponse({"error": "유효하지 않은 JSON 요청입니다."}, status=400)
    except Exception as e:
        # 예상치 못한 오류 처리
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)
