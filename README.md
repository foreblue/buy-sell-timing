주식 종가 비교 프로그램 개발 스펙

1. 프로젝트 개요
이 프로젝트는 CSV 파일에 정의된 주식 종목(한국 및 미국)의 시초가와 사용자가 지정한 과거 날짜의 종가를 비교하여 수익률 및 수익 금액을 콘솔에 출력하는 Python 프로그램입니다. 사용자 인터페이스(UI/UX)는 필요 없으며, 모든 상호작용과 출력은 콘솔을 통해 이루어집니다.

2. 파일 구조 및 내용
프로젝트는 다음 파일들로 구성됩니다.

stocks.csv: 사용자가 관리할 주식 종목 데이터.
stock_analyzer.py: 핵심 프로그램 로직.
requirements.txt: 필요한 Python 라이브러리 목록.

3. stocks.csv 파일 스펙
사용자가 직접 생성하고 관리하는 CSV 파일입니다.

파일명: stocks.csv

컬럼: type, code, initial_price, name

type: 문자열. 종목의 구분자. KR (한국 주식) 또는 US (미국 주식)만 허용합니다.
code: 문자열. 한국 주식의 종목 코드 (예: 005930), 미국 주식의 티커 (예: AAPL).
initial_price: 숫자 (float 또는 int). 사용자가 설정한 해당 종목의 매수 시초가.
name: 문자열 (선택 사항). 종목의 이름 (예: 삼성전자, Apple Inc.). 비워둘 수 있습니다.

예시 stocks.csv 내용:

type,code,initial_price,name
KR,005930,75000,삼성전자
US,AAPL,180.5,Apple Inc.
KR,035720,50000,카카오
US,MSFT,250.0,Microsoft Corp