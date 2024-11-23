<template>
    <div class="d-flex justify-center align-center">
        <v-card class="px-10 pt-8" width="950px" height="785px" rounded="xl">
            
            
            <v-btn variant="flat" @click="goBack">
                <svg-icon type="mdi" :path="mdiArrowLeft" width="20px"></svg-icon>
                뒤로가기
            </v-btn>

            <p :style="{ fontWeight: 'bold' , fontSize: '24px'}" class="mt-5">
                글
                <span :style="{ color: '#0B5BCB' }">수정</span>
                하기
            </p>

            <div class="d-flex ga-2 mt-4">
                <v-select
                    placeholder="카테고리 선택"
                    :items="['질문/답변', '팁/정보 공유', '자유']"
                    width="160px"
                    v-model="category"
                ></v-select>

                <v-text-field
                     placeholder="제목을 작성해주세요."
                     width="686px"
                     v-model.trim="title"
                ></v-text-field>
            </div>

            <textarea placeholder="공유하고싶은 팁이나 정보를 작성해보세요." v-model.trim="content"></textarea>

            <div class="d-flex justify-end">
                <v-btn class="mt-4" variant="flat" @click="updateArticle" rounded="lg" color="#0B5BCB" width="92px" height="36px">
                    <p>수정하기</p>
                </v-btn>
            </div>
            
        </v-card>
    </div>
</template>

<script setup>
import { useArticleStore } from '@/stores/article';
import { ref } from 'vue';
// pictogrammers mdi icon
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiArrowLeft } from '@mdi/js';

const articleStore = useArticleStore()


// 뒤로가기 함수
const goBack = () => {
  window.history.back(); // 브라우저의 뒤로가기
}

const title = ref(articleStore.articledetail.title)
const content = ref(articleStore.articledetail.content)
const category = ref(articleStore.articledetail.category)

const updateArticle = function () {

    const payload = {
        articleid: articleStore.articledetail.id,
        title: title.value,
        content: content.value,
        category: category.value
    }
    articleStore.createArticle(payload)
}



</script>

<style scoped>
textarea {
  width: 100%; /* 폭 설정 */
  height: 60%; /* 높이 설정 */
  border: 1px solid #797979; /* 윤곽선 설정 (검정색) */
  padding: 10px; /* 내부 여백 (선택 사항) */
  border-radius: 1cap;
  padding: 34px;
}

.delete-a-underline-color {
  text-decoration: none;
  color: inherit;
}
</style>