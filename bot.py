import telebot
from logic import ImgAPI
from config import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
api = ImgAPI()


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Напиши текстовый запрос (промпт), и я сгенерирую картинку",
    )


@bot.message_handler(content_types=["text"])
def generate_and_send(message):
    status_msg = bot.reply_to(message, "Генерирую картинку, подождите...")

    image_bytes = api.generate_image(message.text)

    if image_bytes:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=image_bytes,
            caption=f"**Запрос:** {message.text}",
            parse_mode="Markdown",
        )
        bot.delete_message(
            chat_id=message.chat.id, message_id=status_msg.message_id
        )
    else:
        bot.edit_message_text(
            "Не удалось сгенерировать изображение. Попробуй еще раз.",
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
        )


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()