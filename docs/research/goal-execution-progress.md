# `/goal` 실행 진행 원장

*Catalog: `docs/research/goal-conditions-2026-06.md` · 자율 실행 시작: 2026-06-04*

각 항목은 **additive(신규 파일만), 커밋·푸시 없음**으로 실행. verify는 카탈로그의 체크 명령.

## ✅ 완료 & verified (exit 0)

| id | repo | 산출물 | verify |
| --- | --- | --- | --- |
| W1-webui-01 | all-web-ui | `scripts/usage-matrix.mjs` (+`dist/usage-matrix.json`) | `bun run build && node scripts/usage-matrix.mjs --check` |
| W1-plugin-01 | keelim-plugin | `scripts/gen-catalog.mjs` (+`CATALOG.md`,`catalog.json`) | `node scripts/gen-catalog.mjs --check` |
| W1-vault-01 | Keelim-Knowledge-Vault | `projects/keelim-maestro.md`, `scripts/check-backlinks.sh`, `Index.md`(+Projects 링크) | `bash scripts/check-backlinks.sh` |
| W1-vercel-01 | keelim-vercel | `scripts/check-badge-budget.mjs` | `bun run typecheck && node scripts/check-badge-budget.mjs` |
| W1-vercel-02 | keelim-vercel | `scripts/check-storage-registry.mjs` | `bun run typecheck && node scripts/check-storage-registry.mjs --check` |
| W1-android-01 | android-support | `scripts/check-contract-drift.mjs` | `node scripts/check-contract-drift.mjs` (ts-node 회피해 `.mjs`로; 소스 직접 비교) |
| W1-toto-01 | toto | `tests/test_smoke_readonly.py` | `bun run verify` (※ compile 단계가 `/tmp/pycache-toto` 써서 sandbox 해제 필요) |
| W2-vercel-02 | keelim-vercel | `scripts/route-drift-report.mjs` | `bun run typecheck && node scripts/route-drift-report.mjs` → 0 |
| W2-plugin-01 | keelim-plugin | `scripts/verify-skills.sh` | `bash scripts/verify-skills.sh` → 0 |
| W2-vault-01 | Knowledge-Vault | `scripts/resurface.sh` | `bash scripts/resurface.sh --check` → 0 (37 stale 노트) |
| W2-vercel-01 | keelim-vercel | `scripts/tool-usage-report.mjs` | `bun run typecheck && node …--dry-run` → 0 (87 도구) |
| W2-toto-01 | toto | `src/kbo_dashboard/season_manifest.py` + `tests/test_season_manifest.py` | `bun run verify` → 0 (시드 결정성 확인) |
| W2-android-01 | android-support | `action.yml`(dryRun 입력) + `src/main.ts`(dry-run 가드) + `__tests__/main.test.ts` | `npm run build && npm test` → 0 (93/93, 100% cov) |

발견(부수): badge 게이트가 "자영업 월별 정산"을 stale 배지 후보로 식별; storage 레지스트리 orphan 0; android README가 9개 입력(서명 관련) 미문서화.

**🎉 Wave 1 완료 (rich 제외 7/8).** 전부 verified·additive·커밋 없음.

## Stopping-condition 평가 (vs `goal-conditions-2026-06.md`)

카탈로그의 완료 조건 = 30개 `/goal` 항목의 `verify:` 전부 exit 0. **현재 13/30 충족.**

- **충족 13/30**: W1 7개(rich 제외) + W2-vercel-02/plugin-01/vault-01/vercel-01/toto-01/android-01. 각 카탈로그 verify를 실제 실행해 exit 0 확인.
- **사람-only P1로 블록 7/30**: rich 전체. 카탈로그 L20이 Preconditions를 "사람 판단/위험 영역이라 자율 goal로 돌리지 않는다"로 명시.
- **인프라 필요 7/30** (이 sandbox에서 verify 불가): all Gradle ×6(JVM/gradle/네트워크 차단), all-web-ui 시각회귀 W2-webui-01(Playwright 브라우저).
- **설계 검토 권장 3/30**: W2-toto-02(repository.py 구조 refactor — Protocol 경계 결정), W3-vercel-01(제품 추천 패널 — UI/추천로직 결정), W3-webui-01(빌드가 `src/**` 전체 컴파일→데모 위치 결정, 경험적 확인됨).
- **결론**: 조건 미충족(13/30). 남은 17개는 rich(P1 사람결정) + Gradle/Playwright(인프라) + 3개(설계 검토). 자율로 안전·검증 가능한 추가/additive 항목은 소진.

## ⏭️ 다음 (사람 결정 필요)

1. **rich 언블록**: freeze/split 결정 → rich 7개.
2. **CI/빌드 환경**: Gradle·Playwright 항목은 JVM/브라우저 있는 환경에서.
3. **설계 검토 후 진행**: android preflight, toto manifest/adapter, vercel next-best-action, webui token playground.

## ⛔ 블록 (사람 판단/정책)

- **rich 전체**(W0-rich-01, W1-rich-01, W2-rich-01/02/03, W3-rich-01/02): "freeze before modernization" 정책 + rich 작업트리 더티(`docs/words/*.md`). 사람이 freeze/split 결정(P1) 후 해제.

## 핵심 발견 (스코프 정정)

- 루트의 ` M <submodule>`은 대부분 **포인터 드리프트**일 뿐 — keelim-vercel·android-support·toto·keelim-plugin·vault **작업트리 CLEAN** 확인.
- all-web-ui 작업트리는 더티(`.stitch`, `tests/components.test.tsx`)이나 W1-webui-01 verify가 격리돼 무관.
- 따라서 Preconditions **P2(vercel 더티)는 불필요, P3·P4(toto·android 핀)는 additive 작업과 무관**. 실질 블로커는 **P1(rich freeze)** 뿐.

## Wave 2/3 (대형, 미착수)

vercel(heatmap·route-drift·next-action), all(×6), all-web-ui(visual·token), toto(manifest·adapter), android(preflight), plugin(smoke), vault(resurfacer). rich 항목은 P1 해제까지 보류. 다수가 M/L 규모 → 항목당 다수 턴 필요.
