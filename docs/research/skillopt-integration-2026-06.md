# SkillOpt × Codex / Claude Code 접목 — 리서치 리포트

*Generated: 2026-06-06 KST · Sources: 9 + 실제 저장소 `git clone` 검증 · Confidence: 방법론 High / 성능수치 Medium(저자·벤더 보고) / 코드 메커니즘 High(`git clone --depth 1` + 로컬 grep으로 실제 바이트 대조 완료)*

> 목적: `microsoft/SkillOpt`(https://github.com/microsoft/SkillOpt)를 **Codex CLI와 Claude Code에 접목**하기 위한 의사결정·구현 지향 리서치.
> 핵심 결론을 먼저: SkillOpt는 **이미 Codex CLI와 Claude Code를 1급(first-class) 실행 하니스로 지원**하도록 설계돼 있어, "접목"은 새로 만드는 작업이 아니라 **기존 메커니즘을 당신 환경에 연결하는 작업**이다.

---

## Executive Summary

SkillOpt는 Microsoft가 공개한 **text-space optimizer**로, LLM의 가중치를 건드리지 않고(**frozen agent**) 에이전트의 **자연어 "스킬 문서"(`SKILL.md`)를 학습 가능한 상태(trainable state)로 취급**해 신경망 훈련의 규율(epoch·batch·learning rate·validation gating)로 최적화한다. 산출물은 300~2,000 토큰짜리 `best_skill.md` 한 장이며, **배포 시 추가 모델 호출이 0회**다(그냥 컨텍스트로 읽힘). 결정적으로, SkillOpt는 평가를 **direct chat / Codex CLI / Claude Code CLI** 세 하니스에서 수행했고, 소스 코드는 실제로 `codex exec`와 `claude -p`를 subprocess로 구동하면서 최적화된 스킬을 `.agents/skills/skillopt-target/SKILL.md`에 써넣어 주입한다(원본 확인). 따라서 당신의 Codex·Claude Code 사용 흐름에 **(1) 산출 스킬을 소비**하거나 **(2) 당신의 기존 `SKILL.md`를 SkillOpt로 학습**시키는 두 방향으로 접목할 수 있다. 다만 v0.1.0 초기 단계이며, 성능 수치는 저자 보고치이고, 훈련 API 비용이 선불로 크다는 점은 감안해야 한다.

---

## 1. SkillOpt란 무엇인가

| 항목 | 내용 |
|---|---|
| 한 줄 정의 | frozen LLM 에이전트용 **재사용 가능한 자연어 스킬**을, trajectory 기반 편집 + validation-gated 업데이트로 학습시켜 `best_skill.md`로 배포하는 text-space optimizer |
| 만든 곳 / 라이선스 | Microsoft / MIT |
| 릴리스 | v0.1.0 (PyPI, 2026-06-02), 약 5.1k stars |
| 논문 | arXiv:2605.23904, Yifan Yang 외 (15인), 27p — human·TextGrad·Trace2Skill·GEPA·EvoSkill 대비 |
| 언어/스택 | Python 3.10+ (≈82%), HTML(WebUI ≈17%) |
| 설치 | `pip install skillopt` (+ extras: `[alfworld]`, `[webui]`, `[claude]`) |

**해결하는 문제.** 오늘날 에이전트 "스킬"은 사람이 손으로 쓰거나 LLM이 한 번에 생성한다 — 재현 가능하고 측정 가능한 **개선 루프가 없다**. SkillOpt는 *"스킬 문서를 frozen agent의 학습 가능한 외부 상태로 두고, weight-space 최적화를 재현 가능하게 만든 그 규율로 훈련한다"* 는 발상으로 이 공백을 메운다.

**왜 매력적인가 (배포 관점).**
- **추론 시 오버헤드 0**: 최적화 비용은 훈련 때 1회 선불. 배포된 스킬은 그냥 텍스트라 "에이전트의 system prompt나 context에 떨어뜨리면 끝, 특별한 런타임 불필요"(블로그).
- **파인튜닝/RAG와 다름**: 가중치를 안 바꾸므로(파인튜닝 X), 지식 주입이 아니라 **행동·전략을 개선**(RAG와 다름). 깨지기 쉬운 수작업 프롬프트 엔지니어링과 달리 **검증 게이트로 단조(monotonic) 개선**을 보장.

---

## 2. 핵심 방법론 — 신경망처럼 스킬을 "학습"한다

### 훈련 루프 (5단계)
```
Rollout → Reflect → Aggregate → Select → Update & Evaluate
(롤아웃)  (반성·채점) (집계)     (검증게이트) (스킬갱신·평가)
```
1. **Rollout & Score** — 현재 스킬로 에이전트를 배치 과제에 실행, 점수 수집
2. **Reflect** — 별도의 **optimizer model**이 실패를 분석해 **bounded edit(add/delete/replace)** 후보 생성
3. **Aggregate** — 편집 후보 집계
4. **Select (Validation Gating)** — held-out 검증셋에서 **점수가 엄격히 개선될 때만 채택**(hard=정확일치 / soft=부분점수)
5. **Update & Evaluate** — 스킬 문서 갱신 후 평가. epoch 경계에서 **slow/meta 업데이트**로 안정화

### DL 비유 매핑 (문서 `dl-analogy.md`, 원본 확인)
> *"natural-language 프롬프트 최적화는 신경망 훈련과 동일한 구조를 따른다."*

| SkillOpt 개념 | 신경망 훈련 대응 |
|---|---|
| **Skill document** | Model weights (최적화 대상) |
| **Rollout** | Forward pass |
| **Reflect** | Backpropagation |
| **Edit patches** | Gradients |
| **Skill update** | SGD step |
| `learning_rate` | 스텝당 **최대 편집 수** |
| `lr_scheduler` | decay schedule (cosine/linear/constant) |
| Gate patience | Early stopping |
| Slow update | Momentum |
| Meta skill | Meta-learning (epoch 간 옵티마이저 메모리) |
| `batch_size` | 롤아웃당 샘플 과제 수 |
| Selection split | Validation set (채택 게이트) |

**튜닝 경험칙(문서):** `Cosine schedule > constant`, `Moderate LR(4~16) > 매우 높/낮음`. batch·epoch 키우기는 전통 DL과 달리 **수확 체감**.

**기본 설정:** 4 epochs / batch 40 / reflection minibatch 8 / textual LR 4 + cosine decay / strict hard gating / slow-update·meta-skill on.

### `best_skill.md`의 형태 (문서 `skill-document.md`)
Markdown, H1/H2 계층 + 불릿 전략, 300~2,000 토큰. 표준 골격:
```markdown
# Task Strategy
## General Approach
- 복잡한 문제를 하위 단계로 분해 / 중간 결과 항상 검증
## Common Patterns
- X를 보면 Y를 시도 / Z는 오류를 부르니 회피
## Edge Cases
- 입력에 A가 있으면 ... 로 특수 처리 / B 주의 — C가 필요
## Output Format
- 답 앞에 추론을 항상 포함 / 숫자에 단위 표기
```
시드 옵션 3가지: **빈 스킬**(맨바닥 학습) / **시드 스킬**(`init_skill: path/to/initial_skill.md`, 도메인 지식 있으면 수렴 빠름) / **사전학습 스킬**(유사 벤치마크에서 전이).

---

## 3. 성능과 근거 *(저자·벤더 보고치 — 독립 검증 아님)*

- 6 benchmarks × 7 target models × 3 harnesses = **52개 (model, benchmark, harness) 셀에서 best 또는 tied-best**.
- **GPT-5.5 기준 무스킬 대비 평균 정확도 상승**: direct chat **+23.5**p, **Codex 에이전트 루프 +24.8**p, **Claude Code 내부 +19.1**p.
- **전이(transfer)**: 모델 규모·실행 하니스(Codex↔Claude Code)·인접 벤치마크에 재학습 없이 이식 가능(프로젝트 페이지에 cross-harness transfer 사례로 +31.8 언급).
- 내장 벤치마크: SearchQA(QA) · ALFWorld(embodied) · DocVQA(문서QA) · LiveMathematicianBench(수학) · SpreadsheetBench(코드생성) · OfficeQA(tool-augmented QA).

> ⚠️ 이 수치들은 README/논문/블로그발 **저자 주장**이다. 셀 정의·베이스라인·평가 프로토콜은 논문에서 확인 필요. 의사결정에는 "방향성 강한 신호" 정도로 취급 권장.

---

## 4. 아키텍처 — 접목의 뼈대는 "3계층 분리"

README는 *"target model, backend, harness는 고정한 채, 증거 수집·도구 사용·검증·출력 형식을 안내하는 절차가 진화한다"* 고 말한다. 접목을 이해하는 가장 깔끔한 틀은 **세 역할을 분리**하는 것이다:

| 역할 | 무엇 | 어디서 설정 | 당신 환경에서 |
|---|---|---|---|
| **Optimizer model** | 편집(gradient)을 제안 | `model.optimizer` / `--optimizer_model` | 강한 모델 권장(gpt-5.5, claude 등) |
| **Target model** | frozen, 과제를 실제로 수행 | `model.target` / `--target_model` | 배포에 쓸 바로 그 모델 |
| **Harness(=target backend)** | target이 도는 실행 환경 | env `TARGET_BACKEND` (+ `OPTIMIZER_BACKEND`) | `direct chat`(chat enum) 또는 **`codex_exec` / `claude_code_exec`** |

여기서 두 소스 파일이 다른 계층을 담당한다(혼동 주의):
- **`skillopt/model/claude_backend.py`** = **Claude를 "모델 백엔드"로**. Anthropic API를 직접 호출하지 않고 `claude` CLI를 `-p`로 호출(메시지→프롬프트 조립). 인증은 `claude` CLI 바이너리에 위임(`CLAUDE_CLI_BIN`), `ANTHROPIC_API_KEY` 직접 사용 안 함. 기본 배포명 `claude-sonnet-4-6`. → direct-chat target/optimizer로 Claude를 쓸 때의 경로.
- **`skillopt/model/codex_harness.py`** = 이름과 달리 **에이전트 하니스 계층**. `run_codex_exec` + `run_claude_code_exec` + 디스패처 `run_target_exec`를 모두 포함. target 과제를 **풀 에이전트 루프**(도구·샌드박스·파일 읽기)로 실행 → "+24.8 Codex / +19.1 Claude Code" 수치의 출처.

**Backend enum (소스 `backend_config.py` 확인):** optimizer = `openai_chat | claude_chat | qwen_chat | minimax_chat`; target = 여기에 **`codex_exec | claude_code_exec`** 추가(에이전트 하니스). 선택은 env **`OPTIMIZER_BACKEND` / `TARGET_BACKEND`**(기본 `openai_chat`). `TARGET_BACKEND ∈ {codex_exec, claude_code_exec}` 이면 "agentic" 모드(`is_agentic`). Azure는 별도 enum이 아니라 OpenAI 호환 provider로 `openai_chat`에서 env로 설정.
**Provider 환경변수:** `AZURE_OPENAI_ENDPOINT/_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `QWEN_API_BASE`. (※ WebFetch 1차 요약이 준 "azure_openai/qwen" backend명은 실제 enum과 달랐고, 위는 cloned 소스로 정정한 값.)

---

## 5. Codex · Claude Code 접목 메커니즘 *(cloned 소스 직접 대조 — High)*

SkillOpt가 실제로 두 도구를 **어떻게 구동하고 스킬을 주입하는지**를 `git clone --depth 1` 후 `codex_harness.py` 실제 바이트로 확인했다(아래 인용은 행번호까지 대조됨).

### 스킬 주입 (양쪽 공통)
작업 디렉터리 안에 스킬 파일을 써넣고, 프롬프트로 **"읽으라"** 고 지시한다:
```python
os.makedirs(os.path.join(work_dir, ".agents", "skills", "skillopt-target"), exist_ok=True)
skill_path = os.path.join(work_dir, ".agents", "skills", "skillopt-target", "SKILL.md")
# ... f.write(skill_md)
```
프롬프트 지시문(원본):
> *"Read `.agents/skills/skillopt-target/SKILL.md` before answering. ... do not call a Skill tool."*
> *"Read `.agents/skills/skillopt-target/SKILL.md` before writing code; do not call a Skill tool."*

**중요한 뉘앙스 (정정):** 경로는 Claude Code 네이티브 위치인 `.claude/skills/`가 **아니라** 크로스툴 규약 `.agents/skills/`다(`grep .claude` → **NOT FOUND**). 게다가 **일부러 "Skill tool을 호출하지 말고 파일을 직접 읽으라"** 고 강제한다 — 채점 결정성을 위해 **네이티브 스킬 자동탐색을 우회**하는 것. 즉 SkillOpt는 **`SKILL.md`라는 파일 규약은 차용하되 Claude Code의 스킬 디스커버리 시스템은 쓰지 않는다.**

### Claude Code 구동 (`run_claude_code_exec`)
```python
cmd = [
    str(config["path"]), "-p",
    "--output-format", "text",
    "--permission-mode", permission_mode or "bypassPermissions",
    "--add-dir", work_dir,
    "--tools", tools, "--allowedTools", tools,
]
cmd.extend(["--append-system-prompt", f"Profile: {config['profile']}"])
```
(SDK 모드면 구조화 JSON을 `ANSWER_SCHEMA`로 검증: `final_response`/`final_answer` 필드.)

### Codex 구동 (`run_codex_exec`)
```python
cmd = [
    str(config["path"]), "exec",
    "--skip-git-repo-check", "--color", "never",
    "-C", work_dir,
]
# 이어서 조건부: -p <profile>, -c model_reasoning_effort="...",
#   --full-auto, --sandbox <mode>, --output-last-message ... (882~898행 확인)
```
- 디스패처 `run_target_exec()`가 config의 target backend(`codex_exec` / `claude_code_exec`)로 분기.
- 산출 trace: `codex_raw.txt`, `codex_trace_summary.txt`, `claude_raw.txt` 등.
- 주요 함수: `render_skill_md`, `prepare_workspace`, `parse_codex_raw`, `run_claude_code_exec`, `run_codex_exec`, `run_target_exec`.

---

## 6. 당신의 환경에 접목하는 3가지 실전 경로

> 전제: 당신은 이미 Codex(`codex:rescue` / codex CLI runtime)와 Claude Code를 에이전트 하니스로 쓰고 있고, 다수의 `SKILL.md`를 전역(`~/.claude/skills/`)에 유지한다. **당신의 기존 `SKILL.md`들이 곧 SkillOpt의 학습 대상 아티팩트**라는 점이 핵심 접점이다. (이 저장소엔 로컬 `.claude/skills/`·`.agents/`가 없음 — 전역 라이브러리 기준.)

### 경로 A — "소비자"로 접목 (가장 빠름, 저비용)
이미 학습된 스킬(`ckpt/`의 사전학습 스킬 또는 당신이 학습한 `best_skill.md`)을 **그대로 배포**.
- **Claude Code**: `best_skill.md`를 `~/.claude/skills/<name>/SKILL.md`로 배치 → 네이티브 디스커버리로 자동 노출. *주의:* SkillOpt 산출물은 채점용 평문 전략이라 frontmatter(name/description)가 없을 수 있으니, **네이티브 스킬로 쓰려면 frontmatter를 덧붙여 매핑**하라(SkillOpt는 `.agents/` + 직접읽기를 쓰지 `.claude/` 디스커버리를 안 쓰므로 그대로 복사하면 안 잡힐 수 있음).
- **Codex**: 내용을 `AGENTS.md`에 병합하거나, 호출 시 `--append-system-prompt`/프로필로 주입(SkillOpt도 Codex에선 파일 읽기 지시 방식 사용).
- 비용: 추론 오버헤드 0. 위험: 낮음. 효과: 도메인이 맞으면 즉시.

### 경로 B — "최적화 대상"으로 접목 (핵심 가치)
당신의 실제 과제로 **스킬을 학습**시키고 Codex/Claude Code 루프에서 검증.
1. **벤치마크 env 작성**: `skillopt/envs/<your_task>/`에 `dataloader.py`(train/val/test split JSON) + `rollout.py` + `initial.md`. `_template/` 참고.
2. **하니스 지정**: target backend를 `codex_exec` 또는 `claude_code_exec`로 → 당신이 배포할 바로 그 에이전트 루프에서 채점.
3. **모델 분리**: `--optimizer_model`(강한 모델) ≠ `--target_model`(배포 대상). Claude를 target/optimizer로 쓰려면 `pip install skillopt[claude]` + `claude` CLI 인증.
4. **실행**:
   ```bash
   python scripts/train.py --config configs/<your_task>/default.yaml \
       --optimizer_model <strong> --target_model <deploy> \
       --num_epochs 4 --batch_size 40 --workers <N>
   # 옵션 오버라이드 예: optimizer.learning_rate=16
   ```
5. **산출**: `best_skill.md`(+ `skills/skill_vXXXX.md` 스냅샷) → 경로 A로 배포.
- 비용: 훈련 API 비용 **선불·상당**. 위험: 채점 함수 품질에 좌우. 효과: 측정 가능한 단조 개선.

### 경로 C — 파이프라인 통합 (당신 워크플로우와 결합)
- **데이터 소스**: `codex:rescue` 등 기존 실행 로그·trace를 train/val 과제로 수확 → SkillOpt env의 입력으로.
- **CI/주기 학습**: 새 과제가 쌓이면 주기적으로 재학습, 검증 통과한 `best_skill.md`만 스킬 라이브러리에 승격(이전 세션의 goal/조건 기반 자동화와 결합 가능).
- **멀티-하니스 전이**: Codex에서 학습 → Claude Code로 전이 테스트(논문이 주장하는 cross-harness transfer 검증).

---

## 7. 비용 · 전제조건 · 함정

| 구분 | 내용 |
|---|---|
| **선불 비용** | 훈련 중 API 호출 비용이 **크고 선불**(롤아웃 × 배치 × epoch × optimizer 편집). 배포는 무료. |
| **필수 전제** | (1) 신뢰할 만한 **채점/검증 함수**, (2) train/val/test **split 데이터**, (3) 강한 **optimizer model**. 셋 다 없으면 효과 제한적. |
| **`.agents` vs `.claude` 함정** | 산출 스킬을 Claude Code 네이티브 스킬로 쓰려면 `.claude/skills/<n>/SKILL.md` + frontmatter로 **수동 매핑** 필요. 그대로 복사 ≠ 자동 인식. |
| **eval vs deploy 차이** | SkillOpt 채점은 "Skill tool 쓰지 말고 직접 읽기"로 결정성 확보. 실제 배포에선 네이티브 디스커버리/자동 트리거를 쓰므로 **동작 맥락이 다름** — 배포 후 재검증 권장. |
| **전이 한계** | 인접 도메인엔 전이 잘 되나 **근본적으로 다른 도메인 간 전이는 제한적**(블로그). |
| **성숙도** | **v0.1.0, 초기 연구 아티팩트**. API·구조 변동 가능. 성능 수치는 저자 보고치. |
| **하니스 의존** | `codex` / `claude` CLI 바이너리 존재·인증·플래그 호환에 의존(예: `--append-system-prompt`, `bypassPermissions`). CLI 버전 드리프트 주의. |

---

## Key Takeaways

1. **새로 만들 것 없음 — 연결만 하면 된다.** SkillOpt는 Codex·Claude Code를 이미 1급 하니스로 구동(`run_codex_exec`/`run_claude_code_exec`)하며 스킬을 `.agents/skills/skillopt-target/SKILL.md`로 주입한다(원본 확인).
2. **가장 큰 가치는 경로 B** — 당신의 실제 과제로 기존 `SKILL.md`를 *학습*시켜 측정 가능한 개선을 얻는 것. 당신의 스킬 라이브러리가 곧 학습 대상이다.
3. **3계층(optimizer / target / harness)을 분리해서 사고하라.** Codex와 Claude Code가 꽂히는 곳은 "harness=target backend"다.
4. **`.agents/` ↔ `.claude/` 매핑 + frontmatter**가 배포 시 실질 함정. 채점 모드와 배포 모드의 동작 차이를 배포 후 재검증.
5. **시작은 작게**: 명확한 성공 기준이 있는 과제 1개 + 작은 epoch로 PoC → 비용/효과 측정 후 확대(블로그 권고).

---

## Sources

1. [microsoft/SkillOpt (GitHub)](https://github.com/microsoft/SkillOpt) — 저장소·README·구조·릴리스.
2. [README.md (raw)](https://raw.githubusercontent.com/microsoft/SkillOpt/main/README.md) — 개념·설치·성능 주장.
3. [skillopt/model/codex_harness.py (raw)](https://raw.githubusercontent.com/microsoft/SkillOpt/main/skillopt/model/codex_harness.py) — **하니스 구동·스킬 주입 메커니즘(grep 확인)**.
4. [skillopt/model/claude_backend.py (raw)](https://raw.githubusercontent.com/microsoft/SkillOpt/main/skillopt/model/claude_backend.py) — Claude를 모델 백엔드로 구동.
5. [docs/guide/dl-analogy.md (raw)](https://raw.githubusercontent.com/microsoft/SkillOpt/main/docs/guide/dl-analogy.md) — DL 비유 매핑.
6. [docs/guide/skill-document.md (raw)](https://raw.githubusercontent.com/microsoft/SkillOpt/main/docs/guide/skill-document.md) — 스킬 문서 형식·시드.
7. [docs/guide/configuration.md (raw)](https://raw.githubusercontent.com/microsoft/SkillOpt/main/docs/guide/configuration.md) — optimizer/target/backend 설정.
8. [SkillOpt 프로젝트 페이지](https://microsoft.github.io/SkillOpt/) — 하니스 개념·전이.
9. [arXiv:2605.23904](https://arxiv.org/abs/2605.23904) · [Flowtivity 해설 블로그](https://flowtivity.ai/blog/microsoft-skillopt-train-ai-agent-skills/) — 방법·실무 관점.

## Methodology
서브질문 5개(① 무엇/방법 ② Codex·Claude 하니스 통합 ③ 산출물 배포·`SKILL.md` 관계 ④ 비용·전제 ⑤ 당신 환경 접목)로 분해. WebSearch 1회 + WebFetch 9회(README·문서·프로젝트페이지·arXiv·블로그). **그 뒤 코드 레벨 주장은 WebFetch 요약으로 끝내지 않고, `git clone --depth 1`로 실제 저장소를 받아 로컬 `grep`으로 바이트 대조**했다(스킬 경로, `.agents` vs `.claude`, CLI 플래그 배열, backend enum, 명령어 배열 행번호까지). 성능 수치는 저자·벤더 보고치로 별도 라벨링.

> 검증 메모: WebFetch는 페이지를 소형 모델로 요약하므로 "정확 인용"도 재구성일 수 있다(예: backend enum을 `azure_openai/qwen`으로 근사). 그래서 코드 토큰은 cloned 소스로 재확인했고, 그 결과 §5의 인용·경로·플래그는 실제 바이트와 일치, §4 backend enum 1건은 정정했다.

## 알려진 한계 (이 리포트의)
- 성능 수치는 독립 재현하지 않음(논문 표 미정독) — Medium 신뢰도.
- §5 코드 인용은 clone 시점(2026-06-06) `main` 기준. 이후 커밋으로 드리프트 가능하니 정밀 통합 직전 재pull 권장.
- 당신의 전역 스킬 라이브러리 개별 항목과의 매핑은 미수행(env 작성 시 과제별로 결정 필요).
