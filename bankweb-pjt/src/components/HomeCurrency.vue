<template>
  <div>
    <div class="box">
      <div class="title-box">
        <img src="@/assets/icon/chartIcon.png" alt="환율 그래프 아이콘" class="icon">
        <p class="title">환율 그래프</p>
      </div>
      <div class="exchange-box">
        <ExchangeCard :currency="'USD'" :name="'미국 달러'" width="47%" style="display: inline-block;" class="mb-5"
          elevation="5" />
        <ExchangeCard :currency="'JPY'" :name="'일본 옌'" width="47%" style="display: inline-block;" class="mb-5 ml-3"
          elevation="5" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ExchangeCard from '@/components/ExchangeCard.vue';
</script>

<style scoped>
.box {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 40px;
}

.title-box {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
  gap: 4px;
  padding-bottom: 16px;
}

.icon {
  width: 25px;
  height: 25px;
}

.title {
  font-weight: 600;
  font-size: 20px;
  line-height: 24px;
  color: #000000;
}

.exchange-box {
  display: flex;
  flex-direction: row;
  width: 100%;
}
</style>