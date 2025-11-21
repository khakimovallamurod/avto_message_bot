from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update
import config
import db

USER_IDS = config.get_adminIds()

GROUP_NAME, ID_START = range(2)
REMOVE_ID = range(1)

async def start(update: Update, context: CallbackContext):
    user = update.message.chat
    groupdb = db.TGgroups()
    chat_id = user.id
    if groupdb.check_group_id(chat_id):
        await update.message.reply_text(
            text=f"""Hello {user.full_name}! 👋\n\nUsing this bot, you can monitor seat availability for flights.\nType /addgroupid to begin.""",
        )
    else:
        await update.message.reply_text(
            text=f"""Hello {user.full_name}. 😔\nYou are not authorized to use this bot.""",
        )


async def admin_start(update: Update, context: CallbackContext):
    await update.message.reply_text("Please send the user Name.")
    return GROUP_NAME

async def group_name(update: Update, context: CallbackContext):
    context.user_data['group_name'] = update.message.text.capitalize()
    await update.message.reply_text("Please send the user ID.")
    return ID_START

async def insert_group(update: Update, context: CallbackContext):
    groupdb = db.TGgroups()
    id_text = update.message.text
    chat_id = str(update.message.chat.id)
    acount_name = context.user_data['group_name'] 
    if chat_id in USER_IDS:
        if groupdb.add_group(chat_id=id_text, fio=acount_name):
            await update.message.reply_text(
                f"✅ User successfully added to the admin list!\nAdmin: {acount_name}"
            )
            
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                "⚠️ The entered ID is invalid or this user already exists as an administrator."
            )
    else:
        await update.message.reply_text(
            "⛔ You do not have permission to add users."
        )

    return ConversationHandler.END

async def view_all_groups(update: Update, context: CallbackContext):
    groupdb = db.TGgroups()
    chat_id = update.effective_chat.id
    if str(chat_id) in USER_IDS:
        admin_list = groupdb.view_groups()
        admin_texts = ""
        for admin in admin_list:
            admin_texts += f"{admin['group_name']} ----- {admin['chat_id']}\n"
        await update.message.reply_text(admin_texts)
    else:
        await update.message.reply_text("⛔ You can't see admin lists")

async def remove_start(update: Update, context: CallbackContext):
    
    await update.message.reply_text("Please send the ID to delete the user.")
    return REMOVE_ID

async def remove_group(update: Update, context: CallbackContext):
    groupdb = db.TGgroups()
    chat_id = update.effective_chat.id
    delet_id = update.message.text
    if str(chat_id) in USER_IDS:
        if groupdb.delete_admin(delet_id):
            await update.message.reply_text("✅ This user was removed from the list")
            return ConversationHandler.END
        else:
            await update.message.reply_text("⚠️ This user doesn't exist")
            return ConversationHandler.END
    else:
        await update.message.reply_text("⛔ You can't delete user")
        return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text('❌ Jarayon bekor qilindi.')
    return ConversationHandler.END