<template>
    <div>
        <!-- 임의로 설정한 거니까 컴포넌트 삭제해도 된데이 -->
      <v-card class="chatbot container" color="white" >
        <div style="display: flex; align-items: center; gap: 8px">
          <v-icon size="24" color="black">mdi-cash</v-icon>
          <p :style="{ fontWeight: '700', fontSize: '20px', color: 'black' }">챗봇 바로가기</p>
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
  
  </style>
  