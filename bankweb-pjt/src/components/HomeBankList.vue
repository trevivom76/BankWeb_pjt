<template>
  <div class="box">
    <div class="title-box">
      <img src="@/assets/icon/website.png" alt="환율 그래프 아이콘" class="icon">
      <p class="title">은행 웹 사이트</p>
    </div>
    <div class="grid-container">
      <div v-for="bank in banks" :key="bank.name" class="grid-item" @click="navigateToBank(bank.url)">
        <div class="icon-container">
          <img :src="bank.image" :alt="bank.name" />
        </div>
        <p class="bank-name">{{ bank.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import kb from "@/assets/icon/kb.png"
import sh from "@/assets/icon/sh.png"
import hn from "@/assets/icon/hn.png"
import wo from "@/assets/icon/wo.png"
import nh from "@/assets/icon/nh.png"
import ibk from "@/assets/icon/ibk.png"
import ib from "@/assets/icon/ib.png"
import im from "@/assets/icon/im.png"
import kakao from "@/assets/icon/kakao.png"
import toss from "@/assets/icon/toss.png"

const navigateToBank = (url) => {
  window.open(url, "_blank");
};

const banks = [
  { name: "국민은행", image: kb, url: "https://www.kbstar.com/" },
  { name: "신한은행", image: sh, url: "https://www.shinhan.com/index.jsp" },
  { name: "하나은행", image: hn, url: "https://www.hanabank.com/" },
  { name: "우리은행", image: wo, url: "https://www.wooribank.com/" },
  { name: "농협은행", image: nh, url: "https://www.nhbank.com/nhmn/KO_NHMN_01.do" },
  { name: "기업은행", image: ibk, url: "https://www.ibk.co.kr/" },
  { name: "산업은행", image: ib, url: "https://www.kdb.co.kr/index.jsp" },
  { name: "IM뱅크", image: im, url: "https://www.imbank.co.kr/dgb_ebz_main.jsp" },
  { name: "카카오뱅크", image: kakao, url: "https://www.kakaobank.com/" },
  { name: "토스뱅크", image: toss, url: "https://www.tossbank.com/" },
];
</script>

<style scoped>
.box {
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

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 16px;
  justify-content: center;
  align-items: start;
}

.grid-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.icon-container {
  width: 70px;
  height: 70px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.icon-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.bank-name {
  margin-top: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #424242;
}

.grid-item:hover .icon-container {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.grid-item:hover .bank-name {
  font-weight: 600;
  color: #000;
}
</style>
