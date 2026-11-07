# 워드프레스 연결 정보

- 사이트: https://bnote.kr (카페24 매니지드 워드프레스, Uncode Child 테마)
- Jetpack 연결 사이트 ID: 258503824
- 연결 경로: Jetpack → WordPress.com 커넥터. 카페24 봇 차단(cupid.js)은 이 경로에 영향 없음. 명령줄 직접 호출은 차단됨.
- 시간대: Asia/Seoul · 날짜 형식: Y년 n월 j일 · 시간: H:i

## 카테고리 ID

| 면 | ID | 코너 | ID | slug |
|---|---|---|---|---|
| 1면 | 6 | 01 오늘의 부고 | 15 | obituary |
| 1면 | 6 | 19 같은 씨앗, 다섯 개의 시선 | 16 | special |
| 1면 | 6 | 22 사물의 사설 | 17 | editorial |
| 1면 | 6 | 20 정정란 | 18 | corrections |
| 사회면 | 7 | 04 산문시 | 19 | prose-poem |
| 사회면 | 7 | 09 공고란 | 20 | notice |
| 사회면 | 7 | 10 분실물란 | 21 | lost-and-found |
| 세계면 | 8 | 03 세 줄 뉴스 | 22 | three-lines |
| 경제면 | 9 | 11 시세면 | 23 | prices |
| 경제면 | 9 | 07 광고란 | 24 | ads |
| 과학면 | 10 | 05 숫자 하나의 에세이 | 25 | one-number |
| 과학면 | 10 | 06 일기예보 | 26 | forecast |
| 과학면 | 10 | 24 오늘의 비역사 | 27 | non-history |
| 문화면 | 11 | 12 낱말란 | 28 | words |
| 문화면 | 11 | 15 N년 전 오늘 | 29 | years-ago |
| 문화면 | 11 | 13 세시기 | 30 | seasons |
| 문화면 | 11 | 14 사진 없는 사진면 | 31 | no-photo |
| 문화면 | 11 | 21 십자말풀이 | 32 | crossword |
| 문화면 | 11 | 23 연재소설 | 33 | serial |
| 생활면 | 12 | 02 사물의 편지 | 34 | letters |
| 생활면 | 12 | 16 이달의 운세 | 35 | horoscope |
| 생활면 | 12 | 17 편성표 | 36 | tv-guide |
| 인사면 | 13 | 18 인사란 | 37 | appointments |
| 편집장 | 14 | 08 편집장의 편지 | 38 | editor-letter |

글 하나에는 코너 ID 하나만 단다. 면은 상위 카테고리라 자동으로 묶인다.

## 사용자
- 현재 관리자 계정 1개(badum). 기자 계정 5개는 wp-admin에서 직접 추가(역할: 글쓴이).
  - 최극형 / 훈세김 / 린해박 / 남새진 / (다섯째 기자, 이름 미정)
  - 추가 후 ID를 이 파일에 적는다.

## 사용자 정의 필드 (seed, seed_url, editor_note, editor_request)
- Jetpack 사이트는 REST API에 등록된 메타만 저장한다. 자식 테마 functions.php에 등록 코드가 필요하다(`snippets/register-meta.php` 참조). 등록 전까지는 씨앗 표기를 본문 마지막 블록으로 넣는다.

## 주의
- "Disable XML-RPC-API" 플러그인은 비활성 상태를 유지한다. 활성화하면 Jetpack 연결이 끊긴다.
- WP Fastest Cache가 켜져 있어 발행 직후 공개 화면 반영이 몇 분 늦을 수 있다.
- 설정의 "누구나 가입 가능"이 켜져 있다. wp-admin 설정 → 일반에서 끄는 것을 권장(스팸 가입 방지).
