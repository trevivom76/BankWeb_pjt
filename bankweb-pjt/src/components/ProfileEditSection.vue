<template>
  <div>
    <v-form @submit.prevent="submitChanges" ref="form">
      <div class="form-field">
        <v-text-field v-model="profileData.name" label="이름" :rules="nameRules" variant="outlined"
          density="comfortable"></v-text-field>
      </div>

      <div class="form-field">
        <v-text-field v-model="profileData.nickname" label="닉네임" :rules="nicknameRules" variant="outlined"
          density="comfortable"></v-text-field>
      </div>

      <div class="form-field">
        <v-text-field v-model="profileData.email" label="이메일" type="email" :rules="emailRules" variant="outlined"
          density="comfortable"></v-text-field>
      </div>

      <div class="form-field">
        <v-text-field v-model.number="profileData.age" label="나이" type="number" :rules="ageRules" variant="outlined"
          density="comfortable"></v-text-field>
      </div>

      <div class="form-field">
        <v-text-field v-model.number="profileData.money" label="자산" type="number" :rules="moneyRules" variant="outlined"
          density="comfortable" :prefix="'₩'" :suffix="'원'"></v-text-field>
      </div>

      <div class="form-field">
        <v-text-field v-model.number="profileData.salary" label="급여" type="number" :rules="salaryRules"
          variant="outlined" density="comfortable" :prefix="'₩'" :suffix="'원'"></v-text-field>
      </div>
      <div class="btn-container">
        <button type="submit" class="btn btn-save">수정 완료</button>
        <button type="button" @click="$emit('cancel')" class="btn btn-cancel">수정 취소</button>
      </div>
    </v-form>
  </div>
</template>

<script setup>
import { reactive, defineProps, ref } from "vue";
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";

const accountStore = useAccountStore();
const profileStore = useProfileStore();

const props = defineProps({
  initialData: Object,
});

const emit = defineEmits(["save", "cancel"]);

const profileData = reactive({ ...props.initialData });

const form = ref(null);

const nameRules = [v => !!v || "이름을 입력해주세요"];
const nicknameRules = [v => !!v || "닉네임을 입력해주세요"];
const emailRules = [v => !v || /.+@.+\..+/.test(v) || "유효한 이메일을 입력해주세요"];
const ageRules = [v => v >= 0 || "나이는 0보다 작을 수 없습니다"];
const moneyRules = [v => v >= 0 || "자산은 0보다 작을 수 없습니다"];
const salaryRules = [v => v >= 0 || "급여는 0보다 작을 수 없습니다"];

const submitChanges = async () => {
  const { valid } = await form.value.validate();

  if (!valid) {
    alert("입력값을 확인해주세요.");
    return;
  }

  try {
    await profileStore.updateProfile({
      username: props.initialData.username,
      nickname: profileData.nickname,
      name: profileData.name,
      email: profileData.email,
      age: profileData.age,
      money: profileData.money,
      salary: profileData.salary,
    });

    await accountStore.refreshUserInfo();
    emit("save", { ...profileData }); // 부모 컴포넌트에 업데이트된 데이터를 전달
    alert("프로필이 성공적으로 업데이트되었습니다.");
  } catch (error) {
    console.error("프로필 업데이트 실패:", error);
    alert("프로필 업데이트에 실패했습니다.");
  }
};

</script>

<style scoped>
.btn-container {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  gap: 8px;
}

.btn-save {
  color: white;
  background-color: #76af5f;
}

.btn-cancel {
  color: white;
  background-color: #d0574e;
}
</style>