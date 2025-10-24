#!/usr/bin/env python3
# start.py
# 배포 환경에서 실행되는 메인 스크립트

import os
import sys
import logging
from datetime import datetime
from daily_scheduler import start_scheduler

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mamoori_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_environment():
    """환경변수 확인"""
    required_vars = {
        'TELEGRAM_BOT_TOKEN': '텔레그램 봇 토큰',
        'TELEGRAM_CHAT_ID': '텔레그램 채팅 ID'
    }
    
    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"{var} ({description})")
    
    if missing:
        logger.warning("⚠️  다음 환경변수가 설정되지 않았습니다:")
        for var in missing:
            logger.warning(f"   - {var}")
        logger.warning("   Mock 모드로 실행됩니다 (콘솔 출력만)")
        return False
    else:
        logger.info("✅ 모든 환경변수 확인 완료")
        logger.info(f"   Bot Token: {os.getenv('TELEGRAM_BOT_TOKEN')[:10]}...")
        logger.info(f"   Chat ID: {os.getenv('TELEGRAM_CHAT_ID')}")
        return True

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("🤖 마무리(Mamoori) AI Agent 시작")
    logger.info(f"   시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)
    
    # 환경변수 체크
    env_ok = check_environment()
    
    if env_ok:
        logger.info("✅ 실제 Telegram 발송 모드")
    else:
        logger.info("⚠️  Mock 모드 (개발/테스트)")
    
    logger.info("\n⏰ 스케줄러 시작...")
    logger.info("   매일 오전 7시에 자동 실행됩니다")
    logger.info("   (현지 시간 기준)\n")
    
    # 스케줄러 시작
    try:
        start_scheduler(test_mode=False)
    except KeyboardInterrupt:
        logger.info("\n⏹️  사용자에 의해 중단됨")
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}", exc_info=True)
        sys.exit(1)
