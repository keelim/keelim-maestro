# quant

Last reviewed: 2026-05-03 KST

## Signals

- 원격이 없는 로컬 전용(no remote) 자율 저장소로, 전체 프로젝트 중 유실·재현 불가 위험이 가장 높다.
- `quant/myapi`(FastAPI + SQLAlchemy + Alembic)와 `quant/all_admin`(Django)이 한 저장소 안에 공존하는 이중 서버 구조다.
- Alembic 마이그레이션 체인 6단계, Django 마이그레이션 4단계가 로컬 DB에만 의존한다.
- dirty 상태로 장기 운영 중이라 uncommitted 변경이 언제 어디서 왔는지 추적하기 어렵다.
- 코드맵 기준 question/answer/user 도메인 API(FastAPI)와 Django notice/keyvalue 관리 앱이 별도 마이그레이션 파일로 움직인다.

## Open ideas

### 2026-05-03 - 로컬 상태 안전 보관 및 복구 가능성 게이트

Status: proposed

Why now: `quant`는 원격 없이 dirty 상태로 장기 운영 중이어서, 실수로 파일을 지우거나 마이그레이션 히스토리가 망가지면 복구 방법이 없다. 코드맵이 Alembic 6단계·Django 4단계 마이그레이션 체인을 명시하고 있으므로 이 히스토리의 재현 가능성을 확보하는 게 가장 먼저 해야 할 위험 감소다.

First slice: 현재 dirty 파일 목록과 uncommitted 변경 범위를 정리하고, Alembic 마이그레이션 체인과 Django 마이그레이션이 현재 로컬 DB 상태와 일치하는지 확인한다. 백업 지점(원격 생성 또는 git bundle)을 만들어 유실 위험을 줄인다.

### 2026-05-03 - FastAPI·Django 이중 서버 운영 표면 명세

Status: proposed

Why now: `quant/myapi`(FastAPI)와 `quant/all_admin`(Django)이 같은 로컬 저장소 안에 공존하는데, 각각 어떤 DB를 쓰고 어떻게 연결되는지, 독립 운영이 올바른 구조인지 코드맵 외에 문서가 없다. 원격 등록이나 서브모듈 추가를 논의할 때 이 구조에 대한 이해가 없으면 판단 비용이 커진다.

First slice: FastAPI와 Django가 각각 사용하는 DB 파일·설정·포트·마이그레이션 범위를 한 장의 표로 정리하고, 공유 데이터 모델 유무와 독립 운영 적합성을 명시한다.
