import requests
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from deposits.models import *
from deposits.serializers import *
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Prefetch, F, Max
from openai import OpenAI
import json

def get_filtered_products(user_message):
    # 검색어 기반 필터링을 위한 키워드 정의
    keywords = {
        '예금': ['예금', '정기예금', '예치'],
        '적금': ['적금', '저축', '저금'],
        '단기': ['단기', '6개월', '3개월', '1년'],
        '장기': ['장기', '2년', '3년', '5년'],
        '고금리': ['높은 금리', '고금리', '이자']
    }
    
    message_lower = user_message.lower()
    is_deposit = any(word in message_lower for word in keywords['예금'])
    is_saving = any(word in message_lower for word in keywords['적금'])
    is_short_term = any(word in message_lower for word in keywords['단기'])
    is_long_term = any(word in message_lower for word in keywords['장기'])
    is_high_interest = any(word in message_lower for word in keywords['고금리'])

    result = {}

    # 예금 상품 필터링
    if is_deposit or (not is_deposit and not is_saving):
        deposit_query = Deposit.objects.prefetch_related(
            Prefetch(
                'depositoption_set',
                queryset=DepositOption.objects.order_by('-intr_rate')
            )
        ).distinct()

        # 기간 필터링
        if is_short_term:
            deposit_query = deposit_query.filter(depositoption__save_trm__lte='12')
        elif is_long_term:
            deposit_query = deposit_query.filter(depositoption__save_trm__gt='12')

        # 고금리 필터링
        if is_high_interest:
            deposit_query = deposit_query.annotate(
                max_rate=Max('depositoption__intr_rate')
            ).order_by('-max_rate')

        deposits = []
        for deposit in deposit_query[:3]:  # 상위 3개 상품만 선택
            options = deposit.depositoption_set.all()[:1]  # 최고금리 옵션
            if options:
                deposits.append({
                    'fin_prdt_nm': deposit.fin_prdt_nm,
                    'kor_co_nm': deposit.kor_co_nm,
                    'interest_rate': options[0].intr_rate,
                    'save_trm': options[0].save_trm,
                    'join_way': deposit.join_way,
                    'etc_note': deposit.etc_note
                })
        result['deposits'] = deposits

    # 적금 상품 필터링
    if is_saving or (not is_deposit and not is_saving):
        saving_query = Saving.objects.prefetch_related(
            Prefetch(
                'savingoption_set',
                queryset=SavingOption.objects.order_by('-intr_rate')
            )
        ).distinct()

        # 기간 필터링
        if is_short_term:
            saving_query = saving_query.filter(savingoption__save_trm__lte='12')
        elif is_long_term:
            saving_query = saving_query.filter(savingoption__save_trm__gt='12')

        # 고금리 필터링
        if is_high_interest:
            saving_query = saving_query.annotate(
                max_rate=Max('savingoption__intr_rate')
            ).order_by('-max_rate')

        savings = []
        for saving in saving_query[:3]:  # 상위 3개 상품만 선택
            options = saving.savingoption_set.all()[:1]  # 최고금리 옵션
            if options:
                savings.append({
                    'fin_prdt_nm': saving.fin_prdt_nm,
                    'kor_co_nm': saving.kor_co_nm,
                    'interest_rate': options[0].intr_rate,
                    'save_trm': options[0].save_trm,
                    'join_way': saving.join_way,
                    'etc_note': saving.etc_note
                })
        result['savings'] = savings

    return result

# 환율 API 호출 함수
def get_exchange_rates():
    try:
        # response.json()을 호출하기 전에 response 객체를 먼저 받아야 합니다
        response = requests.get(
            f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_API_KEY}&data=AP01"
        )
        if response.status_code == 200:
            rates = {}
            for item in response.json():
                # 주요 통화만 필터링하고 필요한 정보만 추출
                if item['cur_unit'] in ['USD', 'EUR', 'JPY', 'CNY']:
                    rates[item['cur_unit']] = float(item['tts'].replace(',', ''))
            return rates
        return None
    except Exception as e:
        print(f"환율 정보 조회 중 오류: {str(e)}")
        return None


