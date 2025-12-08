# Kidsnote mitmweb - 개발 로드맵

## 🎯 프로젝트 목표

**비전:** iOS 개발자가 네트워크 문제를 5분 안에 파악할 수 있는 도구

**성공 기준:**
- ✅ API 병목 지점을 즉시 시각화
- ✅ 에러 발생 시 원인을 빠르게 추적
- ✅ 팀원 간 네트워크 이슈 공유 용이
- ✅ 월 1시간 미만의 유지보수

---

## 📅 개발 일정 (4주)

```
Week 1: 환경 설정 & 기본 구조
Week 2: 핵심 기능 개발 (메트릭, 차트)
Week 3: 고급 기능 개발 (타임라인, 의존성 그래프)
Week 4: 테스트, 문서화, 배포
```

---

## Phase 0: 준비 단계 ✅ (완료)

**기간:** Day 1

- [x] 프로젝트 디렉토리 생성
- [x] 아키텍처 설계 문서 작성
- [x] 로드맵 수립
- [x] Git 저장소 초기화
- [x] GitHub 저장소 생성

---

## Phase 1: 환경 설정 & 포크 (Week 1)

### Day 1-2: mitmproxy 포크 및 빌드

**목표:** 로컬에서 mitmproxy 빌드 성공

**작업:**
```bash
# mitmproxy 포크
gh repo fork mitmproxy/mitmproxy --clone

# 개발 환경 설정
cd mitmproxy
uv sync

# 프론트엔드 설정
cd web
npm install

# 개발 서버 테스트
npm start              # Terminal 1
uv run mitmweb        # Terminal 2
```

**체크리스트:**
- [ ] mitmproxy 저장소 포크
- [ ] 로컬 빌드 성공
- [ ] 개발 서버 실행 확인
- [ ] http://localhost:8081 접속 확인
- [ ] HMR (Hot Module Replacement) 동작 확인

**예상 이슈:**
- Python 3.12+ 버전 필요
- Node.js 24+ 필요
- uv 패키지 매니저 설치 필요

---

### Day 3-4: 프로젝트 구조 설정

**목표:** 커스텀 컴포넌트를 위한 디렉토리 구조 생성

**작업:**
```bash
# 신규 디렉토리 생성
cd web/src/js
mkdir -p components/Kidsnote/{MetricsPanel,TimelineView,AdvancedFilters}
mkdir -p ducks/kidsnote
mkdir -p ../css/kidsnote
```

**디렉토리 구조:**
```
web/src/js/
├── components/
│   ├── (기존 컴포넌트들)
│   └── Kidsnote/                    # ⭐ 신규
│       ├── MetricsPanel/
│       │   ├── index.tsx
│       │   ├── SummaryCards.tsx
│       │   ├── ResponseTimeChart.tsx
│       │   ├── StatusCodeChart.tsx
│       │   └── DomainStatsChart.tsx
│       ├── TimelineView/
│       │   ├── index.tsx
│       │   └── WaterfallChart.tsx
│       ├── AdvancedFilters/
│       │   ├── index.tsx
│       │   ├── DomainFilter.tsx
│       │   └── SlowQueryFilter.tsx
│       ├── TaggingSystem/
│       │   ├── index.tsx
│       │   └── TagManager.tsx
│       ├── DependencyGraph/
│       │   ├── index.tsx
│       │   └── NetworkGraph.tsx
│       └── ErrorHighlight/
│           ├── index.tsx
│           └── ErrorPanel.tsx
└── ducks/
    ├── (기존 상태 관리)
    └── kidsnote/                    # ⭐ 신규
        ├── metrics.ts
        ├── bookmarks.ts
        └── filters.ts
```

**체크리스트:**
- [ ] 디렉토리 구조 생성
- [ ] TypeScript 설정 확인
- [ ] 첫 번째 더미 컴포넌트 생성
- [ ] 빌드 에러 없음 확인

---

### Day 5: 차트 라이브러리 통합

**목표:** Recharts 설치 및 샘플 차트 렌더링

**작업:**
```bash
cd web
npm install recharts
```

