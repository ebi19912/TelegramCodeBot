import google.generativeai as genai
import telegram
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

# تنظیمات
GOOGLE_API_KEY = ""
TELEGRAM_BOT_TOKEN = ":-"

# مراحل گفتگو
GET_PROJECT_TYPE, GET_LANGUAGE, GET_DETAILS, TYPING_REPLY = range(4)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

async def start(update: Update, context: CallbackContext) -> int:
    """شروع مکالمه و پرسیدن نوع پروژه"""
    await update.message.reply_text(
        "سلام! من ربات کدنویس تلگرامم. چه نوع پروژه ای نیاز داری؟\n"
        "مثال:\n"
        "- ربات تلگرام\n"
        "- وب اسکراپر\n"
        "- برنامه تحت وب\n"
        "- اتوماسیون\n"
        "- سایر",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GET_PROJECT_TYPE

async def get_project_type(update: Update, context: CallbackContext) -> int:
    """ذخیره نوع پروژه و پرسیدن زبان برنامه نویسی"""
    context.user_data["project_type"] = update.message.text
    reply_keyboard = [["Python", "JavaScript", "دیگر"]]
    await update.message.reply_text(
        "زبان برنامه نویسی مورد نظرت رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True, 
            input_field_placeholder="Python/JavaScript/..."
        ),
    )
    return GET_LANGUAGE

async def get_language(update: Update, context: CallbackContext) -> int:
    """ذخیره زبان و پرسیدن جزئیات"""
    context.user_data["language"] = update.message.text
    await update.message.reply_text(
        "لطفا جزئیات پروژه رو به طور کامل توضیح بده:\n"
        "- عملکرد اصلی\n"
        "- کتابخانه های خاص\n"
        "- ویژگی های کلیدی\n"
        "- هر نکته دیگری که مهمه"
    )
    return GET_DETAILS

async def get_details(update: Update, context: CallbackContext) -> int:
    """ذخیره جزئیات و آماده سازی برای تولید کد"""
    context.user_data["details"] = update.message.text
    await update.message.reply_text(
        "اطلاعات ثبت شد! حالا میتونی درخواستت رو مطرح کنی.\n"
        "مثال:\n"
        "'یک ربات تلگرام که عکس رو ذخیره کنه'\n"
        "'اسکراپر وب با پایتون'"
    )
    return TYPING_REPLY

async def restart(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "اطلاعات پاک شد. برای شروع جدید /start رو بزنید.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

async def generate_code(update: Update, context: CallbackContext) -> int:
    user_request = update.message.text
    state = context.user_data
    
    try:
        prompt = f"""
        شما یک برنامه نویس حرفه ای هستید. برای درخواست زیر کد مناسب بنویسید:
        
        الزامات کاربر:
        {user_request}
        
        نوع پروژه: {state.get('project_type', 'مشخص نشده')}
        زبان برنامه نویسی: {state.get('language', 'Python')}
        جزئیات اضافه: {state.get('details', 'بدون جزئیات')}
        
        موارد درخواستی:
        1. کد کامل و آماده اجرا
        2. استفاده از کتابخانه های استاندارد
        3. توضیحات به زبان ساده فارسی در کامنت ها
        4. سازگاری با پلتفرم تلگرام (اگر مرتبط است)
        5. ساختار تمیز و استاندارد
        """
        
        response = model.generate_content(prompt)
        
        # تقسیم پاسخ به قسمت های 4096 کاراکتری برای تلگرام
        for i in range(0, len(response.text), 4096):
            chunk = response.text[i:i+4096]
            await update.message.reply_text(chunk)
        
        await update.message.reply_text(
            "برای پروژه جدید /restart رو بزنید.\n"
            "برای اصلاح کد میتونی دوباره درخواست بدی!"
        )
        
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("خطا در تولید کد. لطفا دوباره امتحان کنید.")
    
    return TYPING_REPLY

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "عملیات لغو شد. /start رو برای شروع جدید بزنید.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GET_PROJECT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_project_type)],
        GET_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_language)],
        GET_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
        TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_code)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CommandHandler("restart", restart),
    ],
)

application.add_handler(conv_handler)
application.add_handler(CommandHandler("restart", restart))

application.run_polling()