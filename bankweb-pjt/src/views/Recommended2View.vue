<template>
  <div>
22222222222222
  </div>
</template>

<script setup>
import { useFinancialStore } from '@/stores/financial';
import { ref, computed } from 'vue';
const financialStore = useFinancialStore()

// 전체 적금상품 정보
const depositProducts = financialStore.deposits

// 전체 예금상품 정보
const savingProducts = financialStore.savings
</script>

<style lang="" scoped>

</style>