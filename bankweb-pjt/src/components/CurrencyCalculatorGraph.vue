<!-- <template>
  <div>
    <div class="buttons">
      <v-btn @click="showDaily">일간 추이</v-btn>
      <v-btn @click="showWeekly">주간 추이</v-btn>
    </div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Chart } from "chart.js/auto";

// 그래프 캔버스 참조
const chartCanvas = ref(null);

// 일간 추이 데이터
const dailyRates = ref([
  { date: "2024-11-16", rate: 1315 },
  { date: "2024-11-17", rate: 1320 },
  { date: "2024-11-18", rate: 1318 },
  { date: "2024-11-19", rate: 1325 },
  { date: "2024-11-20", rate: 1328 },
  { date: "2024-11-21", rate: 1330 },
  { date: "2024-11-22", rate: 1332 },
]);

// 주간 추이 데이터
const weeklyRates = ref([
  { week: "Week 1", rate: 1300 },
  { week: "Week 2", rate: 1310 },
  { week: "Week 3", rate: 1325 },
  { week: "Week 4", rate: 1332 },
]);

// Chart.js 인스턴스
let chartInstance = null;

// 일간 추이 그래프 표시
const showDaily = () => {
  updateChart(
    dailyRates.value.map((item) => item.date),
    dailyRates.value.map((item) => item.rate),
    "일간 환율 추이"
  );
};

// 주간 추이 그래프 표시
const showWeekly = () => {
  updateChart(
    weeklyRates.value.map((item) => item.week),
    weeklyRates.value.map((item) => item.rate),
    "주간 환율 추이"
  );
};

// 그래프 업데이트 함수
const updateChart = (labels, data, label) => {
  if (chartInstance) {
    chartInstance.destroy(); // 기존 그래프 삭제
  }
  chartInstance = new Chart(chartCanvas.value, {
    type: "line", // 선형 그래프
    data: {
      labels: labels, // X축 데이터
      datasets: [
        {
          label: label, // 데이터 이름
          data: data, // Y축 데이터
          borderColor: "#42A5F5", // 선 색상
          backgroundColor: "rgba(66, 165, 245, 0.2)", // 배경 색상
          fill: true, // 배경 채우기
          tension: 0.4, // 곡선 정도
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: "top", // 범례 위치
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: label.includes("일간") ? "날짜" : "주", // X축 이름
          },
        },
        y: {
          title: {
            display: true,
            text: "환율 (KRW)", // Y축 이름
          },
          beginAtZero: false,
        },
      },
    },
  });
};

// 컴포넌트 마운트 시 기본값 설정
onMounted(() => {
  showDaily(); // 기본: 일간 추이 표시
});
</script>

<style scoped>
.buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 20px;
}

canvas {
  max-width: 100%;
  height: 400px;
}
</style> -->
