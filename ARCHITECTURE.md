# Kidsnote mitmweb - 아키텍처 설계

## 📋 프로젝트 개요

**목표:** iOS 개발자를 위한 네트워크 디버깅 도구
**기반:** mitmproxy/mitmweb 포크 + 커스텀 UI 확장
**전략:** 옵션 A - mitmweb 포크 & 최소 수정으로 최대 효과

---

## 🎯 핵심 사용 시나리오

### 시나리오 1: API 응답이 느린데 어디가 문제인지 모르겠어
**해결:**
- 타임라인 뷰 (Waterfall) - 각 요청의 시간 흐름 시각화
- 응답시간 차트 - 시간대별 API 응답 속도 추이
- 슬로우 쿼리 감지 - 3초 이상 걸리는 API 자동 하이라이트

### 시나리오 2: 앱이 어떤 API를 호출하는지 파악하고 싶어
**해결:**
- 도메인별 통계 - kidsnote.com, api.kidsnote.com 등 도메인별 집계
- API 의존성 그래프 - 어떤 화면에서 어떤 API를 호출하는지 시각화
- 필터링 - 특정 도메인/경로만 집중 분석

### 시나리오 3: 특정 API의 요청/응답을 모니터링하고 싶어
**해결:**
- 북마크/태깅 - 중요한 요청 저장
- 검색 - 요청/응답 내용 전체 검색
- 실시간 필터 - 특정 엔드포인트만 실시간 추적

### 시나리오 4: API 에러율, 응답시간을 시각화하고 싶어
**해결:**
- 지표 뷰어 - 대시보드 형태의 통합 메트릭
- 에러 로그 하이라이트 - 4xx/5xx 에러 강조 표시
- 상태 코드 분포 차트 - 성공/실패 비율 시각화

---

## 🏗️ 아키텍처 구조

```
┌─────────────────────────────────────────────────────────┐
│                  iOS Simulator / Device                 │
│                   (HTTP/HTTPS Proxy)                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Proxy: 127.0.0.1:8080
                         ↓
┌─────────────────────────────────────────────────────────┐
│                    mitmproxy Core                       │
│                   (변경 없음 - 기본 사용)                 │
│                                                         │
│  - HTTP/HTTPS 트래픽 가로채기                            │
│  - SSL/TLS 인증서 처리                                   │
│  - Flow 관리                                            │
│  - WebSocket 지원                                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Internal API
                         ↓
┌─────────────────────────────────────────────────────────┐
│                 mitmweb Backend (Tornado)               │
│                   (최소 수정 - API 확장)                  │
│                                                         │
│  기존 API:                                              │
│  - GET  /flows                                         │
│  - GET  /flows/{id}                                    │
│  - GET  /events                                        │
│  - WebSocket /updates                                  │
│                                                         │
│  추가 API (필요시):                                      │
│  - GET  /metrics/summary     (통계 요약)               │
│  - GET  /metrics/timeline    (시간대별 데이터)          │
│  - POST /flows/{id}/bookmark (북마크 토글)              │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ REST API + WebSocket
                         ↓
┌─────────────────────────────────────────────────────────┐
│              mitmweb Frontend (React 19)                │
│                   (핵심 수정 영역)                        │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │            기존 컴포넌트 (유지)                    │  │
│  │  - FlowTable (요청 목록)                          │  │
│  │  - FlowView (상세 뷰)                             │  │
│  │  - Header (상단 바)                               │  │
│  │  - EventLog (이벤트 로그)                         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         신규 컴포넌트 (추가 개발)                   │  │
│  │                                                  │  │
│  │  📊 MetricsPanel (지표 뷰어)                      │  │
│  │     ├─ SummaryCards (요약 카드)                  │  │
│  │     ├─ ResponseTimeChart (응답시간 차트)         │  │
│  │     ├─ StatusCodeChart (상태코드 분포)           │  │
│  │     └─ DomainStatsChart (도메인별 통계)          │  │
│  │                                                  │  │
│  │  ⏱️  TimelineView (타임라인/Waterfall)           │  │
│  │     └─ WaterfallChart (시간 흐름 시각화)         │  │
│  │                                                  │  │
│  │  🔍 AdvancedFilters (고급 필터)                   │  │
│  │     ├─ DomainFilter (도메인 필터)                │  │
│  │     ├─ SlowQueryFilter (슬로우 쿼리 필터)        │  │
│  │     └─ BookmarkFilter (북마크만 보기)            │  │
│  │                                                  │  │
│  │  🏷️  TaggingSystem (북마크/태깅)                 │  │
│  │     └─ TagManager (태그 관리)                    │  │
│  │                                                  │  │
│  │  📈 DependencyGraph (API 의존성 그래프)           │  │
│  │     └─ NetworkGraph (관계도 시각화)              │  │
│  │                                                  │  │
│  │  ⚠️  ErrorHighlight (에러 하이라이트)             │  │
│  │     └─ ErrorPanel (에러 전용 뷰)                 │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Redux State (확장)                   │  │
│  │                                                  │  │
│  │  기존:                                           │  │
│  │  - flows (플로우 목록)                           │  │
│  │  - ui (UI 상태)                                  │  │
│  │  - eventLog (이벤트)                             │  │
│  │                                                  │  │
│  │  추가:                                           │  │
│  │  - metrics (메트릭 데이터)                       │  │
│  │  - bookmarks (북마크 목록)                       │  │
│  │  - filters (고급 필터 상태)                      │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
                         │ Browser
                         ↓
                http://localhost:8081
```

