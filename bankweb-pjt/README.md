<div align="center">

# 📌 프로젝트 이름 및 소개 🏷️
- **프로젝트명**: BBK 팀
- **프로젝트 개요**: 프로젝트의 목적과 핵심 기능에 대한 간략한 설명을 포함합니다. (예: 사용자 맞춤 금융 상품 추천 서비스)
- **프로젝트 기간**: 2024.11.18 ~ 2024.11.26

---

## 목차 📑
### [프로젝트 개요](#-프로젝트-이름-및-소개-)

### [팀원 정보 및 역할 분담](#팀원-정보-및-역할-분담-)

### [기술 스택](#기술-스택-)

### [주요 기능](#주요-기능-)

### [설계 및 데이터베이스 구조](#설계-및-데이터베이스-구조-)

### [화면 구성](#화면-구성-)

### [개발 과정 이슈](#개발-과정-이슈-)

### [알고리즘 설명](#알고리즘-설명-)

### [성과 및 후기](#성과-및-후기-)

### [기타](#기타-)


---

## 팀원 정보 및 역할 분담 👥
### 팀원

- **심근원**: 팀장, Frontend 개발, 주변 은행 찾기 기능, Figma
- **배지해**: Backend 개발, ERD
- **태성원**: Frontend 개발, ERD, 환율 계산기 기능, 메인페이지 UI/UX, Figma, README 작성




---

## 기술 스택 💻

