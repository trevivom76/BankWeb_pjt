import { ref, computed, toRef } from "vue";
import { defineStore, storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import axios from "@/apis";
import { useAccountStore } from "./account";

export const useProfileStore = defineStore(
  "profile",
  () => {
    // 현재 사용자 프로필 정보
    const userprofile = ref(null);
    const router = useRouter();
    const accountStore = useAccountStore();

    const isLoading = ref(false)
    const error = ref(null)

    // 프로필 초기화 함수 추가
    const resetProfile = () => {
      userprofile.value = null;
    };
    

    // 사용자 프로필 조회
    const getProfile = async (payload) => {
      const { username } = payload;
      isLoading.value = true
      error.value = null
      
      try {
        const response = await axios({
          method: "get",
          url: `/user/${username}/`,
        });
        userprofile.value = response.data
        return response.data
      } catch (err) {
        error.value = err
        throw err
      } finally {
        isLoading.value = false
      }
    }

    // 사용자 프로필 수정
    const updateProfile = async function (payload) {
      const { username, nickname, name, email, age, money, salary } = payload;
      try {
        const response = await axios({
          method: "put",
          url: `/user/${username}/info/`,
          data: {
            nickname, 
            name, 
            email, 
            age, 
            money, 
            salary
          },
          headers: {
            'Content-Type': 'application/json',
          },
        });
        userprofile.value = response.data;
        // 성공 시 accountStore의 userinfo도 업데이트
        const accountStore = useAccountStore();
        await accountStore.refreshUserInfo();
        console.log('프로필 업데이트 성공');
        return response.data;
      } catch (error) {
        console.error("updateProfile error = ", error);
        throw error;
      }
    };
    

    // 사용자 프로필 이미지 수정
    const updateProfileImg = async function (payload) {
      const { username, formData } = payload;
      try {
        const response = await axios({
          method: "put",
          url: `/user/${username}/profile-img/`,
          data: formData,
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        userprofile.value = response.data;
        console.log('프로필 이미지 업데이트 성공');
      } catch (error) {
        console.error("updateProfileImg error = ", error);
        throw error; // 에러를 상위로 전파
      }
    };   


    return { userprofile, isLoading, error, resetProfile, getProfile, updateProfile, updateProfileImg };
  },
  { persist: true }
);
