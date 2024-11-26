<template>
  <div>
    <div class="container">
      <div class="button-box">
        <RouterLink :to="{ name: 'depositList' }" class="button" exact-active-class="active">
          정기예금
        </RouterLink>
        <RouterLink :to="{ name: 'savingList' }" class="button" exact-active-class="active">
          정기적금
        </RouterLink>
      </div>
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useFinancialStore } from "@/stores/financial";


const financialStore = useFinancialStore();

onMounted(() => {
  financialStore.fetchAllData();
  financialStore.getBankDatas()
});

</script>

<style scoped>
.button-box {
  display: flex;
  flex-direction: row;
  gap: 2px;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;

  padding: 12px 30px;
  width: 120px;
  height: 48px;

  border-width: 0.5px 0.5px 0px 0.5px;
  border-style: solid;
  border-color: #DCDCDC;
  border-radius: 20px 20px 0px 0px;

  background: #F3F6F8;
  color: #ACACAC;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  text-decoration: none;

  transition: background-color 0.3s, color 0.3s;
  /* 부드러운 효과 추가 */
}

/* 활성화된 버튼 스타일 */
.button.active {
  background-color: #FFFFFF;
  color: black;
  border-style: none;
}

/* 비활성화된 버튼 호버 효과 */
.button:hover {
  background-color: #e0e0e0;
  color: white;
}
</style>