# telegram_notifier.py
# Phase 1 Day 4: Telegram Bot 연동

import os
import requests
from typing import Optional
from datetime import datetime

class TelegramNotifier:
    """Telegram을 통한 리포트 자동 발송"""
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Args:
            bot_token: Telegram Bot Token (환경변수 TELEGRAM_BOT_TOKEN)
            chat_id: 수신자 Chat ID (환경변수 TELEGRAM_CHAT_ID)
        """
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Mock 모드 (토큰이 없으면)
        self.mock_mode = not self.bot_token or not self.chat_id
        
    def send_message(self, text: str, parse_mode: str = "Markdown") -> dict:
        """
        Telegram 메시지 발송
        
        Args:
            text: 발송할 메시지 (Markdown 지원)
            parse_mode: 메시지 포맷 (Markdown 또는 HTML)
            
        Returns:
            {'success': bool, 'message_id': int or None, 'error': str or None}
        """
        if self.mock_mode:
            return self._mock_send(text)
        
        try:
            url = f"{self.base_url}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True  # 링크 미리보기 비활성화
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ok'):
                return {
                    'success': True,
                    'message_id': result.get('result', {}).get('message_id'),
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'message_id': None,
                    'error': result.get('description', 'Unknown error')
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message_id': None,
                'error': str(e)
            }
    
    def _mock_send(self, text: str) -> dict:
        """Mock 모드: 실제 발송 없이 시뮬레이션"""
        print("="*70)
        print("📱 [MOCK] Telegram 메시지 발송 시뮬레이션")
        print("="*70)
        print(text)
        print("="*70)
        print("✅ Mock 발송 성공 (실제 환경에서는 Telegram으로 전송됩니다)")
        print("="*70)
        
        return {
            'success': True,
            'message_id': 999999,  # Mock ID
            'error': None
        }
    
    def send_report(self, report: str) -> dict:
        """
        경제 브리핑 리포트 발송
        
        Args:
            report: 마무리 경제 브리핑 텍스트
            
        Returns:
            발송 결과 딕셔너리
        """
        # Telegram Markdown에 맞게 포맷 조정
        formatted_report = self._format_for_telegram(report)
        
        return self.send_message(formatted_report)
    
    def _format_for_telegram(self, report: str) -> str:
        """
        Telegram Markdown 포맷에 맞게 텍스트 변환
        
        Telegram은 일부 Markdown 문법만 지원:
        - *bold* 또는 **bold**
        - _italic_ 또는 __italic__
        - `code`
        - [link](URL)
        """
        # 기본적으로 그대로 사용 (CommonMark 호환)
        # 필요시 추가 변환 로직
        
        return report
    
    def test_connection(self) -> bool:
        """
        Telegram Bot 연결 테스트
        
        Returns:
            연결 성공 여부
        """
        if self.mock_mode:
            print("⚠️  Mock 모드: 실제 Telegram 연결 없음")
            print("💡 Bot Token과 Chat ID를 설정하면 실제 발송 가능")
            return True
        
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ok'):
                bot_info = result.get('result', {})
                print(f"✅ Bot 연결 성공!")
                print(f"   Bot 이름: {bot_info.get('first_name')}")
                print(f"   Bot 유저명: @{bot_info.get('username')}")
                return True
            else:
                print(f"❌ Bot 연결 실패: {result.get('description')}")
                return False
                
        except Exception as e:
            print(f"❌ 연결 오류: {e}")
            return False
    
    def get_setup_instructions(self) -> str:
        """Telegram Bot 설정 가이드 반환"""
        
        instructions = """
🤖 Telegram Bot 설정 가이드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Step 1: Bot 생성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Telegram에서 @BotFather 검색
2. /newbot 명령어 입력
3. Bot 이름 설정 (예: 마무리 경제 브리핑)
4. Bot 유저명 설정 (예: mamoori_economy_bot)
5. Bot Token 받기 (예: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz)

