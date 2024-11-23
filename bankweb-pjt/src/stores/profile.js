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
    

    // 사용자 프로필 조회
    const getProfile = async function (payload) {
      const { username } = payload;
      
      try {
        const response = await axios({
          method: "get",
          url: `/user/${username}/`,
        });
        
        userprofile.value = response.data;
        console.log(`현재 유저(${userprofile.value.nickname})프로필 조회 성공`);
        return response.data;  // 필요한 경우 데이터 반환
        
      } catch (error) {
        console.error("getProfile error = ", error);
        throw error;  // 에러를 상위로 전파하여 호출하는 쪽에서 처리할 수 있게 함
      }
    };

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


    return { userprofile, getProfile, updateProfile, updateProfileImg };
  },
  { persist: true }
);
