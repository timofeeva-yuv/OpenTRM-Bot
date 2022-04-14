import telebot
import telegram
import time
import requests
import logging
import os

with open("bot-token.txt", "r") as f:
    token = f.read()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_chat_action(message.from_user.id, action=telegram.ChatAction.TYPING)
    time.sleep(1)
    bot.send_message(message.from_user.id, "Добрый день! Присылайте документы на обработку")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_chat_action(message.from_user.id, action=telegram.ChatAction.TYPING)
    time.sleep(1)
    # TODO написать инструкцию по работе с ботом    

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.reply_to(message, "Текст получен. Начинаем обработку")
    # TODO текст пересылается классификатору
    bot.send_message(message.from_user.id, "Результаты обработки \nКоличество страниц: \nТип распознанного документа: \nИзвлеченная информация: ")

# Получаем документ/картинку/фото файлом
@bot.message_handler(content_types=["document"])
def handle_document(message):
    bot.reply_to(message, "Получили Ваш документ. Начинаем обработку")
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = "./bot/copy_" + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file) # загружает в исходном качестве
    # TODO передача классификатору и получение результатов
    bot.send_message(message.from_user.id, "Результаты обработки \nКоличество страниц: \nТип распознанного документа: \nИзвлеченная информация: ")
    bot.send_chat_action(message.from_user.id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
    bot.send_document(message.chat.id, open(src,"rb"))
    os.remove(src) # отправили документ, можем удалить, чтобы не захламлять память    
    
# !!! Если боту присылают фото/картинку в сжатом (compressed) виде (не файлом),
# то на локалку оно сохраняется в очень плохом качестве !!!
@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.reply_to(message, "Получили Ваш скан. Начинаем обработку")
    
    file_name = "photo"
    file_info = bot.get_file(message.photo[0].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("./bot/" + file_name, 'wb') as new_file: # СОХРАНЯЕТ В УЖАСНОМ КАЧЕСТВЕ!!
        new_file.write(downloaded_file)
        
    bot.send_message(message.from_user.id, "Результаты обработки \nКоличество страниц: \nТип распознанного документа: \nИзвлеченная информация: ")
    bot.send_chat_action(message.from_user.id, action=telegram.ChatAction.UPLOAD_PHOTO)
    bot.send_photo(message.chat.id, open("./bot/example.png","rb"))
    # TODO удалить загруженные файлы
    
def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()