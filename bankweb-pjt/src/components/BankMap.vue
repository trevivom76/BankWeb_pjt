<template>
  <div class="map-container">
    <!-- 지도를 표시할 div -->
    <div class="redbox red" :class="{ shrink: isClicked }" id="map" style="height: 480px"></div>

    <!-- 검색결과 정보리스트 -->
    <div class="result-box blue" :class="{ expand: isClicked }">
      <div class="cards-container">
        <div v-for="(searchResultsInfo, index) in paginatedSearchResultsInfos" :key="index" class="custom-card">
          <p class="card-title">
            <a :href="searchResultsInfo.place_url" class="card-link">
              {{ searchResultsInfo.place_name }}
            </a>
          </p>

          <p class="card-text">{{ searchResultsInfo.road_address_name }}</p>
          <p class="card-text">(지번) {{ searchResultsInfo.address_name }}</p>
          <div v-if="searchResultsInfo.phone" class="telephone">
            <img class="telephone-img" src="@/assets/icon/Telephone.png" alt="">
            <p class="card-phone">{{ searchResultsInfo.phone }}</p>
          </div>
        </div>

        <div>
          <!-- 페이지네이션 -->
          <div class="pagination-container">
            <v-pagination v-model="currentPage" :length="pageCount" :total-visible="5"></v-pagination>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";

const isClicked = ref(false);

// selectedRegion 정보를 props를 통해 받아옴
const props = defineProps({
  selectedRegion: Object,
});

// 마커들과 인포윈도우를 관리할 배열
let markers = [];
let infowindows = []; // InfoWindow 객체들을 관리할 배열

// 검색결과의 장소명, 주소, 도로명주소, 전화번호
const searchResultsInfos = ref([]);

