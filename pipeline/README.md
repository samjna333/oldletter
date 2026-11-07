# 파이프라인

씨앗 → 기자(클로드) 초고 2편 → 자동 검사 → 워드프레스 검토 대기함.

## 흐름
1. `seeds/inbox.json` 에 씨앗을 넣는다 (코너 번호, 씨앗 한 줄, 출처).
2. `python -m pipeline.run --inbox seeds/inbox.json`
3. 기자가 코너 설계서의 지시문대로 초고 2편을 쓴다. 강령·기자 설정·코너 설계서가 시스템 프롬프트(캐시됨).
4. `pipeline/lint.py` 가 금지 표현·개인정보·분량을 검사한다. 걸리면 글 머리에 표시만 하고 투입은 한다(판단은 편집장).
5. 초고 2편이 한 글에 "초고 가 / 초고 나"로 들어가 검토 대기 상태가 된다. 편집장이 한 편을 고르고 고쳐 발행한다.

## 필요한 비밀값 (GitHub Secrets 또는 환경 변수)
- `ANTHROPIC_API_KEY` — console.anthropic.com 에서 발급
- `WP_URL` — https://bnote.kr
- `WP_USER` — 워드프레스 사용자명 (글쓴이 권한 이상)
- `WP_APP_PASSWORD` — 사용자 → 프로필 → 응용 프로그램 비밀번호에서 발급. 카페24 스팸 실드가 켜져 있으면 이 경로가 막히므로 wp-json 예외 또는 실드 해제가 필요하다.

## 재작성
편집장이 글의 `editor_request` 필드(또는 씨앗 항목의 `editor_request`)에 한 줄을 쓰면 같은 기자가 다시 쓴다.
`python -m pipeline.run --corner 01 --seed "..." --url "..." --request "사인을 잔돈으로"`

## 비용 감각
호출 한 번(초고 2편)에 입력 약 6~9천 토큰(대부분 캐시), 출력 1~3천 토큰. Claude Opus 5.5 기준 한 편 묶음에 수십 원 단위.
