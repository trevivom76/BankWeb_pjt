<template>
    <div>
        <!-- 로그인 화면 로고 -->
        <h1 class="my-6 text-center">
            Log In to 
            <span class="text-blue-lighten-2">
                MYBank
            </span>
        </h1>
  
      <!-- 로그인 card -->
      <v-card
        class="mx-auto pa-12 pb-8"
        elevation="8"
        max-width="448"
        rounded="lg"
      >
        
        <!-- 아이디 입력 text-field -->
        <v-text-field
            class="my-2"
            :rules="[userId_rules.required]"        
            v-model="userId"
            color="primary"
            label="아이디"
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
        
        <v-hover
            v-slot="{ isHovering, props }"
        >
            <v-btn
                :class="{ 'on-hover': isHovering }"
                :elevation="isHovering ? 10 : 2"
                v-bind="props"
                class="mb-8"
                color="blue-darken-1"
                size="large"
                block
                @click.prevent="signUp()"
            >
              <p class="font-weight-bold text-white">Log In</p>
            </v-btn>
        </v-hover>

      </v-card>
    </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account';
import { ref } from 'vue';


const accountStore = useAccountStore()

const userId = ref("")
const password1 = ref("")

const userIdIsOk = ref(true)
const password1IsOk = ref(true)

// 비밀번호 공개/비공개상태 변수
const show1 = ref(false)

// udseId 규칙
const userId_rules= {
    required: value => !!value || '아이디를 입력해주세요.',
}

// password1 규칙
const pw1_rules = {
    required: value => !!value || '비밀번호를 입력해주세요.',
    min: v => v.length >= 8 || '비밀번호는 최소 8자 이상입니다.',
    max: v => v.length <= 16 || '비밀번호는 최대 16자 입니다.',
}


// SIGN UP 버튼 클릭시 이상이 없는지 확인
const signUp = function() {
    // id가 입력되었는지 확인
    userIdIsOk.value = userId_rules.required(userId.value) === true;

    // password1이 입력되었는지 확인
    password1IsOk.value = pw1_rules.required(password1.value) === true;

    // 비밀번호 길이 확인 (8자 이상, 16자 이하)
    if (password1.value.length < 8 || password1.value.length > 16) {
        password1IsOk.value = false;
    }
    
    
    // 입력에 이상이 없을시 서버에 회원가입 정보를 넘기기
    if (userIdIsOk.value && password1IsOk.value) {
        const payload = {
            userId: userId.value,
            password1: password1.value,
        }
        // 나중에 주석 풀기!!!!!
        // accountStore.logIn(payload)

        // 위에 주석 풀면서 삭제하기
        accountStore.token = '123123'
        console.log('로그인 성공')
    }
}

</script>

<style scoped>

</style>