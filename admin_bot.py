from telegram.ext import (
    CommandHandler, MessageHandler, filters, 
    ConversationHandler, Application, CallbackQueryHandler
)
from telegram import Update
from config import get_token
import handlears


def main():
    TOKEN = get_token()

    dp = Application.builder().token(TOKEN).build()

    dp.add_handler(CommandHandler('start', handlears.start))

    add_group_handler = ConversationHandler(
        entry_points=[CommandHandler('addgroupid', handlears.admin_start)],
        states={
            handlears.GROUP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.group_name)],
            handlears.ID_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.insert_group)]
        },
        fallbacks=[CommandHandler("cancel", handlears.cancel)],
        allow_reentry=True
    )
    remove_handler = ConversationHandler(
        entry_points=[CommandHandler('remove_group', handlears.remove_start)],
        states={
            handlears.REMOVE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlears.remove_group)],
        },
        fallbacks=[CommandHandler("cancel", handlears.cancel)],
        allow_reentry=True
    )
    
    dp.add_handler(CommandHandler('viewgroups', handlears.view_all_groups))
    dp.add_handler(add_group_handler)
    dp.add_handler(remove_handler)


    dp.run_polling(allowed_updates=Update.ALL_TYPES, timeout=30)

if __name__ == '__main__':
    main()