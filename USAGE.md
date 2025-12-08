# 사용 방법 (Usage Guide)

## 🚀 빠른 시작

### 1. 개발 서버 실행

**방법 1: dev.sh 스크립트 사용 (권장)**

```bash
cd ~/Dev/personal/kidsnote-mitmweb
./dev.sh
```

이 스크립트는 자동으로:
- Vite 개발 서버 시작 (http://localhost:5173)
- mitmweb 백엔드 시작 (http://127.0.0.1:8081)
- 인증 토큰 자동 추출
- 브라우저 자동 열기

**방법 2: 수동 실행**

```bash
# Terminal 1: 프론트엔드 개발 서버
cd ~/Dev/personal/kidsnote-mitmweb/mitmproxy/web
npm start

# Terminal 2: mitmweb 백엔드
cd ~/Dev/personal/kidsnote-mitmweb/mitmproxy
uv run mitmweb --web-host 127.0.0.1 --web-port 8081

# 로그에서 토큰 확인 후 브라우저에서 접속
# http://127.0.0.1:8081/?token=<TOKEN>
```

### 2. Metrics 대시보드 접속

1. 브라우저에서 mitmweb 실행 (자동으로 열림)
2. 상단 네비게이션에서 **"Metrics"** 탭 클릭
3. 네트워크 메트릭 대시보드 확인

---

## 📊 Metrics 대시보드 기능

### 요약 카드 (Summary Cards)

대시보드 상단에 4개의 메트릭 카드가 표시됩니다:

1. **Total Requests**: 총 HTTP 요청 수
2. **Error Rate**: 4xx/5xx 에러 비율 (%)
3. **Avg Response Time**: 평균 응답 시간 (ms)
4. **Slow Queries**: 1초 이상 걸린 요청 수

### 차트 (Charts)

#### 1. Response Time Over Time (응답 시간 추이)
- **타입**: Line Chart
- **설명**: 시간대별 평균 응답 시간 추이
- **X축**: 시간 (HH:MM)
- **Y축**: 응답 시간 (ms)
- **데이터**: 5초 단위로 집계된 최근 50개 데이터 포인트

#### 2. Status Code Distribution (상태 코드 분포)
- **타입**: Pie Chart
- **설명**: HTTP 상태 코드별 요청 분포
- **색상 코딩**:
  - 🟢 2xx (성공): Green
  - 🔵 3xx (리다이렉트): Blue
  - 🟠 4xx (클라이언트 에러): Orange
  - 🔴 5xx (서버 에러): Red
- **데이터**: 상위 10개 상태 코드

#### 3. Top Domains by Request Count (도메인별 통계)
- **타입**: Bar Chart (Dual Axis)
- **설명**: 도메인별 요청 수와 평균 응답 시간
- **왼쪽 Y축**: 요청 수 (파란색 바)
- **오른쪽 Y축**: 평균 응답 시간 (초록색 바)
- **데이터**: 상위 10개 도메인

---

## 🔍 iOS 시뮬레이터 네트워크 디버깅

### 1. 프록시 설정

```bash
# iOS 시뮬레이터에 프록시 설정
xcrun simctl spawn booted launchctl setenv http_proxy http://127.0.0.1:8080
xcrun simctl spawn booted launchctl setenv https_proxy http://127.0.0.1:8080

# 설정 확인
xcrun simctl spawn booted launchctl getenv http_proxy
```

### 2. 인증서 설치

```bash
# 1. mitmproxy 인증서 다운로드
curl http://mitm.it/cert/pem -o mitmproxy-ca-cert.pem

# 2. iOS 시뮬레이터로 인증서 전송
xcrun simctl openurl booted "file://$(pwd)/mitmproxy-ca-cert.pem"

# 3. 시뮬레이터에서:
#    설정 > 일반 > VPN 및 기기 관리 > mitmproxy 인증서 설치
#    설정 > 일반 > 정보 > 인증서 신뢰 설정 > mitmproxy 신뢰 활성화
```

### 3. 앱 실행 및 트래픽 확인

1. iOS 시뮬레이터에서 앱 실행
2. mitmweb의 **Metrics** 탭에서 실시간 네트워크 메트릭 확인
3. **FlowList** 탭에서 상세 요청/응답 확인

### 4. 디버깅 완료 후 정리

```bash
# 프록시 설정 제거
xcrun simctl spawn booted launchctl unsetenv http_proxy
xcrun simctl spawn booted launchctl unsetenv https_proxy

# 시뮬레이터 재시작 (필요시)
xcrun simctl shutdown booted
xcrun simctl boot <DEVICE_UDID>
```

---

## 🏗️ 프로덕션 빌드

### 빌드 명령어

```bash
cd ~/Dev/personal/kidsnote-mitmweb/mitmproxy/web
npm run ci-build-release
```

### 빌드 결과

- 빌드 파일 위치: `mitmproxy/mitmproxy/tools/web/static/`
- 빌드 시간: ~3초
- 번들 크기:
  - `index.js`: ~184 KB (gzip: ~54 KB)
  - `vendor.js`: ~1.2 MB (gzip: ~405 KB)
  - `index.css`: ~39 KB (gzip: ~18 KB)

### 프로덕션 실행

```bash
cd ~/Dev/personal/kidsnote-mitmweb/mitmproxy
uv run mitmweb --web-host 127.0.0.1 --web-port 8081
```

빌드된 정적 파일이 자동으로 로드됩니다.

---

## 🛠️ 개발 가이드

### 프로젝트 구조

```
kidsnote-mitmweb/
├── mitmproxy/                      # mitmproxy 포크 (submodule)
│   └── web/
│       └── src/js/components/
│           └── Kidsnote/          # 커스텀 컴포넌트
│               └── MetricsPanel/
│                   ├── index.tsx              # 메인 패널
│                   ├── MetricsPanel.css       # 스타일
│                   ├── calculateMetrics.ts    # 메트릭 계산
│                   ├── ResponseTimeChart.tsx  # 라인 차트
│                   ├── StatusCodeChart.tsx    # 파이 차트
│                   └── DomainStatsChart.tsx   # 바 차트
├── dev.sh                         # 개발 서버 시작 스크립트
├── ARCHITECTURE_FINAL.md          # 최종 아키텍처 문서
├── ROADMAP.md                     # 개발 로드맵
└── STATUS.md                      # 프로젝트 현황
```

### 의존성

**Frontend:**
- React 19
- Redux
- TypeScript
- Vite
- Recharts (차트 라이브러리)

**Backend:**
- Python 3.12+
- mitmproxy
- Tornado web server

### 새 차트 추가하기

1. **차트 컴포넌트 생성**
```typescript
// web/src/js/components/Kidsnote/MetricsPanel/MyNewChart.tsx
import React from "react";
import { Flow } from "../../../flow";

type MyNewChartProps = {
    flows: Flow[];
};

export default function MyNewChart({ flows }: MyNewChartProps) {
    // 차트 구현
}
```

2. **MetricsPanel에 통합**
```typescript
// web/src/js/components/Kidsnote/MetricsPanel/index.tsx
import MyNewChart from "./MyNewChart";

export function PureMetricsPanel({ flows }: MetricsPanelProps) {
    return (
        <div className="kidsnote-metrics-panel">
            {/* 기존 코드 */}
            <div className="chart-container">
                <h3>My New Chart</h3>
                <MyNewChart flows={flows} />
            </div>
        </div>
    );
}
```

3. **빌드 및 테스트**
```bash
npm run ci-build-release
./dev.sh
```

---

## 🐛 문제 해결 (Troubleshooting)

### 포트 충돌 에러

```
[Errno 48] address already in use
```

**해결:**
```bash
# 기존 프로세스 종료
lsof -ti :8080 | xargs kill -9
lsof -ti :8081 | xargs kill -9

# 재시작
./dev.sh
```

### 인증서 에러

```
SSL: CERTIFICATE_VERIFY_FAILED
```

**해결:**
1. iOS 시뮬레이터 재시작
2. 인증서 재설치 (위의 인증서 설치 단계 참고)
3. "인증서 신뢰 설정" 확인

### 빌드 에러

```
npm ERR! code ELIFECYCLE
```

**해결:**
```bash
cd ~/Dev/personal/kidsnote-mitmweb/mitmproxy/web
rm -rf node_modules package-lock.json
npm install
npm run ci-build-release
```

### 차트가 표시되지 않음

**원인:** flows 데이터가 없거나 계산 오류

**해결:**
1. FlowList 탭에서 트래픽이 캡처되는지 확인
2. 브라우저 콘솔에서 에러 확인 (F12)
3. iOS 시뮬레이터 프록시 설정 확인

---

## 📝 주의사항

1. **업스트림 동기화**: 월 1회 mitmproxy upstream 동기화 권장
   ```bash
   cd ~/Dev/personal/kidsnote-mitmweb/mitmproxy
   git fetch upstream
   git merge upstream/main
   ```

2. **빌드 후 재시작**: 프론트엔드 변경 시 빌드 후 mitmweb 재시작 필요

3. **인증 토큰**: 보안상 토큰은 mitmweb 실행마다 변경됨

4. **서브모듈**: mitmproxy는 git submodule로 관리됨
   ```bash
   git submodule update --init --recursive
   ```

---

## 🔗 관련 링크

- **메인 저장소**: https://github.com/Allen-han21/kidsnote-mitmweb
- **포크한 mitmproxy**: https://github.com/Allen-han21/mitmproxy
- **Upstream mitmproxy**: https://github.com/mitmproxy/mitmproxy
- **mitmproxy 공식 문서**: https://docs.mitmproxy.org/
- **Recharts 문서**: https://recharts.org/

---

**버전**: Phase 1 MVP
**최종 업데이트**: 2025-12-09
