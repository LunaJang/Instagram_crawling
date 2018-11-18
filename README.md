# hierarchical structure of tourist spot dataset-master

## 필요 사항

	beautifulsoup, selenium 라이브러리의 설치가 필요합니다

	instagram_crawler.ipnb 파일과 같은 디렉토리에 
	chromedriver.exe 파일과 /dataset/img 폴더가 있어야 합니다.

## 사용법

	파일 실행 후, 검색할 태그의 이름과 스크롤할 수, 스크롤을 시작할 페이지 수를 입력하면 데이터를 크롤링 할 수 있습니다.

	이미지 파일은 .jpg의 형태로 저장되며
	사용자 아이디, 좋아요 수, 텍스트, 해시태그, 레이블은 json의 형태로 저장됩니다.

	이때, 스크롤 한번당 약 45개의 데이터를 크롤링합니다.



		*전처리 코드는 아직 완성되지 않았습니다.
