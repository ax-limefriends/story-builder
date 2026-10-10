# 스토리 빌더

브랜드스크립트 → 펀딩 스토리 블록 → 점검 → 이미지·텍스트 순서 내보내기. 첫 형식은 와디즈 스토리. 전자책 「살아있는 회사 소개서」(작가×개발자) 와디즈 삼무서점 펀딩에서 처음 사용하고, 이후 홈페이지 메인 등 출력 형식을 늘려 범용 도구로 키운다.

## 파일

- `docs/index.html` 도구 전체 (단일 파일, 인라인 CSS·JS). localStorage 키 `wsb_v1`, 작업 파일 `v:1`.
- `docs/og.png` 1200×630 링크 미리보기 (PIL + `C:/Windows/Fonts/malgunbd.ttf`).
- 기획 문서와 결정 기록: `C:\Users\user\Desktop\프로젝트 정리\와디즈_삼무서점기획펀딩\` (README.md, 03_스토리빌더_MVP)

## 원칙

- 와디즈 화면 수치(스토리 폭 740/390, 접힘선 5,490px 등)는 `FORMATS`에만 두고 `observed` 기준일을 적는다. 바뀌면 거기만 고친다.
- 이름·화면에 '와디즈'를 제품명처럼 쓰지 않는다(형식 이름으로만).
- 예시 데이터의 저자 이력·가격·후기는 "(예시)", "(확인 필요)"로 표시한다. 없는 숫자·후기를 지어내지 않는다.
- 실제로 쓰기 전에 옵션을 미리 늘리지 않는다. 형식 하나 = 설정 한 묶음 + 점검 규칙.

## 배포

- `git push origin main` 한 번으로 `mc-jeon/story-builder`와 `ax-limefriends/story-builder`에 함께 올라감(origin에 push URL 2개). ax-limefriends 인증은 `.git/ax-cred.sh`.
- GitHub Pages: main 브랜치 `docs/` 폴더.
- Cloudflare Workers `story-builder`: 대시보드에서 mc-jeon 저장소 연결 필요(아직 안 함).
- gh CLI 경로: `C:\Program Files\GitHub CLI\gh.exe`
