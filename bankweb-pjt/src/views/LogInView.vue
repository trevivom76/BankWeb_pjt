<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- 로고 섹션 -->
      <div class="logo-section">
        <img src="@/assets/icon/BBK_Logo.png" alt="" height="50px">
        <p class="welcome-text">환영합니다! 서비스 이용을 위해 로그인해주세요.</p>
      </div>

      <!-- 로그인 폼 -->
      <div class="login-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <div class="input-wrapper">
            <input
              id="username"
              v-model="username"
              type="text"
              :class="{ 'error': !usernameIsOk }"
              placeholder="아이디를 입력해주세요"
              @keyup.enter="logIn()"
            />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <div class="input-wrapper">
            <input
              id="password"
              v-model="password"
              :type="show1 ? 'text' : 'password'"
              :class="{ 'error': !passwordIsOk }"
              placeholder="비밀번호를 입력해주세요"
              @keyup.enter="logIn()"
            />
            <span class="input-icon clickable" @click="show1 = !show1">
              <svg v-if="!show1" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 2L22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6.71277 6.7226C3.66479 8.79527 2 12 2 12C2 12 5.63636 19 12 19C14.0503 19 15.8174 18.2734 17.2711 17.2884M11 5.05822C11.3254 5.02013 11.6588 5 12 5C18.3636 5 22 12 22 12C22 12 21.3082 13.3317 20 14.8335" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M14 14.2362C13.4692 14.7112 12.7684 15.0001 12 15.0001C10.3431 15.0001 9 13.657 9 12.0001C9 11.1764 9.33193 10.4303 9.86932 9.88818" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5C18.3636 5 22 12 22 12C22 12 18.3636 19 12 19C5.63636 19 2 12 2 12C2 12 5.63636 5 12 5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
          <span class="hint-text">최소 8자 이상, 최대 16자 이하</span>
        </div>

        <!-- 에러 메시지 -->
        <div v-if="accountStore.loginErrorMessage?.non_field_errors" class="error-message">
          아이디 또는 비밀번호가 올바르지 않습니다.
        </div>

        <div v-if="!usernameIsOk" class="error-message">
          아이디를 입력해주세요
        </div>

        <div v-if="!passwordIsOk" class="error-message">
          비밀번호를 확인해주세요 (8-16자)
        </div>

        <!-- 로그인 버튼 -->
        <button 
          class="login-button" 
          @click.prevent="logIn()"
        >
          로그인
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { onMounted, onUnmounted, ref, watch } from "vue";

const accountStore = useAccountStore();

const username = ref("");
const password = ref("");

// 비밀번호 공개/비공개상태 변수
const show1 = ref(false);

// 입력값 검증 상태 변수
const usernameIsOk = ref(true);
const passwordIsOk = ref(true);

// 폼 입력값이 변경될 때마다 에러 메시지 초기화
watch([username, password], () => {
  accountStore.loginErrorMessage = {};
});

// 컴포넌트가 마운트될 때 에러 메시지 초기화
onMounted(() => {
  accountStore.loginErrorMessage = {};
});

// 컴포넌트가 언마운트될 때(페이지를 벗어날 때) 에러 메시지 초기화
onUnmounted(() => {
  accountStore.loginErrorMessage = {};
});

// userId 규칙
const username_rules = {
  required: (value) => !!value || "아이디를 입력해주세요.",
};

// password 규칙
const pw_rules = {
  required: (value) => !!value || "비밀번호를 입력해주세요.",
  min: (v) => v.length >= 8 || "비밀번호는 최소 8자 이상입니다.",
  max: (v) => v.length <= 16 || "비밀번호는 최대 16자 입니다.",
};

// Log In 버튼 클릭시 이상이 없는지 확인
const logIn = async function () {
  // id가 입력되었는지 확인
  usernameIsOk.value = username_rules.required(username.value) === true;

  // password가 입력되었는지 확인
  passwordIsOk.value = pw_rules.required(password.value) === true;

  // 비밀번호 길이 확인 (8자 이상, 16자 이하)
  if (password.value.length < 8 || password.value.length > 16) {
    passwordIsOk.value = false;
  }

  // 입력에 이상이 없을시 서버에 로그인 정보를 넘기기
  if (usernameIsOk.value && passwordIsOk.value) {
    const payload = {
      username: username.value,
      password: password.value,
    };

    await accountStore.logIn(payload);
  }
};
</script>

<style scoped>
.login-container {
  height: auto;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.login-wrapper {
  width: 100%;
  max-width: 440px;
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.logo-section {
  display: flexbox;
  flex-direction: column;
  text-align: center;
  margin-bottom: 32px;
}

.welcome-text {
  color: #64748b;
  font-size: 16px;
  line-height: 2;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.hint-text {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  display: flex;
  align-items: center;
}

.input-icon.clickable {
  cursor: pointer;
}

input {
  width: 100%;
  padding: 14px 16px;
  padding-right: 48px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.5;
  color: #334155;
  transition: all 0.2s ease;
}

input::placeholder {
  color: #94a3b8;
}

input:focus {
  outline: none;
  border-color: #5A87F2;
  box-shadow: 0 0 0 3px rgba(99, 106, 204, 0.15);
}

input.error {
  border-color: #ef4444;
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  padding: 8px 12px;
  background: #fef2f2;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.login-button {
  background: #5A87F2;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 8px;
}

.login-button:hover {
  background: #4A77E2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 106, 204, 0.2);
}

.login-button:active {
  transform: translateY(0);
}

@media (max-width: 480px) {
  .login-wrapper {
    padding: 24px;
  }

  .brand-title {
    font-size: 28px;
  }

  .welcome-text {
    font-size: 14px;
  }

  input {
    padding: 12px 14px;
    font-size: 14px;
  }

  .login-button {
    padding: 14px;
    font-size: 15px;
  }
}

/* 로그인 카드 애니메이션 */
.login-wrapper {
  opacity: 0;
  animation: slideUp 0.8s ease-out forwards;
}

/* 로고 섹션 애니메이션 */
.logo-section img {
  opacity: 0;
  transform: scale(0.8);
  animation: logoAppear 0.6s ease-out 0.4s forwards;
}

.welcome-text {
  opacity: 0;
  animation: fadeIn 0.6s ease-out 0.8s forwards;
}

/* 폼 그룹 애니메이션 */
.form-group {
  opacity: 0;
  transform: translateX(-20px);
  animation: slideInRight 0.6s ease-out forwards;
}

.form-group:nth-child(1) {
  animation-delay: 1s;
}

.form-group:nth-child(2) {
  animation-delay: 1.2s;
}

/* 로그인 버튼 애니메이션 */
.login-button {
  opacity: 0;
  animation: slideUp 0.6s ease-out 1.4s forwards;
}

/* 에러 메시지 애니메이션 */
.error-message {
  animation: shake 0.5s ease-in-out;
}

/* 애니메이션 키프레임 정의 */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes logoAppear {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
  20%, 40%, 60%, 80% { transform: translateX(2px); }
}
</style>
