# 주식 종가 비교 프로그램

## 프로젝트 개요
이 프로젝트는 CSV 파일에 정의된 주식 종목(한국 및 미국)의 시초가와 사용자가 지정한 과거 날짜의 종가를 비교하여 수익률 및 수익 금액을 콘솔에 출력하는 Python 프로그램입니다. 사용자 인터페이스(UI/UX)는 필요 없으며, 모든 상호작용과 출력은 콘솔을 통해 이루어집니다.

## 파일 구조
프로젝트는 다음 파일들로 구성됩니다:

- `stocks.csv`: 사용자가 관리할 주식 종목 데이터
- `stock_analyzer.py`: 핵심 프로그램 로직
- `requirements.txt`: 필요한 Python 라이브러리 목록

## stocks.csv 파일 스펙
사용자가 직접 생성하고 관리하는 CSV 파일입니다.

### 파일명
`stocks.csv`

### 컬럼 구조
| 컬럼명 | 타입 | 설명 | 비고 |
|--------|------|------|------|
| type | 문자열 | 종목 구분자 | KR(한국 주식) 또는 US(미국 주식)만 허용 |
| code | 문자열 | 종목 코드 | 한국 주식: 종목 코드 (예: 005930)<br>미국 주식: 티커 (예: AAPL) |
| initial_price | 숫자 | 매수 시초가 | float 또는 int 타입 |
| name | 문자열 | 종목 이름 | 선택 사항, 비워둘 수 있음 |

### 예시 데이터
```csv
type,code,initial_price,name
KR,005930,75000,삼성전자
US,AAPL,180.5,Apple Inc.
KR,035720,50000,카카오
US,MSFT,250.0,Microsoft Corp
```

## 설치 및 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/foreblue/buy-sell-timing.git
cd buy-sell-timing
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 또는
.\venv\Scripts\activate  # Windows
```

### 3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 프로그램 실행
```bash
python stock_analyzer.py
```

## 사용 예시
프로그램 실행 후 조회하고 싶은 날짜를 YYYY-MM-DD 형식으로 입력하면, 각 주식의 수익률과 수익금이 계산되어 출력됩니다.

```
조회할 날짜를 입력하세요 (YYYY-MM-DD): 2024-03-15

=== 주식 수익률 분석 결과 ===
기준일: 2024-03-15

종목: 삼성전자 (005930)
매수가: 75,000.00
현재가: 74,800.00
수익률: -0.27%
수익금: -200.00
--------------------------------------------------