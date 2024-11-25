<template>
    <div>
        <div class="profile-field">
            <span class="field-label">아이디</span>
            <span class="separator">|</span>
            <span class="field-value">{{ userInfo.username }}</span>
        </div>
        <div class="profile-field">
            <span class="field-label">이름</span>
            <span class="separator">|</span>
            <span class="field-value">{{ userInfo.name }}</span>
        </div>
        <div class="profile-field">
            <span class="field-label">닉네임</span>
            <span class="separator">|</span>
            <span class="field-value">{{ userInfo.nickname }}</span>
        </div>
        <div class="profile-field">
            <span class="field-label">이메일</span>
            <span class="separator">|</span>
            <span class="field-value">{{ userInfo.email }}</span>
        </div>
        <div class="profile-field">
            <span class="field-label">나이</span>
            <span class="separator">|</span>
            <span class="field-value">{{ userInfo.age }} 세</span>
        </div>
        <div class="profile-field">
            <span class="field-label">자산</span>
            <span class="separator">|</span>
            <span class="field-value">{{ Intl.NumberFormat("ko-KR").format(userInfo.money) || 0 }} 원</span>
        </div>
        <div class="profile-field">
            <span class="field-label">급여</span>
            <span class="separator">|</span>
            <span class="field-value">{{ Intl.NumberFormat("ko-KR").format(userInfo.salary) || 0 }} 원</span>
        </div>
        <div class="actions">
            <button class="btn" @click="$emit('edit')">프로필 수정</button>
        </div>
    </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { onMounted, watch } from "vue";

const accountStore = useAccountStore();

const userInfo = accountStore.userinfo


const syncUserInfo = async () => {
  await accountStore.refreshUserInfo();
};


onMounted(() => {
  syncUserInfo();
});


watch(() => accountStore.userinfo, (newUserInfo) => {
  Object.assign(userInfo, newUserInfo);
});
</script>

<style scoped>
/* 공통 스타일 */
.profile-field {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 18px;
  margin-bottom: 20px;
}

.field-label {
  font-weight: bold;
  font-size: 18px;
  color: #424242;
  width: 15%;
  text-shadow: 0 0 0 rgba(0, 0, 0, 0);
  transition: transform 0.3s, text-shadow 0.3s;
}

.field-value {
  color: #666;
  width: 75%;
  text-align: left;
  text-shadow: 0 0 0 rgba(0, 0, 0, 0);
  transition: transform 0.3s, text-shadow 0.3s;
}

/* 마우스 오버 시 텍스트 튀어나오는 효과 */
.profile-field:hover .field-label,
.profile-field:hover .field-value {
  transform: translateZ(5px);
  color: black;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 분리 기호 */
.separator {
  color: #ccc;
  width: 5%;
  text-align: center;
}
</style>