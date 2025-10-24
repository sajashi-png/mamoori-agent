# market_data_collector.py
# Phase 1 Day 1: 미국 시장 데이터 수집기

import yfinance as yf
from datetime import datetime, timedelta
import json

class MarketDataCollector:
    """미국 주요 지수 데이터 수집 클래스"""
    
    def __init__(self, mock_mode=False):
        # 주요 지수 티커
        self.indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'DOW': '^DJI',
            'VIX': '^VIX'  # 공포지수
        }
        self.mock_mode = mock_mode
        
    def get_market_data(self):
        """전날 시장 데이터 수집"""
        
        # Mock 모드: 실제 같은 데이터 생성
        if self.mock_mode:
            import random
            return {
                'S&P 500': {
                    'price': round(5732.45 + random.uniform(-50, 50), 2),
                    'change_pct': round(random.uniform(-2, 2), 2),
                    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                },
                'NASDAQ': {
                    'price': round(18315.20 + random.uniform(-100, 100), 2),
                    'change_pct': round(random.uniform(-2.5, 2.5), 2),
                    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                },
                'DOW': {
                    'price': round(42863.00 + random.uniform(-300, 300), 2),
                    'change_pct': round(random.uniform(-1.5, 1.5), 2),
                    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                },
                'VIX': {
                    'price': round(17.5 + random.uniform(-3, 3), 2),
                    'change_pct': round(random.uniform(-10, 10), 2),
                    'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                }
            }
        
        # 실제 데이터 수집
        market_summary = {}
        
        for name, ticker in self.indices.items():
            try:
                # 최근 2일 데이터 가져오기
                stock = yf.Ticker(ticker)
                hist = stock.history(period='2d')
                
                if len(hist) >= 2:
                    # 전날 종가와 전전날 종가
                    latest_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    
                    # 등락률 계산
                    change_pct = ((latest_close - prev_close) / prev_close) * 100
                    
                    market_summary[name] = {
                        'price': round(latest_close, 2),
                        'change_pct': round(change_pct, 2),
                        'date': hist.index[-1].strftime('%Y-%m-%d')
                    }
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                market_summary[name] = None
        
        return market_summary
    
    def analyze_market_sentiment(self, market_data):
        """시장 심리 분석"""
        sp500_data = market_data.get('S&P 500')
        nasdaq_data = market_data.get('NASDAQ')
        vix_data = market_data.get('VIX')
        
        if not sp500_data or not nasdaq_data:
            return {
                'sentiment': "데이터 부족",
                'analysis': "시장 데이터를 수집할 수 없습니다.",
                'vix_analysis': ""
            }
        
        sp500_change = sp500_data.get('change_pct', 0)
        nasdaq_change = nasdaq_data.get('change_pct', 0)
        vix = vix_data.get('price', 0) if vix_data else 0
        
        # 기본 분석
        if sp500_change > 1 and nasdaq_change > 1:
            sentiment = "강세"
            analysis = "주요 지수가 모두 강한 상승세를 보이고 있습니다."
        elif sp500_change < -1 and nasdaq_change < -1:
            sentiment = "약세"
            analysis = "주요 지수가 모두 하락세를 나타내고 있습니다."
        elif nasdaq_change < -2 and sp500_change > -1:
            sentiment = "기술주 약세"
            analysis = "나스닥이 상대적으로 큰 하락을 보이며 기술주 중심으로 매도세가 나타났습니다."
        else:
            sentiment = "혼조"
            analysis = "시장이 방향성 없이 혼조세를 보이고 있습니다."
        
        # VIX 분석
        if vix > 25:
            vix_analysis = "공포지수(VIX)가 높아 시장 불안감이 큽니다."
        elif vix < 15:
            vix_analysis = "공포지수(VIX)가 낮아 시장이 안정적입니다."
        else:
            vix_analysis = "공포지수(VIX)는 보통 수준입니다."
        
        return {
            'sentiment': sentiment,
            'analysis': analysis,
            'vix_analysis': vix_analysis
        }
    
    def generate_report(self):
        """일일 리포트 생성"""
        market_data = self.get_market_data()
        sentiment = self.analyze_market_sentiment(market_data)
        
        report = f"""
📊 **마무리 경제 브리핑** | {datetime.now().strftime('%Y년 %m월 %d일')}

━━━━━━━━━━━━━━━━━━━━━━
🇺🇸 **미국 시장 동향**
━━━━━━━━━━━━━━━━━━━━━━

"""
        
        for name, data in market_data.items():
            if data:
                emoji = "🔴" if data['change_pct'] < 0 else "🟢"
                report += f"{emoji} **{name}**: {data['price']:,.2f} ({data['change_pct']:+.2f}%)\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━
📈 **시장 분석**
━━━━━━━━━━━━━━━━━━━━━━

**종합 심리**: {sentiment['sentiment']}
{sentiment['analysis']}
{sentiment['vix_analysis']}

━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return report, market_data

# 테스트 실행
if __name__ == "__main__":
    # Mock 모드로 실행 (실제 환경에서는 False로 변경)
    collector = MarketDataCollector(mock_mode=True)
    report, data = collector.generate_report()
    print(report)
    
    # JSON 저장 (나중에 DB로 대체)
    with open(f'market_data_{datetime.now().strftime("%Y%m%d")}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