---

## 📁 프로젝트 구조

```
kidsnote-mitmweb/
├── .git/
├── docs/                        # 설계 문서
│   ├── ARCHITECTURE.md          # (이 파일)
│   ├── ROADMAP.md              # 개발 로드맵
│   ├── TECH_STACK.md           # 기술 스택 상세
│   └── COMPONENT_DESIGN.md     # 컴포넌트 설계
├── mitmproxy/                   # upstream fork
│   ├── mitmproxy/              # Python 코어 (변경 최소)
│   ├── web/                    # 프론트엔드 (핵심 작업 영역)
│   │   ├── src/
│   │   │   ├── js/
│   │   │   │   ├── components/
│   │   │   │   │   ├── (기존 컴포넌트들)
│   │   │   │   │   └── Kidsnote/     # ⭐ 신규 기능
│   │   │   │   │       ├── MetricsPanel/
│   │   │   │   │       ├── TimelineView/
│   │   │   │   │       ├── AdvancedFilters/
│   │   │   │   │       ├── TaggingSystem/
│   │   │   │   │       ├── DependencyGraph/
│   │   │   │   │       └── ErrorHighlight/
│   │   │   │   └── ducks/
│   │   │   │       ├── (기존 상태 관리)
│   │   │   │       └── kidsnote/      # ⭐ 신규 상태
│   │   │   │           ├── metrics.ts
│   │   │   │           ├── bookmarks.ts
│   │   │   │           └── filters.ts
│   │   │   └── css/
│   │   │       └── kidsnote/          # ⭐ 커스텀 스타일
│   │   ├── package.json
│   │   └── vite.config.ts
│   ├── test/                   # 테스트
│   └── examples/               # 예제
├── scripts/                    # 빌드/배포 스크립트
│   ├── build.sh               # 전체 빌드
│   ├── dev.sh                 # 개발 서버 시작
│   └── docker-build.sh        # Docker 빌드
├── docker/                     # Docker 설정
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/                    # GitHub Actions
│   └── workflows/
│       └── ci.yml
├── README.md                   # 프로젝트 소개
├── LICENSE                     # MIT 라이선스
└── .gitignore
```

---

## 🔧 핵심 수정 포인트

### 1. 백엔드 (최소 수정)

**목표:** 기존 API 활용, 필요시만 확장

**수정 파일:**
- `mitmproxy/tools/web/app.py` (API 엔드포인트 추가 - 선택적)

**추가 API (필요시):**
```python
# /metrics/summary - 통계 요약
{
  "total_requests": 1234,
  "error_rate": 0.05,
  "avg_response_time": 234,
  "slow_queries": 12
}

# /metrics/timeline - 시간대별 데이터
[
  {"timestamp": 1234567890, "count": 45, "avg_time": 200},
  ...
]
```

**대부분은 프론트엔드에서 계산:**
- 기존 `/flows` API로 모든 데이터 조회
- 클라이언트에서 집계/분석
- 성능 이슈 발생 시 백엔드 API 추가 고려

---

### 2. 프론트엔드 (핵심 작업)

#### 2.1 새 탭 추가

**FlowView에 탭 추가:**
```typescript
// web/src/js/components/FlowView/Tabs.tsx
import MetricsTab from '../Kidsnote/MetricsPanel/MetricsTab';
import TimelineTab from '../Kidsnote/TimelineView/TimelineTab';

const tabs = [
  { name: 'Request', Component: Request },
  { name: 'Response', Component: Response },
  { name: 'Details', Component: Details },
  { name: 'Metrics', Component: MetricsTab },      // ⭐ 추가
  { name: 'Timeline', Component: TimelineTab },    // ⭐ 추가
];
```

#### 2.2 메인 대시보드 추가

