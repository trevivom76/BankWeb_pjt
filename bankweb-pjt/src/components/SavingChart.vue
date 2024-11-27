<template>
  <div class="chart-container">
    <ul class="chart-list">
      <li class="chart-item">
        <h3 class="chart-title">예치 기간별 자유 적립식 우대 금리 비교</h3>
        <canvas ref="freeSavingRateChart"></canvas>
      </li>
      <li class="chart-item">
        <h3 class="chart-title">예치 기간별 정액 적립식 우대 금리 비교</h3>
        <canvas ref="fixedSavingRateChart"></canvas>
      </li>
    </ul>
    <p class="chart-label">※ 0%로 표시된 금리는 해당 예치기간이 없는 상품입니다.</p>
  </div>
</template>

<script setup>
import { onMounted, ref, defineProps } from "vue";
import Chart from "chart.js/auto";

const prop = defineProps({
  freeSavingData: Array,
  freeSavingData2: Array,
  freeSavingData3: Array,
  fixedSavingData: Array,
  fixedSavingData2: Array,
  fixedSavingData3: Array,
})

// 캔버스 엘리먼트를 참조할 ref 생성s
const freeSavingRateChart = ref(null);
const fixedSavingRateChart = ref(null);

onMounted(() => {
  // 기간 레이블
  const labels = ["6개월", "12개월", "24개월", "36개월"];

  if (freeSavingRateChart.value) {
    new Chart(freeSavingRateChart.value.getContext("2d"), {
      type: "line", // 라인 차트
      data: {
        labels,
        datasets: [
          {
            label: "저축 금리",
            data: prop.freeSavingData,
            borderColor: "rgba(0, 123, 255, 1)", // 선 색상
            backgroundColor: "rgba(0, 123, 255, 0.1)", // 연한 파란색 점 배경
            borderWidth: 3, // 선 두께
            tension: 0.4, // 부드러운 곡선
            pointStyle: "circle", // 점 모양
            pointRadius: 4, // 점 크기
            pointBackgroundColor: "rgba(255, 255, 255, 1)", // 점 내부 색상
            pointBorderColor: "rgba(0, 123, 255, 1)", // 점 테두리 색상
          },
          {
            label: "최고 우대 금리",
            data: prop.freeSavingData2,
            borderColor: "rgba(255, 99, 132, 1)", // 선 색상
            backgroundColor: "rgba(255, 99, 132, 0.1)", // 연한 빨간색 점 배경
            borderWidth: 3, // 선 두께
            tension: 0.4, // 부드러운 곡선
            pointStyle: "circle",
            pointRadius: 4,
            pointHoverRadius: 4,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointBorderColor: "rgba(255, 99, 132, 1)",
          },
          {
            label: "평균 금리",
            data: prop.freeSavingData3,
            borderColor: "rgba(34, 139, 34, 1)", // 녹색 선 색상 (Forest Green)
            backgroundColor: "rgba(34, 139, 34, 0.1)", // 연한 녹색 점 배경
            borderWidth: 3, // 선 두께
            tension: 0.4, // 부드러운 곡선
            pointStyle: "circle", // 점 스타일
            pointRadius: 4, // 점 크기
            pointHoverRadius: 4, // 마우스 오버 시 점 크기
            pointBackgroundColor: "rgba(255, 255, 255, 1)", // 점 내부 색상
            pointBorderColor: "rgba(34, 139, 34, 1)", // 점 테두리 색상
          }
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true, // 반응형 지원
        plugins: {
          legend: {
            display: true,
            labels: {
              font: {
                size: 12,
                weight: 400,
                family: "pretendard",
              },
              color: "#333",
            },
          },
          tooltip: {
            enabled: true,
            backgroundColor: "rgba(0, 0, 0, 0.7)",
            titleFont: {
              size: 14,
              weight: "bold",
            },
            bodyFont: {
              size: 12,
            },
            cornerRadius: 4,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "예치 기간",
              font: {
                size: 12,
                weight: "bold",
                family: "pretendard",
              },
              color: "#555",
            },
            ticks: {
              font: {
                size: 12,
                family: "pretendard",
              },
              color: "#666",
            },
            grid: {
              color: "rgba(200, 200, 200, 0.3)", // 연한 회색
            },
          },
          y: {
            max: 5.0, // Y축 최대값 설정
            beginAtZero: true, // Y축 0부터 시작
            title: {
              display: true,
              text: "이율 (%)",
              font: {
                size: 12,
                weight: "bold",
                family: "pretendard",
              },
              color: "#555",
            },
            ticks: {
              font: {
                size: 12,
                family: "pretendard",
              },
              color: "#666",
            },
            grid: {
              color: "rgba(200, 200, 200, 0.3)",
            },
          },
        },
      },
      plugins: [
        {
          id: "shadowBackground",
          beforeDraw: (chart) => {
            const ctx = chart.ctx;
            ctx.save();
            ctx.shadowColor = "rgba(0, 0, 0, 0.25)";
            ctx.shadowBlur = 20;
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 10;
            ctx.fillStyle = "white";
            ctx.fillRect(
              chart.chartArea.left,
              chart.chartArea.top,
              chart.chartArea.right - chart.chartArea.left,
              chart.chartArea.bottom - chart.chartArea.top
            );
            ctx.restore();
          },
        },
      ],
    });
  }

  if (fixedSavingRateChart.value) {
    new Chart(fixedSavingRateChart.value.getContext("2d"), {
      type: "line", // 라인 차트
      data: {
        labels,
        datasets: [
          {
            label: "저축 금리",
            data: prop.fixedSavingData,
            borderColor: "rgba(0, 123, 255, 1)", // 선 색상
            backgroundColor: "rgba(0, 123, 255, 0.1)", // 연한 파란색 점 배경
            borderWidth: 3, // 선 두께
            tension: 0.4, // 부드러운 곡선
            pointStyle: "circle", // 점 모양
            pointRadius: 4, // 점 크기
            pointBackgroundColor: "rgba(255, 255, 255, 1)", // 점 내부 색상
            pointBorderColor: "rgba(0, 123, 255, 1)", // 점 테두리 색상
          },
          {
            label: "최고 우대 금리",
            data: prop.fixedSavingData2,
            borderColor: "rgba(255, 99, 132, 1)", // 선 색상
            backgroundColor: "rgba(255, 99, 132, 0.1)", // 연한 빨간색 점 배경
            borderWidth: 3, // 선 두께
            tension: 0.4, // 부드러운 곡선
            pointStyle: "circle",
            pointRadius: 4,
            pointHoverRadius: 4,
            pointBackgroundColor: "rgba(255, 255, 255, 1)",
            pointBorderColor: "rgba(255, 99, 132, 1)",
          },
          {
            label: "평균 금리",
            data: prop.fixedSavingData3,
            borderColor: "rgba(34, 139, 34, 1)", // 녹색 선 색상 (Forest Green)
            backgroundColor: "rgba(34, 139, 34, 0.1)", // 연한 녹색 점 배경
            borderWidth: 3, // 선 두께
            tension: 0.4, // 부드러운 곡선
            pointStyle: "circle", // 점 스타일
            pointRadius: 4, // 점 크기
            pointHoverRadius: 4, // 마우스 오버 시 점 크기
            pointBackgroundColor: "rgba(255, 255, 255, 1)", // 점 내부 색상
            pointBorderColor: "rgba(34, 139, 34, 1)", // 점 테두리 색상
          }
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true, // 반응형 지원
        plugins: {
          legend: {
            display: true,
            labels: {
              font: {
                size: 12,
                weight: 400,
                family: "pretendard",
              },
              color: "#333",
            },
          },
          tooltip: {
            enabled: true,
            backgroundColor: "rgba(0, 0, 0, 0.7)",
            titleFont: {
              size: 14,
              weight: "bold",
            },
            bodyFont: {
              size: 12,
            },
            cornerRadius: 4,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "예치 기간",
              font: {
                size: 12,
                weight: "bold",
                family: "pretendard",
              },
              color: "#555",
            },
            ticks: {
              font: {
                size: 12,
                family: "pretendard",
              },
              color: "#666",
            },
            grid: {
              color: "rgba(200, 200, 200, 0.3)", // 연한 회색
            },
          },
          y: {
            max: 5.0, // Y축 최대값 설정
            beginAtZero: true, // Y축 0부터 시작
            title: {
              display: true,
              text: "이율 (%)",
              font: {
                size: 12,
                weight: "bold",
                family: "pretendard",
              },
              color: "#555",
            },
            ticks: {
              font: {
                size: 12,
                family: "pretendard",
              },
              color: "#666",
            },
            grid: {
              color: "rgba(200, 200, 200, 0.3)",
            },
          },
        },
      },
      plugins: [
        {
          id: "shadowBackground",
          beforeDraw: (chart) => {
            const ctx = chart.ctx;
            ctx.save();
            ctx.shadowColor = "rgba(0, 0, 0, 0.25)";
            ctx.shadowBlur = 20;
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 10;
            ctx.fillStyle = "white";
            ctx.fillRect(
              chart.chartArea.left,
              chart.chartArea.top,
              chart.chartArea.right - chart.chartArea.left,
              chart.chartArea.bottom - chart.chartArea.top
            );
            ctx.restore();
          },
        },
      ],
    });
  }
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 30px 10px 10px 10px;
}

.chart-list {
  list-style: none;
  /* 기본 리스트 스타일 제거 */
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  /* 세로로 나열 */
  gap: 30px;
  /* 아이템 간 간격 */
}

.chart-item {
  background-color: #f9f9f9;
  /* 밝은 배경 */
  border: 1px solid #ddd;
  /* 연한 테두리 */
  border-radius: 8px;
  /* 모서리 둥글게 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* 그림자 효과 */
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 아이템을 가운데 정렬 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  /* 애니메이션 추가 */
}

.chart-item:hover {
  transform: translateY(-5px);
  /* 마우스 올리면 살짝 위로 */
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  /* 그림자 강조 */
}

.chart-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.chart-label {
  font-size: 12px;
  padding: 12px 0px;
}
</style>
