<template>
  <div>
    <div class="select-container">
      <!-- 시/도 선택 -->
      <div class="select-box">
        <p class="select-text">광역시/도</p>
        <article class="cont-select">
          <button class="btn-select" @click="toggleDropDown1">
            {{ selectedCity }}
            <img
            src="@/assets/icon/dropdownIcon.png"
            alt="드롭다운 아이콘"
            class="dropdown-icon"
            :class="{ rotated: isDropdownOpen1 }"
            >
        </button>
        <ul class="list-member" v-show="isDropdownOpen1">
          <li v-for="city in Object.keys(cities)" :key="city">
            <button type="button" @click=" selectCity(city)">{{city}}</button>
          </li>
        </ul>
      </article>
    </div>
      <!-- 시/군/구 선택 -->
      <div class="select-box">
        <p class="select-text">시/군/구</p>
        <article class="cont-select">
          <button class="btn-select" @click="toggleDropDown2" :disabled="selectedCity === '광역시/도를 선택해주세요.'">
            {{ selectedDistrict }}
            <img
              src="@/assets/icon/dropdownIcon.png"
              alt="드롭다운 아이콘"
              class="dropdown-icon"
              :class="{ rotated: isDropdownOpen2 }"
            >
          </button>
          <ul class="list-member" v-show="isDropdownOpen2">
            <li v-for="districts in cities[selectedCity]" :key="districts">
              <button type="button" @click=" selectDistrict(districts)">{{districts}}</button>
            </li>
          </ul>
        </article>
      </div>
      <!-- 은행 선택 -->
      <div class="select-box">
        <p class="select-text">은행명</p>
      <article class="cont-select">
        <button class="btn-select" @click="toggleDropDown3">
          {{ selectedBank }}
          <img
            src="@/assets/icon/dropdownIcon.png"
            alt="드롭다운 아이콘"
            class="dropdown-icon"
            :class="{ rotated: isDropdownOpen3 }"
          >
        </button>
        <ul class="list-member" v-show="isDropdownOpen3">
          <li v-for="bank in banks" :key="bank">
            <button type="button" @click=" selectBank(bank)">{{bank}}</button>
          </li>
        </ul>
      </article>
      </div>
      <v-hover v-slot="{ isHovering, props }">
        <button :class="{ 'on-hover': isHovering }" :elevation="isHovering ? 10 : 2" v-bind="props" class="btn flex" @click.prevent="emitChange()">
          <svg-icon type="mdi" :path="mdiMagnify" class="img"</svg-icon>
          <p>검 색</p>
        </button>
      </v-hover>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

// SvgIcon 컴포넌트와 MDI 아이콘 가져오기
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiMagnify } from "@mdi/js";