**새로운 메인 뷰 추가:**
```typescript
// web/src/js/components/ProxyApp.tsx
import MetricsPanel from './Kidsnote/MetricsPanel';

// 탭 또는 사이드 패널로 추가
<MetricsPanel />
```

#### 2.3 Redux State 확장

```typescript
// web/src/js/ducks/kidsnote/metrics.ts
export interface MetricsState {
  summary: {
    totalRequests: number;
    errorRate: number;
    avgResponseTime: number;
    slowQueries: number;
  };
  timeline: TimelineData[];
  domainStats: DomainStats[];
}
```

---

### 3. 차트 라이브러리

**선택:** Recharts (React 전용, 경량)

```bash
npm install recharts
```

**이유:**
- React 19 호환
- TypeScript 지원
- 간단한 API
- 커스터마이징 용이

---

## 🎨 UI/UX 설계

### 레이아웃 옵션

#### 옵션 1: 탭 기반 (추천)
```
┌─────────────────────────────────────────┐
│  Header                                 │
├─────────────────────────────────────────┤
│  [ Flows | Metrics | Timeline | ... ]  │  ← 탭 추가
├─────────────────────────────────────────┤
│                                         │
│          컨텐츠 영역                     │
│                                         │
└─────────────────────────────────────────┘
```

#### 옵션 2: 사이드 패널
```
┌────────┬────────────────────────────────┐
│        │  Header                        │
│ 메트릭  ├────────────────────────────────┤
│ 패널    │                                │
│        │  FlowTable                     │
│        │                                │
└────────┴────────────────────────────────┘
```

---

## 📊 데이터 흐름

```
사용자 액션 (필터 변경)
    ↓
Redux Action Dispatch
    ↓
Redux Reducer 업데이트
    ↓
Component Re-render
    ↓
계산된 메트릭 표시
```

**실시간 업데이트:**
```
WebSocket /updates
    ↓
flows/add, flows/update 이벤트
    ↓
Redux Store 업데이트
    ↓
메트릭 자동 재계산
    ↓
차트 자동 업데이트
```

---

## 🔒 보안 고려사항

1. **로컬 실행 원칙**
   - 네트워크 노출 최소화
   - localhost:8081에만 바인딩

2. **민감 정보 처리**
   - Authorization 헤더 마스킹 옵션
   - 쿠키 정보 숨김 옵션

3. **팀 공유 시**
   - 세션 데이터 로컬 저장
   - 공유 시 민감 정보 자동 제거

---

## 🧪 테스트 전략

### 1. 단위 테스트 (Jest)
```typescript
// MetricsCalculator.test.ts
describe('MetricsCalculator', () => {
  it('should calculate error rate correctly', () => {
    // ...
  });
});
```

### 2. 통합 테스트
- mitmproxy와 React 앱 간 통신 테스트
- WebSocket 연결 안정성

### 3. E2E 테스트 (선택적)
- Playwright로 전체 워크플로우 테스트

---

## 📦 배포 전략

### 1. Docker (추천)
```dockerfile
FROM mitmproxy/mitmproxy:latest

# 빌드된 웹 자산 복사
COPY web/dist /web/dist

EXPOSE 8081
CMD ["mitmweb", "--web-host", "0.0.0.0"]
```

### 2. Python 패키지
```bash
pip install -e .
mitmweb
```

### 3. 바이너리 (향후)
- PyInstaller로 단일 실행 파일 생성

---

## 🔄 업스트림 동기화 전략

```bash
# 월 1회 실행
git fetch upstream
git merge upstream/main

# 충돌 발생 시
# - web/src/js/components/Kidsnote/ (우리 코드 - 충돌 없음)
# - web/src/js/components/*.tsx (조심히 머지)
```

**원칙:**
- 기존 파일 수정 최소화
- 새 파일 추가 우선
- 오버라이드 패턴 활용

---

## 🎯 성공 지표

1. **개발 속도**
   - MVP: 2주 내 완성
   - 전체 기능: 4주 내 완성

2. **유지보수**
   - 월 1시간 이내 업스트림 동기화
   - 버그 수정 시간 < 2시간

3. **성능**
   - 1000개 요청 처리 시 렌더링 < 2초
   - 메모리 사용량 < 500MB

4. **팀 만족도**
   - 5명 iOS 개발자 활용
   - 디버깅 시간 30% 단축

---

## 📚 참고 문서

- [mitmproxy 공식 문서](https://docs.mitmproxy.org/)
- [React 19 문서](https://react.dev/)
- [Redux Toolkit 문서](https://redux-toolkit.js.org/)
- [Recharts 문서](https://recharts.org/)
