# Kidsnote mitmweb

> **iOS 개발자를 위한 네트워크 디버깅 및 광고/분석 지표 모니터링 도구**
> mitmproxy 기반의 강력한 네트워크 분석 및 시각화 플랫폼

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![mitmproxy](https://img.shields.io/badge/based%20on-mitmproxy-brightgreen)](https://mitmproxy.org/)
[![React](https://img.shields.io/badge/React-19-blue)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)

---

## 🎯 프로젝트 소개

**Kidsnote mitmweb**은 mitmproxy를 포크하여 iOS 앱 개발자에게 특화된 네트워크 디버깅 기능을 추가한 도구입니다. 특히 **키즈노트 광고 트래킹**과 **티아라(Tiara) 사용자 행동 분석** 기능을 통해 앱의 광고 지표와 분석 이벤트를 실시간으로 모니터링할 수 있습니다.

### 핵심 기능

#### 📱 광고 트래킹 분석 (Ad Tracking)
- **광고 요청/노출/클릭 자동 추적** - `/req`, `/imp`, `/click` 이벤트 실시간 모니터링
- **CTR(클릭률) 자동 계산** - 광고별 노출 대비 클릭률 통계
- **Ad ID 기반 필터링** - 특정 광고 캠페인 추적
- **패킷 상세 뷰** - HTTP 요청/응답 전체 분석

#### 📈 티아라 분석 (Tiara Analytics)
- **사용자 행동 이벤트 추적** - ViewImp, Click, Search, PageView 등
- **Action Type 필터링** - 이벤트 유형별 분류 및 검색
- **Raw Event Data 확인** - 전송되는 분석 데이터 원본 조회
- **Page/Section 분석** - 화면별 이벤트 발생 현황

#### 🔧 네트워크 디버깅
- 📊 **실시간 메트릭 대시보드** - API 응답시간, 에러율, 도메인별 통계를 한눈에
- ⏱️ **타임라인 뷰 (Waterfall)** - 요청 간의 시간 관계를 시각적으로 분석
- 🔍 **고급 필터링** - 도메인, 경로, 메서드, 상태 코드별 필터링
- 🐌 **슬로우 쿼리 감지** - 3초 이상 걸리는 API를 자동으로 감지
- ⚠️ **에러 하이라이트** - 4xx/5xx 에러를 색상으로 강조
- 🔎 **전체 검색** - 요청/응답 내용을 실시간 검색

---

## 🚀 빠른 시작

### 전제 조건

- macOS (iOS 시뮬레이터 지원)
- Python 3.12+
- Node.js 24+
- Git

### 설치

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/kidsnote-mitmweb.git
cd kidsnote-mitmweb

# 2. Python 환경 설정 (uv 사용)
uv sync

# 3. 프론트엔드 의존성 설치
cd web
npm install

# 4. 개발 서버 실행
npm start              # Terminal 1 - 프론트엔드 개발 서버
cd ..
uv run mitmweb        # Terminal 2 - 백엔드 서버
```

### iOS 시뮬레이터 설정

```bash
# 1. 시뮬레이터 부팅
xcrun simctl boot "iPhone 15 Pro"
open -a Simulator

# 2. 프록시 환경변수 설정
xcrun simctl spawn booted launchctl setenv http_proxy http://127.0.0.1:8080
xcrun simctl spawn booted launchctl setenv https_proxy http://127.0.0.1:8080

# 3. mitmproxy 인증서 설치
xcrun simctl openurl booted "file://$HOME/.mitmproxy/mitmproxy-ca-cert.pem"

# 시뮬레이터에서:
# 설정 → 일반 → VPN 및 기기 관리 → mitmproxy 프로필 설치
# 설정 → 일반 → 정보 → 인증서 신뢰 설정 → mitmproxy 활성화

# 4. 웹 인터페이스 접속
open http://localhost:8081
```

---

## 📊 주요 기능 상세

### 1. 📱 광고 트래킹 대시보드 (Ad Tracking Panel)

키즈노트 광고 API를 자동으로 모니터링하고 분석합니다.

**모니터링 대상:** `ads-api-kcsandbox-01.kidsnote.com`

```
┌─────────────────────────────────────────────────┐
│  📱 Kidsnote Ad Tracking Analysis               │
├─────────────────────────────────────────────────┤
│  [ 📊 광고 요약 | 📦 패킷 상세 | 📈 티아라 ]     │  ← 탭 메뉴
├─────────────────────────────────────────────────┤
│  총 광고: 45    노출됨: 38    클릭됨: 5         │
│  CTR: 13.2%                                     │
├─────────────────────────────────────────────────┤
│  Ad ID          | 제목      | 상태   | 노출시간 │
│  abc123...      | 광고 A    | 클릭됨 | 14:23:01│
│  def456...      | 광고 B    | 노출됨 | 14:23:05│
└─────────────────────────────────────────────────┘
```

**지원하는 이벤트:**
- `/req` - 광고 목록 요청
- `/imp` - 광고 노출 이벤트
- `/click` - 광고 클릭 이벤트

### 2. 📈 티아라 분석 (Tiara Analytics)

카카오 Tiara를 통한 사용자 행동 분석 이벤트를 추적합니다.

**모니터링 대상:** `stat.tiara.daum.net`

```
┌─────────────────────────────────────────────────┐
│  Action Type: [All ▼]  Showing 156 events       │
├─────────────────────────────────────────────────┤
│  Time     | Type    | Name          | Page     │
│  14:23:01 | ViewImp | trackViewImp  | home     │
│  14:23:05 | Click   | trackClick    | banner   │
│  14:23:10 | Search  | trackSearch   | search   │
└─────────────────────────────────────────────────┘
```

**추적 가능한 Action Types:**
- `ViewImp` - 노출 이벤트 (imp_id, copy 정보 포함)
- `Click` - 클릭 이벤트
- `Search` - 검색 이벤트
- `PageView` - 페이지 조회
- `CustomEvent` - 커스텀 이벤트

### 3. 메트릭 대시보드

실시간으로 업데이트되는 네트워크 지표:

```
┌─────────────────────────────────────────┐
│  총 요청: 1,234    에러율: 2.5%         │
│  평균 응답시간: 234ms   슬로우 쿼리: 12  │
├─────────────────────────────────────────┤
│  📈 응답시간 차트 (시간대별)              │
│  📊 상태 코드 분포 (파이 차트)            │
│  📊 도메인별 통계 (바 차트)               │
└─────────────────────────────────────────┘
```

### 4. 타임라인 뷰 (Waterfall)

요청들의 시간 흐름을 시각화:

```
/api/v1/users       ████████████            200ms
/api/v1/posts          ██████               100ms
/api/v1/comments           ████████████████ 300ms
```

### 5. 고급 필터링

```typescript
// 예: Kidsnote API 중 POST 요청만 보기
도메인: kidsnote.com
메서드: POST
상태: 모두
```

### 6. 슬로우 쿼리 감지

3초 이상 걸리는 API를 자동으로 감지하고 🐌 배지 표시:

```
GET /api/v1/heavy-data  [🐌 Slow] 5.2s  500 Server Error
```

---

## 🏗️ 아키텍처

```
iOS Simulator
    ↓ (Proxy: 127.0.0.1:8080)
mitmproxy Core (트래픽 가로채기)
    ↓
mitmweb Backend (Tornado)
    ↓ (REST API + WebSocket)
React Frontend (커스텀 UI)
    ├─ MetricsPanel
    ├─ TimelineView
    ├─ AdvancedFilters
    └─ ...
```

자세한 내용은 [ARCHITECTURE.md](./ARCHITECTURE.md) 참조.

---

## 📅 개발 로드맵

### v0.1.0 - MVP ✅
- [x] 메트릭 대시보드
- [x] 기본 차트 (응답시간, 상태 코드, 도메인)
- [x] 에러 하이라이트

### v0.2.0 - 광고/분석 지표 ✅
- [x] **광고 트래킹 대시보드** (Ad Tracking Panel)
- [x] 광고 요청/노출/클릭 자동 추적
- [x] CTR 자동 계산
- [x] **티아라 분석** (Tiara Analytics)
- [x] Action Type 필터링
- [x] Raw Event Data 조회
- [x] 3탭 UI (광고 요약 / 패킷 상세 / 티아라)

### v0.3.0 - 고급 기능 (진행 중)
- [ ] 타임라인 뷰 (Waterfall)
- [ ] 슬로우 쿼리 감지
- [ ] 고급 필터링
- [ ] 검색 기능

### v0.4.0 - 완성
- [ ] 북마크/태깅
- [ ] API 의존성 그래프
- [ ] 테스트 및 문서화
- [ ] Docker 배포

### v1.0.0 - 프로덕션 릴리스
- [ ] 팀 배포
- [ ] 사용자 피드백 반영
- [ ] 성능 최적화

자세한 일정은 [ROADMAP.md](./ROADMAP.md) 참조.

---

## 🛠️ 기술 스택

### 백엔드
- **mitmproxy** - HTTP/HTTPS 프록시 코어
- **Python 3.12+** - 백엔드 언어
- **Tornado** - 웹 서버 프레임워크

### 프론트엔드
- **React 19** - UI 프레임워크
- **TypeScript 5** - 타입 안전성
- **Redux Toolkit** - 상태 관리
- **Vite** - 빌드 도구
- **Recharts** - 차트 라이브러리
- **Bootstrap 3** - UI 컴포넌트

### 개발 도구
- **Jest** - 테스트 프레임워크
- **ESLint** - 코드 린팅
- **Prettier** - 코드 포매팅
- **uv** - Python 패키지 관리
- **npm** - JavaScript 패키지 관리

---

## 📖 문서

- [아키텍처 설계](./ARCHITECTURE.md) - 시스템 구조 및 설계 철학
- [개발 로드맵](./ROADMAP.md) - 개발 일정 및 마일스톤
- [설치 가이드](./INSTALLATION.md) - 상세 설치 및 설정 (작성 예정)
- [사용자 가이드](./USER_GUIDE.md) - 기능별 사용법 (작성 예정)
- [개발자 가이드](./DEVELOPER_GUIDE.md) - 기여 가이드 (작성 예정)

---

## 🤝 기여하기

기여는 언제나 환영합니다!

### 개발 환경 설정

```bash
# 1. 저장소 포크
gh repo fork yourusername/kidsnote-mitmweb

# 2. 브랜치 생성
git checkout -b feature/my-feature

# 3. 개발
# (코드 수정)

# 4. 테스트
npm test

# 5. 커밋
git commit -m "feat: Add my awesome feature"

# 6. 푸시
git push origin feature/my-feature

# 7. Pull Request 생성
gh pr create
```

### 커밋 메시지 규칙

```
feat: 새로운 기능 추가
fix: 버그 수정
refactor: 코드 리팩토링
docs: 문서 업데이트
test: 테스트 추가/수정
chore: 빌드, 설정 변경
```

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. [LICENSE](./LICENSE) 파일 참조.

**기반 프로젝트:**
- [mitmproxy](https://github.com/mitmproxy/mitmproxy) - MIT License

---

## 🙏 감사의 글

- [mitmproxy 팀](https://mitmproxy.org/) - 훌륭한 프록시 도구 제공
- [React 팀](https://react.dev/) - 최고의 UI 라이브러리
- [Recharts 팀](https://recharts.org/) - 아름다운 차트 라이브러리

---

## 📞 문의

- **이슈:** [GitHub Issues](https://github.com/yourusername/kidsnote-mitmweb/issues)
- **토론:** [GitHub Discussions](https://github.com/yourusername/kidsnote-mitmweb/discussions)
- **이메일:** your.email@example.com

---

## 🎯 사용 시나리오

### 시나리오 1: 광고 노출/클릭이 제대로 트래킹되는지 확인하고 싶어

```bash
1. mitmweb 실행 후 "Ad Tracking" 탭 선택
2. 📊 광고 요약 탭에서 전체 현황 확인
3. 특정 광고 검색 (Ad ID로 검색)
4. 노출 → 클릭 이벤트 순서 확인
5. 📦 패킷 상세 탭에서 실제 HTTP 요청 분석
→ 광고 트래킹 정상 동작 확인! 🎯
```

### 시나리오 2: 티아라 분석 이벤트가 올바르게 전송되는지 확인하고 싶어

```bash
1. 📈 티아라 탭 선택
2. Action Type 필터로 특정 이벤트 타입 선택 (예: ViewImp)
3. 이벤트 행 클릭하여 상세 모달 열기
4. Raw Event Data에서 전송되는 JSON 데이터 확인
5. imp_id, copy, page, section 등 필드 검증
→ 분석 이벤트 데이터 검증 완료! 🎯
```

### 시나리오 3: API 응답이 느린데 어디가 문제인지 모르겠어

```bash
1. mitmweb 실행
2. Metrics 탭 열기
3. 응답시간 차트 확인
4. 느린 구간 클릭
5. 해당 시간대 요청 확인
→ 병목 지점 발견! 🎯
```

### 시나리오 4: 앱이 어떤 API를 호출하는지 파악하고 싶어

```bash
1. 필터에서 도메인 선택: kidsnote.com
2. 도메인별 통계 차트 확인
3. Timeline 뷰에서 호출 순서 확인
→ API 호출 패턴 파악! 🎯
```

### 시나리오 5: 특정 광고의 전체 라이프사이클 추적

```bash
1. Ad Tracking → 📦 패킷 상세 탭
2. 광고 요청(req) 패킷 확인 → 광고 목록 수신
3. 노출(imp) 패킷 확인 → 사용자에게 광고 표시
4. 클릭(click) 패킷 확인 → 사용자가 광고 클릭
5. Query Parameters로 상세 파라미터 분석
→ 광고 라이프사이클 완전 분석! 🎯
```

---

## 📸 스크린샷

### 메트릭 대시보드
```
[이미지 추가 예정]
```

### 타임라인 뷰
```
[이미지 추가 예정]
```

### 필터링 예제
```
[이미지 추가 예정]
```

---

## 🔧 트러블슈팅

### Q: 인증서 오류가 발생해요
```bash
# 인증서 재생성
rm -rf ~/.mitmproxy
mitmproxy  # Ctrl+C로 즉시 종료
# 시뮬레이터에 다시 설치
```

### Q: 트래픽이 보이지 않아요
```bash
# 프록시 환경변수 확인
xcrun simctl spawn booted launchctl getenv http_proxy
xcrun simctl spawn booted launchctl getenv https_proxy

# 제대로 설정되지 않았다면 다시 설정
xcrun simctl spawn booted launchctl setenv http_proxy http://127.0.0.1:8080
xcrun simctl spawn booted launchctl setenv https_proxy http://127.0.0.1:8080
```

### Q: 빌드가 실패해요
```bash
# 의존성 재설치
rm -rf node_modules package-lock.json
npm install

# Python 환경 재구성
uv sync --reinstall
```

---

## 🚀 배포

### Docker로 배포

```bash
# 빌드
docker build -t kidsnote-mitmweb .

# 실행
docker run -p 8081:8081 kidsnote-mitmweb

# 브라우저에서 접속
open http://localhost:8081
```

### Python 패키지로 배포

```bash
# 설치
pip install -e .

# 실행
mitmweb

# 브라우저에서 접속
open http://localhost:8081
```

---

**Made with ❤️ for iOS Developers**
