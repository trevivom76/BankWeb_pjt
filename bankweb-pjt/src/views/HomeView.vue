<template>
  <v-container>
    <v-select label="Select" :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']" variant="outlined" class="custom-outline"></v-select>
  </v-container>
</template>

<style scoped>
.custom-outline .v-input {
  border: 2px solid blue; /* 윤곽선 색을 파란색으로 설정 */
  border-radius: 8px; /* 선택적으로 테두리를 더 둥글게 설정 가능 */
}

.custom-outline .v-input:focus-within {
  border-color: #007bff; /* 포커스 상태의 색상 */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* 포커스 시 약간의 빛남 효과 추가 */
}
</style>
