import random
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from shivu import (
    PHOTO_URL,
    SUPPORT_CHAT,
    UPDATE_CHAT,
    BOT_USERNAME,
    db,
    GROUP_ID,
    pm_users as collection,
)

TOKEN = "your_bot_token_here"  # <- yahan apna bot token daalna


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(
            chat_id=GROUP_ID,
            text=f"New user Started The Bot..\nUser: <a href='tg://user?id={user_id}'>{escape(first_name)}</a>",
            parse_mode='HTML'
        )
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    caption = """
***Heyyyy...***

***I am An Open Source Character Catcher Bot...Add Me in Your group.. And I will send Random Characters After every 100 messages in Group... Use /guess to Collect that Characters in Your Collection.. and see Collection by using /Harem... So add in Your groups and Collect Your harem***
    """

    keyboard = [
        [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
        [
            InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{UPDATE_CHAT}')
        ],
        [InlineKeyboardButton("HELP", callback_data='help')],
        [InlineKeyboardButton("SOURCE", url='https://github.com/MyNameIsShekhar/WAIFU-HUSBANDO-CATCHER')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_url = random.choice(PHOTO_URL)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode='markdown'
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
***Help Section:***

***/guess: To Guess character (only works in group)***
***/fav: Add Your fav***
***/trade: To trade Characters***
***/gift: Give any Character from Your Collection to another user (only in groups)***
***/collection: To see Your Collection***
***/topgroups: See Top Groups***
***/top: See Top Users***
***/ctop: ChatTop***
***/changetime: Change Character appear time (Groups only)***
"""
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]
        ])

        await query.edit_message_caption(caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':
        caption = """
***Hoyyyy...*** ✨

***I am An Open Source Character Catcher Bot.. Add Me in Your group.. Use /guess to Collect characters, and /Harem to view them.***
"""
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [
                InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
                InlineKeyboardButton("UPDATES", url=f'https://t.me/{UPDATE_CHAT}')
            ],
            [InlineKeyboardButton("HELP", callback_data='help')],
            [InlineKeyboardButton("SOURCE", url='https://github.com/MyNameIsShekhar/WAIFU-HUSBANDO-CATCHER')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_caption(caption=caption, reply_markup=reply_markup, parse_mode='markdown')


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="^(help|back)$"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