**샘플 컴포넌트:**
```typescript
// components/Kidsnote/MetricsPanel/ResponseTimeChart.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const sampleData = [
  { time: '12:00', responseTime: 234 },
  { time: '12:01', responseTime: 456 },
  { time: '12:02', responseTime: 189 },
];

export default function ResponseTimeChart() {
  return (
    <LineChart width={600} height={300} data={sampleData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="responseTime" stroke="#8884d8" />
    </LineChart>
  );
}
```

**체크리스트:**
- [ ] Recharts 설치
- [ ] 샘플 차트 렌더링 확인
- [ ] 반응형 차트 동작 확인

---

## Phase 2: MVP 기능 개발 (Week 2)

### Day 6-7: 메트릭 패널 기본 구조

**목표:** 메트릭 대시보드 첫 버전 완성

**구현 기능:**
1. **요약 카드 (SummaryCards)**
   ```typescript
   interface SummaryData {
     totalRequests: number;
     errorRate: number;
     avgResponseTime: number;
     slowQueries: number;
   }
   ```

2. **Redux State 연결**
   ```typescript
   // ducks/kidsnote/metrics.ts
   export const metricsSlice = createSlice({
     name: 'kidsnote/metrics',
     initialState,
     reducers: {
       updateSummary: (state, action) => {
         state.summary = action.payload;
       }
     }
   });
   ```

3. **Flows 데이터 활용**
   ```typescript
   const flows = useAppSelector(state => state.flows.list);
   const summary = calculateSummary(flows);
   ```

**체크리스트:**
- [ ] SummaryCards 컴포넌트 구현
- [ ] Redux metrics slice 생성
- [ ] flows 데이터로 통계 계산
- [ ] 실시간 업데이트 동작 확인

---

### Day 8-9: 응답 시간 차트

**목표:** 시간대별 API 응답 속도 시각화

**구현 내용:**
```typescript
interface TimelineDataPoint {
  timestamp: number;
  avgResponseTime: number;
  requestCount: number;
}

function calculateTimeline(flows: Flow[]): TimelineDataPoint[] {
  // 1분 단위로 그룹화
  const grouped = groupByMinute(flows);

  return Object.entries(grouped).map(([timestamp, items]) => ({
    timestamp: parseInt(timestamp),
    avgResponseTime: average(items.map(f => f.response.duration)),
    requestCount: items.length
  }));
}
```

**차트 옵션:**
- 실시간 업데이트 (WebSocket)
- 줌/팬 기능
- 툴팁에 상세 정보 표시

**체크리스트:**
- [ ] 시간대별 데이터 집계 로직 구현
- [ ] LineChart 렌더링
- [ ] 실시간 데이터 추가 시 차트 업데이트
- [ ] 성능 최적화 (memo, useMemo)

---

### Day 10: 상태 코드 분포 & 도메인 통계

**목표:** 성공/실패 비율 및 도메인별 트래픽 시각화

**차트 1: 상태 코드 분포 (파이 차트)**
```typescript
interface StatusCodeData {
  code: string;
  count: number;
  percentage: number;
}

// 2xx: 성공 (녹색)
// 3xx: 리다이렉트 (노란색)
// 4xx: 클라이언트 에러 (주황색)
// 5xx: 서버 에러 (빨간색)
```

**차트 2: 도메인별 통계 (바 차트)**
```typescript
interface DomainStats {
  domain: string;
  requestCount: number;
  avgResponseTime: number;
  errorRate: number;
}
```

**체크리스트:**
- [ ] StatusCodeChart 구현
- [ ] DomainStatsChart 구현
- [ ] 색상 코딩 적용
- [ ] 범례 및 툴팁 추가

---

### Day 11: 에러 하이라이트

**목표:** 4xx/5xx 에러 자동 강조 표시

**구현:**
1. **FlowTable 행 색상 변경**
   ```typescript
   function getRowClassName(flow: Flow): string {
     if (flow.response.status >= 500) return 'error-server';
     if (flow.response.status >= 400) return 'error-client';
     return '';
   }
   ```

2. **에러 전용 필터**
   ```typescript
   const errorFlows = flows.filter(f => f.response.status >= 400);
   ```

3. **에러 패널**
   - 에러 목록
   - 에러 발생 시간
   - 에러 메시지 하이라이트

