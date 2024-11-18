<template>
    <div>
      <!-- 지도를 표시할 div -->
      <div id="map" style="width:50%;height:350px;"></div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue';
  
  onMounted(() => {
    // 카카오 맵 스크립트 로드
    const script = document.createElement('script');
    script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=dfb2e0bec61965ccabc61e2b16c946f5&autoload=false"; // autoload=false 추가
    script.async = true;
    script.onload = () => {
      // 카카오 맵 SDK가 로드된 후, 카카오 맵 객체 초기화
      window.kakao.maps.load(() => {
        const mapContainer = document.getElementById('map'); // 지도를 표시할 div
        const mapOption = {
          center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심 좌표
          level: 3 // 지도의 확대 레벨
        };
        const map = new kakao.maps.Map(mapContainer, mapOption); // 지도 생성
      });
    };
  
    document.head.appendChild(script);
  });

  </script>
  
  <style scoped>
  /* 스타일이 필요하면 추가 가능합니다 */
  </style>
  