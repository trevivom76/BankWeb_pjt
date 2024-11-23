<template>
  <div class="profile-container">
    <v-card class="profile-card">
      <!-- 헤더 -->
      <div class="profile-header">
        <h2 class="text-h5">
          <span class="username">{{userInfo?.name }}</span>
          님의 프로필
        </h2>
      </div>
      
      <v-divider class="my-4"></v-divider>

      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
        <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
      </div>

      <div v-else class="profile-content">
        <!-- 왼쪽: 프로필 이미지 섹션 -->
        <div class="image-section">
          <div class="profile-image-container">
            <img 
              :src="profileStore.userprofile?.profile_img" 
              alt="프로필 이미지" 
              class="profile-image"
            />
          </div>
          <input
            type="file"
            ref="fileInput"
            @change="handleFileChange"
            accept="image/*"
            style="display: none"
          />
          <v-btn
            @click="$refs.fileInput.click()"
            color="primary"
            variant="outlined"
            class="mt-4"
          >
            프로필 이미지 변경
          </v-btn>
        </div>

        <!-- 오른쪽: 프로필 정보 수정 폼 -->
        <div class="info-section">
          <v-form @submit.prevent="updateProfile" ref="form">
            <!-- 아이디 (수정 불가) -->
            <div class="form-field">
              <v-text-field
                v-model="userInfo.username"
                label="아이디"
                readonly
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </div>

            <!-- 이름 -->
            <div class="form-field">
              <v-text-field
                v-model="profileData.name"
                label="이름"
                :rules="nameRules"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </div>

            <!-- 닉네임 -->
            <div class="form-field">
              <v-text-field
                v-model="profileData.nickname"
                label="닉네임"
                :rules="nicknameRules"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </div>

            <!-- 이메일 -->
            <div class="form-field">
              <v-text-field
                v-model="profileData.email"
                label="이메일"
                type="email"
                :rules="emailRules"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </div>

            <!-- 나이 -->
            <div class="form-field">
              <v-text-field
                v-model.number="profileData.age"
                label="나이"
                type="number"
                :rules="ageRules"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </div>

            <!-- 자산 -->
            <div class="form-field">
              <v-text-field
                v-model.number="profileData.money"
                label="자산"
                type="number"
                :rules="moneyRules"
                variant="outlined"
                density="comfortable"
                :prefix="'₩'"
                :suffix="'원'"
              ></v-text-field>
            </div>

            <!-- 급여 -->
            <div class="form-field">
              <v-text-field
                v-model.number="profileData.salary"
                label="급여"
                type="number"
                :rules="salaryRules"
                variant="outlined"
                density="comfortable"
                :prefix="'₩'"
                :suffix="'원'"
              ></v-text-field>
            </div>

            <!-- 수정 버튼 -->
            <div class="actions">
              <v-btn
                color="primary"
                type="submit"
                :loading="isUpdating"
                min-width="120"
              >
                프로필 수정
              </v-btn>
            </div>
          </v-form>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";
import { onMounted, ref, reactive } from "vue";

const accountStore = useAccountStore();
const profileStore = useProfileStore();
const isLoading = ref(true);
const isUpdating = ref(false);
const fileInput = ref(null);
const form = ref(null);

const userInfo = accountStore.userinfo

// 프로필 데이터
const profileData = reactive({
  name: userInfo.username,
  nickname: userInfo.nickname,
  email: userInfo.email,
  age: userInfo.age,
  money: userInfo.money,
  salary: userInfo.salary
});

// 유효성 검사 규칙
const nameRules = [
  v => !!v || '이름을 입력해주세요',
  v => v.length <= 50 || '이름은 50자를 초과할 수 없습니다'
];

const nicknameRules = [
  v => !!v || '닉네임을 입력해주세요',
  v => v.length <= 20 || '닉네임은 20자를 초과할 수 없습니다'
];

const emailRules = [
  v => !v || /.+@.+\..+/.test(v) || '유효한 이메일을 입력해주세요'
];

const ageRules = [
  v => v >= 0 || '나이는 0보다 작을 수 없습니다'
];

const moneyRules = [
  v => v >= 0 || '자산은 0보다 작을 수 없습니다'
];

const salaryRules = [
  v => v >= 0 || '급여는 0보다 작을 수 없습니다'
];

// 프로필 업데이트 함수
const updateProfile = async () => {
  const { valid } = await form.value.validate();
  
  if (!valid) {
    alert('입력값을 확인해주세요.');
    return;
  }

  try {
    isUpdating.value = true;
    await profileStore.updateProfile({
      username: userInfo.username,
      nickname: profileData.nickname,
      name: profileData.name,
      email: profileData.email,
      age: profileData.age,
      money: profileData.money,
      salary: profileData.salary
    });

    // 프로필 정보와 계정 정보를 모두 새로고침
    await Promise.all([
      profileStore.getProfile({
        username: userInfo.username
      }),
      accountStore.refreshUserInfo()
    ]);

    alert('프로필이 성공적으로 업데이트되었습니다.');
  } catch (error) {
    console.error('프로필 업데이트 실패:', error);
    if (error.response?.data) {
      // 서버에서 반환한 구체적인 에러 메시지가 있다면 표시
      const errorMessage = Object.values(error.response.data).join('\n');
      alert(`프로필 업데이트 실패:\n${errorMessage}`);
    } else {
      alert('프로필 업데이트에 실패했습니다.');
    }
  } finally {
    isUpdating.value = false;
  }
};

// 파일 선택 시 호출되는 함수
const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 파일 크기 체크 (예: 5MB 제한)
  const maxSize = 5 * 1024 * 1024; // 5MB
  if (file.size > maxSize) {
    alert('파일 크기는 5MB를 초과할 수 없습니다.');
    return;
  }

  // 이미지 파일 타입 체크
  if (!file.type.startsWith('image/')) {
    alert('이미지 파일만 업로드 가능합니다.');
    return;
  }

  try {
    isLoading.value = true;
    const formData = new FormData();
    formData.append('profile_img[]', file);

    await profileStore.updateProfileImg({
      username: userInfo.username,
      formData: formData
    });

    // 프로필 정보 새로고침
    await profileStore.getProfile({
      username: userInfo.username
    });
  } catch (error) {
    console.error('프로필 이미지 업데이트 실패:', error);
    alert('이미지 업로드에 실패했습니다.');
  } finally {
    isLoading.value = false;
  }
};

// 초기 데이터 로드
onMounted(async () => {
  try {
    const payload = {
      username: userInfo?.username,
    };
    if (payload.username) {
      await profileStore.getProfile(payload);
      // 프로필 데이터 초기화
      Object.assign(profileData, {
        name: userInfo.name,
        nickname: userInfo.nickname,
        email: userInfo.email,
        age: userInfo.age,
        money: userInfo.money,
        salary: userInfo.salary
      });
    }
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.profile-card {
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-header {
  margin-bottom: 1rem;
}

.username {
  color: #1867C0;
  font-weight: 600;
}

.profile-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image-container {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #E0E0E0;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-section {
  padding: 1rem;
}

.form-field {
  margin-bottom: 1rem;
}

.actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }

  .image-section {
    margin-bottom: 2rem;
  }
}
</style>