<!-- Last updated: 2026-04-19 -->
# Keelim Design System

## 1. 개요

Keelim Design System은 `all-web-ui` 패키지를 단일 공급자로, 모든 하위 프로젝트가 공유하는 `--kui-*` CSS 변수 계약 기반의 크로스플랫폼 디자인 시스템이다.

- **토큰 계약**: `--kui-*` CSS 변수 — 소비자는 값을 몰라도 된다
- **테마**: finance(기본 라이트) + admin-bw(다크) 두 가지
- **플랫폼**: Web(CSS/React) 완료, Android(Compose M3) 완료, iOS 미정

---

## 2. 소비자 맵

```
all-web-ui  ← 공급자 (--kui-* 토큰 계약, React 프리미티브)
  ├─ keelim-vercel  [Next.js / 금융 허브]
  ├─ rich/web       [Next.js / 관리자 콘솔]
  └─ all            [Android / Compose — Material, 별도 적용]
```

각 소비자는 `all-web-ui`의 CSS와 JSX를 import하고 자체 테마 클래스로 오버라이드한다.

---

## 3. 테마

| 클래스 | 별칭 | 용도 | 배경 |
|--------|------|------|------|
| (없음 / `:root`) | `theme-finance`, `.kui-theme-finance` | 기본 라이트 — 금융 허브 | 흰 배경, 잉크 텍스트 |
| `.theme-admin-bw` | `.kui-theme-admin-bw` | 운영 콘솔 다크 | 순수 흑백 |

두 테마 모두 **동일한 `--kui-*` 변수명**을 사용하므로 컴포넌트 코드 변경 없이 클래스 교체만으로 전환된다.

```html
<!-- 라이트 (기본) -->
<html>

<!-- 다크 전환 -->
<html class="theme-admin-bw">
```

---

## 4. 색상 토큰 (`--kui-*` contract)

### 4-1. 표면(Surface)

| 변수 | Finance | 용도 |
|------|---------|------|
| `--kui-color-bg` | `#ffffff` | 페이지 캔버스 |
| `--kui-color-surface` | `#ffffff` | 카드 표면 |
| `--kui-color-surface-soft` | `rgb(15 23 42 / 0.04)` | 보조 표면, ghost 버튼 배경 |
| `--kui-color-surface-strong` | `rgb(15 23 42 / 0.08)` | hover 강조 |
| `--kui-color-border` | `hsl(214.3 31.8% 91.4%)` | 선, 구분자 |

### 4-2. 텍스트(Ink)

| 변수 | Finance |
|------|---------|
| `--kui-color-text` | `hsl(222.2 84% 4.9%)` |
| `--kui-color-muted` | `hsl(215.4 16.3% 46.9%)` |

### 4-3. 강조(Accent)

| 변수 | Finance |
|------|---------|
| `--kui-color-accent` | `hsl(222.2 47.4% 11.2%)` |
| `--kui-color-accent-ink` | `hsl(210 40% 98%)` |

### 4-4. 상태(Status) — 각 3종(bg / border / text)

| 접두사 | 의미 |
|--------|------|
| `--kui-color-danger-*` | 오류, 경보 |
| `--kui-color-success-*` | 정상, 완료 |
| `--kui-color-warning-*` | 주의 |
| `--kui-color-info-*` | 안내 |

### 4-5. 한국 금융 마켓 색상

> **중요**: 한국 관례는 서양과 반전 — 상승=빨강, 하락=파랑

| 변수 | 값 | 의미 |
|------|----|------|
| `--kui-color-up` | `hsl(2 78% 55%)` | 상승 (red) |
| `--kui-color-up-soft` | `hsl(2 78% 55% / 0.1)` | 상승 배경 |
| `--kui-color-down` | `hsl(214 85% 45%)` | 하락 (blue) |
| `--kui-color-down-soft` | `hsl(214 85% 45% / 0.1)` | 하락 배경 |
| `--kui-color-flat` | `hsl(215.4 16.3% 46.9%)` | 보합 |

### 4-6. shadcn/Tailwind HSL 브리지

