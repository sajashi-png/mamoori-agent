# market_analyst.py
# Phase 1 Day 3: Claude API를 활용한 시장 분석 고도화

import json
import os
from typing import Dict, List

class MarketAnalyst:
    """Claude API를 활용한 지능형 시장 분석"""
    
    def __init__(self, api_key: str = None):
        """
        Args:
            api_key: Anthropic API 키 (환경변수 ANTHROPIC_API_KEY 사용 가능)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.mock_mode = not self.api_key  # API 키 없으면 Mock 모드
        
        # 시장 분석 전문가 페르소나
        self.system_prompt = """당신은 20년 경력의 글로벌 투자 애널리스트입니다.

전문 분야:
- 미국 및 한국 증시 분석
- 섹터 로테이션 및 상관관계 분석
- 기술적/기본적 분석 통합
- 한국 개인투자자 관점의 실용적 조언

분석 원칙:
1. 간결하고 실용적인 3줄 요약
2. 과장 없는 객관적 분석
3. 리스크와 기회 균형있게 제시
4. 한국 투자자가 실제 활용 가능한 인사이트

금지사항:
- 특정 종목 매수/매도 권유
- 수익률 보장 또는 예측
- 과도한 전문 용어
"""
    
    def analyze_market(self, us_market_data: Dict, korea_impact: Dict) -> Dict:
        """
        시장 데이터를 종합 분석하여 인사이트 생성
        
        Args:
            us_market_data: 미국 시장 데이터
            korea_impact: 한국 영향 분석 결과
            
        Returns:
            {
                'insight': str,  # 핵심 인사이트
                'key_points': List[str],  # 주요 포인트 3가지
                'risk_note': str,  # 주의사항
                'action_items': List[str]  # 투자 시사점
            }
        """
        if self.mock_mode:
            return self._generate_mock_insight(us_market_data, korea_impact)
        
        # 실제 Claude API 호출
        return self._call_claude_api(us_market_data, korea_impact)
    
    def _generate_mock_insight(self, us_market_data: Dict, korea_impact: Dict) -> Dict:
        """Mock 모드: 규칙 기반 인사이트 생성"""
        
        # 미국 시장 평균 등락률
        nasdaq_change = us_market_data.get('NASDAQ', {}).get('change_pct', 0)
        sp500_change = us_market_data.get('S&P 500', {}).get('change_pct', 0)
        vix = us_market_data.get('VIX', {}).get('price', 0)
        
        avg_change = (nasdaq_change + sp500_change) / 2
        
        # 시장 상황 판단
        if avg_change > 1.5:
            market_tone = "강세"
            sentiment = "긍정적"
        elif avg_change < -1.5:
            market_tone = "약세"
            sentiment = "부정적"
        else:
            market_tone = "혼조"
            sentiment = "중립적"
        
        # 인사이트 생성
        insight = f"미국 증시 {market_tone} 흐름 속에서 "
        
        if korea_impact.get('primary_sector'):
            insight += f"국내 {korea_impact['primary_sector']} 섹터가 주목받고 있습니다. "
        
        if vix > 20:
            insight += "다만 변동성이 높아 단기 조정 가능성에 유의해야 합니다."
        elif vix < 15:
            insight += "변동성이 낮아 상대적으로 안정적인 흐름이 예상됩니다."
        else:
            insight += "변동성은 보통 수준으로 추세 지속 여부를 지켜봐야 합니다."
        
        # 주요 포인트
        key_points = []
        
        if abs(nasdaq_change) > abs(sp500_change):
            key_points.append(f"기술주 중심의 {'상승' if nasdaq_change > 0 else '하락'} 장세")
        else:
            key_points.append(f"시장 전반적인 {'상승' if sp500_change > 0 else '하락'} 흐름")
        
        if korea_impact.get('top_stocks'):
            top_stock = korea_impact['top_stocks'][0]['name']
            key_points.append(f"국내 {top_stock} 등 연관주 수혜 예상")
        
        if vix > 25:
            key_points.append("공포지수 급등으로 방어적 포지션 고려 필요")
        elif avg_change > 2:
            key_points.append("강한 상승이나 과열 여부 점검 필요")
        else:
            key_points.append("점진적 흐름으로 추세 추종 전략 유효")
        
        # 리스크 노트
        risk_note = ""
        if vix > 20:
            risk_note = "⚠️ 변동성 확대 구간으로 손절매 기준 설정 권장"
        elif abs(avg_change) > 2.5:
            risk_note = "⚠️ 급격한 변동 후 조정 가능성 대비 필요"
        else:
            risk_note = "💡 안정적 흐름이나 돌발 변수 모니터링 지속"
        
        # 액션 아이템
        action_items = []
        
        if sentiment == "긍정적":
            action_items.append("상승 모멘텀 활용: 관련주 분할 매수 고려")
            action_items.append("익절 타이밍 사전 설정으로 이익 실현 준비")
        elif sentiment == "부정적":
            action_items.append("방어적 포지션: 현금 비중 확대 검토")
            action_items.append("저가 매수 기회: 관심 종목 리스트 점검")
        else:
            action_items.append("관망: 뚜렷한 방향성 나올 때까지 대기")
            action_items.append("분할 매매: 리스크 분산하며 포지션 조절")
        
        if vix < 15:
            action_items.append("저변동성 활용: 중장기 포지션 구축 적기")
        
        return {
            'insight': insight,
            'key_points': key_points[:3],
            'risk_note': risk_note,
            'action_items': action_items[:2]
        }
    
    def _call_claude_api(self, us_market_data: Dict, korea_impact: Dict) -> Dict:
        """실제 Claude API 호출 (Day 3 후반부 구현)"""
        
        # 분석 요청 프롬프트 구성
        prompt = self._build_analysis_prompt(us_market_data, korea_impact)
        
        # TODO: Anthropic API 호출
        # 현재는 Mock 모드로 폴백
        return self._generate_mock_insight(us_market_data, korea_impact)
    
    def _build_analysis_prompt(self, us_market_data: Dict, korea_impact: Dict) -> str:
        """Claude에게 보낼 분석 요청 프롬프트"""
        
        prompt = f"""다음 시장 데이터를 분석해주세요:

