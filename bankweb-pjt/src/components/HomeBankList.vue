<template>
    <!-- 이거는 다했는데 반응형이 완벽한지 의문이야. 그거만 확인하면 될 거야. -->
  <div class="center-container">
    <v-card>
      <!-- 아이콘과 텍스트 정렬 -->
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px">
        <v-icon size="24" color="black">mdi-bank</v-icon>
        <p style="font-size: 20px; font-weight: 600">은행 웹 사이트</p>
      </div>

      <!-- 은행 목록 -->
      <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: center">
        <!-- 국민은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.kbstar.com/')">
          <img src="@/assets/icon/kb.png" alt="국민은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">국민은행</p>
        </div>

        <!-- 신한은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.shinhan.com/index.jsp')">
          <img src="@/assets/icon/sh.png" alt="신한은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">신한은행</p>
        </div>

        <!-- 하나은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.hanabank.com/')">
          <img src="@/assets/icon/hn.png" alt="하나은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">하나은행</p>
        </div>

        <!-- 우리은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.wooribank.com/')">
          <img src="@/assets/icon/wo.png" alt="우리은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">우리은행</p>
        </div>

        <!-- 농협은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.nhbank.com/nhmn/KO_NHMN_01.do')">
          <img src="@/assets/icon/nh.png" alt="농협은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">농협은행</p>
        </div>

        <!-- 기업은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.ibk.co.kr/')">
          <img src="@/assets/icon/ibk.png" alt="기업은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">기업은행</p>
        </div>

        <!-- 산업은행 -->
        <div style="text-align: center" @click="navigateToBank('https://www.kdb.co.kr/index.jsp')">
          <img src="@/assets/icon/ib.png" alt="산업은행" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">산업은행</p>
        </div>

        <!-- IM뱅크 -->
        <div style="text-align: center" @click="navigateToBank('https://www.imbank.co.kr/dgb_ebz_main.jsp')">
          <img src="@/assets/icon/im.png" alt="IM뱅크" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">IM뱅크</p>
        </div>

        <!-- 카카오뱅크 -->
        <div style="text-align: center" @click="navigateToBank('https://www.kakaobank.com/')">
          <img src="@/assets/icon/kakao.png" alt="카카오뱅크" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">카카오뱅크</p>
        </div>

        <!-- 토스뱅크 -->
        <div style="text-align: center" @click="navigateToBank('https://www.tossbank.com/')">
          <img src="@/assets/icon/toss.png" alt="토스뱅크" style="width: 50px; height: 50px; cursor: pointer" />
          <p style="margin-top: 8px">토스뱅크</p>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
// 함수 정의
const navigateToBank = (url) => {
  window.open(url, "_blank"); // 새 탭에서 은행 사이트 열기
};
</script>

<style scoped>
/* 부모 컨테이너를 가로축 기준 중앙 정렬 */
.center-container {
  display: flex; /* 플렉스 컨테이너 */
  justify-content: center; /* 가로 중앙 정렬 */
  padding-top: 50px; /* 세로 여백 추가 */
  background-color: #f5f5f5; /* 필요하면 배경색 추가 */
}

img {
  border-radius: 8px; /* 이미지 모서리 둥글게 */
  border: 1px solid #ccc; /* 이미지 테두리 */
}
</style>