`--background`, `--foreground`, `--primary`, `--primary-foreground`, `--secondary`, `--muted`, `--muted-foreground`, `--accent`, `--border`, `--ring`, `--radius` 등 20개 변수 — `keelim-vercel/app/globals.css`와 동기화 유지.

---

## 5. 타이포그래피

### 폰트 스택

| 변수 | 폰트 | 용도 |
|------|------|------|
| `--font-sans` | Pretendard | KR + Latin UI 텍스트 |
| `--font-display` | Pretendard | 대형 헤드라인 |
| `--font-mono` | JetBrains Mono | 코드 |
| `--font-numeric` | JetBrains Mono | 숫자 (tabular-nums 강제) |

### 타입 램프

| 클래스 | 크기 | weight | 용도 |
|--------|------|--------|------|
| `.type-display-xl` | 3rem | 700 | 히어로 제목 |
| `.type-display-lg` | 2.25rem | 700 | 섹션 제목 |
| `.type-h1` | 1.875rem | 700 | — |
| `.type-h2` | 1.5rem | 600 | — |
| `.type-h3` | 1.25rem | 600 | — |
| `.type-h4` | 1.125rem | 600 | — |
| `.type-body-lg` | 1.0625rem | 400 | 주요 본문 |
| `.type-body` | 0.9375rem | 400 | 기본 본문 |
| `.type-body-sm` | 0.875rem | 400 | 보조 본문 |
| `.type-caption` | 0.75rem | 400 | 캡션 |
| `.type-overline` | 0.6875rem | 500 | 섹션 레이블 (ALL CAPS) |
| `.type-label` | 0.8125rem | 500 | 폼 레이블 |
| `.type-numeric` | — | — | `font-variant-numeric: tabular-nums` |
| `.type-ticker` | — | — | 실시간 가격 표시 |
| `.type-code` | — | — | 인라인 코드 |

### 전경색 유틸리티

`.fg-1` (primary text) · `.fg-2` (muted) · `.fg-accent` · `.fg-up` · `.fg-down` · `.fg-flat`

---

## 6. 간격 & 레이아웃

### 4px 그리드

| 변수 | 값 |
|------|-----|
| `--space-1` | 0.25rem (4px) |
| `--space-2` | 0.5rem |
| `--space-3` | 0.75rem |
| `--space-4` | 1rem |
| `--space-6` | 1.5rem |
| `--space-8` | 2rem |
| `--space-12` | 3rem |
| `--space-16` | 4rem |

### 컴포넌트 높이

| 크기 | 높이 |
|------|------|
| sm | 2.5rem |
| md | 2.75rem |
| lg | 3rem |

### 레이아웃 규칙

| 영역 | 값 |
|------|-----|
| 사이드바 너비 | 3.5rem (아이콘 전용, sticky) |
| 헤더 높이 | 3.5rem (h-14, sticky, border-bottom) |
| 카드 내부 패딩 | 1.5rem (p-6) |
| 섹션 간격 | gap-4 |
| 메인 콘텐츠 패딩 | p-4 sm:px-6 sm:py-0 |
| 배경 캔버스 | `bg-muted/40` |
| 폼 max-width (auth) | max-w-sm |
| 폼 max-width (modal) | max-w-md |

---

## 7. 모서리 반경 & 그림자

### 반경

| 변수 | 값 |
|------|-----|
| `--kui-radius-sm` | 0.85rem |
| `--kui-radius-md` | 1.15rem |
| `--kui-radius-lg` | 1.5rem |
| `--radius` (shadcn) | 0.5rem |

### 그림자

| 변수 | 용도 |
|------|------|
| `--kui-shadow-card` | 기본 카드 |
| `--kui-shadow-soft` | 드롭다운, 팝오버 |
| `--kui-shadow-panel` | 모달, 시트 |

---

## 8. 컴포넌트 목록

### 기본 프리미티브 (`all-web-ui`)

| 컴포넌트 | 상태 |
|---------|------|
| Button | stable |
| Input / TextField | stable |
| Panel / Card | stable |
| Badge | stable |
| LoadingInline | stable |
| LoadingPanel | stable |
| EmptyState | stable |

