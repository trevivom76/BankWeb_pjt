<template>
  <div class = "box">
    <div class="title-box">
      <img src="@/assets/icon/website.png" alt="환율 그래프 아이콘" class="icon">
      <p class="title">은행 웹 사이트</p>
    </div>
    <div class="grid-container">
      <!-- 은행 아이템 반복 -->
      <div 
        v-for="bank in banks" 
        :key="bank.name" 
        class="grid-item" 
        @click="navigateToBank(bank.url)"
      >
        <div class="icon-container">
          <img :src="`@/assets/icon/${bank.imageNM}.png`" :alt="bank.name" />
        </div>
        <p class="bank-name">{{ bank.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// 함수 정의
const navigateToBank = (url) => {
  window.open(url, "_blank"); // 새 탭에서 은행 사이트 열기
};

const banks = [
  { name: "국민은행", imageNM: "kb", url: "https://www.kbstar.com/" },
  { name: "신한은행", imageNM: "sh", url: "https://www.shinhan.com/index.jsp" },
  { name: "하나은행", imageNM: "hn", url: "https://www.hanabank.com/" },
  { name: "우리은행", imageNM: "wo", url: "https://www.wooribank.com/" },
  { name: "농협은행", imageNM: "nh", url: "https://www.nhbank.com/nhmn/KO_NHMN_01.do" },
  { name: "기업은행", imageNM: "ibk", url: "https://www.ibk.co.kr/" },
  { name: "산업은행", imageNM: "ib", url: "https://www.kdb.co.kr/index.jsp" },
  { name: "IM뱅크", imageNM: "im", url: "https://www.imbank.co.kr/dgb_ebz_main.jsp" },
  { name: "카카오뱅크", imageNM: "kakao", url: "https://www.kakaobank.com/" },
  { name: "토스뱅크", imageNM: "toss", url: "https://www.tossbank.com/" },
];
</script>

<style scoped>

.box{
  background: #FFFFFF;
  border-radius: 20px;
  padding: 40px;
}

.title-box {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
  gap: 4px;
  padding-bottom: 16px;
}

.icon {
  width: 25px;
  height: 25px;
}

.title {
  font-weight: 600;
  font-size: 20px;
  line-height: 24px;
  color: #000000;
}

/* Grid 컨테이너 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); /* 최소 100px, 최대 1fr */
  gap: 16px;
  justify-content: center;
  align-items: start;
}

/* Grid 아이템 */
.grid-item {
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* 아이콘 컨테이너 */
.icon-container {
  background-color: white; /* 흰색 배경 */
  border-radius: 8px; /* 모서리 둥글게 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 기본 그림자 */
  padding: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.icon-container img {
  width: 50px;
  height: 50px;
  object-fit: contain; /* 아이콘 크기에 맞춤 */
}

/* 아이템 텍스트 */
.bank-name {
  margin-top: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #424242;
}

/* Hover 효과 */
.grid-item:hover .icon-container {
  transform: translateY(-5px); /* 위로 이동 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 더 진한 그림자 */
}

.grid-item:hover .bank-name {
  font-weight: 600; /* 텍스트 강조 */
  color: #000; /* 색상 강조 */
}
</style>
