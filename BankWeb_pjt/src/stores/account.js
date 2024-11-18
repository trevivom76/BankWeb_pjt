import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

// 로그인, 로그아웃, 회원가입 기능 
export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const router = useRouter()

  // 회원가입 요청
  const signUp = function (payload) {
    const { userId, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        userId, password1, password2
      }
    })
    .then((response) => {
      const password = password1
      logIn({ userId, password })
      // console.log('회원가입 성공')
    })
    .catch((error) => {
      console.log('error = ', error);
    })
  }


  // 로그인 요청
  const logIn = function (payload) {
    const { userId, password1 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        userId, password1
      }
    })
    .then((response) => {
      token.value = response.data.key
      router.push({ name:'home' })
      // console.log('로그인 성공');
      
    })
    .catch((error) => {
      console.log('error = ', error);
    })
  }

  // 로그아웃 요청
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
    .then((response) => {
      token.value = null
      router.push({name: 'home'})
    })
    .catch((error) => {
      console.log(error)
    })
  }
  

  return { API_URL, token, isLogin, router, signUp, logIn, logOut}
}, { persist: true })
