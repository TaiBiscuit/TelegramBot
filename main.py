from typing import Final
from telegram import Update, Sticker, StickerSet
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters




async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'En que te puedo ayudar?')




#Responses

def handle_response(text: str) -> str:
    processedText: str = text.lower()

    if 'hello' in processedText:
        return 'Hey there!'
    return 'I do not understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {update.message.type}: {text}')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await update.message.reply_text(response)


async def handle_image(update:Update, context: ContextTypes.DEFAULT_TYPE):
    new_img = await update.message.effective_attachment[-1].get_file()
    return new_img

async def handle_sticker(update:Update, context: ContextTypes.DEFAULT_TYPE):
    if(not update.message or not update.effective_chat or not update.message.photo):
        return
    
    received_img = await handle_image(update, context)
    if not received_img:
        await update.message.reply_text("Something went wrong, try again!")
        return
    
    print(received_img)
    filename = received_img.download()
    context.bot.add_sticker_to_set(TOKEN, "@nicks_sticker_bot", open(filename, 'rb'), "😀")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused {context.error}')


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('hello', hello))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_sticker))
    app.add_error_handler(error)
    app.run_polling()

