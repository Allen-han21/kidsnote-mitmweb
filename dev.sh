#!/bin/bash

# Kidsnote mitmweb Development Server

echo "🚀 Starting Kidsnote mitmweb development servers..."
echo ""

# 프로젝트 디렉토리
PROJECT_DIR="$HOME/Dev/personal/kidsnote-mitmweb"
MITMPROXY_DIR="$PROJECT_DIR/mitmproxy"

# 백그라운드 프로세스 정리 함수
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    pkill -f "npm start"
    pkill -f "mitmweb"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 1. 프론트엔드 개발 서버 시작
echo "📦 Starting Vite frontend dev server..."
cd "$MITMPROXY_DIR/web"
npm start > /tmp/mitmweb-vite.log 2>&1 &
VITE_PID=$!

# Vite 시작 대기
sleep 3
echo "✅ Vite dev server: http://localhost:5173"

# 2. mitmweb 백엔드 시작
echo "🔧 Starting mitmweb backend..."
cd "$MITMPROXY_DIR"
uv run mitmweb --web-host 127.0.0.1 --web-port 8081 > /tmp/mitmweb-backend.log 2>&1 &
MITMWEB_PID=$!

# mitmweb 시작 및 토큰 추출
sleep 3

# 토큰 추출
TOKEN=$(grep -o 'token=[a-f0-9]*' /tmp/mitmweb-backend.log | cut -d= -f2)

echo "✅ mitmweb backend: http://127.0.0.1:8081"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Access URL with token:"
echo "   http://127.0.0.1:8081/?token=$TOKEN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Click 'Metrics' tab to see the dashboard"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# 브라우저 자동 열기
open "http://127.0.0.1:8081/?token=$TOKEN"

# 로그 모니터링
echo "📝 Monitoring logs (Ctrl+C to exit)..."
tail -f /tmp/mitmweb-backend.log /tmp/mitmweb-vite.log
