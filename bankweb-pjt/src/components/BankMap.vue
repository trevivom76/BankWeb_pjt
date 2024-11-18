<template>
    <div>
      <!-- 지도를 표시할 div -->
      <div id="map" style="width:100%;height:350px;"></div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue';
  
  onMounted(() => {
    // 카카오 맵 스크립트 로드
    const script = document.createElement('script');
    script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=dfb2e0bec61965ccabc61e2b16c946f5&autoload=false&libraries=services"; // autoload=false 추가
    script.async = true;
    script.onload = () => {
        // 카카오 맵 SDK가 로드된 후, 카카오 맵 객체 초기화
        window.kakao.maps.load(() => {
        // 마커를 클릭하면 장소명을 표출할 인포윈도우 입니다
        const infowindow = new kakao.maps.InfoWindow({zIndex:1});
        const mapContainer = document.getElementById('map'); // 지도를 표시할 div
        const mapOption = {
          center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심 좌표
          level: 3 // 지도의 확대 레벨
        };
        const map = new kakao.maps.Map(mapContainer, mapOption); // 지도 생성

        // 장소 검색 객체를 생성합니다
        const ps = new kakao.maps.services.Places(map); 

        // 카테고리로 은행을 검색합니다
        ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true}); 

        // 키워드 검색 완료 시 호출되는 콜백함수 입니다
        function placesSearchCB (data, status, pagination) {
            if (status === kakao.maps.services.Status.OK) {
                for (let i=0; i<data.length; i++) {
                    displayMarker(data[i]);    
                }       
            }
        }

        // 지도에 마커를 표시하는 함수입니다
        function displayMarker(place) {
            // 마커를 생성하고 지도에 표시합니다
            const marker = new kakao.maps.Marker({
                map: map,
                position: new kakao.maps.LatLng(place.y, place.x) 
            });

            // 마커에 클릭이벤트를 등록합니다
            kakao.maps.event.addListener(marker, 'click', function() {
                // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
                infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
                infowindow.open(map, marker);
            });
        }


      });
    };
  
    document.head.appendChild(script);
  });

  </script>
  
  <style scoped>
  /* 스타일이 필요하면 추가 가능합니다 */
  </style>
  