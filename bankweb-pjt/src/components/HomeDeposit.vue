<template>
  <div>
    <!-- 예금 계산기는 레이아웃까지만 만들었고 데이터 끌어오지는 않았어. -->
    <v-card class="deposit container" color="white" >
      <div style="display: flex; align-items: center; gap: 8px">
        <v-icon size="24" color="black">mdi-cash</v-icon>
        <p :style="{ fontWeight: '700', fontSize: '20px', color: 'black' }">예금 계산기</p>
      </div>

      <div>
        <v-select label="열심히 모은 목돈을 예치할 때" :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']" variant="outlined"></v-select>
      </div>

      <div style="margin-top: 16px">
        <!-- 문구와 입력 필드 정렬 -->
        <p style="font-size: 16px">
            <div>
            <input type="text" class="custom-input" placeholder="금액 입력">
            _원을
            <input type="text" class="custom-input" placeholder="개월 입력">
            개월 간
            <input type="text" class="custom-input" placeholder="이율 입력">
            %의 예금상품에 저축하면?
          </div>
        </p>

        
      </div>
    </v-card>
  </div>
</template>

<script setup></script>

<style scoped>
/* 입력 필드 커스터마이징 */
.custom-input {
  width: 80px; /* 가로 크기를 줄임 */
  background-color: #f0f0f0; /* 회색 배경 추가 */
  border: 1px solid #ccc; /* 테두리 설정 */
  border-radius: 4px; /* 둥근 테두리 */
  padding: 4px; /* 내부 여백 */
  text-align: center; /* 텍스트 중앙 정렬 */
  margin: 0 4px; /* 입력 필드 간 간격 */
  font-size: 14px; /* 글자 크기 */
}

.custom-input:focus {
  outline: none; /* 포커스 시 기본 outline 제거 */
  border-color: #6200ea; /* 포커스 시 보라색 테두리 */
}
</style>
