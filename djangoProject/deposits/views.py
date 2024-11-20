from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from deposits.models import *
from deposits.serializers import *
from django.db import transaction
import requests


# 예적금 데이터 가져오기
@api_view(['GET'])
def create_financial_data(request):

    # 예금 URL 설정
    depositURL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    # 적금 URL 설정
    savingURL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"

    params = {
        'auth':f'{settings.FINLIFE_API_KEY}',
        'topFinGrpNo':'020000',
        'pageNo':'1',
    }

    # API 데이터 가져오기
    deposit_res = requests.get(depositURL, params=params).json()
    saving_res = requests.get(savingURL, params=params).json()

    print(deposit_res['result']['max_page_no'])
    deposit_base_lst = deposit_res.get('result', {}).get('baseList', [])
    deposit_option_list = deposit_res.get('result', {}).get('optionList', [])

    saving_base_list = saving_res.get('result', {}).get('baseList', [])
    saving_option_list = saving_res.get('result', {}).get('optionList', [])


    # 예금 데이터 저장
    for depositData in deposit_base_lst:
        # Deposit 데이터가 DB에 존재한다면,
        if Deposit.objects.filter(fin_prdt_cd=depositData.get('fin_prdt_cd')).exists():
            continue
        # 존재하지 않는다면
        save_product = {
            'fin_prdt_cd': depositData.get('fin_prdt_cd', '-1'),
            'fin_co_no': depositData.get('fin_co_no', '-1'),
            'kor_co_nm': depositData.get('kor_co_nm', '-1'),
            'fin_prdt_nm': depositData.get('fin_prdt_nm', '-1'),
            'dcls_month': depositData.get('dcls_month', '-1'),
            'mtrt_int': depositData.get('mtrt_int', '-1'),
            'etc_note': depositData.get('etc_note', '-1'),
            'join_deny': depositData.get('join_deny', -1),
            'join_member': depositData.get('join_member', '-1'),
            'join_way': depositData.get('join_way', '-1'),
            'spcl_cnd': depositData.get('spcl_cnd', '-1'),
            'max_limit': depositData.get('max_limit', -1),
        }

        serializer = DepositSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    

    # 예금 옵션 데이터 저장
    for depositOptionData in deposit_option_list:
        prdt_cd = depositOptionData.get('fin_prdt_cd', '-1')
        try:
            product = Deposit.objects.get(fin_prdt_cd=prdt_cd)

            # DepositOption 데이터가 DB에 존재한다면,
            if DepositOption.objects.filter(
                deposit=product,
                intr_rate_type_nm=depositOptionData.get('intr_rate_type_nm', '-1'),
                save_trm=depositOptionData.get('save_trm', -1),
                intr_rate=depositOptionData.get('intr_rate', -1),
                intr_rate2=depositOptionData.get('intr_rate2', -1)
            ).exists():
                continue

            save_option = {
                'intr_rate_type_nm': depositOptionData.get('intr_rate_type_nm', '-1'),
                'intr_rate': depositOptionData.get('intr_rate', -1),
                'intr_rate2': depositOptionData.get('intr_rate2', -1),
                'save_trm': depositOptionData.get('save_trm', -1),
            }

            serializer = DepositOptionSerializer(data=save_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit=product)
        except Deposit.DoesNotExist:
            continue
    

    # 적금 데이터 저장
    for savingData in saving_base_list:
        if Saving.objects.filter(fin_prdt_cd=savingData.get('fin_prdt_cd')).exists():
            continue

        save_product = {
            'fin_prdt_cd': savingData.get('fin_prdt_cd', '-1'),
            'fin_co_no': savingData.get('fin_co_no', '-1'),
            'kor_co_nm': savingData.get('kor_co_nm', '-1'),
            'fin_prdt_nm': savingData.get('fin_prdt_nm', '-1'),
            'dcls_month': savingData.get('dcls_month', '-1'),
            'mtrt_int': savingData.get('mtrt_int', '-1'),
            'etc_note': savingData.get('etc_note', '-1'),
            'join_deny': savingData.get('join_deny', -1),
            'join_member': savingData.get('join_member', '-1'),
            'join_way': savingData.get('join_way', '-1'),
            'spcl_cnd': savingData.get('spcl_cnd', '-1'),
            'max_limit': savingData.get('max_limit', -1),
        }

        serializer = SavingSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()


    # 적금 옵션 데이터 저장
    for savingOptionData in saving_option_list:
        prdt_cd = savingOptionData.get('fin_prdt_cd', '-1')
        try:
            product = Saving.objects.get(fin_prdt_cd=prdt_cd)

            # 중복 데이터 확인
            if SavingOption.objects.filter(
                saving=product,
                intr_rate_type_nm=savingOptionData.get('intr_rate_type_nm', '-1'),
                rsrv_type_nm=savingOptionData.get('rsrv_type_nm', '-1'),
                save_trm=savingOptionData.get('save_trm', -1),
                intr_rate=savingOptionData.get('intr_rate', -1),
                intr_rate2=savingOptionData.get('intr_rate2', -1)
            ).exists():
                continue

            save_option = {
                'intr_rate_type_nm': savingOptionData.get('intr_rate_type_nm', '-1'),
                'rsrv_type_nm': savingOptionData.get('rsrv_type_nm', '-1'),
                'intr_rate': savingOptionData.get('intr_rate', -1),
                'intr_rate2': savingOptionData.get('intr_rate2', -1),
                'save_trm': savingOptionData.get('save_trm', -1),
            }

            serializer = SavingOptionSerializer(data=save_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving=product)
        except Saving.DoesNotExist:
            continue
    
    return Response({'message':'금융 데이터 생성 완료'})


# 전체 예금 리스트 조회
@api_view(['GET'])
def deposit_list(request):
    if request.method == 'GET':
        deposits = get_list_or_404(Deposit)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)


# 단일 예금 정보 조회
@api_view(['GET'])
def deposit_detail(request, deposit_id):
    if request.method == 'GET':
        deposit = get_object_or_404(Deposit, id=deposit_id)
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)


# 전체 적금 리스트 조회
@api_view(['GET'])
def saving_list(request):
    if request.method == 'GET':
        savings = get_list_or_404(Saving)
        serializer = SavingSerializer(savings, many=True)
        return Response(serializer.data)


# 단일 적금 정보 조회
@api_view(['GET'])
def saving_detail(request, saving_id):
    if request.method == 'GET':
        saving = get_object_or_404(Saving, id=saving_id)
        serializer = SavingSerializer(saving)
        return Response(serializer.data)


# 은행 리스트 추출
@api_view(['GET'])
def bank_list(request):
    banks = Deposit.objects.values_list('kor_co_nm', flat=True).distinct()
    return Response({'banks': banks})