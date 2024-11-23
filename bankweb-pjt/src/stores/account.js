import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

// 로그인, 로그아웃, 회원가입 기능
export const useAccountStore = defineStore(
  "account",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const token = ref(null);
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });

    const signUpErrorMessage = ref({})

    const router = useRouter();

    const userinfo = ref(null);

    // 회원가입 요청
    const signUp = async function (payload) {
      const { username, password1, password2, nickname, name, email } = payload;
      console.log(email);
      
      try {
        const response = await axios({
          method: "post",
          url: `${API_URL}/accounts/signup/`,
          data: {
            username,
            password1,
            password2,
            nickname,
            name
          },
        });
        
        const password = password1;
        console.log("회원가입 성공");
        await logIn({ username, password });
        
      } catch (error) {
        console.log("signUp error = ", error);
        signUpErrorMessage.value = error.response.data
        console.log(signUpErrorMessage.value)
      }
    };

    const logIn = async function (payload) {
      const { username, password } = payload;
    
      try {
        // 로그인 요청
        const loginResponse = await axios({
          method: "post",
          url: `${API_URL}/accounts/login/`,
          data: {
            username,
            password,
          },
        });
        
        token.value = loginResponse.data.key;
    
        try {
          // 유저 정보 조회 요청
          const profileResponse = await axios({
            method: "get",
            url: `${API_URL}/user/${username}/`,
            headers: {
              Authorization: `Token ${token.value}`,
            },
          });
    
          userinfo.value = profileResponse.data;
          console.log(`현재 유저(${userinfo.value.nickname})프로필 조회 성공`);
          
        } catch (error) {
          console.log("getProfile error = ", error);
        }
    
        console.log("로그인 성공");
        router.push({ name: "home" });
        
      } catch (error) {
        console.log("logIn error = ", error);
      }
    };

    // 로그아웃 요청
    const logOut = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
      })
        .then((response) => {
          token.value = null;
          userinfo.value = null
          router.push({ name: "home" });
        })
        .catch((error) => {
          console.log("logOut error = ", error);
        });
    };

    // 유저 정보 새로고침 함수 추가
    const refreshUserInfo = async function () {
      try {
        const response = await axios({
          method: "get",
          url: `${API_URL}/user/${userinfo.value.username}/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });
        userinfo.value = response.data;
        console.log('사용자 정보 새로고침 성공');
        return response.data;
      } catch (error) {
        console.error('사용자 정보 새로고침 실패:', error);
        throw error;
      }
    };

    return { token, isLogin, router, userinfo, signUpErrorMessage, signUp, logIn, logOut, refreshUserInfo   };
  },
  { persist: true }
);
