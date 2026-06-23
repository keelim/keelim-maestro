# Dependencies Codemap

<!-- Generated: 2026-06-23 -->

## Bun Workspace Catalog

Pinned in root `package.json` `catalog:` field. Used by `rich/web` for `catalog:` dependency references.

| Package | Pinned version |
| --- | --- |
| `@radix-ui/react-accordion` | 1.2.12 |
| `@radix-ui/react-alert-dialog` | 1.1.15 |
| `@radix-ui/react-avatar` | 1.1.11 |
| `@radix-ui/react-checkbox` | 1.3.3 |
| `@radix-ui/react-dialog` | 1.1.15 |
| `@radix-ui/react-dropdown-menu` | 2.1.16 |
| `@radix-ui/react-hover-card` | 1.1.15 |
| `@radix-ui/react-label` | 2.1.8 |
| `@radix-ui/react-popover` | 1.1.15 |
| `@radix-ui/react-progress` | 1.1.8 |
| `@radix-ui/react-radio-group` | 1.3.8 |
| `@radix-ui/react-scroll-area` | 1.2.10 |
| `@radix-ui/react-select` | 2.2.6 |
| `@radix-ui/react-slider` | 1.3.6 |
| `@radix-ui/react-slot` | 1.2.4 |
| `@radix-ui/react-tabs` | 1.1.13 |
| `@radix-ui/react-toast` | 1.2.15 |
| `@radix-ui/react-tooltip` | 1.2.8 |
| `@tailwindcss/postcss` | 4.2.2 |
| `@testing-library/jest-dom` | 6.9.1 |
| `@testing-library/react` | 16.3.2 |
| `@testing-library/user-event` | 14.6.1 |
| `@types/react` | 19.2.14 |
| `@types/react-dom` | 19.2.3 |
| `class-variance-authority` | 0.7.1 |
| `clsx` | 2.1.1 |
| `date-fns` | 4.1.0 |
| `jsdom` | 26.1.0 |
| `lucide-react` | 0.562.0 |
| `next` | 16.2.4 |
| `react` | 19.2.5 |
| `react-day-picker` | 9.13.2 |
| `react-dom` | 19.2.5 |
| `tailwind-merge` | 3.4.1 |
| `tailwindcss` | 4.2.2 |
| `typescript` | 5.9.3 |
| `vitest` | 2.1.1 |

## Python uv Constraint Dependencies

Pinned in root `pyproject.toml` `tool.uv.constraint-dependencies`. Enforced across
`toto` and `rich` workspace members.

| Package | Constraint range |
| --- | --- |
| `anyio` | >=4.13.0,<5.0.0 |
| `certifi` | >=2026.4.22 |
| `charset-normalizer` | >=3.4.7,<4.0.0 |
| `click` | >=8.3.3,<9.0.0 |
| `h11` | >=0.16.0,<1.0.0 |
| `idna` | >=3.14,<4.0.0 |
| `iniconfig` | >=2.3.0,<3.0.0 |
| `narwhals` | >=2.21.0,<3.0.0 |
| `numpy` | >=2.4.4,<3.0.0 |
| `packaging` | >=26.2,<27.0.0 |
| `pandas` | >=3.0.3,<4.0.0 |
| `pillow` | >=12.2.0,<13.0.0 |
| `pluggy` | >=1.6.0,<2.0.0 |
| `pygments` | >=2.20.0,<3.0.0 |
| `pytest` | >=9.0.3,<10.0 |
| `python-dateutil` | >=2.9.0.post0,<3.0.0 |
| `python-multipart` | >=0.0.28,<0.1.0 |
| `requests` | >=2.34.0,<3.0.0 |
| `six` | >=1.17.0,<2.0.0 |
| `starlette` | >=1.0.0,<2.0.0 |
| `typing-extensions` | >=4.15.0,<5.0.0 |
| `urllib3` | >=2.7.0,<3.0.0 |
| `uvicorn` | >=0.46.0,<1.0.0 |
| `websockets` | >=15.0.1,<16.0.0 |

## Dependency Verification

```bash
uv run python scripts/verify-python-dependency-constraints.py  # Python constraint check
uv lock --check                                                  # uv lock integrity
bun run typecheck:web                                            # Frontend type safety
```
