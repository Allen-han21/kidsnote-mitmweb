# mitmios

> **Configurable network debugging tool for iOS developers, built on mitmproxy**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![mitmproxy](https://img.shields.io/badge/based%20on-mitmproxy-brightgreen)](https://mitmproxy.org/)

mitmios intercepts iOS app traffic through mitmproxy and displays it in a custom React dashboard with **config-driven tracker plugins**. Define your analytics endpoints in YAML, and mitmios automatically matches, extracts, and visualizes the data.

---

## Quick Start

```bash
# Install
uv tool install mitmios

# First-time certificate setup
mitmios setup

# Start proxy + web dashboard
mitmios start
```

Open the web UI at the URL printed in the terminal (includes authentication token).

---

## Connecting Devices

### iOS Simulator

```bash
# Set proxy environment variables on the booted simulator
xcrun simctl spawn booted launchctl setenv http_proxy http://127.0.0.1:8080
xcrun simctl spawn booted launchctl setenv https_proxy http://127.0.0.1:8080
```

Then relaunch the app in the simulator — traffic will be captured.

### Physical Device (WireGuard — recommended)

1. In the mitmios web UI, go to **Capture** tab
2. Check **Run WireGuard Server**
3. Scan the QR code with the [WireGuard app](https://apps.apple.com/app/wireguard/id1441195209) on your device
4. Name the tunnel (e.g. `mitmios`) and enable it

### Physical Device (Manual Proxy)

1. Connect device to the same Wi-Fi network as your Mac
2. On iPhone: **Settings → Wi-Fi → (i) → Configure Proxy → Manual**
   - Server: your Mac's local IP (e.g. `192.168.x.x`)
   - Port: `8080`
3. Start mitmios listening on all interfaces:
   ```bash
   mitmios start --host 0.0.0.0
   ```

### Certificate Setup (required for HTTPS)

```bash
mitmios setup
```

Or manually: open Safari on the device/simulator → navigate to `http://mitm.it` → install profile → **Settings → General → About → Certificate Trust Settings** → enable mitmproxy.

---

## How It Works

```
iOS Simulator / Device
    | (HTTP/HTTPS via proxy :8080 or WireGuard)
    v
mitmproxy core (traffic interception)
    |
    v
mitmweb backend (Tornado + WebSocket)
    |
    v
React dashboard (custom UI)
    ├── Capture       — configure proxy modes (HTTP, WireGuard, Reverse, etc.)
    ├── Flow List     — request/response inspector with search & filter
    ├── Options       — strip cache headers, display settings
    ├── Metrics       — response time, status codes, domain stats
    └── Trackers      — config-driven event tracking (YAML plugins)
```

### Tracker Plugin System

Each YAML config file defines a **tracker** that:

1. **Matches** HTTP flows by host + path regex
2. **Extracts** data from query params, headers, or body
3. **Displays** results in a dynamic table with configurable columns

```yaml
# configs/my-tracker.yaml
name: "My Analytics"
description: "Track custom analytics events"

matchers:
  - id: "event"
    label: "Event"
    color: "#8b5cf6"
    host: "analytics.myapp.com"
    path_pattern: "/v1/events(\\?|$)"

extractors:
  - source: "request.query"
    field: "event_name"
    display_name: "Event Name"

display:
  type: "event_table"
  columns:
    - { field: "Event Name", label: "Event", type: "badge" }
    - { field: "matcher_label", label: "Type", type: "badge" }
    - { field: "timestamp", label: "Time", type: "timestamp" }
    - { field: "status_code", label: "Status", type: "status_code" }
```

Each tracker gets its own **sub-tab** in the Trackers panel. No code changes needed.

---

## Installation

### Via uv (recommended)

```bash
uv tool install mitmios
```

### Via pip

```bash
pip install mitmios
```

### From source

```bash
git clone --recursive https://github.com/Allen-han21/mitmios.git
cd mitmios
uv sync
uv pip install -e .
```

---

## CLI Reference

### `mitmios start`

Start the proxy and web dashboard.

```bash
mitmios start                        # default: proxy :8080, web :8081
mitmios start --port 9090            # custom web UI port
mitmios start --proxy-port 9080      # custom proxy port
mitmios start --no-browser           # don't auto-open browser
mitmios start --no-simulator         # skip simulator detection
```

### `mitmios setup`

Install mitmproxy CA certificate to macOS keychain and iOS simulators.

```bash
mitmios setup
```

This will:
1. Generate the CA cert if missing (`~/.mitmproxy/`)
2. Add it to the macOS system keychain
3. Install it to all booted iOS simulators via `simctl keychain`
4. Print manual installation instructions as fallback

### `mitmios config`

Manage tracker configurations.

```bash
mitmios config list                  # show all configs (built-in + user)
mitmios config add path/to/my.yaml   # copy config to user directory
mitmios config validate my.yaml      # validate against schema
mitmios config example               # print example YAML config
```

**Config locations:**
- Built-in: `<install-dir>/configs/`
- User: `~/.config/mitmios/trackers/`

---

## Built-in Tracker Configs

| Config | Host | Matchers | Description |
|--------|------|----------|-------------|
| `kidsnote-ads.yaml` | `ads-api-kcsandbox-01.kidsnote.com` | 3 | Ad request/impression/click |
| `kidsnote-tiara.yaml` | `stat.tiara.daum.net` | 1 | Kakao Tiara analytics |
| `firebase-analytics.yaml` | `app-measurement.com` | 2 | Firebase Analytics |
| `amplitude.yaml` | `api2.amplitude.com` | 2 | Amplitude analytics |

---

## Writing Custom Trackers

### YAML Schema

```yaml
# Required fields
name: "Tracker Name"              # displayed as tab title
description: "What this tracks"   # shown in config list

matchers:                         # at least one required
  - id: "unique_id"              # unique within this config
    label: "Display Label"        # shown as badge text
    color: "#hex"                 # badge color
    host: "api.example.com"       # exact match on request host
    path_pattern: "/path(\\?|$)"  # regex on request path

extractors:                       # optional, can be empty []
  - source: "request.query"       # request.query | request.header | response.header
    field: "param_name"           # query param key or header name
    display_name: "Column Name"   # used as key in extracted data
    primary_key: true             # optional, marks as identifier

display:
  type: "event_table"             # currently only event_table
  columns:
    - field: "Column Name"        # extracted data key or built-in field
      label: "Header"             # table column header
      type: "text"                # text | code | badge | timestamp | status_code
```

### Built-in Fields

These fields are always available without extractors:

| Field | Description |
|-------|-------------|
| `matcher_label` | Matched rule's label (rendered as colored badge) |
| `timestamp` | Request timestamp |
| `method` | HTTP method |
| `host` | Request host |
| `path` | Request path |
| `status_code` | Response status code |

### Extractor Sources

| Source | Extracts from |
|--------|--------------|
| `request.query` | URL query parameters |
| `request.header` | Request headers |
| `response.header` | Response headers |
| `request.body` | Request body (planned) |
| `response.body` | Response body (planned) |

---

## Development

### Prerequisites

- macOS (for iOS simulator support)
- Python 3.12+
- Node.js 20+
- uv

### Dev Setup

```bash
git clone --recursive https://github.com/Allen-han21/mitmios.git
cd mitmios
uv venv && source .venv/bin/activate
uv pip install -e .

# Install mitmproxy from the forked submodule (required for custom web UI)
uv pip install -e ./mitmproxy

# Build the frontend (YAML configs → TypeScript → Vite bundle)
./scripts/build-frontend.sh

# Start dev servers (frontend + backend)
./scripts/dev.sh
```

> **Important:** You must install mitmproxy from the submodule (`./mitmproxy`), not from PyPI. The submodule contains the custom React dashboard with Trackers and Metrics tabs.

### Build Frontend

```bash
# Convert YAML configs → TypeScript → Vite production bundle
./scripts/build-frontend.sh
```

### Project Structure

```
mitmios/
├── mitmios/                  # Python CLI package
│   ├── cli.py                # typer CLI (start, setup, config)
│   ├── proxy.py              # iOS simulator detection
│   ├── cert.py               # Certificate installation
│   └── config.py             # YAML config management
├── configs/                  # Tracker YAML configs
│   ├── kidsnote-ads.yaml
│   ├── kidsnote-tiara.yaml
│   ├── firebase-analytics.yaml
│   └── amplitude.yaml
├── scripts/
│   ├── dev.sh                # Development server
│   └── build-frontend.sh     # Production build
├── mitmproxy/                # Git submodule (forked mitmproxy)
│   └── web/src/js/
│       ├── trackers/         # Tracker engine (TypeScript)
│       │   ├── types.ts      # TrackerConfig, MatcherRule, TrackedEvent
│       │   ├── engine.ts     # TrackerEngine (matching + extraction)
│       │   ├── registry.ts   # Singleton config registry
│       │   └── configs.generated.ts  # Auto-generated from YAML
│       └── components/Trackers/
│           ├── EventTrackerPanel/    # Config-driven tracker UI
│           └── MetricsPanel/         # Network metrics dashboard
└── pyproject.toml
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Proxy | mitmproxy (forked, 13.x-dev) |
| CLI | Python 3.12+ / typer / rich |
| Config | YAML / PyYAML |
| Frontend | React 19 / TypeScript 5 / Redux / Vite |
| Charts | Recharts |

---

## License

MIT License. See [LICENSE](./LICENSE).

Based on [mitmproxy](https://github.com/mitmproxy/mitmproxy) (MIT License).
