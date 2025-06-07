import pandas as pd
from pykrx import stock
import finnhub
from datetime import datetime, timedelta
import argparse
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

def get_korean_width(text):
    """
    한글 문자열의 실제 표시 폭을 계산하는 함수
    
    Args:
        text (str): 계산할 문자열
    
    Returns:
        int: 문자열의 실제 표시 폭
    """
    width = 0
    for char in text:
        if ord(char) > 127:  # 한글, 한자 등 2바이트 문자
            width += 2
        else:  # 영문, 숫자, 특수문자 등 1바이트 문자
            width += 1
    return width

def calculate_price_change(initial_price, current_price):
    """
    주가 변동 정보를 계산하는 함수
    
    Args:
        initial_price (float): 기초가
        current_price (float): 현재가
    
    Returns:
        tuple: (변동금액, 변동률)
    """
    if current_price is None:
        return None, None
    
    change_amount = current_price - initial_price
    change_rate = (change_amount / initial_price) * 100
    return change_amount, change_rate

def get_kr_stock_price(code, date=None):
    """
    pykrx를 이용해 한국 주식 가격을 조회하는 함수
    
    Args:
        code (str): 주식 종목 코드 (예: '005930' for 삼성전자)
        date (str, optional): 조회할 날짜 (YYYY-MM-DD 형식). 기본값은 어제 날짜
    
    Returns:
        float: 종가, 실패시 None
    """
    try:
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        else:
            date = date.replace('-', '')
            
        df = stock.get_market_ohlcv_by_date(date, date, code)
            
        if df.empty:
            print(f"Warning: {code}의 {date} 데이터를 찾을 수 없습니다.")
            return None
            
        return df['종가'].iloc[0]
        
    except Exception as e:
        print(f"Error: {code} 데이터 조회 중 오류 발생: {str(e)}")
        return None

def get_us_stock_price(ticker, date=None):
    """
    Finnhub API를 이용해 미국 주식 가격을 조회하는 함수
    
    Args:
        ticker (str): 주식 티커 심볼 (예: 'AAPL' for 애플)
        date (str, optional): 조회할 날짜 (YYYY-MM-DD 형식). 기본값은 어제 날짜
    
    Returns:
        float: 종가, 실패시 None
    """
    try:
        if not FINNHUB_API_KEY:
            print("Error: FINNHUB_API_KEY가 설정되지 않았습니다.")
            print("1. https://finnhub.io/ 에서 API 키를 발급받으세요.")
            print("2. .env 파일에 FINNHUB_API_KEY=your_api_key 형식으로 저장하세요.")
            return None

        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Finnhub 클라이언트 초기화
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        
        # 주식 가격 데이터 조회
        quote = finnhub_client.quote(ticker)
        
        if quote and 'c' in quote:  # 'c'는 현재 종가를 의미
            return quote['c']
        else:
            print(f"Warning: {ticker}의 {date} 데이터를 찾을 수 없습니다.")
            return None
            
    except Exception as e:
        print(f"Error: {ticker} 데이터 조회 중 오류 발생: {str(e)}")
        return None

def load_stocks():
    """stocks.csv 파일에서 주식 데이터를 로드합니다."""
    try:
        return pd.read_csv('stocks.csv')
    except FileNotFoundError:
        print("Error: stocks.csv 파일을 찾을 수 없습니다.")
        return None

def main():
    parser = argparse.ArgumentParser(description='주식 가격 분석 프로그램')
    parser.add_argument('--date', type=str, help='조회할 날짜 (YYYY-MM-DD 형식)')
    args = parser.parse_args()
    
    # 주식 데이터 로드
    stocks_df = load_stocks()
    if stocks_df is None:
        return
    
    # 날짜 설정
    date = args.date if args.date else (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"\n{date} 기준 주식 가격 분석:")
    print("-" * 80)
    
    # 한국 주식과 미국 주식 분리
    kr_stocks = stocks_df[stocks_df['type'] == 'KR']
    us_stocks = stocks_df[stocks_df['type'] == 'US']
    
    # 한국 주식 조회
    if not kr_stocks.empty:
        print("\n[한국 주식]")
        # 헤더 출력
        print(f"{'종목명':<12} {'기초가':>12} {'현재가':>12} {'변동금액':>12} {'변동률':>8}")
        print("-" * 60)
        
        # 각 주식 정보 출력
        for _, stock in kr_stocks.iterrows():
            current_price = get_kr_stock_price(stock['code'], date)
            if current_price:
                change_amount, change_rate = calculate_price_change(stock['initial_price'], current_price)
                # 한글 종목명의 실제 폭 계산
                name_width = get_korean_width(stock['name'])
                # 필요한 공백 계산 (기본 12칸에서 한글 폭을 뺀 만큼)
                padding = max(12 - name_width, 0)
                print(f"{stock['name']}{' ' * padding} {stock['initial_price']:>12,.0f} {current_price:>12,.0f} {change_amount:>12,.0f} {change_rate:>7.1f}%")
            else:
                name_width = get_korean_width(stock['name'])
                padding = max(12 - name_width, 0)
                print(f"{stock['name']}{' ' * padding} {stock['initial_price']:>12,.0f} {'조회실패':>12}")
    
    # 미국 주식 조회
    if not us_stocks.empty:
        print("\n[미국 주식]")
        print(f"{'종목명':<20} {'기초가':>12} {'현재가':>12} {'변동금액':>12} {'변동률':>8}")
        print("-" * 70)
        for _, stock in us_stocks.iterrows():
            current_price = get_us_stock_price(stock['code'], date)
            if current_price:
                change_amount, change_rate = calculate_price_change(stock['initial_price'], current_price)
                print(f"{stock['name']:<20} ${stock['initial_price']:>11,.2f} ${current_price:>11,.2f} ${change_amount:>11,.2f} {change_rate:>7.1f}%")
            else:
                print(f"{stock['name']:<20} ${stock['initial_price']:>11,.2f} {'조회실패':>12}")

if __name__ == "__main__":
    main() 