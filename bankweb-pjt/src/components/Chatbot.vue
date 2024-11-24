<template>
    <div class="chatbot-container">
        <div class="chatbot-header">
        <h2>BBK 금융 서비스 챗봇 "핀" 😊</h2>
        </div>
        <div class="chatbot-messages" ref="messagesContainer">
        <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['chat-message', message.role]"
        >
            <div class="message-content">
            {{ message.content }}
            </div>
        </div>
        </div>
        <div class="chatbot-input">
        <input
            v-model="userMessage"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="메시지를 입력하세요..."
        />
        <button @click="sendMessage">전송</button>
        </div>
    </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import axios from "axios";
import { useProfileStore } from "@/stores/profile";

// 전역 상태 변수 정의
const messages = ref([
  {
    role: "assistant",
    content: `
    안녕하세요! 저는 BBK의 금융 서비스 챗봇 핀입니다. 😆\n 
    어떤 도움을 드릴까요?\n
\n
    아래에서 필요한 서비스를 선택해 주세요!\n
\n
    1️⃣ 예적금 상품 추천
    2️⃣ 🏦 주변 은행 위치 찾기
    3️⃣ 🌎 환율 계산기
    4️⃣ 📊 금융 상품 비교
    5️⃣ 💬 기타 문의

    원하시는 서비스를 번호로 입력하거나 직접 질문을 입력해 주세요!
    예) “금리가 높은 적금 추천해주세요” 또는 “가까운 은행 찾아줘”
    `,
  },
]);

const userMessage = ref("");

// 함수 정의
function sendMessage() {
  if (!userMessage.value.trim()) return;

  // 사용자 메시지 추가
  messages.value.push({ role: "user", content: userMessage.value });

  // 서버에 메시지 전송
  axios({
    method:"post",
    url:"http://127.0.0.1:8000/api/chatbot/",
    data:{
        message: userMessage.value,
    }
  })
    .then((response) => {
      // 챗봇 응답 추가
      messages.value.push({ role: "assistant", content: response.data.response });
    })
    .catch(() => {
      // 오류 발생 시 처리
      messages.value.push({
        role: "assistant",
        content: "오류가 발생했습니다. 다시 시도해 주세요.",
      });
    })
    .finally(() => {
      // 입력 필드 초기화 및 스크롤 이동
      userMessage.value = "";
      scrollToBottom();
    });
}

// 메시지 목록 자동 스크롤
function scrollToBottom() {
  nextTick(() => {
    const container = document.querySelector(".chatbot-messages");
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
}

</script>
<style scoped>
.chatbot-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 400px;
  height: 600px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background: #f9f9f9;
  overflow: hidden;
}

.chatbot-header {
  background: #007bff;
  color: white;
  padding: 15px;
  text-align: center;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #fff;
}

.chat-message {
  display: flex;
  margin-bottom: 10px;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 20px;
  background: #e1e1e1;
  word-wrap: break-word;
}

.chat-message.user .message-content {
  background: #007bff;
  color: white;
}

.chatbot-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
  background: #f9f9f9;
}

.chatbot-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
}

.chatbot-input button {
  margin-left: 10px;
  padding: 10px 15px;
  border: none;
  border-radius: 20px;
  background: #007bff;
  color: white;
  cursor: pointer;
}

.chatbot-input button:hover {
  background: #0056b3;
}
</style>