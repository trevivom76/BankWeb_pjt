<template>
  <div>
    <header>
      <CommonHeader />
    </header>

    <div class="RouterView-div">
      <RouterView />
    </div>
    <!-- 챗봇 -->
    <Transition name="bounce">
      <v-card v-show="expand" style="position: fixed; bottom: 130px; right: 50px; z-index: 1000" class="expand-component" height="600" width="400">
        <Chatbot />
      </v-card>
    </Transition>
    <p class="chatbot-info">AI챗봇에게 물어보세요!</p>
    <v-avatar @click="expand = !expand" class="chatbot-btn" size="90" color="transparent">
    </v-avatar>

  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import CommonHeader from "./components/CommonHeader.vue";
import Chatbot from "@/components/Chatbot.vue";
import { ref } from "vue";

const expand = ref(false);

</script>

<style scoped>
.RouterView-div {
  background: #f3f6f8;
  padding-top: 40px;
  padding-bottom: 40px;
}
.expand-container {
  text-align: right;
  position: fixed;
  bottom: 20px; /* 원하는 위치로 조절하세요 */
  right: 20px; /* 원하는 위치로 조절하세요 */
  z-index: 1000; /* 다른 요소 위로 배치되도록 설정 */
}
.expand-component {
  position: fixed;
  bottom: 20px; /* 원하는 위치로 조절하세요 */
  right: 20px; /* 원하는 위치로 조절하세요 */
  z-index: 1000; /* 다른 요소 위로 배치되도록 설정 */
}
.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0.5);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.chatbot-btn {
  /* background-color: rgba(253, 248, 222, 0.658); */
  position: fixed;
  bottom: 50px;
  right: 100px;
  z-index: 1000;
  padding: 10px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.chatbot-btn:hover {
  transform: translateY(-5px);
}

.chatbot-info {
  color: grey;
  font-size: 14px;
  position: fixed;
  bottom: 35px;
  right: 75px;
  z-index: 1000;
}
</style>
