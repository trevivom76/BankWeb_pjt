<template>
  <div class="d-flex justify-center align-center">
    <v-card class="px-10 pt-8" width="950px" height="785px" rounded="xl">
      <v-btn variant="flat" @click="goBack" class>
        <svg-icon type="mdi" :path="mdiArrowLeft" width="20px"></svg-icon>
        뒤로가기
      </v-btn>

        <!-- 프로필 (아이디) -->
        <div class="d-flex justify-space-between">
            <div div class="d-flex align-center">
              <img :src="articleStore.articledetail.user.profile_img" alt="프로필 이미지" class="profile-img" />
              <p :style="{fontSize: '16px', marginLeft:'16px'}">
                  {{ articleStore.articledetail.user.nickname }}
              </p>
            </div>
            <v-btn variant="flat" color="blue">질문/답변</v-btn>
        </div>

      <p>{{ articleStore.articledetail.title }}</p>
      <div class="d-flex justify-space-between align-center">
          <p>{{ articleStore.articledetail.created_at }}</p>
            <div class="d-flex ga-2">
                <a href="#">수정</a>
                <a href="#">삭제</a>
            </div>
      </div>
      <p>{{ articleStore.articledetail.content }}</p>
      

      <p>
        {{ articleStore.articledetail }}
        <hr>
      </p>
    </v-card>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { onMounted } from "vue";
import { useRoute } from "vue-router";

const articleStore = useArticleStore();
const route = useRoute();


onMounted(() => {
    const payload = {
        articleid: route.params.id
    }
    articleStore.getArticleDetail(payload)
})

</script>

<style scoped>
.profile-img {
  width: 44px;
}
</style>
