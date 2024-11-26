<template>
  <div class="recommendation-container">
    <nav class="nav-container">
      <div class="tab-wrapper">
        <RouterLink :to="{ name: 'recommended1' }" class="nav-link" active-class="active">
          <div class="link-content">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
                <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2" />
                <circle cx="12" cy="12" r="1" stroke="currentColor" stroke-width="2" />
              </svg>
            </span>
            <div class="link-text">
              <span class="title">금융 목표 기반</span>
              <span class="subtitle">나의 목표에 맞는 금융상품 추천</span>
            </div>
          </div>
        </RouterLink>

        <RouterLink :to="{ name: 'recommended2' }" class="nav-link" active-class="active">
          <div class="link-content">
            <span class="nav-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 15L8 11L12 15L20 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" />
                <path d="M4 19L8 15L12 19L20 11" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" />
                <circle cx="20" cy="7" r="2" stroke="currentColor" stroke-width="2" />
              </svg>
            </span>
            <div class="link-text">
              <span class="title">성장 시뮬레이션 기반</span>
              <span class="subtitle">자산 성장을 위한 맞춤 추천</span>
            </div>
          </div>
        </RouterLink>
      </div>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.recommendation-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-container {
  margin: 40px 0 32px;
}

.tab-wrapper {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.nav-link {
  position: relative;
  text-decoration: none;
  padding: 20px 24px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.link-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: #f8f9fa;
  border-radius: 12px;
  color: #5A87F2;
  transition: all 0.3s ease;
}

.link-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title {
  font-size: 16px;
  font-weight: 600;
  color: #343a40;
  transition: color 0.3s ease;
}

.subtitle {
  font-size: 14px;
  color: #868e96;
  transition: color 0.3s ease;
}

/* 호버 상태 */
.nav-link:hover {
  background: #f8f9fa;
}

.nav-link:hover .nav-icon {
  background: #edf2ff;
  transform: translateY(-2px);
}

/* 활성화 상태 */
.nav-link.active {
  background: #edf2ff;
}

.nav-link.active .nav-icon {
  background: #5A87F2;
  color: white;
}

.nav-link.active .title {
  color: #2f68ef;
}

.nav-link.active .subtitle {
  color: #748ffc;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .recommendation-container {
    padding: 0 16px;
  }

  .nav-container {
    margin: 24px 0;
  }

  .tab-wrapper {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 8px;
  }

  .nav-link {
    padding: 16px;
  }

  .link-content {
    gap: 12px;
  }

  .nav-icon {
    width: 36px;
    height: 36px;
  }

  .title {
    font-size: 15px;
  }

  .subtitle {
    font-size: 13px;
  }
}
</style>