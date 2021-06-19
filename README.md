# Discord_Translator_2room [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Charahiro-tan/Discord_Translator_2room) [![CodeQL](https://github.com/Charahiro-tan/Discord_Translator_2room/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Charahiro-tan/Discord_Translator_2room/actions/workflows/codeql-analysis.yml) [![OSSAR](https://github.com/Charahiro-tan/Discord_Translator_2room/actions/workflows/ossar-analysis.yml/badge.svg)](https://github.com/Charahiro-tan/Discord_Translator_2room/actions/workflows/ossar-analysis.yml)
Discord translator that posts with webhooks that can be deployed on Heroku  
Herokuの無料枠にデプロイできるDiscordの翻訳Botです。  
詳しい使い方はDiscordサーバーに書いてあります。  
  
Translate into each other's language using two channels  
言語を指定した2つのチャンネルを使用してお互いの言語に翻訳します。  
エモートを含んだ文字の翻訳は非対応ですが、エモートのみの投稿はそのまま相手のチャンネルに流します。  

![image](img/2room.gif)  

## Environment variable(環境変数)
|Required(必須)||
|---|---|
|DISCORD_TOKEN|Discord bot Token|
|CHANNEL1_ID|1st channel ID(integer)|
|CHANNEL1_URL|Webhook URL for the 1st channel|
|CHANNEL1_LANG|Language of the 1st channel(e.g. en)|
|CHANNEL2_ID|2nd channel ID|
|CHANNEL2_URL|Webhook URL for the 2nd channel|
|CHANNEL2_LANG|Language of the 2nd channel(e.g. ja)|
  
|Options(オプション)||
|---|---|
|IGNORE_ID|Author IDs to ignore (":" delimited, integers)|
|GAS_URL|Look at my DiscordServer|  
  
## Other
- [__Discord Server__](https://discord.gg/bhpBKCJV8R)
- [Twitter](https://twitter.com/__Charahiro)
