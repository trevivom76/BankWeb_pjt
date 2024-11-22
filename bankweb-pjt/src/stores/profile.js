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
    const getProfile = function (payload) {
      const { username } = payload;
      axios({
        method: "get",
        url: `/user/${username}/`,
      })
        .then((response) => {
          userprofile.value = response.data;
          console.log(`현재 유저(${userprofile.value.nickname})프로필 조회 성공`);
        })
        .catch((error) => {
          console.log("getProfile error = ", error);
        });
    };


    // 프로필 사진 수정

    return { userprofile, getProfile };
  },
  { persist: true }
);
