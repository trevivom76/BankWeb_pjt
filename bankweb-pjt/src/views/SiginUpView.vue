<template>
  <div>
    <!-- 로그인 화면 로고 -->
    <h1 class="my-6 text-center">
      Sign Up to
      <span class="text-blue-lighten-2">MYBank</span>
    </h1>

    <!-- 로그인 card -->
    <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
      <!-- 아이디 입력 text-field -->
      <v-text-field class="my-2" :rules="[username_rules.required]" v-model="username" color="primary" label="아이디" variant="outlined"></v-text-field>

      <!-- 이름 입력 text-field -->
      <v-text-field 
        class="my-2" 
        v-model="name" 
        :rules="[name_rules.required]"
        color="primary" 
        label="이름" 
        placeholder="홍길동" 
        variant="outlined"
      ></v-text-field>

      <!-- 닉네임 입력 text-field -->
      <v-text-field 
        class="my-2" 
        v-model="nickname" 
        :rules="[nickname_rules.required]"
        color="primary" 
        label="닉네임" 
        placeholder="닉네임" 
        variant="outlined"
      ></v-text-field>

      <!-- "비밀번호" 입력 text-field -->
      <v-text-field
        class="my-2"
        v-model="password1"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[pw1_rules.required, pw1_rules.min, pw1_rules.max]"
        :type="show1 ? 'text' : 'password'"
        hint="최소8자 이상 최대16자이하"
        color="primary"
        label="비밀번호"
        variant="outlined"
        name="input-10-1"
        counter
        @click:append="show1 = !show1"
      ></v-text-field>

      <!-- "비밀번호 확인" 입력 text-field -->
      <v-text-field
        class="my-2"
        v-model="password2"
        :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[pw2_rules.required, pw2_rules.min, pw2_rules.max, pw2_rules.match]"
        :type="show2 ? 'text' : 'password'"
        hint="최소8자 이상 최대16자이하"
        color="primary"
        label="비밀번호 확인"
        variant="outlined"
        name="input-10-2"
        counter
        @click:append="show2 = !show2"
      ></v-text-field>

      <!-- 이메일 입력 text-field -->
      <v-text-field 
        v-model="email" 
        :rules="[email_rules.format]"
        color="primary" 
        label="이메일" 
        variant="outlined" 
        placeholder="(선택사항)"
      ></v-text-field>

      <!-- 이용약관 체크박스1 -->
      <v-checkbox density="compact" v-model="checkbox1" :rules="[(v1) => !!v1 || '서비스 이용 약관에 동의해주세요.']" label="(필수) 서비스 이용 약관 동의" required></v-checkbox>

      <!-- 이용약관 체크박스2 -->
      <v-checkbox density="compact" v-model="checkbox2" :rules="[(v2) => !!v2 || '개인정보 처리에 동의해주세요.']" label="(필수) 개인정보 처리 동의" required></v-checkbox>

    <!-- 아이디 중복 에러 -->
    <v-alert
      v-if="accountStore.signUpErrorMessage?.username"
      class="my-2"
      type="error"
      text="중복된 아이디입니다."
      variant="tonal"
    ></v-alert>

    <!-- 비밀번호 관련 에러 -->
    <v-alert
      v-if="accountStore.signUpErrorMessage?.password1"
      class="my-2"
      type="error"
      text="비밀번호가 너무 단순합니다."
      variant="tonal"
    ></v-alert>

    <!-- 닉네임 관련 에러 -->
    <v-alert
      v-if="accountStore.signUpErrorMessage?.nickname"
      class="my-2"
      type="error"
      variant="tonal"
      :text="accountStore.signUpErrorMessage.nickname[0]"
    ></v-alert>

    <!-- 이름 관련 에러 -->
    <v-alert
      v-if="accountStore.signUpErrorMessage?.name"
      class="my-2"
      type="error"
      variant="tonal"
      :text="accountStore.signUpErrorMessage.name[0]"
    ></v-alert>

      <!-- 아이디를 입력하지 않았을때 -->
      <v-alert v-if="!usernameIsOk" class="my-2" text="아이디를 입력해주세요" type="error" variant="tonal"></v-alert>

      <!-- 이름 입력 확인 -->
      <v-alert v-if="!nameIsOk" class="my-2" text="이름을 입력해주세요" type="error" variant="tonal"></v-alert>

      <!-- 닉네임 입력 확인 -->
      <v-alert v-if="!nicknameIsOk" class="my-2" text="닉네임을 입력해주세요" type="error" variant="tonal"></v-alert>

      <!-- "비밀 번호"를 입력/길이조건에 맞게 입력하지 않았을때 -->
      <v-alert v-if="!password1IsOk" class="my-2" text="비밀번호를 확인해주세요" type="error" variant="tonal"></v-alert>

      <!-- "비밀번호 확인"을 입력/길이조건에 맞게 입력하지 않았을때 -->
      <v-alert v-if="!password2IsOk" class="my-2" text="비밀번호 확인란을 확인해주세요" type="error" variant="tonal"></v-alert>

      <!-- 입력은 했으나 "비밀번호 !== 비밀번호 확인" 일때 -->
      <v-alert v-if="!passwordsIsOk" class="my-2" text="비밀번호와 비밀번호 확인이 같지 않습니다." type="error" variant="tonal"></v-alert>

        <!-- 이메일 형식 에러 -->
      <v-alert 
        v-if="!emailIsOk" 
        class="my-2" 
        text="이메일을 올바르게 입력해 주세요" 
        type="error"
        variant="tonal"
      ></v-alert>

      <!-- 이용약관(체크박스)에 체크하지 않은 경우 -->
      <v-alert v-if="!checkboxsIsOk" class="my-2" text="이용약관에 동의해주세요." type="error" variant="tonal"></v-alert>

      <v-hover v-slot="{ isHovering, props }">
        <v-btn :class="{ 'on-hover': isHovering }" :elevation="isHovering ? 10 : 2" v-bind="props" class="mt-3 ,mb-8" color="blue-darken-1" size="large" block @click.prevent="signUp()">
          <p class="font-weight-bold text-white">SIGN UP</p>
        </v-btn>
      </v-hover>
    </v-card>
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
    return emailPattern.test(value) || '이메일을 올바르게 입력해 주세요';
  }
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
  if (usernameIsOk.value && 
      password1IsOk.value && 
      password2IsOk.value && 
      passwordsIsOk.value && 
      nameIsOk.value && 
      nicknameIsOk.value && 
      checkboxsIsOk.value && 
      emailIsOk.value) {
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
      email: email.value
    };
    accountStore.signUp(payload);
  }
};
</script>

<style scoped></style>
