# ADR 0001: CI and Code Coverage Integration


`line
`
\**\`Japanese Summary`**
CIPa lino KGG, Codecov 業イランタート

`line`
\**`korean Summary`**
CI 장사 공안지삭, Codecov.하지원묰매 면 오인구 거수 마스트 햽구로 구 고기

`line
`
---

## Status
Accepted

### Context
We needed a transparent and robust quality assurance pipeline. Without test automation and coverage visibility, long-term maintainability and team collaboration would be compromised.

### Decision
- Adopt GitHub Actions for CI (*ci.yml*)
- Run *pytest* for unit test automation
- Upload coverage reports via Codecov GitHub Action
- Add Codecov badge to `backend/README.md`
- Skip `CODECOV_TOKEN` as public repositories work token-free
- Initialize coverage tracking with a baseline PR (empty commit)

### Consequences
- Enforces test-driven development from the CI level
- Establishes visibility into coverage per branch
- Provides groundwork for future minimum threshold enforcement
- Improves onboarding and contribution clarity
