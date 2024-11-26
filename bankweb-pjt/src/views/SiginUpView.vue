<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- 로고 섹션 -->
      <div class="logo-section">
        <img src="@/assets/icon/BBK_Logo.png" alt="" height="50px">
        <p class="welcome-text">환영합니다! BB뱅크의 회원이 되어주세요.</p>
      </div>

      <!-- 회원가입 폼 -->
      <div class="login-form">
        <!-- 아이디 입력 -->
        <div class="form-group">
          <label for="username">아이디</label>
          <div class="input-wrapper">
            <input
              id="username"
              v-model="username"
              type="text"
              :class="{ 'error': !usernameIsOk }"
              placeholder="아이디를 입력해주세요"
            />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- 이름 입력 -->
        <div class="form-group">
          <label for="name">이름</label>
          <div class="input-wrapper">
            <input
              id="name"
              v-model="name"
              type="text"
              :class="{ 'error': !nameIsOk }"
              placeholder="홍길동"
            />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- 닉네임 입력 -->
        <div class="form-group">
          <label for="nickname">닉네임</label>
          <div class="input-wrapper">
            <input
              id="nickname"
              v-model="nickname"
              type="text"
              :class="{ 'error': !nicknameIsOk }"
              placeholder="닉네임을 입력해주세요"
            />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 16l-3-3 3-3m-6 0l-3 3 3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- 비밀번호 입력 -->
        <div class="form-group">
          <label for="password1">비밀번호</label>
          <div class="input-wrapper">
            <input
              id="password1"
              v-model="password1"
              :type="show1 ? 'text' : 'password'"
              :class="{ 'error': !password1IsOk }"
              placeholder="비밀번호를 입력해주세요"
            />
            <span class="input-icon clickable" @click="show1 = !show1">
              <svg v-if="!show1" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 2L22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6.71277 6.7226C3.66479 8.79527 2 12 2 12C2 12 5.63636 19 12 19C14.0503 19 15.8174 18.2734 17.2711 17.2884M11 5.05822C11.3254 5.02013 11.6588 5 12 5C18.3636 5 22 12 22 12C22 12 21.3082 13.3317 20 14.8335" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5C18.3636 5 22 12 22 12C22 12 18.3636 19 12 19C5.63636 19 2 12 2 12C2 12 5.63636 5 12 5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
          <span class="hint-text">최소 8자 이상, 최대 16자 이하</span>
        </div>

        <!-- 비밀번호 확인 입력 -->
        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <div class="input-wrapper">
            <input
              id="password2"
              v-model="password2"
              :type="show2 ? 'text' : 'password'"
              :class="{ 'error': !password2IsOk }"
              placeholder="비밀번호를 다시 입력해주세요"
            />
            <span class="input-icon clickable" @click="show2 = !show2">
              <svg v-if="!show2" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 2L22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M6.71277 6.7226C3.66479 8.79527 2 12 2 12C2 12 5.63636 19 12 19C14.0503 19 15.8174 18.2734 17.2711 17.2884M11 5.05822C11.3254 5.02013 11.6588 5 12 5C18.3636 5 22 12 22 12C22 12 21.3082 13.3317 20 14.8335" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5C18.3636 5 22 12 22 12C22 12 18.3636 19 12 19C5.63636 19 2 12 2 12C2 12 5.63636 5 12 5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- 이메일 입력 -->
        <div class="form-group">
          <label for="email">이메일</label>
          <div class="input-wrapper">
            <input
              id="email"
              v-model="email"
              type="email"
              :class="{ 'error': !emailIsOk }"
              placeholder="example@naver.com"
            />
            <span class="input-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" stroke="currentColor" stroke-width="2"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- 체크박스 그룹 -->
        <div class="checkbox-group">
          <label class="checkbox-wrapper">
            <input 
              type="checkbox" 
              v-model="checkbox1"
              :class="{ 'error': !checkboxsIsOk }"
            >
            <span class="checkbox-label">(필수) 서비스 이용 약관 동의</span>
          </label>
          <label class="checkbox-wrapper">
            <input 
              type="checkbox" 
              v-model="checkbox2"
              :class="{ 'error': !checkboxsIsOk }"
            >
            <span class="checkbox-label">(필수) 개인정보 처리 동의</span>
          </label>
        </div>

        <!-- 에러 메시지들 -->
        <div v-if="accountStore.signUpErrorMessage?.username" class="error-message">
          중복된 아이디입니다.
        </div>

        <div v-if="accountStore.signUpErrorMessage?.password1" class="error-message">
          비밀번호가 너무 단순합니다.
        </div>

        <div v-if="accountStore.signUpErrorMessage?.nickname" class="error-message">
          {{ accountStore.signUpErrorMessage.nickname[0] }}
        </div>

        <div v-if="accountStore.signUpErrorMessage?.name" class="error-message">
          {{ accountStore.signUpErrorMessage.name[0] }}
        </div>

        <div v-if="!usernameIsOk" class="error-message">
          아이디를 입력해주세요
        </div>

        <div v-if="!nameIsOk" class="error-message">
          이름을 입력해주세요
        </div>

        <div v-if="!nicknameIsOk" class="error-message">
          닉네임을 입력해주세요
        </div>

        <div v-if="!password1IsOk" class="error-message">
          비밀번호를 확인해주세요
        </div>

        <div v-if="!password2IsOk" class="error-message">
          비밀번호 확인란을 확인해주세요
        </div>

        <div v-if="!passwordsIsOk" class="error-message">
          비밀번호와 비밀번호 확인이 같지 않습니다
        </div>

        <div v-if="!emailIsOk" class="error-message">
          이메일을 올바르게 입력해 주세요
        </div>

        <div v-if="!checkboxsIsOk" class="error-message">
          이용약관에 동의해주세요
        </div>

        <!-- 회원가입 버튼 -->
        <button 
          class="login-button" 
          @click.prevent="signUp()"
        >
          회원가입
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
const name = ref("");
const nickname = ref(null);
const password1 = ref("");
const password2 = ref("");
const email = ref("");

