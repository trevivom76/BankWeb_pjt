<template>
  <div>
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading-container">
      <div class="loading-spinner"></div>
    </div>

    <div v-else class="profile-content">
      <!-- 왼쪽: 프로필 이미지 섹션 -->
      <div class="image-section">
        <div class="title-container">
          <span class="title-name">{{ userInfo?.name }}</span>
          <span class="title-description">님의 프로필</span>
        </div>
        <div class="profile-image-container-wrapper">
          <div class="profile-image-container">
            <img :src="profileStore.userprofile?.profile_img" alt="프로필 이미지" class="profile-image" />
          </div>
          <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none" />
          <button @click="$refs.fileInput.click()" class="btn-primary mt-4">프로필 이미지 등록</button>
        </div>
      </div>

      <!-- 오른쪽: 프로필 정보 섹션 -->
      <div class="info-section">
        <template v-if="isEditing">
          <ProfileEditSection :initialData="userInfo" @save="handleSaveChanges" @cancel="cancelEditing" />
        </template>
        <template v-else>
          <ProfileViewSection @edit="startEditing" />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";
import ProfileEditSection from "@/components/ProfileEditSection.vue";
import ProfileViewSection from "@/components/ProfileViewSection.vue";

const accountStore = useAccountStore();
const profileStore = useProfileStore();

const isLoading = ref(true);
const isEditing = ref(false);
const userInfo = ref({ ...accountStore.userinfo });

const startEditing = async () => {
  await syncUserInfo();
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
};

const handleSaveChanges = async (updatedData) => {
  try {
    await profileStore.updateProfile(updatedData);
    await syncUserInfo();
    isEditing.value = false;
  } catch (error) {
    console.error("Failed to refresh user info:", error);
  }

  isEditing.value = false;
};

const syncUserInfo = async () => {
  try {
    await accountStore.refreshUserInfo();
    userInfo.value = { ...accountStore.userinfo };
  } catch (error) {
    console.error("Failed to refresh user info:", error);
  }
};

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 파일 크기 체크 (예: 5MB 제한)
  const maxSize = 5 * 1024 * 1024; // 5MB
  if (file.size > maxSize) {
    alert("파일 크기는 5MB를 초과할 수 없습니다.");
    return;
  }

  // 이미지 파일 타입 체크
  if (!file.type.startsWith("image/")) {
    alert("이미지 파일만 업로드 가능합니다.");
    return;
  }

  try {
    isLoading.value = true;
    const formData = new FormData();
    formData.append("profile_img[]", file);

    await profileStore.updateProfileImg({
      username: userInfo.value.username,
      formData: formData,
    });

    await profileStore.getProfile({
      username: userInfo.value.username,
    });
  } catch (error) {
    console.error("프로필 이미지 업데이트 실패:", error);
    alert("이미지 업로드에 실패했습니다.");
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  try {
    await syncUserInfo();
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
/* 공통 스타일 */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.2);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.profile-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  margin-top: 20px;
}

/* 프로필 이미지 섹션 */
.image-section {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.title-container {
  text-align: left;
  margin-bottom: 20px;
}

.title-text {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  gap: 10px;
}

.title-name {
  font-weight: bold;
  font-size: 24px;
}

.title-description {
  color: #888;
}

.profile-image-container-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.profile-image-container {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #e0e0e0;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 정보 섹션 */
.info-section {
  display: flex;
  flex-direction: column;
  align-content: space-between;
  justify-content: space-between;
  height: 100%;
  background-color: #ffffff;
  padding: 28px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 버튼 스타일 */
.btn-primary {
  background-color: #5a87f2;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:active {
  transform: scale(0.95);
  background-color: #3f75f2;
}

.btn-primary:hover {
  transform: scale(1.05);
  background-color: #3f75f2;
}
</style>