**체크리스트:**
- [ ] FlowTable 스타일 수정
- [ ] 에러 필터 버튼 추가
- [ ] ErrorPanel 컴포넌트 구현
- [ ] 에러 발생 시 알림 (선택적)

---

## Phase 3: 고급 기능 개발 (Week 3)

### Day 12-13: 타임라인 뷰 (Waterfall)

**목표:** 요청 간 시간 관계를 시각화

**Waterfall 차트 구조:**
```
Request 1 ████████████                    (200ms)
Request 2       ██████                     (100ms)
Request 3           ████████████████       (300ms)
```

**구현:**
```typescript
interface WaterfallItem {
  id: string;
  url: string;
  startTime: number;
  duration: number;
  status: number;
}

function renderWaterfall(items: WaterfallItem[]) {
  const minTime = Math.min(...items.map(i => i.startTime));

  return items.map(item => ({
    ...item,
    offset: item.startTime - minTime,
    width: item.duration
  }));
}
```

**고려사항:**
- 스크롤 가능한 뷰
- 확대/축소 (줌)
- 각 요청 클릭 시 상세 정보

**체크리스트:**
- [ ] Waterfall 레이아웃 구현
- [ ] 시간 축 렌더링
- [ ] 요청 바 렌더링
- [ ] 상세 정보 툴팁
- [ ] 줌/팬 기능 (선택적)

---

### Day 14-15: 슬로우 쿼리 감지

**목표:** 3초 이상 걸리는 API 자동 감지 및 표시

**구현:**
```typescript
const SLOW_QUERY_THRESHOLD = 3000; // 3초

function detectSlowQueries(flows: Flow[]): Flow[] {
  return flows.filter(f => {
    const duration = f.response.timestamp_end - f.request.timestamp_start;
    return duration >= SLOW_QUERY_THRESHOLD;
  });
}

// FlowTable에서 배지 표시
function FlowRow({ flow }) {
  const isSlow = flow.duration >= SLOW_QUERY_THRESHOLD;

  return (
    <tr className={isSlow ? 'slow-query' : ''}>
      {isSlow && <Badge color="warning">🐌 Slow</Badge>}
      {/* ... */}
    </tr>
  );
}
```

**필터 옵션:**
- "슬로우 쿼리만 보기" 토글
- 임계값 설정 (1초, 2초, 3초, 5초)

**체크리스트:**
- [ ] 슬로우 쿼리 감지 로직
- [ ] FlowTable 배지 표시
- [ ] 슬로우 쿼리 필터
- [ ] 임계값 설정 UI

---

### Day 16-17: 고급 필터링

**목표:** 도메인, 경로, 메서드별 필터링

**필터 타입:**
```typescript
interface FilterState {
  domains: string[];        // ['kidsnote.com', 'api.kidsnote.com']
  paths: string[];          // ['/api/v1/users', '/api/v1/posts']
  methods: string[];        // ['GET', 'POST']
  statusCodes: number[];    // [200, 404, 500]
  showErrorsOnly: boolean;
  showSlowQueriesOnly: boolean;
}
```

**UI 구조:**
```
┌─────────────────────────────────────┐
│  필터                               │
├─────────────────────────────────────┤
│  도메인: [kidsnote.com ▼]           │
│  경로: [/api/v1/users ▼]            │
│  메서드: [GET] [POST] [PUT]         │
│  상태: [ ] 에러만  [ ] 느린 쿼리만    │
│  [적용] [초기화]                     │
└─────────────────────────────────────┘
```

**체크리스트:**
- [ ] FilterState Redux slice 생성
- [ ] AdvancedFilters 컴포넌트 구현
- [ ] 필터 적용 로직
- [ ] URL 쿼리 파라미터와 동기화 (선택적)

---

### Day 18: 검색 기능

**목표:** 요청/응답 내용 전체 검색

