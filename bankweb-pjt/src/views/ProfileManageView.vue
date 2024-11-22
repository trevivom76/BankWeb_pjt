<template>
  <div>
    <div>
      <p>
        <span class="username">{{ accountStore.userinfo.name }}</span>
        님의 프로필 페이지
      </p>
    </div>
    <hr />

    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
      <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
    </div>

    <div v-else>
      <div>
        <!-- 프로필이미지, 이미지 변경 -->
        <div class="d-flex flex-column justify-space-between">
          <div>
            <img :src="profileStore.userprofile.profile_img" alt="프로필 이미지" class="profile-img" />
          </div>
          <div>
            <a href="#">프로필 이미지 변경하기</a>
          </div>
        </div>

        <!-- 프로필 정보 -->
        <div>
          <p>이름: {{ accountStore.userinfo.name }}</p>
          <p>닉네임: {{ accountStore.userinfo.nickname }}</p>
          <p>아이디: {{ accountStore.userinfo.username }}</p>
          <p>이메일: {{ accountStore.userinfo.email }}</p>
          <p>나이: {{ accountStore.userinfo.age }}</p>
          <p>자산: {{ accountStore.userinfo.money }}</p>
          <p>급여: {{ accountStore.userinfo.salary }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";
import { onMounted, ref } from "vue";

const accountStore = useAccountStore();
const profileStore = useProfileStore();

const isLoading = ref(true); // 로딩 상태를 관리하는 ref 추가

// 프로필 정보 가져오기
onMounted(async () => {
  try {
    const payload = {
      username: accountStore.userinfo.username,
    };
    await profileStore.getProfile(payload);
  } finally {
    isLoading.value = false; // 데이터 로딩이 완료되면 로딩 상태를 false로 변경
  }
});
</script>

<style scoped>
.username {
  color: blue;
}

.profile-img {
  width: 220px;
}
</style>
