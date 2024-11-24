<template>
  <div class="box">
    <div class="chatbot-layer">
      <img class="chatbot" src="@/assets/icon/MessageIcon.png" alt="챗봇 아이콘" />
      <img src="@/assets/icon/chatbotText.png" alt="챗봇 메세지" />
      <div class="btn-layer">
        <button class="btn">챗봇 바로가기</button>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
/* 전체 박스 설정 */
.box {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 36px;
  display: inline-flex; /* 내용물에 맞춰 감싸기 */
  flex-direction: column;
  align-items: center; /* 모든 요소 가운데 정렬 */
  gap: 20px; /* 요소 간 간격 */
}

/* 챗봇 레이어 */
.chatbot-layer {
  display: flex;
  flex-direction: column; /* 기본 세로 정렬 */
  align-items: center; /* 수직 가운데 정렬 */
  justify-content: center;
  gap: 20px; /* 아이템 간 간격 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shake {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(5deg);
  }
  75% {
    transform: rotate(-5deg);
  }
}

.chatbot {
  animation: fadeIn 1s ease-in-out, shake 0.7s ease-in-out 1.2s infinite; /* 1.2초 후 반복 */
}

/* 이미지 스타일 */
img {
  width: 100%;
  height: auto;
  max-width: 200px; /* 이미지 최대 크기 제한 */
  object-fit: contain;
  padding-bottom: 20px;
}

/* 버튼 레이어 */
.btn-layer {
  display: flex;
  justify-content: center; /* 버튼 가운데 정렬 */
  width: 100%; /* 부모 컨테이너의 너비에 맞춤 */
}

/* 버튼 스타일 */
.btn {
  display: flex;
  justify-content: center; /* 텍스트 가운데 정렬 */
  align-items: flex-end; /* 세로 정렬 */
  padding: 6px 16px; /* 내부 여백 */
  background: #636ACC; /* 배경색 */
  border-radius: 32px; /* 둥근 모서리 */
  color: white; /* 텍스트 색상 */
  font-size: 13px; /* 글씨 크기 */
  font-weight: 700; /* 글씨 굵기 */
  cursor: pointer; /* 클릭 가능한 커서 */
  width: auto; /* 버튼 너비를 텍스트에 맞춤 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 선택 사항: 버튼 그림자 */
  transition: transform 0.3s ease, background-color 0.3s ease; /* 선택 사항: 애니메이션 */
}

.btn:active {
  transform: scale(0.95); /* 살짝 줄어듦 */
  background-color: #5058cc; /* 색상 변화 */
}

.btn:hover {
  transform: scale(1.05); /* 호버 시 확대 효과 */
  background-color: #5058cc; /* 호버 시 배경색 변경 */
}

/* 반응형 설정 */
@media (max-width: 1700px) {
  .chatbot-layer {
    flex-direction: row; /* 작은 화면에서는 세로 배치 */
    gap: 40px;
    justify-content: space-evenly;
    align-items: flex-end; /* 세로 정렬 */
  }

  img {
    max-width: 150px; /* 이미지 크기 축소 */
  }

  .btn {
    font-size: 14px; /* 버튼 텍스트 크기 축소 */
    padding: 6px 12px;
  }
}
</style>