onMounted(() => {
  // 카카오 맵 스크립트 로드
  const script = document.createElement("script");
  script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=dfb2e0bec61965ccabc61e2b16c946f5&autoload=false&libraries=services"; // autoload=false 추가
  script.async = true;

  script.onload = () => {
    // 카카오 맵 SDK가 로드된 후, 카카오 맵 객체 초기화
    window.kakao.maps.load(() => {
      const mapContainer = document.getElementById("map"); // 지도를 표시할 div
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 기본 중심 좌표 (서울)
        level: 3, // 지도 확대 레벨
      };
      const map = new kakao.maps.Map(mapContainer, mapOption); // 지도 생성

      // HTML5의 geolocation으로 현재 위치를 확인합니다
      if (navigator.geolocation) {
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(function (position) {
          const lat = position.coords.latitude; // 위도
          const lon = position.coords.longitude; // 경도

          const locPosition = new kakao.maps.LatLng(lat, lon); // 마커가 표시될 위치

          map.setCenter(locPosition);
        });
      } else {
        // HTML5의 GeoLocation을 사용할 수 없을 때, 기본 위치로 설정
        const locPosition = new kakao.maps.LatLng(33.450701, 126.570667); // 기본 위치

        map.setCenter(locPosition);
      }

      // props.selectedRegion 값을 감지하여 해당 위치에 마커를 표시합니다
      watch(
        () => props.selectedRegion,
        (newRegion) => {
          if (newRegion && newRegion.city && newRegion.district && newRegion.bank) {
            const searchQuery = `${newRegion.city} ${newRegion.district} ${newRegion.bank}`; // 도시, 구, 은행 이름을 조합하여 검색 쿼리 생성
            searchAndPlaceMarker(searchQuery, map); // 검색 수행

            // 카카오맵, 결과검색 리스트 css 수행
            isClicked.value = true;
          }
        },
        { immediate: true } // props.selectedRegion 값이 초기값이라도 즉시 실행
      );

      // 장소 검색을 하고, 해당 위치에 마커를 추가하는 함수
      function searchAndPlaceMarker(query, map) {
        const ps = new kakao.maps.services.Places(); // 장소 검색 객체 생성
        ps.keywordSearch(query, placesSearchCB); // 키워드로 장소 검색

        function placesSearchCB(data, status) {
          if (status === kakao.maps.services.Status.OK) {
            const bounds = new kakao.maps.LatLngBounds(); // LatLngBounds 객체 생성

            // 기존에 추가된 마커를 모두 삭제
            clearMarkers();

            // 검색 결과 정보를 넣어줄 리스트 초기화
            searchResultsInfos.value = [];

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정
            for (let i = 0; i < data.length; i++) {
              displayMarker(data[i], map); // 마커 표시
              bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x)); // 좌표 추가

              // 검색 결과 정보를 넣어줌
              searchResultsInfos.value.push({
                place_name: data[i].place_name,
                address_name: data[i].address_name,
                phone: data[i].phone,
                road_address_name: data[i].road_address_name,
                place_url: data[i].place_url,
              });
            }
            // 지도 범위를 검색된 장소를 포함하도록 설정
            map.setBounds(bounds);
          }
        }
      }

      // 지도에 마커를 표시하는 함수
      function displayMarker(place, map) {
        const marker = new kakao.maps.Marker({
          map: map,
          position: new kakao.maps.LatLng(place.y, place.x),
        });

        // 이전의 모든 인포윈도우를 닫습니다
        clearInfowindows();

        // 새 인포윈도우를 생성하여 마커에 연결
        const infowindow = new kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`,
          removable: true,
        });

        // 마커 클릭 시, 장소명을 인포윈도우에 표시
        kakao.maps.event.addListener(marker, "click", function () {
          infowindow.open(map, marker);
          infowindows.push(infowindow); // 새 인포윈도우 배열에 추가
        });

        // 마커를 배열에 저장
        markers.push(marker);
      }

      // 마커를 모두 삭제하는 함수
      function clearMarkers() {
        for (let i = 0; i < markers.length; i++) {
          markers[i].setMap(null); // 마커 제거
        }
        markers = []; // 마커 배열 초기화
      }

      // 모든 인포윈도우를 닫는 함수
      function clearInfowindows() {
        for (let i = 0; i < infowindows.length; i++) {
          infowindows[i].close(); // 인포윈도우 닫기
        }
        infowindows = []; // 인포윈도우 배열 초기화
      }
    });
  };

  document.head.appendChild(script);
});

// 반응형 변수와 계산된 속성
const currentPage = ref(1); // 현재 페이지
const searchResultsInfosPerPage = 3; // 페이지당 항목 수

// 총 페이지 수 계산
const pageCount = computed(() => Math.ceil(searchResultsInfos.value.length / searchResultsInfosPerPage));

// 현재 페이지의 데이터 계산
const paginatedSearchResultsInfos = computed(() => {
  const start = (currentPage.value - 1) * searchResultsInfosPerPage;
  const end = start + searchResultsInfosPerPage;
  return searchResultsInfos.value.slice(start, end);
});

</script>

<style scoped>
.map-container {
  display: flex;
  flex-direction: row;
}

.redbox {
  height: 500px;
  border-radius: 3%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.red {
  transition: 1.3s ease-in-out;
  width: 870px;
}

.blue {
  transition: 1.55s ease-in-out;
  position: relative;
  right: 0;
  width: 0;
  overflow: hidden;
  height: 500px;
}

.shrink {
  width: 570px;
}

.expand {
  width: 300px;
}

.result-box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.cards-container {
  overflow-y: auto;
  height: 100%;
  padding-left: 20px;
  padding-right: 20px;
  flex-grow: 1;
}

.custom-card {
  background-color: #f6f6f6;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  word-wrap: break-word;
  min-width: 200px;
  margin-bottom: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.custom-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.card-link {
  text-decoration: none;
  color: inherit;
}

.card-text {
  font-size: 12px;
  margin: 0px;
  font-weight: 300;
}

.card-phone {
  font-size: 15px;
  color: #0b5bcb;
}

.telephone {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
}

.telephone-img {
  height: 12px;
}
</style>