def search_banks_by_location(query, bank_type=None):
    try:
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {
            "Authorization": f"KakaoAK {settings.KAKAO_API_KEY}"
        }
        
        # 검색어 최적화
        search_query = f"{query} "
        if bank_type:
            search_query += f"{bank_type} "
        search_query += "은행"
        
        params = {
            "query": search_query,
            "size": 5,
            "sort": "distance"  # 거리순 정렬 추가
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # 검색 결과 가공
            banks = []
            for place in data.get('documents', []):
                # 거리 형식화
                distance = place.get('distance')
                if distance:
                    distance = f"{float(distance)/1000:.1f}km" if float(distance) >= 1000 else f"{distance}m"
                
                banks.append({
                    'name': place['place_name'],
                    'address': place['address_name'],
                    'phone': place.get('phone', '정보 없음'),
                    'distance': distance or '정보 없음',
                    'url': f"https://map.kakao.com/link/map/{place['id']}",
                    'lat': place['y'],
                    'lng': place['x']
                })
            return banks
        return None
    except Exception as e:
        print(f"은행 위치 검색 중 오류: {str(e)}")
        return None


def process_user_query(user_message, query_location):
    # 키워드 정의
    keywords = {
        '예적금': ['예금', '적금', '저축', '이자'],
        '환율': ['환율', '환전', '달러', '엔화', '유로'],
        '은행위치': ['은행', '지점', 'ATM', '위치', '찾기']
    }
    
    # 메시지 의도 파악
    message_lower = user_message.lower()
    is_exchange = any(word in message_lower for word in keywords['환율'])
    is_location = any(word in message_lower for word in keywords['은행위치'])
    
    result = {
        'type': 'general',
        'data': {}
    }

    # 환율 정보 처리
    if is_exchange:
        exchange_data = get_exchange_rates()
        if exchange_data:
            result['type'] = 'exchange'
            result['data']['exchange_rates'] = exchange_data
            # 환율 정보가 없을 때 처리
            if not exchange_data:
                result['error'] = "현재 환율 정보를 조회할 수 없습니다."
    
    # 은행 위치 처리
    elif is_location:
        banks = search_banks_by_location(query_location)
        if banks:
            result['type'] = 'location'
            result['data']['banks'] = banks
            result['data']['query_location'] = query_location
        else:
            result['error'] = f"{query_location} 주변의 은행 정보를 찾을 수 없습니다."
    
    # 예적금 정보 처리
    else:
        filtered_products = get_filtered_products(user_message)
        result['type'] = 'financial'
        result['data']['products'] = filtered_products

    return result

def generate_prompt(query_result, query_location="서울 강남구"):
    response = ""
    
    if query_result['type'] == 'exchange':
        # 환율 정보 포맷팅
        rates = query_result['data']['exchange_rates']
        response += "\n💱 현재 환율 정보:\n\n"
        for currency, rate in rates.items():
            response += f"• {currency}: {rate:,.2f}원\n"
    
    elif query_result['type'] == 'location':
        # 은행 위치 정보 포맷팅
        banks = query_result['data']['banks']
        response += f"\n🏦 {query_location} 주변 은행 정보:\n\n"
        for bank in banks:
            response += (
                f"• **{bank['name']}**\n"
                f"  - 주소: {bank['address']}\n"
                f"  - 연락처: {bank['phone']}\n"
                f"  - 🗺️ [지도 보기]({bank['url']})\n\n"
            )
    
    elif query_result['type'] == 'financial':
        # 기존 예적금 상품 정보 포맷팅
        products = query_result['data']['products']
        if 'deposits' in products:
            response += "\n🏦 예금상품:\n\n"
            for product in products['deposits']:
                response += (
                    f"• **{product['fin_prdt_nm']}** ({product['kor_co_nm']})\n"
                    f"  - 금리: {product['interest_rate']}%\n"
                    f"  - 기간: {product['save_trm']}개월\n"
                    f"  - 가입방법: {product['join_way']}\n\n"
                )
                
        if 'savings' in products:
            response += "\n💰 적금상품:\n\n"
            for product in products['savings']:
                response += (
                    f"• **{product['fin_prdt_nm']}** ({product['kor_co_nm']})\n"
                    f"  - 금리: {product['interest_rate']}%\n"
                    f"  - 기간: {product['save_trm']}개월\n"
                    f"  - 가입방법: {product['join_way']}\n\n"
                )

    response += f"""
    참고사항:
    • 상품별 자세한 가입조건과 제한사항이 있을 수 있습니다
    • {query_location} 지역 기준 은행 검색이 가능합니다
    • 환율 정보는 실시간 변동될 수 있습니다

    추가 문의사항이 있으시다면 말씀해 주세요! 😊
    """
    
    return response

@csrf_exempt
@api_view(['POST'])
def chatbot_response(request):
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")
        query_location = data.get("query", "서울 강남구")

        if not user_message:
            return JsonResponse({"error": "메시지가 비어 있습니다."}, status=400)

        # 사용자 쿼리 처리
        query_result = process_user_query(user_message, query_location)
        
        # GPT 프롬프트 생성
        prompt = generate_prompt(query_result, query_location)
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        chatbot_message = completion.choices[0].message.content
        return JsonResponse({
            "response": chatbot_message,
            "data": query_result
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "유효하지 않은 JSON 요청입니다."}, status=400)
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {str(e)}")
        return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)