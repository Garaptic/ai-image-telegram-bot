import os
import telebot
from config import API_TOKEN
from logic import ImgAPI

bot = telebot.TeleBot(API_TOKEN)
api = ImgAPI()


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    description = (
        "**Привет! Я бот-генератор изображений.**\n\n"
        "Я умею создавать уникальные картинки по вашему текстовому описанию (промпту).\n\n"
        "**Как пользоваться:**\n"
        "Просто отправь мне текст с описанием того, что ты хочешь увидеть "
        "(лучше писать на английском языке для более точного результата).\n\n"
        "*Пример:* `a cute cat sitting on a neon roof in a cyberpunk city`"
    )
    bot.reply_to(message, description, parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def generate_and_send(message):
    bot.send_chat_action(message.chat.id, "upload_photo")

    status_msg = bot.reply_to(message, "Генерирую картинку, подождите...")

    file_path = api.generate_image(message.text)

    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as photo:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"**Запрос:** {message.text}",
                parse_mode="Markdown",
            )

        bot.delete_message(
            chat_id=message.chat.id, message_id=status_msg.message_id
        )

        os.remove(file_path)
        print(f"Файл {file_path} успешно удален с диска.")

    else:
        bot.edit_message_text(
            "Не удалось сгенерировать изображение. Попробуй еще раз.",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
        )


if __name__ == "__main__":
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()