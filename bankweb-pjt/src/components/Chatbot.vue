<template>
  <div class="chatbot-container">
    <div class="chatbot-header">
      <p class="chatbot-title"> <img src="@/assets/icon/bot_profile.png" height="25px">핀과의 메세지 :-)</p>
    </div>
    <div class="chatbot-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['chat-message', message.role]"
      >
        <div class="message-content" v-html="formatMessage(message.content)">
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

// 타이핑 상태를 위한 ref 추가
const isTyping = ref(false);


// 전역 상태 변수 정의
const messages = ref([
  {
    role: "assistant",
    content: `안녕하세요! 저는 BBK의 금융 서비스 챗봇 핀입니다. 😆
    어떤 도움을 드릴까요?

    아래에서 필요한 서비스를 선택해 주세요!

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

function formatMessage(content) {
  return content
    .replace(/\n/g, '<br>')  // 줄바꿈을 <br>태그로 변환
    .replace(/•/g, '&bull;')  // 불릿 포인트 변환
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // **텍스트** 를 <strong> 태그로 변환
    .replace(/^\s+/gm, '')    // 각 줄 시작의 불필요한 공백 제거
    .trim();
}

function extractLocation(message) {
  // 위치 관련 키워드 뒤에 오는 지역명 추출
  const locationKeywords = ['근처', '주변', '가까운', '위치', '찾아줘'];
  const message_lower = message.toLowerCase();
  
  // 기본 위치
  let location = "서울 강남구";
  
  // 메시지에서 위치 키워드가 있는지 확인
  for (const keyword of locationKeywords) {
    if (message_lower.includes(keyword)) {
      // 키워드 앞에 나오는 지역명 추출
      const beforeKeyword = message.split(keyword)[0].trim();
      if (beforeKeyword && beforeKeyword !== '') {
        location = beforeKeyword;
        break;
      }
    }
  }
  
  return location;
}

function sendMessage() {
  if (!userMessage.value.trim()) return;

  const formattedUserMessage = userMessage.value.trim();
  messages.value.push({ role: "user", content: formattedUserMessage });

  // 사용자 메시지 추가 후 스크롤
  scrollToBottom();
  
  isTyping.value = true;

  const queryLocation = extractLocation(formattedUserMessage);

  axios({
    method: "post",
    url: "http://127.0.0.1:8000/api/chatbot/",
    data: {
      message: formattedUserMessage,
      query: queryLocation
    }
  })
    .then((response) => {
      setTimeout(() => {
        const botResponse = response.data.response
            .replace(/\\n/g, '\n')
            .trim();
        
        messages.value.push({ 
            role: "assistant", 
            content: botResponse,
            data: response.data.data
        });

        scrollToBottom();
        
        // 특별한 데이터 처리
        if (response.data.data.type === 'location') {
            // 지도 표시 로직
            showMap(response.data.data.banks);
        } else if (response.data.data.type === 'exchange') {
            // 환율 차트 표시 로직
            showExchangeChart(response.data.data.exchange_rates);
        }
        
        isTyping.value = false;
      }, 500);
    })
    .catch(() => {
      isTyping.value = false;
      messages.value.push({
          role: "assistant",
          content: "오류가 발생했습니다. 다시 시도해 주세요.",
      });
    })
    .finally(() => {
      userMessage.value = "";
      scrollToBottom();
    });
}

// 메시지 목록 자동 스크롤 함수 수정
function scrollToBottom() {
  nextTick(() => {
    setTimeout(() => {  // 약간의 지연 추가
      const container = document.querySelector(".chatbot-messages");
      if (container) {
        container.scrollTo({
          top: container.scrollHeight,
          behavior: 'smooth'  // 부드러운 스크롤 효과 추가
        });
      }
    }, 100);  // 100ms 지연
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
  background: #3F75F2;
  overflow: hidden;
}

.chatbot-header {
  color: white;
  padding: 16px 20px;
  text-align: left;
}

.chatbot-title {
  font-size: 17px;
  font-weight: 500;
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #ffffff;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.2);
}

.chat-message {
  display: flex;
  margin-bottom: 10px;
  font-size: 15px;
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
  background: #3F75F2;
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
  padding: 10px 18px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
}

.chatbot-input button {
  margin-left: 10px;
  padding: 10px 15px;
  border: none;
  border-radius: 20px;
  background: #3F75F2;
  color: white;
  cursor: pointer;
}

.chatbot-input button:hover {
  background: #205ff1;
}

.message-content {
    max-width: 70%;
    padding: 10px 15px;
    border-radius: 20px;
    background: #e1e1e1;
    word-wrap: break-word;
    white-space: pre-line;  /* 줄바꿈 유지 */
    line-height: 1.4;       /* 줄간격 조정 */
}

/* 불릿 포인트가 있는 줄의 들여쓰기 */
.message-content ::v-deep(br) + • {
    margin-left: 1em;
}

/* 목록 스타일 개선 */
.message-content ::v-deep(ul) {
    margin: 0.5em 0;
    padding-left: 1.5em;
}

.message-content ::v-deep(li) {
    margin: 0.3em 0;
}


/* 헤더 타이틀 바운스 애니메이션 */
.animate-bounce {
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(-1px); }
    50% { transform: translateY(1px); }
}

/* 메시지 페이드 인 애니메이션 */
.message-fade-enter-active,
.message-fade-leave-active {
    transition: all 0.3s ease;
}

.message-fade-enter-from,
.message-fade-leave-to {
    opacity: 0;
    transform: translateY(20px);
}

/* 타이핑 인디케이터 */
.typing-indicator {
    display: flex;
    gap: 4px;
    padding: 10px 15px;
    background: #e1e1e1;
    border-radius: 20px;
    width: fit-content;
    margin: 10px 0;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    background: #666;
    border-radius: 50%;
    animation: typing 1s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: 0.1s; }
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.3s; }

@keyframes typing {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* 입력창 활성화 애니메이션 */
.chatbot-input input {
    transition: all 0.3s ease;
}

.input-active {
    box-shadow: 0 0 5px rgba(63, 117, 242, 0.5);
    border-color: #3F75F2 !important;
}

/* 버튼 호버 및 활성화 애니메이션 */
.chatbot-input button {
    transition: all 0.3s ease;
}

.button-active {
    transform: scale(1.05);
}

.chatbot-input button:hover {
    background: #205ff1;
    transform: scale(1.05);
}

/* 스크롤바 스타일링 */
.chatbot-messages::-webkit-scrollbar {
    width: 6px;
}

.chatbot-messages::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.chatbot-messages::-webkit-scrollbar-thumb {
    background: #3F75F2;
    border-radius: 3px;
}

.chatbot-messages::-webkit-scrollbar-thumb:hover {
    background: #205ff1;
}

/* 메시지 호버 효과 */
.message-content {
    transition: all 0.2s ease;
}

.message-content:hover {
    transform: scale(1.02);
}

/* 챗봇 컨테이너 시작 애니메이션 */
.chatbot-container {
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 링크 스타일 */
.message-content ::v-deep(a) {
    color: #3F75F2;
    text-decoration: none;
    transition: all 0.2s ease;
}

.message-content ::v-deep(a:hover) {
    text-decoration: underline;
    opacity: 0.8;
}

/* 강조 텍스트 애니메이션 */
.message-content ::v-deep(strong) {
    background: linear-gradient(120deg, rgba(63, 117, 242, 0.2) 0%, rgba(63, 117, 242, 0.2) 100%);
    background-repeat: no-repeat;
    background-size: 100% 0.2em;
    background-position: 0 88%;
    transition: all 0.25s ease;
}

.message-content ::v-deep(strong:hover) {
    background-size: 100% 100%;
}
</style>