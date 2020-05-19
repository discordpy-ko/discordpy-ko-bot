# discordpy-ko-bot
## 문서 업데이트와 검색을 위한 봇  
discordpy-ko 봇 소스코드입니다.  

## 사용법:
1. `botsetup.json`에 내용을 채워주세요.
- stable_token: 봇 메인 토큰입니다. 필수입니다.
- canary_token: 봇 테스트 토큰입니다. 선택입니다.
- bot_name: 봇 이름입니다. 선택입니다.
- default_prefix: 프리픽스입니다. 필수입니다.
- chosen_token: 토큰 선택입니다. 그냥 `stable`로 놔두면 됩니다.
- sys_lang: ~~템플릿에 있던거 귀찮아서 안뺀건데~~ `ko`로 넣으면 됩니다.
- owner_id: 봇 소유자 ID입니다. 필수입니다.
- github_token: 깃헙 토큰입니다. 필수입니다.
- org_name: 깃헙 Organization 이름입니다. 필수입니다.
- loc_repository: 로케일 파일 리포지토리 이름입니다. 필수입니다.
- web_repository: 웹사이트 리포지토리 이름입니다. 필수입니다.
2. [이곳](https://github.com/Rapptz/discord.py)에서 이 리포지토리를 클론하고 **봇 폴더**에 **그대로** 넣으세요.
3. 봇 폴더에서 `convert_html.bat` 파일을 discord.py-master/docs 폴더로 옮겨주세요.
4. 이제 봇을 켜주세요.
