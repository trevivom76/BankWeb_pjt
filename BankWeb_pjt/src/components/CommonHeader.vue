<template>
    <div>
      <!-- 네비게이션 바 -->
      <nav class="d-flex justify-space-between align-center pa-3">
        <!-- 은행 로고 -->
        <div>
            <a href="#" @click.prevent="goToHome">
                <img :src="BBK_Logo" alt="Example Image" class="bank-logo"/>
            </a>
        </div>
  
        <!-- 네비게이션바 주요 링크 -->
        <!-- 로그인 되어있다면 -->
        <div v-if="isLogin()">
            <div class="text-center">

                <!-- 금리비교 태그 -->
                <RouterLink :to="{name:'interestrate'}">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                            금리비교
                        </v-btn>
                    </v-hover>
                </RouterLink>

                <!-- 환율계산 태그 -->
                <RouterLink :to="{name:'currencycalculator'}">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        환율계산
                        </v-btn>
                    </v-hover>
                </RouterLink>

                <!-- 주변은행 태그 -->
                <RouterLink :to="{name:'aroundbank'}">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        주변은행
                        </v-btn>
                    </v-hover>
                </RouterLink>

                <!-- 커뮤니티 태그 -->
                <RouterLink :to="{name:'community'}">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        커뮤니티
                        </v-btn>
                    </v-hover>
                </RouterLink>
            </div>
        </div>

        <!-- 로그인 되어있지 않다면 -->
        <div v-else>
            <div class="text-center">
                <!-- 금리비교 태그 -->
                <a href="#" @click="dialog = true" >
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        금리비교
                        </v-btn>
                    </v-hover>                    
                </a>

                <!-- 환율계산 태그 -->
                <a href="#" @click="dialog = true" >
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        환율계산
                        </v-btn>
                    </v-hover>                    
                </a>

                <!-- 주변은행 태그 -->
                <a href="#" @click="dialog = true">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        주변은행
                        </v-btn>
                    </v-hover>   
                </a>

                <!-- 커뮤니티 태그 -->
                <a href="#" @click="dialog = true">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-btn
                        :class="{ 'hovered-btn': isHovering }"
                        :elevation="isHovering ? 10 : 0"
                        v-bind="props"
                        >
                        커뮤니티
                        </v-btn>
                    </v-hover>   
                </a>
            </div>
        </div>



  
        <!-- 로그인/회원가입 버튼 -->
        <!-- 로그인 되어있다면 -->
        <div v-if="isLogin()">
            <div class="d-flex ga-2">
                <!-- 로그아웃 버튼 -->
                <v-hover
                v-slot="{ isHovering, props }"
                >
                    <v-btn
                    :class="{ 'on-hover': isHovering }"
                    :elevation="isHovering ? 10 : 2"
                    v-bind="props"
                    @click.prevent="logOut"
                    >
                        <!-- 사용자 아이콘 -->
                        <SvgIcon type="mdi" :path="mdiLogout" />
                        <p>로그아웃</p>
                    </v-btn>
                </v-hover>
        
                <!-- 프로필 버튼 (아직 미구현) -->

            </div>
        </div>

        <!-- 로그인 되어있지 않다면 -->
        <div v-else>
            <div class="d-flex ga-2">
                <!-- 로그인 버튼 -->
                <RouterLink :to="{name:'login'}">
                    <v-hover
                    v-slot="{ isHovering, props }"
                    >
                        <v-btn
                        :class="{ 'on-hover': isHovering }"
                        :elevation="isHovering ? 10 : 2"
                        v-bind="props"
                        >
                            <!-- 사용자 아이콘 -->
                            <SvgIcon type="mdi" :path="mdiAccount" />
                            <p>로그인</p>
                        </v-btn>
                    </v-hover>
                </RouterLink>
                
    
                <!-- 회원가입 버튼 -->
                <RouterLink :to="{name:'signup'}">
                    <v-hover
                    v-slot="{ isHovering, props }"
                    >
                        <v-btn
                        :class="{ 'on-hover': isHovering , }"
                        :elevation="isHovering ? 10 : 2"
                        v-bind="props"
                        color="blue-lighten-1"
                        >
                            <p>회원가입</p>
                        </v-btn>
                    </v-hover>
                </RouterLink>
            </div>
        </div>

      </nav>

    <!-- 로그인 안내 다이얼로그 -->
    <v-dialog
        v-model="dialog"
        max-width="380"
        height="190"
        persistent   
    >
        <v-card
            text="안전한 금융서비스를 위해 로그인 화면으로 이동합니다"
        >
        <!-- 중앙 정렬을 위해 flexbox 사용 -->
        <v-card-text class="d-flex justify-center align-center mb-5 pt-0">
            <v-progress-circular
            color="primary"
            indeterminate
            disable-shrink
            size="40"
            width="4"
            ></v-progress-circular>
        </v-card-text>

        </v-card>    
    </v-dialog>
      
    </div>
</template>
  
<script setup>
// SvgIcon 컴포넌트와 MDI 아이콘 가져오기
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiAccount } from '@mdi/js';
import { mdiLogout } from '@mdi/js';

// BBK_Logo 사진 가져오기
import BBK_Logo from '@/images/BBK_Logo.png';

import { RouterLink, useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/account';
import { ref, watch } from 'vue';
  
const accountStore = useAccountStore()

const router = useRouter();

// dialog 상태를 ref로 선언
const dialog = ref(false);

// 홈페이지로 push하는 함수
const goToHome = () => {
    router.push({name:'home'})
}

// 로그인 되어있는지 아닌지 확인하는 함수
const isLogin = function() {
    return accountStore.isLogin 
}

const logOut = function () {

    // 나중에 주석 풀기
    // accountStore.logOut()

    // 위에 주석 풀면서 삭제하기
    console.log('로그아웃 성공')
    accountStore.token = null
    router.push({name:'home'})

}

// dialog 값이 변경될 때, watch로 4초 후에 dialog를 false로 설정
watch(dialog, (val) => {
    if (!val) return;

    setTimeout(() => {
        dialog.value = false
        router.push({name:'login'})
    }, 1500);
});

</script>

<style scoped>
.bank-logo {
    width: 150px;
    height: auto;
} 
/* 기본 버튼 스타일 */
.custom-hover-btn {
  background-color: white;  /* 기본 배경색 */
  color: black;  /* 기본 텍스트 색상 */
  width: 200px;  /* 버튼 크기 */
  height: 50px;  /* 버튼 높이 */
  font-size: 16px;  /* 글꼴 크기 */
  border-radius: 8px;  /* 둥근 모서리 */
  transition: background-color 0.3s ease, color 0.3s ease;  /* 색상 전환 부드럽게 */
}

/* Hover 상태에서 버튼 색상 변경 */
.hovered-btn {
  background-color: #1976d2;  /* 파란색 */
  color: white;  /* 텍스트 색상 흰색 */
}
</style>