**구현:**
```typescript
function searchFlows(flows: Flow[], query: string): Flow[] {
  const lowerQuery = query.toLowerCase();

  return flows.filter(flow => {
    // URL 검색
    if (flow.request.url.toLowerCase().includes(lowerQuery)) return true;

    // 헤더 검색
    const headers = Object.values(flow.request.headers).join(' ');
    if (headers.toLowerCase().includes(lowerQuery)) return true;

    // 바디 검색 (선택적 - 성능 고려)
    if (flow.request.content) {
      const body = flow.request.content.toString();
      if (body.toLowerCase().includes(lowerQuery)) return true;
    }

    return false;
  });
}
```

**UI:**
- Header에 검색 바 추가
- 실시간 검색 (디바운스 적용)
- 검색 결과 하이라이트

**체크리스트:**
- [ ] 검색 입력 UI
- [ ] 검색 로직 구현
- [ ] 디바운스 적용 (300ms)
- [ ] 검색 결과 하이라이트

---

### Day 19: 북마크/태깅 시스템

**목표:** 중요한 요청 저장 및 관리

**데이터 구조:**
```typescript
interface Bookmark {
  id: string;
  flowId: string;
  tags: string[];
  note: string;
  createdAt: number;
}

interface BookmarksState {
  bookmarks: Bookmark[];
  tags: string[];
}
```

**기능:**
1. **북마크 추가**
   - FlowTable 행에 별 아이콘
   - 클릭 시 북마크 추가/제거

2. **태그 관리**
   - 북마크에 태그 추가 (예: "버그", "성능이슈")
   - 태그별 필터링

3. **메모 추가**
   - 각 북마크에 메모 첨부

**체크리스트:**
- [ ] Bookmarks Redux slice
- [ ] 북마크 토글 버튼
- [ ] 태그 입력 UI
- [ ] 북마크 목록 패널
- [ ] LocalStorage에 저장 (세션 유지)

---

### Day 20: API 의존성 그래프 (보너스)

**목표:** API 간 호출 관계 시각화

**구현:**
```typescript
interface DependencyNode {
  id: string;
  url: string;
  method: string;
}

interface DependencyEdge {
  from: string;
  to: string;
  weight: number; // 호출 횟수
}
```

**라이브러리:** react-flow 또는 vis-network

**체크리스트:**
- [ ] 의존성 분석 로직
- [ ] 그래프 렌더링
- [ ] 노드 클릭 시 상세 정보
- [ ] 레이아웃 알고리즘 적용

---

## Phase 4: 테스트 & 배포 (Week 4)

### Day 21-22: 테스트 작성

**목표:** 핵심 로직 테스트 커버리지 80% 이상

**테스트 영역:**
1. **유틸리티 함수**
   ```typescript
   // __tests__/utils/metrics.test.ts
   describe('calculateSummary', () => {
     it('should calculate total requests', () => {
       const flows = [/* mock data */];
       const summary = calculateSummary(flows);
       expect(summary.totalRequests).toBe(10);
     });
   });
   ```

2. **Redux Reducers**
   ```typescript
   // __tests__/ducks/metrics.test.ts
   describe('metricsSlice', () => {
     it('should update summary', () => {
       const state = reducer(initialState, updateSummary(newData));
       expect(state.summary).toEqual(newData);
     });
   });
   ```

3. **컴포넌트 렌더링**
   ```typescript
   // __tests__/components/MetricsPanel.test.tsx
   describe('MetricsPanel', () => {
     it('should render summary cards', () => {
       render(<MetricsPanel />);
       expect(screen.getByText('Total Requests')).toBeInTheDocument();
     });
   });
   ```

**체크리스트:**
- [ ] 유틸리티 함수 테스트
- [ ] Redux 테스트
- [ ] 컴포넌트 렌더링 테스트
- [ ] 테스트 커버리지 확인

---

### Day 23: 문서화

**목표:** 사용자 및 개발자 문서 작성

**문서 목록:**
1. **README.md** - 프로젝트 소개 및 빠른 시작
2. **INSTALLATION.md** - 설치 가이드
3. **USER_GUIDE.md** - 사용자 매뉴얼
4. **DEVELOPER_GUIDE.md** - 개발자 가이드
5. **CHANGELOG.md** - 버전 히스토리

**스크린샷:**
- 메트릭 대시보드
- 타임라인 뷰
- 필터링 예제

**체크리스트:**
- [ ] README.md 작성
- [ ] 사용 예제 추가
- [ ] 스크린샷 캡처
- [ ] 트러블슈팅 가이드

