<template>
  <div class="app-container">
    <header>
      <CommonHeader />
    </header>
    <div class="RouterView-div">
      <RouterView />
    </div>
    <footer ref="footerRef">
      <CommonFooter />
    </footer>
    <!-- 챗봇 -->
    <Transition name="bounce">
      <v-card v-show="expand" :class="['expand-component', { 'raised': isFooterVisible }]" height="600" width="400">
        <Chatbot />
      </v-card>
    </Transition>

    <p :class="['chatbot-info', { 'raised': isFooterVisible }]">
      AI챗봇에게 물어보세요!
    </p>
    <v-avatar @click="expand = !expand" :class="['chatbot-btn', { 'raised': isFooterVisible }]" size="90"
      color="transparent">
      <img src="@/assets/icon/botIcon.png" height="90px" alt="" />
    </v-avatar>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import CommonHeader from "@/components/CommonHeader.vue";
import CommonFooter from "@/components/CommonFooter.vue";
import Chatbot from "@/components/Chatbot.vue";
import { ref, onMounted, onUnmounted } from "vue";

const expand = ref(false);
const footerRef = ref(null);
const isFooterVisible = ref(false);

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      isFooterVisible.value = entry.isIntersecting;
    },
    {
      threshold: 0,
    }
  );

  if (footerRef.value) {
    observer.observe(footerRef.value);
  }

  // 컴포넌트가 제거될 때 observer도 정리
  onUnmounted(() => {
    observer.disconnect();
  });
});
</script>

<style scoped>
/* 기존 스타일 유지 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.RouterView-div {
  background: #f3f6f8;
  padding-top: 40px;
  padding-bottom: 40px;
  flex: 1;
}

footer {
  margin-top: auto;
}

.expand-component {
  position: fixed;
  bottom: 70px;
  right: 180px;
  z-index: 1000;
  transition: bottom 0.3s ease;
}

.expand-component.raised {
  bottom: 170px;
  /* footer가 보일 때 더 위로 올라감 */
}

.chatbot-btn {
  position: fixed;
  bottom: 60px;
  right: 60px;
  z-index: 1000;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chatbot-btn.raised {
  bottom: 160px;
  /* footer가 보일 때 더 위로 올라감 */
}

.chatbot-info {
  color: grey;
  font-size: 14px;
  position: fixed;
  bottom: 20px;
  right: 65px;
  z-index: 1000;
  transition: bottom 0.3s ease;
}

.chatbot-info.raised {
  bottom: 120px;
  /* footer가 보일 때 더 위로 올라감 */
}

/* 나머지 기존 스타일 유지 */
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

.chatbot-btn:hover {
  transform: translateY(-5px);
}
</style>