// 비밀번호 공개/비공개상태 변수
const show1 = ref(false);
const show2 = ref(false);

// 이용약관1, 2 체크박스상태 변수
const checkbox1 = ref(false);
const checkbox2 = ref(false);

const usernameIsOk = ref(true);
const password1IsOk = ref(true);
const password2IsOk = ref(true);
const passwordsIsOk = ref(true);
const checkboxsIsOk = ref(true);
const nameIsOk = ref(true);
const nicknameIsOk = ref(true);
const emailIsOk = ref(true);

// 폼 입력값이 변경될 때마다 에러 메시지 초기화
watch([username, password1, password2, nickname, name], () => {
  accountStore.signUpErrorMessage = {};
});

// 컴포넌트가 마운트될 때 에러 메시지 초기화
onMounted(() => {
  accountStore.signUpErrorMessage = {};
});

// 컴포넌트가 언마운트될 때(페이지를 벗어날 때) 에러 메시지 초기화
onUnmounted(() => {
  accountStore.signUpErrorMessage = {};
});

// udseId 규칙
const username_rules = {
  required: (value) => !!value || "아이디는 필수 입력 사항입니다.",
};

// name 규칙
const name_rules = {
  required: (value) => !!value || "이름은 필수 입력 사항입니다.",
};

// nickname 규칙
const nickname_rules = {
  required: (value) => !!value || "닉네임은 필수 입력 사항입니다.",
};

// password1 규칙
const pw1_rules = {
  required: (value) => !!value || "비밀번호는 필수 입력 사항입니다.",
  min: (v) => v.length >= 8 || "비밀번호는 최소 8자 이상이어야 합니다.",
  max: (v) => v.length <= 16 || "비밀번호는 최대 16자 입니다.",
};

// password2 규칙
const pw2_rules = {
  required: (value) => !!value || "비밀번호는 필수 입력 사항입니다.",
  min: (v) => v.length >= 8 || "비밀번호는 최소 8자 이상이어야 합니다.",
  max: (v) => v.length <= 16 || "비밀번호는 최대 16자 입니다.",
  match: (v) => v === password1.value || "비밀번호가 일치하지 않습니다.",
};

// email 형식 검증 규칙
const email_rules = {
  format: (value) => {
    if (!value) return true; // 선택사항이므로 빈 값은 허용

    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailPattern.test(value) || "이메일을 올바르게 입력해 주세요";
  },
};