### 확장 프리미티브 (`primitives.jsx`)

Checkbox, Radio, Switch, Select, Textarea, Avatar, Tooltip, Alert, Progress, Skeleton, LoadingInline, LoadingPanel, Dialog, Sheet, Toast, Pagination

### 금융 허브 컴포짓 (`keelim-vercel` 전용)

KPICard, TickerRow, Sidebar, Header, Breadcrumb, DropdownMenu, Tabs

> 금융 컴포짓은 `all-web-ui`에 포함되지 않는다. `keelim-vercel/` 내에서만 관리.

---

## 9. 아이콘 규칙

- 라이브러리: `lucide-react`
- stroke: `2px`, color: `currentColor`
- 크기: h-5 (20px 기본) / h-4 (16px 보조) / h-3.5 (14px 소형)
- **이모지 금지**
- **유니코드 글리프 아이콘 금지**
- 로고: `assets/keelim-logo.svg` (filled) / `assets/keelim-mark-mono.svg` (mono)

### 애니메이션 키프레임

| 이름 | 용도 |
|------|------|
| `kui-spin` | 로딩 스피너 |
| `kui-pulse` | 스켈레톤 펄스 |
| `kui-shimmer` | 스켈레톤 shimmer |
| `kui-toast-in` | 토스트 진입 |

전환 타이밍: `160ms ease` (전체 공통)

---

## 10. 콘텐츠 규칙

### 이중 언어 정책

| 영역 | 언어 |
|------|------|
| UI 레이블, 버튼, 내비게이션 | 영어 |
| 전략 문서, 아이디어, 주석 | 한국어 |

### 어조(Tone)

- **운영자(operator)** 어조 — 마케터 어조 금지
- 느낌표 금지
- 태그라인·슬로건 금지
- 이모지 절대 금지

### 케이싱 규칙

| 위치 | 규칙 |
|------|------|
| 내비게이션 레이블 | Title Case |
| 설명, 본문 | Sentence case |
| `.type-overline` 텍스트 | ALL CAPS |

### 숫자 표기

- `font-variant-numeric: tabular-nums` 필수
- 통화: `₩1,234,000`
- 상승률: `+2.34%` (red)
- 하락률: `−0.12%` (blue, 마이너스 기호는 U+2212)
- **서양 관례(빨강=하락)로 절대 역전 금지**

---

## 11. 유지 보수 규칙 (Maintenance Rules)

### Token & Component Lifecycle

상태: `stable` | `deprecated` | `removed`

- `deprecated` 선언 시: 교체 경로 + 예고 기한을 export manifest에 명시
- `removed` 전: 모든 소비자 import 지점 제거 확인 필수
- 변수명 변경(rename) 금지 — 추가만 허용

### Cross-Platform Canary

- `keelim-vercel`, `rich/web`: import 경로 fixture 빌드 (타입체크 포함)
- `all` (Android): Compose 컴포넌트 smoke 빌드 (해당 시)
- CI 실패 → 소비자 영향 경고 출력

### PR Maintenance Gate

병합 전 필수 통과 조건:

1. Lifecycle 상태 업데이트 여부 확인
2. Cross-platform canary 통과
3. export manifest 일치 확인

### Per-Project 적용 의무

| 프로젝트 | 역할 | 의무 |
|----------|------|------|
| all-web-ui | 공급자 | lifecycle 선언, export manifest 유지 |
| keelim-vercel | 소비자 | canary fixture, adapter 계약 유지 |
| rich/web | 소비자 | canary fixture, theme import 유지 |
| all | 소비자(선택) | Compose 토큰 동기화 |

### CSS 변수 추가 절차

```
1. all-web-ui/src/styles/styles.css  ← :root 에 추가
2. all-web-ui/src/styles/themes/finance.css  ← .theme-finance 에 추가
3. all-web-ui/src/styles/themes/admin-bw.css  ← .theme-admin-bw 에 다크 값 추가
4. 이 문서 섹션 4 업데이트
5. canary 빌드 통과 확인
```
