# 🤖 마무리(Mamoori) AI Agent

> **"마무리가 부족한 달희를 위한 자동 경제 브리핑"**

매일 아침 7시, 미국 시장 분석과 한국 관련주 인사이트를 자동으로 Telegram으로 받아보세요.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

---

## ✨ 주요 기능

### 📊 자동 시장 분석
- **미국 시장 데이터**: S&P 500, NASDAQ, DOW, VIX 실시간 수집
- **한국 관련주**: 미국 시장 동향 기반 영향받을 국내 종목 자동 분석
- **AI 인사이트**: 20년 경력 애널리스트 관점의 투자 시사점 제공

### 🤖 완전 자동화
- **매일 오전 7시** 자동 실행
- **Telegram 알림**으로 편리하게 수신
- **24시간 클라우드** 운영 (손댈 필요 없음)

### 💡 실용적 조언
- 핵심 인사이트 (2-3문장)
- 주요 포인트 3가지
- 리스크 알림
- 투자 시사점

---

## 🚀 빠른 시작

### 1. 사전 준비

```bash
# Python 3.8+ 필요
python --version

# 저장소 클론
git clone https://github.com/yourusername/mamoori-agent.git
cd mamoori-agent

# 패키지 설치
pip install -r requirements.txt
```

### 2. Telegram Bot 설정

```
1. Telegram에서 @BotFather 검색
2. /newbot 입력하고 Bot 생성
3. Bot Token 복사
4. @userinfobot에서 Chat ID 확인
```

### 3. 환경변수 설정

```bash
# Linux/Mac
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Windows
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

### 4. 실행

```bash
# 즉시 테스트
python daily_scheduler.py --once

# 자동 스케줄 시작
python daily_scheduler.py
```

**완료! 🎉 내일 아침 7시에 첫 리포트를 받게 됩니다.**

---

## 📱 리포트 예시

```
📊 마무리 경제 브리핑 | 2025년 10월 24일

━━━━━━━━━━━━━━━━━━━━━━
🇺🇸 미국 시장 동향
━━━━━━━━━━━━━━━━━━━━━━

🟢 S&P 500: 5,800.00 (+1.50%)
🟢 NASDAQ: 18,500.00 (+2.30%)
🟢 DOW: 43,000.00 (+0.80%)
🟢 VIX: 14.50 (-5.00%)

━━━━━━━━━━━━━━━━━━━━━━
💡 Today's Insight
━━━━━━━━━━━━━━━━━━━━━━

미국 증시 강세 흐름 속에서 국내 반도체 
섹터가 주목받고 있습니다.

📌 주요 포인트
1. 기술주 중심의 상승 장세
2. 국내 삼성전자 등 연관주 수혜 예상
3. 점진적 흐름으로 추세 추종 전략 유효

🎯 투자 시사점
• 상승 모멘텀 활용: 관련주 분할 매수 고려
• 익절 타이밍 사전 설정으로 이익 실현 준비

━━━━━━━━━━━━━━━━━━━━━━
🇰🇷 한국 시장 영향 예측
━━━━━━━━━━━━━━━━━━━━━━

📌 주목 관련주 TOP 3
1. 🟢 삼성전자 (반도체)
2. 🟢 SK하이닉스 (반도체)
3. 🟢 네이버 (IT플랫폼)
```

---

## 🏗️ 시스템 구조

```
마무리 AI Agent
├─ market_data_collector.py    # 핵심 엔진
│  ├─ 데이터 수집 (yfinance)
│  ├─ 시장 분석
│  └─ 리포트 생성
│
├─ korean_stock_mapper.py       # 한국 관련주 분석
│  ├─ 5개 섹터 매핑
│  ├─ 15개 대표 종목
│  └─ 영향도 계산
│
├─ market_analyst.py            # AI 인사이트
│  ├─ 상황 분석
│  ├─ 투자 조언
│  └─ 리스크 알림
│
├─ telegram_notifier.py         # Telegram 발송
│  ├─ 메시지 포맷팅
│  ├─ 에러 핸들링
│  └─ Mock 모드 지원
│
└─ daily_scheduler.py           # 자동 스케줄러
   ├─ 매일 7시 실행
   ├─ 로깅
   └─ 재시작 처리
```

---

## 🌐 배포 가이드

### Option 1: Railway (추천)

```
1. https://railway.app 가입
2. GitHub 저장소 연결
3. 환경변수 설정
4. 자동 배포 완료!
```

**무료 크레딧**: $5/월 (충분함)

### Option 2: Render

```
1. https://render.com 가입
2. Background Worker 생성
3. 환경변수 설정
4. 배포!
```

**완전 무료** (15분 Sleep 있음)

### Option 3: 로컬 서버

```bash
# systemd 서비스 생성
sudo nano /etc/systemd/system/mamoori.service

# 서비스 시작
sudo systemctl enable mamoori
sudo systemctl start mamoori
```

**자세한 내용**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 참고

---

## 🛠️ 고급 설정

### 발송 시간 변경

```python
# daily_scheduler.py
schedule.every().day.at("06:30").do(run_daily_report)  # 6시 30분
```

### 주말 제외

```python
def run_daily_report():
    if datetime.now().weekday() >= 5:  # 토, 일
        return
    # ... 기존 코드
```

### 여러 사람에게 발송

```python
chat_ids = ["123456", "789012", "345678"]
for chat_id in chat_ids:
    notifier = TelegramNotifier(token, chat_id)
    notifier.send_report(report)
```

---

## 📊 기술 스택

- **Python 3.8+**: 메인 언어
- **yfinance**: 미국 시장 데이터
- **requests**: Telegram API
- **schedule**: 작업 스케줄링
- **pandas**: 데이터 처리

---

## 🤝 기여하기

개선 아이디어나 버그 리포트는 언제나 환영입니다!

```bash
# Fork & Clone
git clone https://github.com/yourusername/mamoori-agent.git

# 브랜치 생성
git checkout -b feature/amazing-feature

# 커밋 & 푸시
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# PR 생성
```

---

## 📝 로드맵

### Phase 1 ✅ (완료)
- [x] 미국 시장 데이터 수집
- [x] 한국 관련주 분석
- [x] AI 인사이트 생성
- [x] Telegram 자동 발송

### Phase 2 (계획)
- [ ] 뉴스 헤드라인 통합
- [ ] 포트폴리오 분석
- [ ] 웹 대시보드
- [ ] 챗봇 인터페이스

### Phase 3 (계획)
- [ ] 개인 일정 관리 통합
- [ ] AI 큐레이션
- [ ] 음성 브리핑
- [ ] 모바일 앱

---

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

---

## 👤 만든 사람

**달희** - "마무리가 부족해서 만들었습니다"

- 블로그: [링크]
- 이메일: [이메일]
- Telegram: [@yourusername]

---

## 🙏 감사의 말

- **Claude (Anthropic)**: AI 개발 파트너
- **Yahoo Finance**: 시장 데이터 제공
- **Telegram**: 최고의 알림 플랫폼
- **Railway/Render**: 무료 호스팅

---

## ⭐ Star History

이 프로젝트가 도움이 되었다면 ⭐️ 를 눌러주세요!

---

**Built with ❤️ by 달희**  
**"시작한 것은 반드시 마무리한다"**

---

## 📞 문의

- Issues: [GitHub Issues](https://github.com/yourusername/mamoori-agent/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/mamoori-agent/discussions)

---

*Last Updated: 2025-10-24*