【미국 시장】
"""
        for index, data in us_market_data.items():
            if data:
                prompt += f"- {index}: {data['change_pct']:+.2f}%\n"
        
        prompt += f"""
【한국 영향 분석】
- 주요 섹터: {korea_impact.get('primary_sector', 'N/A')}
- 심리: {korea_impact.get('sentiment', 'N/A')}
- 트리거: {korea_impact.get('trigger_index', 'N/A')} {korea_impact.get('trigger_change', 0):+.2f}%

주목 종목:
"""
        for stock in korea_impact.get('top_stocks', [])[:3]:
            prompt += f"- {stock['name']} ({stock['sector']})\n"
        
        prompt += """
다음 형식으로 분석해주세요:

1. 핵심 인사이트 (2-3문장)
2. 주요 포인트 3가지
3. 주의사항 (1문장)
4. 투자 시사점 2가지

객관적이고 실용적으로 작성해주세요.
"""
        
        return prompt
    
    def format_insight_section(self, analysis: Dict) -> str:
        """인사이트 섹션 포맷팅"""
        
        section = """
💡 **Today's Insight**
━━━━━━━━━━━━━━━━━━━━━━

"""
        
        # 핵심 인사이트
        section += f"{analysis['insight']}\n\n"
        
        # 주요 포인트
        section += "**📌 주요 포인트**\n"
        for i, point in enumerate(analysis['key_points'], 1):
            section += f"{i}. {point}\n"
        
        section += f"\n**⚡ 주의사항**\n{analysis['risk_note']}\n\n"
        
        # 액션 아이템
        if analysis.get('action_items'):
            section += "**🎯 투자 시사점**\n"
            for item in analysis['action_items']:
                section += f"• {item}\n"
        
        section += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return section


# 테스트
if __name__ == "__main__":
    analyst = MarketAnalyst()  # Mock 모드
    
    # 테스트 데이터
    test_us_data = {
        'NASDAQ': {'change_pct': 2.3, 'price': 18400},
        'S&P 500': {'change_pct': 1.5, 'price': 5800},
        'DOW': {'change_pct': 0.8, 'price': 43000},
        'VIX': {'change_pct': -5.0, 'price': 14.5}
    }
    
    test_korea_impact = {
        'sentiment': 'positive',
        'primary_sector': '반도체',
        'top_stocks': [
            {'name': '삼성전자', 'sector': '반도체'},
            {'name': 'SK하이닉스', 'sector': '반도체'},
            {'name': '네이버', 'sector': 'IT플랫폼'}
        ],
        'trigger_index': 'NASDAQ',
        'trigger_change': 2.3
    }
    
    # 분석 실행
    result = analyst.analyze_market(test_us_data, test_korea_impact)
    
    print("=== AI 시장 분석 결과 ===\n")
    print(f"인사이트: {result['insight']}\n")
    print("주요 포인트:")
    for i, point in enumerate(result['key_points'], 1):
        print(f"  {i}. {point}")
    print(f"\n주의사항: {result['risk_note']}\n")
    print("투자 시사점:")
    for item in result['action_items']:
        print(f"  • {item}")
    
    print("\n" + "="*60)
    print(analyst.format_insight_section(result))
