# 💵 금융 서비스 웹 | BB뱅크

![화면 기록 2024-11-27 오전 5 06 09](https://github.com/user-attachments/assets/9ec3c95c-773c-4652-983b-2504f3a68a3d)

<br/>

---


<details><summary>
목차 📑

</summary>

##### [프로젝트 개요](#-프로젝트-이름-및-소개-)

##### [팀원 정보 및 역할 분담](#팀원-정보-및-역할-분담-)

##### [기술 스택](#기술-스택-)

##### [주요 기능](#주요-기능-)

##### [설계 및 데이터베이스 구조](#설계-및-데이터베이스-구조-)

##### [화면 구성](#화면-구성-)

##### [개발 과정 이슈](#개발-과정-이슈-)

##### [알고리즘 설명](#알고리즘-설명-)

##### [성과 및 후기](#성과-및-후기-)

##### [기타](#기타-)
</details>



---
<br/>

## 📌 프로젝트 이름 및 소개 🏷️
- **프로젝트명**: BB뱅크
- **프로젝트 개요**:
  - 사용자 맞춤 금융 상품 추천 서비스
  - 예적금 상품 리스트 제공
  - 실시간 위치 기반 은행 검색
  - 챗봇 서비스
  - 환율 계산기 기능 지원
- **프로젝트 기간**: 2024.11.18 ~ 2024.11.26 [ 9일 ]

<br/>
<br/>

## 팀원 정보 및 역할 분담 👥
### [팀원]


- **심근원(팀장)**:
  - Frontend 개발
	  - 회원가입/로그인
	  - 주변 은행 찾기
	  - 커뮤니티
	  - 프로필 페이지
	  - 금융 상품 추천 페이지
  - 금융 상품 추천 알고리즘
  - 발표

- **배지해**: 
  - Backend 개발
  - Frontend 개발
	  - 메인페이지
	  - 금리비교 예금/적금 비교
	  - ChatBot
	  - 사용자 관심 상품 페이지
	  - 환율 계산기의 차트
	  - CSS 작업
   - 디자인

- **태성원**:
  - Frontend 개발
    - 환율 계산기
    - 메인페이지의 은행 리스트
  - README 작성

- **공통**
	- ERD
	- Figma 작업



<br/>
<br/>

## 설계 및 데이터베이스 구조 📊
### 🍀 설계 아키텍처
![설계 아키텍처 (수정 후)](https://github.com/user-attachments/assets/7ffbf3e9-4e1d-44a8-a890-d24d8cb17233)

<br/>

### ☁ 데이터베이스 모델링(ERD)
![image](https://github.com/user-attachments/assets/5ceb7dc2-397f-4ce4-ba03-97f3323eac46)

<br/>


### 🎨 Figma

[**Figma**](https://www.figma.com/design/dDetrQDZK7zapQfm4PAs4r/bank-web-project?node-id=0-1&t=b9xu6cysizeSGOdb-1)

![image](https://github.com/user-attachments/assets/3094f9b4-d1ec-47df-a34a-dcb91ed4ed7a)

<br/>
<br/>

### 🖼 디자인 목업
![디자인 목업](https://github.com/user-attachments/assets/069939af-5bbd-46ba-bba9-1d72482c227a)


<br/>
<br/>


## 기술 스택 💻
#####  **Language**
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

##### **Frontend**
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Vuetify](https://img.shields.io/badge/Vuetify-1867C0?style=for-the-badge&logo=vuetify&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-yellow?style=for-the-badge&logo=vue.js&logoColor=black)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)

##### **Backend**
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-FF1709?style=for-the-badge&logo=django&logoColor=white)
![dj-rest-auth](https://img.shields.io/badge/dj--rest--auth-FF1709?style=for-the-badge&logo=django&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-3C9A43?style=for-the-badge&logo=pillow&logoColor=white)

##### **Database**
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![API](https://img.shields.io/badge/API-005571?style=for-the-badge&logo=api&logoColor=white)


##### **기타**
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![MiridCanvas](https://img.shields.io/badge/MiridCanvas-00C4CC?style=for-the-badge&logo=canva&logoColor=white)


<br/>
<br/>



## 주요 기능 🛠️
- 로그인 및 로그아웃 기능  
: 사용자가 서비스에 접근하기 위해 로그인하거나, 로그아웃할 수 있는 기능을 제공합니다.  
**사용된 기술**: Django Authentication (dj-rest-auth 토큰 인증 사용)

- 회원가입 기능  
: 새로운 사용자가 계정을 등록하고 서비스에 가입할 수 있는 기능입니다.  
**사용된 기술**: Django Authentication, SQLLite

- 예적금 데이터 관리 (최소 50개 이상)  
: 다양한 예적금 상품 데이터를 저장하고 관리합니다.  
**사용된 기술**: 금융감독원 API, SQLLite

- 예적금 상품 목록 조회  
: 사용자가 다양한 예적금 상품을 목록 형태로 볼 수 있는 기능을 제공합니다.  
**사용된 기술**: Vue.js, Django REST API 등.  

-  예적금 상품 상세 목록 조회  
: 특정 예적금 상품의 상세 정보를 보여주는 기능입니다.  
**사용된 기술**: Vue.js, Axios 등.  

- 커뮤니티 게시글 기능  
: 사용자가 금융 관련 정보를 공유할 수 있는 게시글 작성 및 조회 기능입니다.  
**사용된 기술**: Django REST Framework, Vue.js 등.  

- 커뮤니티 댓글 기능  
: 사용자가 게시글에 댓글을 달고 상호작용할 수 있는 기능을 제공합니다.  
**사용된 기술**: Django REST Framework, Vue.js 등.  

- 환율 계산 기능  
: 사용자가 원화와 외화를 상호 변환할 수 있도록 지원하는 환율 계산 기능입니다.  
**사용된 기술**: 한국수출입은행 환율 API, JavaScript 계산 로직 등.  

- 프로필 기능  
: 사용자가 자신의 프로필을 조회하고 정보를 업데이트할 수 있는 기능을 제공합니다.  
**사용된 기술**: Django User 모델, Vue.js 등.  

- 주변 은행 검색 기능  
: 사용자가 특정 은행을 검색하고, 주변 위치를 지도에서 확인할 수 있는 기능입니다.  
**사용된 기술**: Kakao Map API, Vue.js 등.  

- 금융 상품 추천 알고리즘  
: 사용자의 입력을 기반으로 적합한 금융 상품을 추천하는 알고리즘입니다.  
**사용된 기술**: Pandas, Django ORM, 머신 러닝 모델.  
**예시**: 사용자 나이, 자산, 투자 성향 등을 고려하여 유사한 사용자가 선택한 금융 상품 추천.  

- AI 추천/검색 기능  
: AI를 활용하여 사용자에게 최적의 금융 상품을 추천하거나, 사용자가 검색한 조건에 맞는 결과를 반환하는 기능입니다.  
**사용된 기술**: Python 기반의 추천 시스템, 머신 러닝 등.  


<br/>
<br/>

---

### 프로젝트 주요 화면  

<br/>

#### 메인 페이지  
: 서비스의 주요 기능에 대한 개요와 네비게이션을 제공.

##### 메인 화면 구성
https://github.com/user-attachments/assets/0dfc5127-4534-4bca-8404-cce481034573

##### 메인 화면 - 예금 계산기
https://github.com/user-attachments/assets/2dca2aaa-dead-49a2-944d-5bf013bb4e46

##### 메인 화면 - 환율 차트
https://github.com/user-attachments/assets/5b1dcec0-a9e4-4f03-a26d-fb6121240bf0

##### 메인 화면 - 은행 사이트
https://github.com/user-attachments/assets/24036f43-ba6a-4ac0-8fec-46cdf0378043

<br/>

#### 로그인 페이지 
기존 사용자들이 계정으로 접근할 수 있는 로그인 화면.  

#### 회원가입 페이지  
새로운 사용자가 회원으로 가입할 수 있는 화면.  

https://github.com/user-attachments/assets/bd4f122f-9f77-4a0f-b6b0-027f3046239f

<br/>

#### 정기 예금 검색하기 페이지  
다양한 정기 예금 상품을 검색하고 정보를 제공하는 화면.

#### 정기 예금 상세 페이지  
선택한 정기 예금 상품의 상세 정보를 제공하는 페이지.  


#### 정기 적금 검색하기 페이지  
여러 정기 적금 상품을 찾아볼 수 있는 화면.  

#### 정기 적금 상세 페이지  
특정 정기 적금 상품에 대한 자세한 정보를 보여주는 화면.  

https://github.com/user-attachments/assets/86299277-fd78-45ca-bc40-f03e02b850a1

<br/>

#### 환율 계산기 페이지  
다양한 통화의 환율을 계산하고 환전 금액을 쉽게 확인할 수 있는 페이지.  

https://github.com/user-attachments/assets/3a61746b-4509-49e8-ac65-a1ad2ab06bb0

https://github.com/user-attachments/assets/5b0d9052-39b4-4ba8-b9e4-2773e9a50c61

<br/>

#### 주변 은행 페이지  
카카오 맵 API를 사용해 사용자의 위치를 기반으로 주변 은행 지점을 보여주는 화면.  
https://github.com/user-attachments/assets/e10e9f84-58e0-492d-b6a3-3ceb236c1ada

https://github.com/user-attachments/assets/aaf040f4-00f5-49b6-8b4d-5879080dd897

<br/>

#### 커뮤니티 페이지  
사용자 간 소통을 위한 게시판 및 커뮤니티 기능을 제공하는 페이지.

https://github.com/user-attachments/assets/213557e6-e444-4ee3-8680-ead9e97a694b

https://github.com/user-attachments/assets/e97ece93-71ed-4cd3-b95f-0c6241cf8451

https://github.com/user-attachments/assets/20d012f6-258d-4375-8df2-85bd12a4da49

https://github.com/user-attachments/assets/b9da45d0-4541-477a-9554-b48e7a642be4

https://github.com/user-attachments/assets/81d59ee2-64c4-43ae-b15f-0a3aeaa7588e


#### 회원정보 관리 페이지  
사용자 정보 확인 및 수정이 가능한 화면.  

https://github.com/user-attachments/assets/75abeb77-d92b-4792-bd5d-8672a74bcb63

https://github.com/user-attachments/assets/8ea8624f-8ada-4a24-98ff-8a57720cebad


#### 관심상품 관리 페이지  
사용자가 관심을 가진 금융 상품을 관리하는 화면.  

#### 관심상품 상세 페이지  
사용자가 관심을 등록한 특정 상품에 대한 상세 정보를 제공하는 화면.  

https://github.com/user-attachments/assets/21887c04-bfa5-4159-81b9-62c2da825482

#### 상품 추천받기 페이지  
사용자의 입력 정보를 바탕으로 맞춤형 금융 상품을 추천해주는 화면.

https://github.com/user-attachments/assets/3abd7dd1-8523-4145-a257-2eaa5182adab

https://github.com/user-attachments/assets/d9f826fc-066a-4de0-a430-671927d86723

#### 챗봇 기능
사용자의 입력 정보를 바탕으로 금융상품및 주변은행위치, 환율등을 채팅으로 알려주는 서비스.


<br/>
<br/>

## 개발 과정 이슈  

### 심근원

- **카카오맵 API 검색 정확도**  
**이슈 내용**: 현재 selectbox에서 검색어를 선택하면 카카오맵의 검색엔진을 통해 위치를 받아와 마커를 찍는 방법을 사용하고 있습니다. 그러나 선택한 지역의 중심점을 기준으로 상하좌우 지정된 범위 내의 모든 검색 결과가 표시되다 보니, 특정 구역이 가로세로로 길 경우 예상 범위 밖의 은행 지점까지 검색되는 문제가 발생하고 있습니다.  
**해결 방법**: 검색 결과를 저장한 뒤, 구미시가 아닌 결과들을 제외하여 마커와 infowindow를 표시하는 방법으로 해결 하였습니다.

- **카카오맵 CSS 적용 시 검색 핀 중앙 화면 출력 불가**  
**이슈 내용**: 카카오맵 슬라이드 CSS 적용 시 맵 중앙이 출력되지 않고 살짝 왼쪽으로 출력되는 문제 발생.  
**해결 방법**: shrink 이후 width 값을 제대로 인식하도록 수정해야 했습니다.


- **댓글 작성 시 댓글 리스트 비동기적 변화 문제**  
**이슈 내용**: detail 페이지에서 댓글 작성 후 댓글 리스트가 동기적으로 업데이트되지 않는 문제 발생.  
**해결 방법**: axios 요청을 모두 async 함수로 감싸고, `await`를 사용하여 비동기 작업을 기다린 후 처리.

- **중앙 저장소 간의 token 전달 문제**  
**이슈 내용**: token을 중앙 저장소 간에 주고받는 과정에서 반응성을 유지하지 못해 문제가 발생.  
**해결 방법**: API 모듈을 따로 만들어 모든 axios 요청에 대해 token 값을 넘겨주는 방식으로 문제 해결.

- **프로필 이미지 불러오기 오류**  
**이슈 내용**: Django의 media 파일에 저장된 프로필 이미지를 상대경로로 읽어오게 되어 이미지 출력 문제 발생.  
**해결 방법**: Django의 `get_absolute_url`을 사용하여 절대경로로 읽어오도록 수정.

<br/>

### 배지해

- **dj-rest-auth의 커스텀 User 모델 회원가입 문제**  
**이슈 내용**: 커스텀한 User 모델의 필드(name, nickname 등)가 DB에 저장되지 않음.  
**해결 방법**: 추가된 필드 데이터를 업데이트한 후 다시 `user.save()`를 호출하여 저장.

- **dj-rest-auth의 회원가입 폼 수정 후 발생하는 오류**  
**이슈 내용**: 회원가입 폼 수정 후 오류 메시지가 제대로 나타나지 않는 문제 발생.  
**해결 방법**: `settings` 파일에서 custom serializer의 변수명을 올바르게 수정.

- **예적금 데이터 불러오기 오류**  
**이슈 내용**: API를 통해 데이터를 불러오는 과정에서, 새 컴퓨터에서 프로젝트를 clone할 때 데이터를 불러오지 않는 문제 발생.  
**해결 방법**: financial의 store 함수가 호출될 때마다 데이터를 다운받도록 수정.

<br/>

### 태성원

- **프론트 작업 중 환율 API 활용**  
**이슈 내용**: 환율 API를 활용하는 과정에서 CORS 에러가 발생하여 데이터 불러오지 못함.  
**해결 방법**: 최종적으로 백엔드에서 JSON 형식으로 데이터를 받는 방식으로 전환.

- **환율 계산기 flex-wrap 문제**  
**이슈 내용**: 화면 크기 축소 시 레이아웃이 제대로 유지되지 않는 문제 발생.  
**해결 방법**: flex-wrap을 삭제하고 `currencyCalculator.vue` 파일에 `min-width`를 부여하여 해결.

- **환율 계산기 실행 오류**  
**이슈 내용**: 오전 11시 이전에는 API가 작동하지 않아 데이터가 불러와지지 않음.  
**해결 방법**: 환율 계산기 실행을 오전 11시 이후로 제한하거나, 데이터를 미리 저장하는 방식을 고려 중.


<br/>
<br/>

### 추천 알고리즘 설명
사용자 데이터를 기반으로 맞춤형 추천을 제공하는 알고리즘에 대한 설명.  
나이, 자산, 투자 성향을 고려해 비슷한 사용자들이 선택한 금융 상품을 추천.  


<br/>
<br/>

### 성과 및 후기

[ **심근원** ]

관통 프로젝트를 통해 한 학기 동안 배운 기술 스택을 종합적으로 활용하며 여러 도전과 성장의 기회를 경험했습니다.

특히 프론트엔드 개발 과정에서 Vue의 Life Cycle Hook에 대한 깊은 이해가 필요했고, 이는 프로필 이미지 관리와 댓글 기능 구현에 많은 시간이 소요되는 계기가 되었습니다. 또한 여러 개의 중앙 저장소(Store)를 다루는 과정에서 데이터 동기화 문제, 그리고 데이터베이스에 성공적으로 저장된 정보를 프론트엔드에서 제대로 불러오지 못하는 등 다양한 기술적 문제들을 해결하며 프론트엔드와 백엔드의 상호작용에 대한 이해도를 높일 수 있었습니다.

프로젝트를 통해 얻은 또 다른 중요한 경험은 Git을 활용한 팀 협업이었습니다. 팀원들과의 효과적인 역할 분담과 원활한 의사소통이 프로젝트의 성공에 얼마나 큰 영향을 미치는지 직접 체감할 수 있었고, 이를 통해 업무 효율성이 크게 향상되는 것을 경험했습니다.

이번 프로젝트 기간 동안 마주친 다양한 문제들과 그 해결 과정, 그리고 배운 점들을 체계적으로 정리하고 학습함으로써, 개발자로서 한 단계 더 성장할 수 있는 의미 있는 기회가 되었습니다.

<br/>

[ **배지해** ]

반년 동안 배운 내용을 실제 프로젝트에 적용해 보면서 많은 흥미와 깨달음을 얻을 수 있었습니다.
에러가 발생했을 때, 꼼꼼하게 학습한 부분은 비교적 빠르게 해결할 수 있었지만, 부족한 부분에서는 꽤 오랫동안 막히기도 했습니다.
이를 통해 개념 학습의 중요성을 절실히 느낄 수 있었습니다.

이번 웹 프로젝트를 진행하면서 백엔드의 구조를 어떻게 기획해야 하는지에 대해 깊이 이해하게 되었고, 
다양한 CSS 기술을 실습해볼 수 있었습니다. 
또한, 팀원들과의 협업을 통해 프론트엔드와 백엔드 간의 원활한 소통이 얼마나 중요한지 실감했습니다.

반학기 동안 배운 개념 중 부족한 부분을 보충할 수 있는 좋은 기회가 되었고,
앞으로도 지속적으로 학습하며 성장할 수 있는 계기가 되었습니다.

우리 팀원들 수고하셨습니다~

<br/>

[ **태성원** ]

이번 프로젝트는 제게 많은 깨달음과 배움의 시간이었습니다.
팀 내에서 부족한 실력을 가진 학생이었고, 팀원들의 도움을 받아 프로젝트에 참여할 수 있었습니다. 

다만, 이 점이 가장 아쉽게 느껴졌습니다. 1학기 동안 학습에 좀 더 충실했더라면, 이번 프로젝트에서 더 나은 성과를 보여줄 수 있었을 텐데 하는 아쉬움이 큽니다. 

그럼에도 불구하고, 이번 경험은 제게 팀 활동의 중요성을 처음으로 느끼게 해주었습니다. 
팀원들이 맡은 역할을 120% 소화하며 협업하는 모습을 보며 큰 자극을 받았고, 저 역시 부족하지만 맡은 기능을 완성하기 위해 최선을 다했습니다. 

비록 개발 속도가 느려 하나의 기능을 완성하는 데 3일이나 걸리기도 했습니다. 
기능을 만드는 과정에서 CSS 기술 이슈와 DB 저장 이슈가 발생해서 이걸 보완하고자 시도하였지만 역량이 부족한 탓에 다른 팀원의 도움 덕에 팀 적으로 해결할 수 있었습니다.
그 과정에서 배운 점이 많았습니다. 
저 스스로 아쉬움과 부족함을 느끼면서도, 이런 경험들이 저를 성장시키는 자양분이 될 것이라는 확신이 들었습니다.

무엇보다 이번 프로젝트를 통해 얻은 가장 큰 교훈은, 협업의 중요성과 프로젝트를 끝까지 해내는 의지입니다. 
이번 경험을 바탕으로, 2학기 프로젝트에서는 제가 팀을 이끌어갈 수 있을 만큼 성장하고 싶습니다. 
더 나아가, 팀원들에게 의존하기보다는 함께 이끌어갈 수 있는 동료로 자리 잡고 싶습니다.
짧았지만 의미 있었던 첫 프로젝트를 통해, 부족함을 인정하고 앞으로 나아갈 방향을 잡을 수 있었습니다. 
이런 기회를 주신 팀원들과 모르는 부분을 물어봐도 성심성의껏 도와준 반 친구들에게 진심으로 고맙습니다.


<br/>
<br/>


### 기타
**참조 링크**: 프로젝트와 관련된 외부 링크나 참고 자료를 추가합니다.  
- [Notion 프로젝트 페이지] https://www.notion.so/ssafy-jinhyeok/3-Bang-Bang-BanK-1377f669b133800c8d13d670f9055e41
