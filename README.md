# datadrift
Evidently를 통한 데이터 드리프트 현상 관측 및 분석 보고서 작성<br>
<br>



## Evidently
다양한 형태의 데이터셋에 대한 데이터 품질, 모델 평가, 드리프트 등의 시각화 보고서를 출력해주는 프로젝트<br>
[Evidently Docs](https://www.evidentlyai.com/)



## 데이터셋
임베딩 데이터 드리프트 관측을 위해 이미지 데이터 임베딩 생성 작업 수행<br>
evidently가 요구하는 포맷에 맞춰 정제, 시나리오에 맞는 표본 구성<br>

**p02 파일서버에 업로드** (별도 문의)

### Orange3
데이터셋에 대한 다양한 조작 및 정제를 지원하는 어플리케이션<br>
[Orange3 Downlaod](https://orangedatamining.com/download/)

#### 이미지 임베딩 생성기
orange3 application을 활용하여 원하는 이미지 데이터에 대한 임베딩 생성 가능

```image_embedd_gen.ows```<br>

1. ```Import Images```<br>

   이미지 파일 업로드<br>
   폴더명을 컬럼명으로 치환
     >ex) ```male/1.jpg | female/2.jpg``` 구성 시 ```male```, ```female``` 두 개의 클래스로 구성된 데이터셋 생성<br>
     
   ```Unique``` 기능을 통해 생성될 컬럼 목록 확인가능
   
3. ```Image Embedding```<br>

   이미지 임베딩 생성
     >생성 차원 width * height * 3(RGB)
   
5. ```Save Data```<br>

   원하는 포맷으로 데이터 추출
     >pkl, tab, csv, xls etc...

   ```Data Table``` 기능을 통해 생성된 데이터셋 미리보기



## 분석 보고서
시각화 보고서 테스트, 가상 시나리오 수립 및 시나리오 기반 데이터 정제를 통한 드리프트 현상 관측 및 분석

### 분석 보고서 실행

#### 보고서 파일 다운로드
```git clone https://github.com/ethicsense/datadrift.git```

#### evidently 패키지 다운로드
```pip install evidently```

#### dataset 세팅
* 데이터셋 압축해제
  
  ```
  ## 데이터셋 파일명이 datasets가 아닌 경우
  mv {DATASET_NAME} datasets.zip

  mv datasets.zip datadrift/datasets.zip
  unzip datasets.zip
  ```

#### 노트북 실행
* 교통 관련 데이터 분석 보고서 (사람 얼굴, 차량 정보 등)<br>
  => ```scenario_based_drift_traffic.ipynb```
  
* 패션 관련 데이터 분석 보고서 (패션 트렌드, 브랜드 평판, 제품 판매량 등)<br>
  => ```scenario_based_drift_fashion.ipynb```

<br>
<br>

>(참고) 주피터 확장기능 동작하지 않을 시
><br>
>
>jupyter nbextension 패키지 설치
> 
>```
>pip install  jupyter_nbextensions_configurator jupyter_contrib_nbextensions
>```



## 모델 및 분석 앱 배포
학습 모델을 실제 환경에 배포하고 사용하면서 성능과 수집되는 데이터를 분석하는 기술적인 방법론에 대해<br>

todo

### DriftKube MVP

todo



## 데이터 분석 앱
다양한 분석 모니터링 기능 서비스화 실험<br>

todo

### Evidently UI
todo