### Language
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Frontend
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Vuetify](https://img.shields.io/badge/Vuetify-1867C0?style=for-the-badge&logo=vuetify&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-yellow?style=for-the-badge&logo=vue.js&logoColor=black)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)

### Backend
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-FF1709?style=for-the-badge&logo=django&logoColor=white)
![dj-rest-auth](https://img.shields.io/badge/dj--rest--auth-FF1709?style=for-the-badge&logo=django&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3C9A43?style=for-the-badge&logo=pillow&logoColor=white)

### Database
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![API](https://img.shields.io/badge/API-005571?style=for-the-badge&logo=api&logoColor=white)

### 기타
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)


---

## 주요 기능 🛠️
### 로그인 및 로그아웃 기능  
사용자가 서비스에 접근하기 위해 로그인하거나, 로그아웃할 수 있는 기능을 제공합니다.  
**사용된 기술**: JWT 인증, Django Authentication 등.

### 회원가입 기능  
새로운 사용자가 계정을 등록하고 서비스에 가입할 수 있는 기능입니다.  
**사용된 기술**: Django Forms, MySQL 등.

### 예적금 데이터 관리 (최소 50개 이상)  
다양한 예적금 상품 데이터를 저장하고 관리합니다.  
**사용된 기술**: 금융감독원 API, Django ORM 등.

### 예적금 상품 목록 조회  
사용자가 다양한 예적금 상품을 목록 형태로 볼 수 있는 기능을 제공합니다.  
**사용된 기술**: Vue.js, Django REST API 등.  
**스크린샷**: ![예적금 목록 조회](./assets/deposit_list.png)

### 예적금 상품 상세 목록 조회  
특정 예적금 상품의 상세 정보를 보여주는 기능입니다.  
**사용된 기술**: Vue.js, Axios 등.  
**스크린샷**: ![예적금 상세 조회](./assets/deposit_detail.png)

### 커뮤니티 게시글 기능  
사용자가 금융 관련 정보를 공유할 수 있는 게시글 작성 및 조회 기능입니다.  
**사용된 기술**: Django REST Framework, Vue.js 등.  
**스크린샷**: ![커뮤니티 게시글](./assets/community_posts.png)

### 커뮤니티 댓글 기능  
사용자가 게시글에 댓글을 달고 상호작용할 수 있는 기능을 제공합니다.  
**사용된 기술**: Django REST Framework, Vue.js 등.  
**스크린샷**: ![댓글 기능](./assets/community_comments.png)

### 환율 계산 기능  
사용자가 원화와 외화를 상호 변환할 수 있도록 지원하는 환율 계산 기능입니다.  
**사용된 기술**: 한국수출입은행 환율 API, JavaScript 계산 로직 등.  
**스크린샷**: ![환율 계산기](./assets/exchange_calculator.png)

### 프로필 기능  
사용자가 자신의 프로필을 조회하고 정보를 업데이트할 수 있는 기능을 제공합니다.  
**사용된 기술**: Django User 모델, Vue.js 등.  
**스크린샷**: ![프로필 페이지](./assets/profile_page.png)

### 주변 은행 검색 기능  
사용자가 특정 은행을 검색하고, 주변 위치를 지도에서 확인할 수 있는 기능입니다.  
**사용된 기술**: Kakao Map API, Vue.js 등.  
**스크린샷**: ![주변 은행 검색](./assets/nearby_banks.png)

### 금융 상품 추천 알고리즘  
사용자의 입력을 기반으로 적합한 금융 상품을 추천하는 알고리즘입니다.  
**사용된 기술**: Pandas, Django ORM, 머신 러닝 모델.  
**예시**: 사용자 나이, 자산, 투자 성향 등을 고려하여 유사한 사용자가 선택한 금융 상품 추천.  
**스크린샷**: ![금융 상품 추천](./assets/financial_recommendations.png)

### AI 추천/검색 기능  
AI를 활용하여 사용자에게 최적의 금융 상품을 추천하거나, 사용자가 검색한 조건에 맞는 결과를 반환하는 기능입니다.  
**사용된 기술**: Python 기반의 추천 시스템, 머신 러닝 등.  
**스크린샷**: ![AI 추

---

## 설계 및 데이터베이스 구조 📊
### 아키텍처 다이어그램  
프로젝트 전체 구조를 시각화한 다이어그램을 첨부합니다.  
![아키텍처 다이어그램](./assets/architecture.png)

### ERD (Entity Relationship Diagram)  
데이터베이스 모델링을 설명하는 ERD 이미지를 포함합니다.  
![ERD 다이어그램](./assets/ERD.png)


---

### 프로젝트 주요 화면  

#### 메인 페이지  
서비스의 주요 기능에 대한 개요와 네비게이션을 제공.  
![메인 페이지](./src/images/main.png)

#### 로그인 페이지  
기존 사용자들이 계정으로 접근할 수 있는 로그인 화면.  
![로그인 페이지](./src/images/login.png)

#### 회원가입 페이지  
새로운 사용자가 회원으로 가입할 수 있는 화면.  
![회원가입 페이지](./src/images/signup.png)

#### 정기 예금 검색하기 페이지  
다양한 정기 예금 상품을 검색하고 정보를 제공하는 화면.  
![정기 예금 검색하기 페이지](./src/images/deposit.png)

#### 정기 적금 검색하기 페이지  
여러 정기 적금 상품을 찾아볼 수 있는 화면.  
![정기 적금 검색하기 페이지](./src/images/saving.png)

#### 정기 예금 상세 페이지  
선택한 정기 예금 상품의 상세 정보를 제공하는 페이지.  
![정기 예금 상세 페이지](./src/images/depositdetail.png)

#### 정기 적금 상세 페이지  
특정 정기 적금 상품에 대한 자세한 정보를 보여주는 화면.  
![정기 적금 상세 페이지](./src/images/savingdetail.png)

#### 환율 계산기 페이지  
다양한 통화의 환율을 계산하고 환전 금액을 쉽게 확인할 수 있는 페이지.  
![환율 계산기 페이지](./src/images/currency.png)

#### 주변 은행 페이지  
카카오 맵 API를 사용해 사용자의 위치를 기반으로 주변 은행 지점을 보여주는 화면.  
![주변 은행 페이지](./src/images/bankmap.png)

#### 커뮤니티 페이지  
사용자 간 소통을 위한 게시판 및 커뮤니티 기능을 제공하는 페이지.  
![커뮤니티 페이지](./src/images/community.png)

#### 회원정보 관리 페이지  
사용자 정보 확인 및 수정이 가능한 화면.  
![회원정보 관리 페이지](./src/images/profile.png)

#### 관심상품 관리 페이지  
사용자가 관심을 가진 금융 상품을 관리하는 화면.  
![관심상품 관리 페이지](./src/images/profilebank.png)

#### 관심상품 상세 페이지  
사용자가 관심을 등록한 특정 상품에 대한 상세 정보를 제공하는 화면.  
![관심상품 상세 페이지](./src/images/profilebankchart.png)

#### 상품 추천받기 페이지  
사용자의 입력 정보를 바탕으로 맞춤형 금융 상품을 추천해주는 화면.

---

## 개발 과정 이슈  

### <span style="color:red;">심근원</span>  

**카카오맵 API 검색 정확도**  
**이슈 내용**: 현재 selectbox에서 검색어를 선택하면 카카오맵의 검색엔진을 통해 위치를 받아와 마커를 찍는 방법을 사용하고 있습니다. 그러나 선택한 지역의 중심점을 기준으로 상하좌우 지정된 범위 내의 모든 검색 결과가 표시되다 보니, 특정 구역이 가로세로로 길 경우 예상 범위 밖의 은행 지점까지 검색되는 문제가 발생하고 있습니다.  
**해결 방법**: 검색 결과를 저장한 뒤, 구미시가 아닌 결과들을 제외하여 마커와 infowindow를 표시하는 방법으로 해결 예정.

**카카오맵 CSS 적용 시 검색 핀 중앙 화면 출력 불가**  
**이슈 내용**: 카카오맵 슬라이드 CSS 적용 시 맵 중앙이 출력되지 않고 살짝 왼쪽으로 출력되는 문제 발생.  
**해결 방법**: shrink 이후 width 값을 제대로 인식하도록 수정해야 함. (현재 해결 방법을 찾지 못한 상태)

**유저 프로필 불러오기 문제**  
**이슈 내용**: Django에서 유저 프로필 이미지를 넘겨주는 문자열 경로로는 프로필 이미지를 제대로 출력할 수 없음.  
**해결 방법**: `Model Article`과 `comment` 모델 모두에 대해 설정을 추가.

**댓글 작성 시 댓글 리스트 비동기적 변화 문제**  
**이슈 내용**: detail 페이지에서 댓글 작성 후 댓글 리스트가 동기적으로 업데이트되지 않는 문제 발생.  
**해결 방법**: axios 요청을 모두 async 함수로 감싸고, `await`를 사용하여 비동기 작업을 기다린 후 처리.

**중앙 저장소 간의 token 전달 문제**  
**이슈 내용**: token을 중앙 저장소 간에 주고받는 과정에서 반응성을 유지하지 못해 문제가 발생.  
**해결 방법**: API 모듈을 따로 만들어 모든 axios 요청에 대해 token 값을 넘겨주는 방식으로 문제 해결.

**프로필 이미지 불러오기 오류**  
**이슈 내용**: Django의 media 파일에 저장된 프로필 이미지를 상대경로로 읽어오게 되어 이미지 출력 문제 발생.  
**해결 방법**: Django의 `get_absolute_url`을 사용하여 절대경로로 읽어오도록 수정.

### <span style="color:red;">배지해</span>  

**dj-rest-auth의 커스텀 User 모델 회원가입 문제**  
**이슈 내용**: 커스텀한 User 모델의 필드(name, nickname 등)가 DB에 저장되지 않음.  
**해결 방법**: 추가된 필드 데이터를 업데이트한 후 다시 `user.save()`를 호출하여 저장.

**dj-rest-auth의 회원가입 폼 수정 후 발생하는 오류**  
**이슈 내용**: 회원가입 폼 수정 후 오류 메시지가 제대로 나타나지 않는 문제 발생.  
**해결 방법**: `settings` 파일에서 custom serializer의 변수명을 올바르게 수정.

**예적금 데이터 불러오기 오류**  
**이슈 내용**: API를 통해 데이터를 불러오는 과정에서, 새 컴퓨터에서 프로젝트를 clone할 때 데이터를 불러오지 않는 문제 발생.  
**해결 방법**: financial의 store 함수가 호출될 때마다 데이터를 다운받도록 수정.

### <span style="color:red;">태성원</span>  

**프론트 작업 중 환율 API 활용**  
**이슈 내용**: 환율 API를 활용하는 과정에서 CORS 에러가 발생하여 데이터 불러오지 못함.  
**해결 방법**: 최종적으로 백엔드에서 JSON 형식으로 데이터를 받는 방식으로 전환.

**환율 계산기 flex-wrap 문제**  
**이슈 내용**: 화면 크기 축소 시 레이아웃이 제대로 유지되지 않는 문제 발생.  
**해결 방법**: flex-wrap을 삭제하고 `currencyCalculator.vue` 파일에 `min-width`를 부여하여 해결.

**환율 계산기 실행 오류**  
**이슈 내용**: 오전 11시 이전에는 API가 작동하지 않아 데이터가 불러와지지 않음.  
**해결 방법**: 환율 계산기 실행을 오전 11시 이후로 제한하거나, 데이터를 미리 저장하는 방식을 고려 중.

---

### 알고리즘 설명(수정 전)
**추천 알고리즘**: 사용자 데이터를 기반으로 맞춤형 추천을 제공하는 알고리즘에 대한 설명.  
**예시**: 나이, 자산, 투자 성향을 고려해 비슷한 사용자들이 선택한 금융 상품을 추천.  
**사용된 기술**: Pandas, Django ORM 등 데이터 처리 기술 설명.

---

### 성과 및 후기(수정 전)
**프로젝트 성과**: 프로젝트 결과나 수상 내용 등을 명시합니다.  
**예시**: "SSAFY 1학기 관통 프로젝트 최우수상 수상"

**팀원 후기**: 각 팀원이 프로젝트를 진행하며 느낀 점을 간략하게 기록합니다.  
**예시**: "이 프로젝트를 통해 백엔드와 프론트엔드의 통합 과정을 깊이 이해할 수 있었습니다."

---

### 기타
**참조 링크**: 프로젝트와 관련된 외부 링크나 참고 자료를 추가합니다.  
- [Notion 프로젝트 페이지] https://www.notion.so/ssafy-jinhyeok/3-Bang-Bang-BanK-1377f669b133800c8d13d670f9055e41
- [시연 영상]

</div>

