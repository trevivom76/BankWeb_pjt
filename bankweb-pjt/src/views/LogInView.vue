<template>
  <div>
    <!-- 로그인 화면 로고 -->
    <h1 class="my-6 text-center">
      Log In to
      <span class="text-blue-lighten-2">BB뱅크</span>
    </h1>

    <!-- 로그인 card -->
    <v-card class="mx-auto pa-12 pb-8" elevation="8" max-width="448" rounded="lg">
      <!-- 아이디 입력 text-field -->
      <v-text-field class="my-2" :rules="[username_rules.required]" v-model="username" color="primary" label="아이디" variant="outlined" @keyup.enter="logIn()"></v-text-field>

      <!-- "비밀번호" 입력 text-field -->
      <v-text-field
        class="my-2"
        v-model="password"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[pw_rules.required, pw_rules.min, pw_rules.max]"
        :type="show1 ? 'text' : 'password'"
        hint="최소8자 이상 최대16자이하"
        color="primary"
        label="비밀번호"
        variant="outlined"
        name="input-10-1"
        counter
        @click:append="show1 = !show1"
        @keyup.enter="logIn()"
      ></v-text-field>

      <!-- 서버에서 받은 에러 메시지 -->
      <v-alert v-if="accountStore.loginErrorMessage?.non_field_errors" class="my-2" type="error" variant="tonal">아이디 또는 비밀번호가 올바르지 않습니다.</v-alert>

      <!-- 입력값 검증 에러 메시지 -->
      <v-alert v-if="!usernameIsOk" class="my-2" text="아이디를 입력해주세요" type="error" variant="tonal"></v-alert>

      <v-alert v-if="!passwordIsOk" class="my-2" text="비밀번호를 확인해주세요 (8-16자)" type="error" variant="tonal"></v-alert>

      <v-hover v-slot="{ isHovering, props }">
        <v-btn :class="{ 'on-hover': isHovering }" :elevation="isHovering ? 10 : 2" v-bind="props" class="mb-8" color="blue-darken-1" size="large" block @click.prevent="logIn()">
          <p class="font-weight-bold text-white">Log In</p>
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
/* Add any specific styles here */
</style>