---

### Day 24: Docker 빌드 & 배포

**목표:** Docker 이미지 빌드 및 배포 자동화

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

# mitmproxy 설치
RUN pip install mitmproxy

# 프론트엔드 빌드
COPY web/dist /app/web/dist

WORKDIR /app
EXPOSE 8081

CMD ["mitmweb", "--web-host", "0.0.0.0", "--web-port", "8081"]
```

**GitHub Actions:**
```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t kidsnote-mitmweb .
      - name: Push to Docker Hub
        run: docker push ${{ secrets.DOCKER_USERNAME }}/kidsnote-mitmweb
```

**체크리스트:**
- [ ] Dockerfile 작성
- [ ] docker-compose.yml 작성
- [ ] GitHub Actions 설정
- [ ] Docker Hub에 이미지 푸시

---

### Day 25: 팀 공유 & 피드백

**목표:** 팀원에게 배포 및 피드백 수집

**배포 방법:**
```bash
# 팀원 사용법
docker pull yourname/kidsnote-mitmweb
docker run -p 8081:8081 yourname/kidsnote-mitmweb

# 또는
git clone https://github.com/yourname/kidsnote-mitmweb
cd kidsnote-mitmweb
./scripts/dev.sh
```

**피드백 수집:**
- [ ] 5명 iOS 개발자 테스트
- [ ] 사용성 피드백
- [ ] 버그 리포트
- [ ] 기능 요청 수집

---

## 향후 개발 계획 (v1.1+)

### v1.1 (1-2주)
- [ ] 세션 저장/불러오기 (HAR 포맷)
- [ ] Export 기능 (JSON, CSV, cURL)
- [ ] 다크 모드
- [ ] 커스텀 테마

### v1.2 (2-3주)
- [ ] 팀 협업 기능 (세션 공유)
- [ ] 클라우드 스토리지 연동
- [ ] 알림 시스템 (Slack, Discord)
- [ ] Webhook 지원

### v2.0 (1-2개월)
- [ ] AI 기반 이상 탐지
- [ ] 성능 추천 엔진
- [ ] 자동 리포트 생성
- [ ] API 문서 자동 생성

---

## 🚀 릴리스 전략

### v0.1.0 (Week 2)
- MVP: 메트릭 대시보드 + 기본 차트

### v0.2.0 (Week 3)
- 타임라인 뷰 + 고급 필터링

### v0.3.0 (Week 4)
- 북마크/태깅 + 완전한 테스트

### v1.0.0 (Week 4+)
- 프로덕션 준비 완료
- Docker 이미지 배포
- 팀 사용 시작

---

## 📊 성공 지표 추적

| 지표 | 목표 | 현재 | 상태 |
|------|------|------|------|
| MVP 완성 | 2주 | - | 🔜 |
| 테스트 커버리지 | 80% | - | 🔜 |
| 빌드 시간 | <5분 | - | 🔜 |
| 번들 크기 | <2MB | - | 🔜 |
| 팀 도입 | 5명 | - | 🔜 |
| 버그 리포트 | <5건 | - | 🔜 |

---

## 🤝 기여 가이드

**코드 스타일:**
- ESLint + Prettier 사용
- TypeScript strict 모드
- 컴포넌트당 1개 파일
- 테스트 필수

**브랜치 전략:**
```
main (프로덕션)
  └─ develop (개발)
      ├─ feature/metrics-panel
      ├─ feature/timeline-view
      └─ feature/advanced-filters
```

**커밋 메시지:**
```
feat: Add response time chart
fix: Fix WebSocket reconnection issue
refactor: Extract metrics calculation logic
docs: Update installation guide
```

---

## 📞 문의 및 지원

**이슈 트래킹:**
- GitHub Issues: 버그 리포트, 기능 요청
- GitHub Discussions: 질문, 아이디어

**문서:**
- [설치 가이드](./INSTALLATION.md)
- [사용자 가이드](./USER_GUIDE.md)
- [개발자 가이드](./DEVELOPER_GUIDE.md)

**팀 채널:**
- Slack: #network-debugging
- 주간 회의: 매주 금요일 2PM
