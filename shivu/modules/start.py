import random
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler  # Add CallbackQueryHandler import

from shivu import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from shivu import pm_users as collection


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    # Progress bar message
    baby = await update.message.reply_text("▒▒▒▒▒▒▒▒▒▒ 0%")

    # Update progress bar step by step
    await baby.edit_text(f"█▒▒▒▒▒▒▒▒▒ 10%")
    await baby.edit_text(f"██▒▒▒▒▒▒▒▒ 20%")
    await baby.edit_text(f"███▒▒▒▒▒▒▒ 30%")
    await baby.edit_text(f"████▒▒▒▒▒▒ 40%")
    await baby.edit_text(f"█████▒▒▒▒▒ 50%")
    await baby.edit_text(f"██████▒▒▒▒ 60%")
    await baby.edit_text(f"███████▒▒▒ 70%")
    await baby.edit_text(f"████████▒▒ 80%")
    await baby.edit_text(f"█████████▒ 90%")
    await baby.edit_text(f"██████████ 100%")
    
    # Now process user data
    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id=GROUP_ID,
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)}</a>",
                                       parse_mode='HTML')
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})
    
    # After progress, show the main message with the new format
    caption = f"""
    **How are you?** 😊  
    I’m **Phantom**, your friendly **Character Collecting Game Bot**! 🎮 Ready to dive into the world of collecting your favorite characters? 🌟  
    Need help? Click on the **Use** button! 🆘 I'll guide you through every step!  
    Want to report bugs or get support? Click on the **Support** button! 🛠️ We're always here to help!  
    For updates and useful information, click on the **Updates** button! 🔄 Stay updated with new features and improvements!  
    
    Join the fun and start collecting your dream characters today! ✨
    """
    
    keyboard = [
        [InlineKeyboardButton("ᴧᴅᴅ мᴇ", url=f'https://t.me/Waifu_World_Robot?startgroup=true')],
        [InlineKeyboardButton("Support", url=f'https://t.me/{SUPPORT_CHAT}'),
        InlineKeyboardButton("Updates", url=f'https://t.me/{UPDATE_CHAT}')],
        [InlineKeyboardButton("Help and Commands", callback_data='help')],
        [InlineKeyboardButton("Owner", url=f'https://t.me/iamakki001')],
        [InlineKeyboardButton("Co.owner", url=f'https://t.me/Pro_otaku')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_url = random.choice(PHOTO_URL)

    # Send the final message after showing the progress bar
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')
    await baby.delete()  # delete the progress bar message after it's complete


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    **Help Section:**
    /catch - Guess Character (only in group)
    /fav - Add Your Fav
    /trade - To Trade Characters
    /gift - Give Any Character To Another User (works in groups)
    /myworld - See Your Collection
    /topgroups - See Top Groups
    /top - See Top Users
    /ctop - Your Chat Top
    /changetime - Change Character Appearance Time (only in Groups)
   """
        help_keyboard = [[InlineKeyboardButton("⤾ Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':
        caption = f"""
        **How are you?** 😊  
        I’m **Phantom**, your friendly **Character Collecting Game Bot**! 🎮 Ready to dive into the world of collecting your favorite characters? 🌟  
        Need help? Click on the **Use** button! 🆘 I'll guide you through every step!  
        Want to report bugs or get support? Click on the **Support** button! 🛠️ We're always here to help!  
        For updates and useful information, click on the **Updates** button! 🔄 Stay updated with new features and improvements!  
        
        Join the fun and start collecting your dream characters today! ✨
        """
        
        keyboard = [
            [InlineKeyboardButton("ᴧᴅᴅ мᴇ", url=f'https://t.me/Waifu_World_Robot?startgroup=true')],
            [InlineKeyboardButton("Support", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("Updates", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("Help and Commands", callback_data='help')],
            [InlineKeyboardButton("Owner", url=f'https://t.me/iamakki001')],
            [InlineKeyboardButton("Co.owner", url=f'https://t.me/Pro_otaku')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
