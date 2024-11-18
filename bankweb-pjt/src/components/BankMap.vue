<template>
  <div>
    <!-- 지도를 표시할 div -->
    <div id="map" style="width:50%;height:400px;"></div>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue';

// selectedRegion 정보를 props를 통해 받아옴
const props = defineProps({
  selectedRegion: Object
});

// 마커들과 인포윈도우를 관리할 배열
let markers = [];
let infowindows = []; // InfoWindow 객체들을 관리할 배열

onMounted(() => {
  // 카카오 맵 스크립트 로드
  const script = document.createElement('script');
  script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=dfb2e0bec61965ccabc61e2b16c946f5&autoload=false&libraries=services"; // autoload=false 추가
  script.async = true;

  script.onload = () => {
    // 카카오 맵 SDK가 로드된 후, 카카오 맵 객체 초기화
    window.kakao.maps.load(() => {
      const mapContainer = document.getElementById('map'); // 지도를 표시할 div
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 기본 중심 좌표 (서울)
        level: 3 // 지도 확대 레벨
      };
      const map = new kakao.maps.Map(mapContainer, mapOption); // 지도 생성

      // HTML5의 geolocation으로 현재 위치를 확인합니다
      if (navigator.geolocation) {
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(function(position) {
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

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정
            for (let i = 0; i < data.length; i++) {
              displayMarker(data[i], map); // 마커 표시
              bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x)); // 좌표 추가
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
          position: new kakao.maps.LatLng(place.y, place.x)
        });

        // 이전의 모든 인포윈도우를 닫습니다
        clearInfowindows();

        // 새 인포윈도우를 생성하여 마커에 연결
        const infowindow = new kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:12px;">${place.place_name}</div>`,
          removable: true
        });

        // 마커 클릭 시, 장소명을 인포윈도우에 표시
        kakao.maps.event.addListener(marker, 'click', function () {
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
</script>

<style scoped>
/* 스타일이 필요하면 추가 가능합니다 */
</style>
