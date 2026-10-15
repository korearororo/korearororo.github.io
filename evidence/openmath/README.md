# OpenMath 검색 동작 재현

2026-10-15에 Node.js 24.19.0에서 실행했습니다. Node.js 24 이상에서 별도 패키지 설치 없이 실행할 수 있습니다.

```sh
node compare.mjs result.json
```

- `rag-client.ts`: OpenMath PR #8의 병합 커밋 `3eb62c8f5b60bb19795fb93034d15b3875d60c6f`에서 그대로 가져온 실행 코드입니다. 타입 전용 import는 Node의 TypeScript 타입 제거 기능으로 지워집니다.
- `corpus.jsonl`: 이후 main 커밋 `62f2a41edcba83a9f53ec6add56697ca9911ab3a`에 공개된 `packages/agent/data/corpus/math-sample-unified-v1.jsonl`의 seed 7건입니다. AI Hub 전체 코퍼스가 아닙니다. 소스의 `source_label_type=seed`를 유지했습니다.
- `compare.mjs`: 이번 포트폴리오용 실행 스크립트입니다. 비교군은 단원·문제·해설의 키워드 포함 여부만 검사한 뒤 ID로 정렬합니다. 실제 클라이언트는 학년·성취기준 코드·유형·난이도로 필터링합니다. 두 방식의 기능 차이를 관찰하는 통제된 예시입니다.
- 정답 적합성은 문항 메타데이터가 요청 조건과 일치하는지로만 계산합니다. 교육적 관련성이나 의미 검색 품질의 사람 평가가 아닙니다.
- 실행 결과에 입력 질의·전체 반환 문항·코드와 데이터의 SHA-256을 저장합니다. 실행 시각은 재실행 때 달라집니다.

## 원본

[PR #8 코드](https://github.com/openmath2/OpenMath/blob/3eb62c8f5b60bb19795fb93034d15b3875d60c6f/packages/agent/src/tools/rag-client.ts)

[공개 seed](https://github.com/openmath2/OpenMath/blob/62f2a41edcba83a9f53ec6add56697ca9911ab3a/packages/agent/data/corpus/math-sample-unified-v1.jsonl)

원본 프로젝트의 코드·데이터 출처는 OpenMath이며, 포트폴리오의 재현 자료로 포함했습니다. 새로운 라이선스를 부여하지 않습니다.
