# ADR 0001: CI and Code Coverage Integration

\"pn** japanese summary **
This CI paipeline is implemented using GitHub Actions and code coverage recording with Codecov.

\pn** kirean summary **
 CI 장사 공안지삭, Codecov.하지원묰매 면 오인구 거수 마스트 햽구로 구 고기

## Status
Accepted

## Context
We needed a transparent and robust quality assurance workflow. Without test automation and coverage visibility, long term maintainability and team collaboration would be compromised.

## Decision
- Implement GitHub Actions for CI (ci.yml)
- Run pytest for unit test automation
- Integrate Codecov for uploading coverage reports
- Add Codecov badge to backend/README.md
- Skip CODECOV_TOKEN since this is a public repository
- Create a baseline PR allowing empty commit to initialize coverage

## Consequences
- Enforces test-driven development from the CI level
- Establishes visibility into coverage per branch
- Provides groundwork for future minimum threshold enforcement
- Improves onboarding and contribution clarity
