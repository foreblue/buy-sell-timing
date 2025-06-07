import pandas as pd
import yfinance as yf
from datetime import datetime
import sys

def load_stocks():
    """stocks.csv 파일에서 주식 데이터를 로드합니다."""
    try:
        return pd.read_csv('stocks.csv')
    except FileNotFoundError:
        print("Error: stocks.csv 파일을 찾을 수 없습니다.")
        sys.exit(1)

def get_stock_price(stock_type, code, date):
    """주어진 날짜의 주식 종가를 조회합니다."""
    try:
        # 한국 주식인 경우 시장 심볼 추가
        if stock_type == 'KR':
            ticker = f"{code}.KS"  # 코스피 기준
        else:
            ticker = code

        stock = yf.Ticker(ticker)
        # 주어진 날짜의 데이터 조회
        data = stock.history(start=date, end=date)
        
        if data.empty:
            print(f"Warning: {code}의 {date} 데이터를 찾을 수 없습니다.")
            return None
            
        return data['Close'].iloc[0]
    except Exception as e:
        print(f"Error: {code} 데이터 조회 중 오류 발생: {str(e)}")
        return None

def calculate_profit(initial_price, current_price):
    """수익률과 수익금을 계산합니다."""
    if current_price is None:
        return None, None
    
    profit_amount = current_price - initial_price
    profit_rate = (profit_amount / initial_price) * 100
    return profit_rate, profit_amount

def main():
    # 사용자로부터 날짜 입력 받기
    while True:
        date_str = input("조회할 날짜를 입력하세요 (YYYY-MM-DD): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("올바른 날짜 형식이 아닙니다. YYYY-MM-DD 형식으로 입력해주세요.")

    # 주식 데이터 로드
    stocks_df = load_stocks()
    
    print("\n=== 주식 수익률 분석 결과 ===")
    print(f"기준일: {date_str}\n")
    
    # 각 주식에 대해 분석 수행
    for _, stock in stocks_df.iterrows():
        current_price = get_stock_price(stock['type'], stock['code'], date_str)
        if current_price is not None:
            profit_rate, profit_amount = calculate_profit(stock['initial_price'], current_price)
            
            print(f"종목: {stock['name']} ({stock['code']})")
            print(f"매수가: {stock['initial_price']:,.2f}")
            print(f"현재가: {current_price:,.2f}")
            print(f"수익률: {profit_rate:,.2f}%")
            print(f"수익금: {profit_amount:,.2f}")
            print("-" * 50)

if __name__ == "__main__":
    main() 