// 도시 데이터
const cities = {
  서울특별시: [
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구",
  ],
  부산광역시: ["강서구", "금정구", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
  대구광역시: ["남구", "달서구", "동구", "북구", "서구", "수성구", "중구"],
  인천광역시: ["계양구", "남동구", "동구", "미추홀구", "부평구", "서구", "연수구", "중구"],
  광주광역시: ["광산구", "남구", "동구", "북구", "서구"],
  대전광역시: ["대덕구", "동구", "서구", "유성구", "중구"],
  울산광역시: ["남구", "동구", "북구", "중구"],
  세종특별자치시: ["세종시"],
  경기도: [
    "가평군",
    "고양시",
    "과천시",
    "광명시",
    "광주시",
    "구리시",
    "군포시",
    "김포시",
    "남양주시",
    "동두천시",
    "부천시",
    "성남시",
    "수원시",
    "시흥시",
    "안산시",
    "안성시",
    "안양시",
    "양주시",
    "양평군",
    "여주시",
    "연천군",
    "오산시",
    "용인시",
    "의왕시",
    "의정부시",
    "이천시",
    "파주시",
    "평택시",
    "포천시",
    "하남시",
    "화성시",
  ],
  강원도: ["강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
  충청북도: ["괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "진천군", "청주시", "충주시"],
  충청남도: ["계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "예산군", "천안시", "청양군", "태안군", "홍성군"],
  전라북도: ["고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
  전라남도: [
    "강진군",
    "고흥군",
    "곡성군",
    "광양시",
    "구례군",
    "나주시",
    "담양군",
    "목포시",
    "무안군",
    "보성군",
    "순천시",
    "신안군",
    "여수시",
    "영광군",
    "영암군",
    "완도군",
    "장성군",
    "장흥군",
    "진도군",
    "함평군",
    "해남군",
    "화순군",
  ],
  경상북도: [
    "경산시",
    "경주시",
    "고령군",
    "구미시",
    "군위군",
    "김천시",
    "문경시",
    "봉화군",
    "상주시",
    "성주군",
    "안동시",
    "영덕군",
    "영양군",
    "영주시",
    "영천시",
    "예천군",
    "울릉군",
    "울진군",
    "의성군",
    "청도군",
    "청송군",
    "칠곡군",
    "포항시",
  ],
  경상남도: ["거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
  제주특별자치도: ["서귀포시", "제주시"],
};

// 은행 목록
const banks = ["KB국민은행", "신한은행", "우리은행", "하나은행", "NH농협은행", "IBK기업은행", "SC제일은행", "씨티은행", "KDB산업은행", "케이뱅크", "카카오뱅크", "토스뱅크"];

// 반응형 상태 정의
const selectedCity = ref("광역시/도를 선택해주세요.");
const selectedDistrict = ref("시/군/구를 선택해주세요.");
const selectedBank = ref("은행을 선택해주세요.");
const isDropdownOpen1 = ref(false)
const isDropdownOpen2 = ref(false)
const isDropdownOpen3 = ref(false)

// 선택 변경사항을 부모 컴포넌트에 전달
const emit = defineEmits(["change"]);

const emitChange = () => {
  if ( selectedCity.value === "광역시/도를 선택해주세요." || selectedDistrict.value === "시/군/구를 선택해주세요." || selectedBank.value === "은행을 선택해주세요.") {
    window.alert("검색 옵션을 선택해주세요.")
  } else {
    emit("change", {
      city: selectedCity.value,
      district: selectedDistrict.value,
      bank: selectedBank.value,
    });
  }
};

const toggleDropDown1 = () => {
  isDropdownOpen1.value = !isDropdownOpen1.value
}

const toggleDropDown2 = () => {
  isDropdownOpen2.value = !isDropdownOpen2.value
}

const toggleDropDown3 = () => {
  isDropdownOpen3.value = !isDropdownOpen3.value
}

const selectCity = (option) => {
  selectedCity.value = option
  isDropdownOpen1.value = false
}

const selectDistrict = (option) => {
  selectedDistrict.value = option
  isDropdownOpen2.value = false
}

const selectBank = (option) => {
  selectedBank.value = option
  isDropdownOpen3.value = false
}
</script>

<style scoped>
.select-container {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  padding-bottom: 24px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 16px;
}

.select-box {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  max-width: 250px;
  margin: 0px 10px;
}

.select-text {
  padding-left: 4px;
  padding-bottom: 4px;
  font-weight: 400;
  font-size: 12px;
}

.cont-select {
  position: relative;
  width: 100%;
}

.btn-select {
  display: flex;
  width: 100%;
  padding:8px 12px;
  font-size: 15px;
  line-height: 13px;
  font-weight: 600;
  border: 1px solid #C4C4C4;
  color: #424242;
  box-sizing: border-box;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
}

.btn-select:disabled {
  color: #4242425c;
}

/* 드롭다운 리스트 */
.list-member {
  list-style-type: none;
  position: absolute;
  width: 100%;
  top: 50px;
  left: 0;
  padding: 0;
  border: 1px solid #C4C4C4;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 4px 4px 14px rgba(0, 0, 0, 0.15);
  transition: opacity 0.3s ease, visibility 0.3s ease;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.search-button-container {
  margin-top: auto; /* 버튼을 컨테이너의 가장 아래로 밀어냄 */
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

/* v-show 상태 활성화 */
.list-member[v-show="true"] {
  opacity: 1;
  visibility: visible;
}

.list-member[v-show="false"] {
  opacity: 0;
  visibility: hidden;
}

.list-member li {
  padding: 8px;
}

.list-member li button {
  width: 100%;
  padding: 8px 4px;
  border: none;
  font-size: 13px;
  line-height: 13px;
  background-color: transparent;
  text-align: left;
  cursor: pointer;
  color: #676767;
}

.list-member li button:hover {
  background-color: #ffffff87;
  border-radius: 4px;
  color: #424242;
  font-weight: 600;
}

.dropdown-icon {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease; /* 부드러운 회전 애니메이션 */
}

/* 드롭다운 열림 상태에서 아이콘 회전 */
.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.flex {
  align-items: center;
  gap: 2px;
}

.img {
  width: 16px;
}
</style>
