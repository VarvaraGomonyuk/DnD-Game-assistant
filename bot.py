from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
import random
import json


RACES = ["Дварф", "Эльф", "Полурослик", "Человек", "Драконорожденный", "Гном", "Полуэльф", "Полуорк", "Тифлинг"]
CLASSES = ["Варвар", "Бард", "Жрец", "Друид", "Воин", "Монах", "Паладин", "Следопыт", "Плут", "Чардей", "Колдун", "Волшебник"]


def start_bot(update, context):
    reply_keyboard = [["/create_character"], ["/character_info"], ["/class_info"], ["/roll_dice"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет, я бот для игры в Dungeons&Dragons! Поиграем?\n"
        "P.S. Если тебе нужна помощь нажми /help", reply_markup=markup)


def help(update, context):
    reply_keyboard = [["/create_character"], ["/character_info"], ["/class_info"], ["/roll_dice"], ["/back"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Приветствую тебя, игрок! Я бот для игры в Dungeons&Dragons!\n"
        "Я помогу тебе создать персонажа, просто нажми /create_character!\n"
        "Я могу показать информацию о расе персонжа, надо только нажать /character_info\n"
        "или я покажу тебе информацию о классе персонажа, просто нажми /class_info\n"
        "Кроме того, если ты боишься бросать кубик, я сделаю это за тебя! Надо только нажать /roll_dice!\n"
        "Приятной игры!", reply_markup=markup)


def back(update, context):
    reply_keyboard = [["/create_character"], ["/character_info"], ["/class_info"], ["/roll_dice"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет, я бот для игры в Dungeons&Dragons! Поиграем?\n"
        "P.S. Если тебе нужна помощь нажми /help", reply_markup=markup)


def roll_dice(update, context):
    reply_keyboard = [["/D4"], ["/D6"], ["/D8"], ["/D10"], ["/D12"], ["/D20"], ["/D100"], ["/back"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Бросай кубик!", reply_markup=markup)


def roll_d4(update, context):
    update.message.reply_text(f"{random.randrange(1, 4)}")


def roll_d6(update, context):
    update.message.reply_text(f"{random.randrange(1, 6)}")


def roll_d8(update, context):
    update.message.reply_text(f"{random.randrange(1, 8)}")


def roll_d10(update, context):
    update.message.reply_text(f"{random.randrange(1, 10)}")


def roll_d12(update, context):
    update.message.reply_text(f"{random.randrange(1, 12)}")


def roll_d20(update, context):
    update.message.reply_text(f"{random.randrange(1, 20)}")


def roll_d100(update, context):
    update.message.reply_text(f"{random.randrange(1, 10)}{random.randrange(1, 10)}")


def create_character(update, context):
    update.message.reply_text("Сначала надо выбрать расу персонажа! Интересно, кем он будет? Эльфом? Человеком? А может гномом?\n"
                                "Ну что, приступим к созданию?")
    return 1


def characters_race(update, context):
    race = random.choice(RACES)
    context.user_data['race'] = race
    update.message.reply_text(f"Раса твоего персонажа: {context.user_data['race']}\n"
                                "Файтер, клирик, вор и маг... А теперь выберем класс персонажа! Ты готов?")

    return 2


def characters_class(update, context):
    ch_class = random.choice(CLASSES)
    context.user_data['class'] = ch_class
    update.message.reply_text(f"Класс вашего персонажа: {context.user_data['class']}\n"
                                "Поздравляю, теперь ты можешь играть!")
    return 3


def character_information(update, context):
    reply_keyboard = [["/back"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    race, ch_class = context.user_data['race'], context.user_data['class']
    update.message.reply_text(f"Раса вашего персонажа: {race}, класс вашего персонажа: {ch_class}\n"
                                "Вперед! Навстречу приключениям!", reply_markup=markup)
    return ConversationHandler.END


def character_info(update, context):
    context.user_data.clear()
    reply_keyboard = [["/back"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Напиши расу персонажаб и я расскажу все, что знаю!", reply_markup=markup)
    return 1
    

def characteristics(update, context):
    race = update.message.text.capitalize()

    reply_keyboard = [["/back"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text("ОСОБЕННОСТИ")
    with open("data/race_info.json") as race_info:
        data = json.load(race_info)
        for key in data[race]['Особенности']:
            update.message.reply_text(f"{key}: {data[race]['Особенности'][key]}")

        update.message.reply_text("РАЗНОВИДНОСТИ")
        if race not in ['Драконорожденный', 'Полуэльф', 'Полуорк', 'Тифлинг']:
            for key in data[race]['Разновидности']:
                update.message.reply_text(f"{key}: {data[race]['Разновидности'][key]}", reply_markup=markup)
        else:
            update.message.reply_text("У этой расы нет разновидностей", reply_markup=markup)

    return ConversationHandler.END


def class_info(update, context):
    context.user_data.clear()
    reply_keyboard = [["/back"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Напиши класс персонажа, и я расскажу все, что знаю!", reply_markup=markup)
    return 1


def specialization(update, context):
    ch_class = update.message.text.capitalize()

    reply_keyboard = [["/back"], ["/help"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text("ОБЩИАЯ ИНФОРМАЦИЯ")
    with open("data/class_info.json") as class_info:
        data = json.load(class_info)
        update.message.reply_text(data[ch_class]['Общая информация'])

        update.message.reply_text("КЛАССОВЫЕ УМЕНИЯ")
        for key in data[ch_class]['Классовые умения']:
            update.message.reply_text(f"{key}: {data[ch_class]['Классовые умения'][key]}", reply_markup=markup)

    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_bot))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("roll_dice", roll_dice))

    dp.add_handler(CommandHandler("D4", roll_d4))
    dp.add_handler(CommandHandler("D6", roll_d6))
    dp.add_handler(CommandHandler("D8", roll_d8))
    dp.add_handler(CommandHandler("D10", roll_d10))
    dp.add_handler(CommandHandler("D12", roll_d12))
    dp.add_handler(CommandHandler("D20", roll_d20))
    dp.add_handler(CommandHandler("D100", roll_d100))


    conv_handler_creation = ConversationHandler(

    entry_points=[CommandHandler("create_character", create_character)],

            states={
                1: [MessageHandler(Filters.text, characters_race, pass_user_data=True)], 
                2: [MessageHandler(Filters.text, characters_class, pass_user_data=True)],
                3: [MessageHandler(Filters.text, character_information, pass_user_data=True)]
            },

            fallbacks=[CommandHandler("back", back)]
    )

    dp.add_handler(conv_handler_creation)


    conv_handler_character_info = ConversationHandler(

    entry_points=[CommandHandler("character_info", character_info)],

            states={
                1: [MessageHandler(Filters.text, characteristics, pass_user_data=True)]
            },

            fallbacks=[CommandHandler("back", back)]
    )

    dp.add_handler(conv_handler_character_info)

    conv_handler_character_info = ConversationHandler(

    entry_points=[CommandHandler("class_info", class_info)],

            states={
                1: [MessageHandler(Filters.text, specialization, pass_user_data=True)]
            },

            fallbacks=[CommandHandler("back", back)]
    )

    dp.add_handler(conv_handler_character_info)

    print("Bot started")
    updater.start_polling()

    updater.idle()
    print("Bot stopped")


if __name__ == "__main__":
    main()