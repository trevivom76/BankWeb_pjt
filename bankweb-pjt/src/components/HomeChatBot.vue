<template>
  <div class="box">
    <div class="chatbot-layer">
      <img class="chatbot" src="@/assets/icon/MessageIcon.png" alt="챗봇 아이콘" />
      <img src="@/assets/icon/chatbotText.png" alt="챗봇 메세지" />
      <div class="btn-layer">
        <button class="btn" @click="clickLink">챗봇 바로가기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { emitter } from '@/utils/eventBus';

const clickLink = () => {
  emitter.emit('open-chatbot');
}
</script>

<style scoped>
.box {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 36px;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.chatbot-layer {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
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

  0%,
  100% {
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
  animation: fadeIn 1s ease-in-out, shake 0.7s ease-in-out 1.2s infinite;
}

img {
  width: 100%;
  height: auto;
  max-width: 200px;
  object-fit: contain;
  padding-bottom: 20px;
}

.btn-layer {
  display: flex;
  justify-content: center;
  width: 100%;
}

.btn {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  padding: 6px 16px;
  background: #636ACC;
  border-radius: 32px;
  color: white;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  width: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.btn:active {
  transform: scale(0.95);
  background-color: #5058cc;
}

.btn:hover {
  transform: scale(1.05);
  background-color: #5058cc;
}

@media (max-width: 1200px) {
  .chatbot-layer {
    flex-direction: row;
    gap: 40px;
    justify-content: space-evenly;
    align-items: flex-end;
  }

  img {
    max-width: 150px;
  }

  .btn {
    font-size: 14px;
    padding: 6px 12px;
  }
}
</style>