// SIGN UP 버튼 클릭시 이상이 없는지 확인
const signUp = function () {
  // id가 입력되었는지 확인
  usernameIsOk.value = username_rules.required(username.value) === true;

  // 이름이 입력되었는지 확인
  nameIsOk.value = name_rules.required(name.value) === true;

  // 닉네임이 입력되었는지 확인
  nicknameIsOk.value = nickname_rules.required(nickname.value) === true;

  // password1이 입력되었는지 확인
  password1IsOk.value = pw1_rules.required(password1.value) === true;

  // password2가 입력되었는지 확인
  password2IsOk.value = pw2_rules.required(password2.value) === true;

  // 이메일이 입력되었다면 형식 검증
  if (email.value) {
    emailIsOk.value = email_rules.format(email.value) === true;
  } else {
    emailIsOk.value = true; // 이메일은 선택사항이므로 입력하지 않았을 때는 true
  }

  // 비밀번호 길이 확인 (8자 이상, 16자 이하)
  if (password1.value.length < 8 || password1.value.length > 16) {
    password1IsOk.value = false;
  }

  if (password2.value.length < 8 || password2.value.length > 16) {
    password2IsOk.value = false;
  }

  // 비밀번호 확인 일치 여부
  if (password1.value !== password2.value) {
    passwordsIsOk.value = false;
  } else {
    passwordsIsOk.value = true;
  }

  // 이용약관1, 2 체크 여부
  if (!checkbox1.value || !checkbox2.value) {
    checkboxsIsOk.value = false;
  } else {
    checkboxsIsOk.value = true;
  }

  // 입력에 이상이 없을시 서버에 회원가입 정보를 넘기기
  if (usernameIsOk.value && password1IsOk.value && password2IsOk.value && passwordsIsOk.value && nameIsOk.value && nicknameIsOk.value && checkboxsIsOk.value && emailIsOk.value) {
    const payload = {
      // 아이디
      username: username.value,
      // 비밀번호 1
      password1: password1.value,
      // 비밀번호 2
      password2: password2.value,
      // 닉네임
      nickname: nickname.value,
      // 사용자 이름
      name: name.value,
      // 이메일
      email: email.value,
    };
    accountStore.signUp(payload);
  }
};
</script>

<style scoped>
/* 로그인 페이지와 동일한 기본 스타일 */
.login-container {
  height: auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

.login-wrapper {
  width: 100%;
  max-width: 440px;
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  opacity: 0;
  animation: slideUp 0.8s ease-out forwards;
}

/* 로고 섹션 스타일 */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 32px;
}

.logo-section img {
  opacity: 0;
  transform: scale(0.8);
  animation: logoAppear 0.6s ease-out 0.4s forwards;
}

.welcome-text {
  color: #64748b;
  font-size: 16px;
  line-height: 2;
  opacity: 0;
  animation: fadeIn 0.6s ease-out 0.8s forwards;
}

/* 폼 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  opacity: 0;
  transform: translateX(-20px);
  animation: slideInRight 0.6s ease-out forwards;
}

/* 각 폼 그룹에 순차적 애니메이션 적용 */
.form-group:nth-child(1) { animation-delay: 1.0s; }
.form-group:nth-child(2) { animation-delay: 1.1s; }
.form-group:nth-child(3) { animation-delay: 1.2s; }
.form-group:nth-child(4) { animation-delay: 1.3s; }
.form-group:nth-child(5) { animation-delay: 1.4s; }
.form-group:nth-child(6) { animation-delay: 1.5s; }

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

/* 체크박스 스타일링 */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  opacity: 0;
  animation: fadeIn 0.6s ease-out 1.6s forwards;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-wrapper input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label {
  font-size: 14px;
  color: #475569;
}

/* 에러 메시지 */
.error-message {
  color: #ef4444;
  font-size: 14px;
  padding: 8px 12px;
  background: #fef2f2;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: shake 0.5s ease-in-out;
}

/* 회원가입 버튼 */
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
  opacity: 0;
  animation: slideUp 0.6s ease-out 1.8s forwards;
}

.login-button:hover {
  background: #4A77E2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 106, 204, 0.2);
}

.login-button:active {
  transform: translateY(0);
}

/* 애니메이션 키프레임 */
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
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

/* 반응형 디자인 */
@media (max-width: 480px) {
  .login-wrapper {
    padding: 24px;
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

  .checkbox-label {
    font-size: 13px;
  }
}
</style>
