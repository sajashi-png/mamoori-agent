# daily_scheduler.py
# Phase 1 Day 4: 매일 자동 실행 스케줄러

import schedule
import time
from datetime import datetime
from market_data_collector import MarketDataCollector
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mamoori_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_daily_report():
    """매일 실행되는 리포트 생성 및 발송"""
    try:
        logger.info("="*70)
        logger.info("🚀 마무리 경제 브리핑 시작")
        logger.info("="*70)
        
        # Collector 생성 (실제 환경에서는 mock_mode=False)
        collector = MarketDataCollector(mock_mode=True)
        
        # 리포트 생성 및 발송
        report, data, korea_data, ai_insight, telegram_result = collector.generate_and_send_report()
        
        if telegram_result and telegram_result['success']:
            logger.info(f"✅ 리포트 발송 성공! (메시지 ID: {telegram_result['message_id']})")
        else:
            logger.error(f"❌ 리포트 발송 실패: {telegram_result.get('error') if telegram_result else 'Unknown'}")
        
        logger.info("="*70)
        logger.info("✅ 마무리 경제 브리핑 완료")
        logger.info("="*70 + "\n")
        
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}", exc_info=True)

def test_immediate_run():
    """즉시 실행 테스트"""
    logger.info("\n🧪 즉시 실행 테스트 모드")
    run_daily_report()

def start_scheduler(test_mode=False):
    """
    스케줄러 시작
    
    Args:
        test_mode: True면 즉시 실행, False면 매일 7시 실행
    """
    if test_mode:
        # 테스트: 즉시 실행
        test_immediate_run()
    else:
        # 실제 운영: 매일 오전 7시 실행
        schedule.every().day.at("07:00").do(run_daily_report)
        
        logger.info("⏰ 스케줄러 시작!")
        logger.info("   매일 오전 7시에 자동 실행됩니다.")
        logger.info("   중단하려면 Ctrl+C를 누르세요.\n")
        
        # 다음 실행 시간 표시
        next_run = schedule.next_run()
        logger.info(f"📅 다음 실행 예정: {next_run}\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크
        except KeyboardInterrupt:
            logger.info("\n⏹️  스케줄러 중단됨")

if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              🤖 마무리(Mamoori) AI Agent 스케줄러                    ║
║                                                                      ║
║              "마무리가 부족한 달희를 위한 자동 브리핑"                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # 실행 모드 선택
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("🧪 테스트 모드: 즉시 실행\n")
        start_scheduler(test_mode=True)
    elif len(sys.argv) > 1 and sys.argv[1] == '--once':
        print("▶️  단일 실행 모드\n")
        run_daily_report()
    else:
        print("⏰ 스케줄 모드: 매일 오전 7시 자동 실행")
        print("   (테스트: python daily_scheduler.py --test)")
        print("   (1회 실행: python daily_scheduler.py --once)\n")
        start_scheduler(test_mode=False)
