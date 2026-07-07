"""
Main Telegram Bot Handler
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)
from config import TELEGRAM_TOKEN, BOT_NAME, BOT_VERSION
from bypasser import LinkBypassser, DownloadManager
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States untuk conversation
WAITING_FOR_LINK = 1

# Initialize modules
bypasser = LinkBypassser()
downloader = DownloadManager()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /start command"""
    user = update.effective_user
    welcome_text = f"""
👋 Halo {user.first_name}! Welcome ke {BOT_NAME} v{BOT_VERSION}

🤖 Bot ini bisa:
• ✅ Bypass verification page
• 📌 Bypass shortlink
• 💾 Download file otomatis

📝 Cara pakai:
Kirim link yang ingin di-bypass, contoh:
• https://example-shortlink.com/abc123
• https://verify.site.com/download
• Atau link download langsung

⚠️ Catatan:
Bot hanya untuk edukasi, gunakan dengan bijak!
    """
    await update.message.reply_text(welcome_text)


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk link yang dikirim user"""
    user = update.effective_user
    text = update.message.text
    
    # Validate URL
    if not text.startswith(('http://', 'https://')):
        await update.message.reply_text(
            "❌ Tolong kirim link yang valid (mulai dari http:// atau https://)"
        )
        return
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        "⏳ Sedang memproses link...\n"
        "🔍 Mendeteksi tipe link...\n"
        "⚙️ Memproses bypass..."
    )
    
    try:
        logger.info(f"User {user.id} mengirim link: {text}")
        
        # Detect dan bypass
        result = bypasser.bypass_link(text)
        
        if result.get('success'):
            # Format hasil
            response_text = f"""
✅ <b>BYPASS BERHASIL!</b>

📋 <b>Informasi:</b>
• Tipe: {result.get('type', 'Unknown').upper()}
• Metode: {result.get('method', 'Unknown')}

🔗 <b>Link Asli:</b>
<code>{text}</code>

📌 <b>Hasil Bypass:</b>
"""
            
            # Tambah link yang sudah di-bypass
            if 'bypassed_url' in result:
                response_text += f"<code>{result['bypassed_url']}</code>\n"
            elif 'download_link' in result:
                response_text += f"<code>{result['download_link']}</code>\n"
            elif 'nested_link' in result:
                response_text += f"<code>{result['nested_link']}</code>\n"
            
            response_text += """
💡 <b>Pilihan:</b>
• Klik tombol di bawah untuk download
• Atau copy link untuk buka sendiri
            """
            
            # Create buttons
            keyboard = [
                [InlineKeyboardButton("📥 Download", callback_data="download")],
                [InlineKeyboardButton("🔗 Copy Link", callback_data="copy")],
                [InlineKeyboardButton("🔄 Bypass Link Lain", callback_data="new_link")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await processing_msg.edit_text(response_text, parse_mode='HTML', reply_markup=reply_markup)
            
            # Store link di context
            context.user_data['last_link'] = result.get('bypassed_url') or result.get('download_link') or result.get('nested_link')
            context.user_data['original_link'] = text
        
        else:
            error_msg = f"""
❌ <b>BYPASS GAGAL</b>

🔴 Error: {result.get('error', 'Unknown error')}

💡 Kemungkinan penyebab:
• Link sudah expired
• Format link tidak didukung
• Server error/timeout
• Link memerlukan autentikasi

🔄 Coba lagi dengan link lain!
            """
            await processing_msg.edit_text(error_msg, parse_mode='HTML')
    
    except Exception as e:
        logger.error(f"Error processing link: {str(e)}")
        await processing_msg.edit_text(
            f"❌ Error: {str(e)}\n\n"
            "Silakan coba lagi atau gunakan link yang berbeda."
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "download":
        await query.edit_message_text(
            text="📥 Fitur download otomatis sedang dikembangkan!\n\n"
                 "Untuk sekarang, gunakan link di atas untuk download manual."
        )
    
    elif query.data == "copy":
        link = context.user_data.get('last_link', 'Tidak ada link')
        await query.edit_message_text(
            text=f"📋 Link untuk di-copy:\n\n<code>{link}</code>",
            parse_mode='HTML'
        )
    
    elif query.data == "new_link":
        await query.edit_message_text(
            text="🔄 Kirim link baru yang ingin di-bypass!"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /help command"""
    help_text = """
🆘 <b>BANTUAN</b>

<b>Perintah yang tersedia:</b>
/start - Mulai bot
/help - Tampilkan bantuan ini
/about - Info tentang bot
/stats - Statistik penggunaan

<b>Cara Pakai:</b>
1️⃣ Kirim link yang ingin di-bypass
2️⃣ Bot akan memproses link
3️⃣ Pilih aksi (download/copy/bypass lain)

<b>Link yang Support:</b>
✅ Shortlink (bit.ly, tinyurl, dll)
✅ Verification page
✅ Download link (MediaFire, MEGA, Google Drive)
✅ Link redirect

<b>Tips:</b>
• Pastikan link valid dan aktif
• Beberapa link memerlukan waktu lebih lama
• Jika gagal, coba bypass link yang berbeda

<b>Butuh bantuan lebih?</b>
Hubungi @support atau buka dokumentasi di GitHub
    """
    await update.message.reply_text(help_text, parse_mode='HTML')


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /about command"""
    about_text = f"""
ℹ️ <b>TENTANG BOT</b>

<b>Nama:</b> {BOT_NAME}
<b>Versi:</b> {BOT_VERSION}
<b>Fungsi:</b> Bypass verification & shortlink

<b>Developer:</b> @alfiedafa3
<b>Repository:</b> github.com/alfiedafa3/BypasnksBOT

<b>Fitur Utama:</b>
• Bypass link verification
• Resolve shortlink
• Download file otomatis
• Multi-link support

<b>Status:</b> ✅ Active
<b>Uptime:</b> 24/7

Terima kasih telah menggunakan {BOT_NAME}!
    """
    await update.message.reply_text(about_text, parse_mode='HTML')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /stats command"""
    stats_text = """
📊 <b>STATISTIK PENGGUNAAN</b>

<b>Total Links Processed:</b> -
<b>Success Rate:</b> -
<b>Total Users:</b> -
<b>Active Users (24h):</b> -

���� <b>Tipe Link Terbanyak:</b>
• Shortlink: -
• Verification: -
• Download: -

⏱️ <b>Rata-rata Processing Time:</b> -

(Statistik real-time akan ditampilkan setelah integrasi database)
    """
    await update.message.reply_text(stats_text, parse_mode='HTML')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Message handler untuk link
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    
    # Button handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Error handler
    application.add_error_handler(error_handler)

    # Run the bot
    logger.info(f"🤖 {BOT_NAME} v{BOT_VERSION} sedang dijalankan...")
    application.run_polling()


if __name__ == '__main__':
    main()
