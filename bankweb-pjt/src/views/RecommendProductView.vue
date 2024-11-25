<template>
  <div class="recommendation-container">
    <nav class="nav-container">
      <RouterLink 
        :to="{ name: 'recommended1' }" 
        class="nav-link"
        active-class="active"
      >
        <span class="icon">🎯</span>
        나의 금융 목표 기반 추천
      </RouterLink>
      
      <div class="separator"></div>
      
      <RouterLink 
        :to="{ name: 'recommended2' }" 
        class="nav-link"
        active-class="active"
      >
        <span class="icon">📈</span>
        자산 성장 시뮬레이션 기반 추천
      </RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.recommendation-container {
  max-width: 1200px;
  margin: 0 auto;
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin: 24px 0;
  background: #fff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  color: #495057;
  text-decoration: none;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-link:hover {
  background: #f8f9fa;
  color: #5A87F2;
  transform: translateY(-2px);
}

.nav-link.active {
  background: #5A87F2;
  color: white;
}

.separator {
  width: 1px;
  height: 24px;
  background: #dee2e6;
}

.icon {
  font-size: 18px;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 12px;
    padding: 12px;
  }

  .nav-link {
    width: 100%;
    justify-content: center;
    padding: 10px 16px;
    font-size: 14px;
  }

  .separator {
    width: 80%;
    height: 1px;
    margin: 4px 0;
  }
}

/* 호버 애니메이션 */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.nav-link:active {
  transform: scale(0.95);
}
</style>