from django.db import models

class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=10)  # 통화 코드 (예: USD, EUR)
    cur_nm = models.CharField(max_length=50)  # 통화 이름 (예: 미국 달러)
    ttb = models.DecimalField(max_digits=10, decimal_places=2)  # 매입 환율
    tts = models.DecimalField(max_digits=10, decimal_places=2)  # 매도 환율
    deal_bas_r = models.DecimalField(max_digits=10, decimal_places=2)  # 기준 환율
    bkpr = models.DecimalField(max_digits=10, decimal_places=2)  # 장부 가격
    date_fetched = models.DateField(auto_now_add=True)  # 데이터가 저장된 날짜
