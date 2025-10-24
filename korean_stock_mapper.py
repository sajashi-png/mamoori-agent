# korean_stock_mapper.py
# Phase 1 Day 2: 한국 관련주 매핑 및 영향 분석

from typing import Dict, List, Tuple

class KoreanStockMapper:
    """미국 시장 동향 기반 한국 관련주 분석"""
    
    def __init__(self):
        # 섹터별 한국 관련주 매핑
        self.sector_mapping = {
            'tech_semiconductor': {
                'name': '반도체',
                'stocks': [
                    {'name': '삼성전자', 'code': '005930', 'weight': 1.0},
                    {'name': 'SK하이닉스', 'code': '000660', 'weight': 0.9},
                ],
                'us_trigger': 'NASDAQ',
                'threshold': 1.0,  # 1% 이상 등락
                'keywords': ['반도체', 'AI', '메모리', '칩']
            },
            'tech_platform': {
                'name': 'IT플랫폼',
                'stocks': [
                    {'name': '네이버', 'code': '035420', 'weight': 1.0},
                    {'name': '카카오', 'code': '035720', 'weight': 0.8},
                ],
                'us_trigger': 'NASDAQ',
                'threshold': 1.5,
                'keywords': ['빅테크', '플랫폼', 'AI']
            },
            'energy': {
                'name': '에너지',
                'stocks': [
                    {'name': 'SK이노베이션', 'code': '096770', 'weight': 1.0},
                    {'name': 'S-Oil', 'code': '010950', 'weight': 0.9},
                    {'name': '한국전력', 'code': '015760', 'weight': 0.7},
                ],
                'us_trigger': 'S&P 500',
                'threshold': 1.2,
                'keywords': ['유가', '에너지', '전력']
            },
            'auto': {
                'name': '자동차',
                'stocks': [
                    {'name': '현대차', 'code': '005380', 'weight': 1.0},
                    {'name': '기아', 'code': '000270', 'weight': 0.9},
                    {'name': 'LG에너지솔루션', 'code': '373220', 'weight': 0.85},
                ],
                'us_trigger': 'DOW',
                'threshold': 1.0,
                'keywords': ['전기차', 'EV', '배터리']
            },
            'steel_chemical': {
                'name': '철강/화학',
                'stocks': [
                    {'name': 'POSCO홀딩스', 'code': '005490', 'weight': 1.0},
                    {'name': 'LG화학', 'code': '051910', 'weight': 0.9},
                ],
                'us_trigger': 'DOW',
                'threshold': 1.2,
                'keywords': ['원자재', '철강', '화학']
            }
        }
    
    def analyze_korea_impact(self, us_market_data: Dict) -> Dict:
        """
        미국 시장 데이터 기반 한국 시장 영향 분석
        
        Args:
            us_market_data: {
                'NASDAQ': {'change_pct': 2.5, ...},
                'S&P 500': {'change_pct': 1.2, ...},
                'DOW': {'change_pct': 0.8, ...}
            }
        
        Returns:
            {
                'sentiment': str,
                'primary_sector': str,
                'top_stocks': List[Dict],
                'analysis': str
            }
        """
        if not us_market_data:
            return self._empty_analysis()
        
        # 각 섹터별 영향도 계산
        sector_impacts = []
        
        for sector_key, sector_info in self.sector_mapping.items():
            trigger_index = sector_info['us_trigger']
            threshold = sector_info['threshold']
            
            # 해당 미국 지수 데이터 가져오기
            trigger_data = us_market_data.get(trigger_index)
            if not trigger_data:
                continue
            
            change_pct = trigger_data.get('change_pct', 0)
            
            # 임계값 초과 여부 확인
            if abs(change_pct) >= threshold:
                impact_score = abs(change_pct) / threshold
                direction = 'positive' if change_pct > 0 else 'negative'
                
                sector_impacts.append({
                    'sector_key': sector_key,
                    'sector_name': sector_info['name'],
                    'impact_score': impact_score,
                    'direction': direction,
                    'trigger_index': trigger_index,
                    'change_pct': change_pct,
                    'stocks': sector_info['stocks'],
                    'keywords': sector_info['keywords']
                })
        
        # 영향도 순으로 정렬
        sector_impacts.sort(key=lambda x: x['impact_score'], reverse=True)
        
        if not sector_impacts:
            return self._neutral_analysis(us_market_data)
        
        # 가장 큰 영향을 받은 섹터 선택
        primary_sector = sector_impacts[0]
        
        # Top 3 관련주 선정
        top_stocks = self._select_top_stocks(sector_impacts[:2])  # 상위 2개 섹터에서 선정
        
        # 분석 텍스트 생성
        analysis_text = self._generate_analysis(primary_sector, us_market_data)
        
        return {
            'sentiment': primary_sector['direction'],
            'primary_sector': primary_sector['sector_name'],
            'top_stocks': top_stocks[:3],
            'analysis': analysis_text,
            'trigger_index': primary_sector['trigger_index'],
            'trigger_change': primary_sector['change_pct']
        }
    
    def _select_top_stocks(self, top_sectors: List[Dict]) -> List[Dict]:
        """상위 섹터에서 가중치 기반으로 Top 3 종목 선정"""
        all_stocks = []
        
        for sector in top_sectors:
            for stock in sector['stocks']:
                all_stocks.append({
                    'name': stock['name'],
                    'code': stock['code'],
                    'sector': sector['sector_name'],
                    'impact_score': sector['impact_score'] * stock['weight'],
                    'direction': sector['direction'],
                    'keywords': sector['keywords']
                })
        
        # 영향도 점수로 정렬
        all_stocks.sort(key=lambda x: x['impact_score'], reverse=True)
        
        return all_stocks[:3]
    
    def _generate_analysis(self, primary_sector: Dict, us_market_data: Dict) -> str:
        """분석 텍스트 자동 생성"""
        trigger = primary_sector['trigger_index']
        change = primary_sector['change_pct']
        direction = "상승" if change > 0 else "하락"
        sector_name = primary_sector['sector_name']
        
        # 변동폭에 따른 강도 표현
        if abs(change) >= 2.5:
            intensity = "급격한"
        elif abs(change) >= 1.5:
            intensity = "강한"
        else:
            intensity = "완만한"
        
        analysis = f"{trigger}의 {intensity} {direction}({change:+.2f}%)으로 국내 {sector_name} 섹터 "
        
        if change > 0:
            analysis += "상승이 예상됩니다."
        else:
            analysis += "압박이 예상됩니다."
        
        # 키워드 기반 추가 설명
        keywords = primary_sector['keywords']
        if keywords:
            analysis += f" ({', '.join(keywords[:2])} 관련주 주목)"
        
        return analysis
    
    def _neutral_analysis(self, us_market_data: Dict) -> Dict:
        """중립적 시장 상황 분석"""
        return {
            'sentiment': 'neutral',
            'primary_sector': '전 섹터',
            'top_stocks': [
                {'name': '삼성전자', 'code': '005930', 'sector': '반도체', 'direction': 'neutral'},
                {'name': 'SK하이닉스', 'code': '000660', 'sector': '반도체', 'direction': 'neutral'},
                {'name': '현대차', 'code': '005380', 'sector': '자동차', 'direction': 'neutral'}
            ],
            'analysis': '미국 시장이 혼조세를 보이며 국내 시장도 관망세가 예상됩니다.',
            'trigger_index': 'Mixed',
            'trigger_change': 0.0
        }
    
    def _empty_analysis(self) -> Dict:
        """데이터 부족 시"""
        return {
            'sentiment': 'unknown',
            'primary_sector': '-',
            'top_stocks': [],
            'analysis': '미국 시장 데이터가 부족하여 분석이 어렵습니다.',
            'trigger_index': '-',
            'trigger_change': 0.0
        }
    
    def format_korea_section(self, impact_analysis: Dict) -> str:
        """한국 시장 섹션 포맷팅"""
        if impact_analysis['sentiment'] == 'unknown':
            return ""
        
        section = """
🇰🇷 **한국 시장 영향 예측**
━━━━━━━━━━━━━━━━━━━━━━

"""
        
        # 분석 내용
        section += f"{impact_analysis['analysis']}\n\n"
        
        # Top 3 관련주
        if impact_analysis['top_stocks']:
            section += "📌 **주목 관련주 TOP 3**\n"
            for i, stock in enumerate(impact_analysis['top_stocks'], 1):
                emoji = "🟢" if stock.get('direction') == 'positive' else "🔴" if stock.get('direction') == 'negative' else "⚪"
                section += f"{i}. {emoji} **{stock['name']}** ({stock['sector']})\n"
        
        section += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return section


# 테스트 코드
if __name__ == "__main__":
    # Mock 데이터로 테스트
    mapper = KoreanStockMapper()
    
    test_data = {
        'NASDAQ': {'change_pct': 2.3},
        'S&P 500': {'change_pct': 1.1},
        'DOW': {'change_pct': 0.5}
    }
    
    result = mapper.analyze_korea_impact(test_data)
    print("=== 분석 결과 ===")
    print(f"주요 섹터: {result['primary_sector']}")
    print(f"심리: {result['sentiment']}")
    print(f"\nTop 3 종목:")
    for stock in result['top_stocks']:
        print(f"  - {stock['name']} ({stock['sector']})")
    print(f"\n분석: {result['analysis']}")
    
    print("\n" + "="*50)
    print(mapper.format_korea_section(result))
