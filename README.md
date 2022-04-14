# OpenTRM-Bot

Поместите токен бота в файл [bot-token.txt](./bot-token.txt) (телеграм-боты создаются через спец. бота BotFather)  
  
Проблемы:  
1) **В Телеграме есть ограничения на размер загружаемых и выгружаемых файлов!** Возможные решения:  
(1) архивация; (2) установка Local API Server ([читать подробнее](https://core.telegram.org/bots/api) в разделе *Using a Local Bot API Server*  
2) Если присылается фото/картинка в сжатом формате (не файлом), то на локалку оно сохраняется в ужасном качестве. Возможное решение - запретить пользователям присылать фото/картинку боту в сжатом формате; разрешить присылать только файлами (не compressed)