💬 Step 2: Chat ID 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
방법 A: 직접 확인
1. 생성한 Bot에게 아무 메시지 전송
2. 브라우저에서 접속:
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
3. "chat":{"id": 숫자} 찾기

방법 B: @userinfobot 사용
1. Telegram에서 @userinfobot 검색
2. /start 입력
3. 표시되는 ID 확인

🔐 Step 3: 환경변수 설정
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Linux/Mac
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Windows (PowerShell)
$env:TELEGRAM_BOT_TOKEN="your_bot_token_here"
$env:TELEGRAM_CHAT_ID="your_chat_id_here"

# Python 코드에서 직접 설정
notifier = TelegramNotifier(
    bot_token="your_bot_token",
    chat_id="your_chat_id"
)

✅ Step 4: 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python telegram_notifier.py

📌 참고사항
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Bot Token은 절대 공개하지 마세요!
- Chat ID는 숫자 형태입니다 (예: 123456789)
- Mock 모드에서는 콘솔에만 출력됩니다
"""
        return instructions


# 테스트 및 설정 가이드
if __name__ == "__main__":
    print("🚀 마무리 AI Agent - Telegram 연동 테스트\n")
    
    # Notifier 생성 (Mock 모드)
    notifier = TelegramNotifier()
    
    # 설정 가이드 출력
    if notifier.mock_mode:
        print(notifier.get_setup_instructions())
        print("\n" + "="*70)
        print("⚠️  현재 Mock 모드로 실행 중입니다")
        print("="*70 + "\n")
    
    # 연결 테스트
    print("📡 Bot 연결 테스트 중...\n")
    notifier.test_connection()
    
    # 샘플 리포트 발송 테스트
    print("\n📨 샘플 리포트 발송 테스트...\n")
    
    sample_report = """📊 **마무리 경제 브리핑** | 2025년 10월 24일

━━━━━━━━━━━━━━━━━━━━━━
🇺🇸 **미국 시장 동향**
━━━━━━━━━━━━━━━━━━━━━━

🟢 **S&P 500**: 5,800.00 (+1.50%)
🟢 **NASDAQ**: 18,500.00 (+2.30%)
🟢 **DOW**: 43,000.00 (+0.80%)
🟢 **VIX**: 14.50 (-5.00%)

━━━━━━━━━━━━━━━━━━━━━━
💡 **Today's Insight**
━━━━━━━━━━━━━━━━━━━━━━

미국 증시 강세 흐름 속에서 국내 반도체 섹터가 주목받고 있습니다.

**📌 주요 포인트**
1. 기술주 중심의 상승 장세
2. 국내 삼성전자 등 연관주 수혜 예상
3. 점진적 흐름으로 추세 추종 전략 유효

**🎯 투자 시사점**
• 상승 모멘텀 활용: 관련주 분할 매수 고려
• 익절 타이밍 사전 설정으로 이익 실현 준비

━━━━━━━━━━━━━━━━━━━━━━
🇰🇷 **한국 시장 영향 예측**
━━━━━━━━━━━━━━━━━━━━━━

**📌 주목 관련주 TOP 3**
1. 🟢 **삼성전자** (반도체)
2. 🟢 **SK하이닉스** (반도체)
3. 🟢 **네이버** (IT플랫폼)
"""
    
    result = notifier.send_report(sample_report)
    
    print(f"\n발송 결과:")
    print(f"  성공: {result['success']}")
    print(f"  메시지 ID: {result['message_id']}")
    if result['error']:
        print(f"  오류: {result['error']}")
    
    print("\n" + "="*70)
    print("✅ Telegram 연동 테스트 완료!")
    print("="*70)
    
    if notifier.mock_mode:
        print("\n💡 실제 발송을 위해서는:")
        print("   1. Bot Token 발급")
        print("   2. Chat ID 확인")
        print("   3. 환경변수 설정 또는 코드에 직접 입력")
        print("\n   자세한 내용은 위의 설정 가이드를 참고하세요!")
