import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# പ്രധാന വേരിയബിളുകൾ കൃത്യമായി നൽകിയിരിക്കുന്നു
CHANNELS = -1002015288592  # Database Channel ID
AUTH_CHANNEL = -1002110922261    # Update Channel ID
BOT_USERNAME = "Anujith2bot"          

@Client.on_message(filters.chat(CHANNELS) & (filters.document | filters.video))
async def auto_post_formatter(client, message):
    try:
        # ഫയലിന്റെ ഒറിജിനൽ പേര് സുരക്ഷിതമായി എടുക്കുന്നു
        if message.document:
            file_name_raw = message.document.file_name
        elif message.video:
            file_name_raw = message.video.file_name or "Media File"
        else:
            return

        # 1. File Name ക്ലീൻ ചെയ്യുന്നു
        clean_name = re.sub(r's\d+|season\s*\d+|e\d+|episode\s*\d+|\d{3,4}p', '', file_name_raw, flags=re.IGNORECASE).strip()
        clean_name = clean_name.replace('.', ' ').replace('_', ' ').strip()
        if not clean_name:
            clean_name = "Malayalam Serial"

        # 2. Season കണ്ടെത്താൻ
        season_match = re.search(r'(?:s|season\s*)(\d+)', file_name_raw, re.IGNORECASE)
        season = season_match.group(1).zfill(2) if season_match else "01"

        # 3. Episode കണ്ടെത്താൻ
        episode_match = re.search(r'(?:e|episode\s*)(\d+)', file_name_raw, re.IGNORECASE)
        episode_num = episode_match.group(1) if episode_match else "1"
        episode_str = f"E{episode_num}"

        # 4. Quality കണ്ടെത്താൻ
        quality_match = re.search(r'(\d{3,4}p)', file_name_raw, re.IGNORECASE)
        quality = quality_match.group(1) if quality_match else "720p"

        # ക്യാപ്ഷൻ ഫോർമാറ്റ്
        caption = (
            f"📁 **File Name :** {clean_name}\n"
            f"🎞️ **Season :** {season}\n"
            f"📌 **Episode :** {episode_num}\n"
            f"🎬 **Quality :** {quality}"
        )

        # കസ്റ്റം സ്റ്റാർട്ട് ലിങ്ക് ഫോർമാറ്റ്
        formatted_name_for_link = clean_name.replace(" ", "")
        bot_link = f"https://telegram.me/{BOT_USERNAME}?start=getfile-{formatted_name_for_link}-S{season}{episode_str}"

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Get File", url=bot_link)]]
        )

        # നിങ്ങൾ നൽകിയ ഇമേജ് ലിങ്ക്
        BANNER_PHOTO = "https://files.catbox.moe/k0fvgh.jpg"

        # അപ്ഡേറ്റ് ചാനലിലേക്ക് ഫോട്ടോയും ക്യാപ്ഷനും അയക്കുന്നു
        await client.send_photo(
            chat_id=AUTH_CHANNEL,
            photo=BANNER_PHOTO,
            caption=caption,
            reply_markup=reply_markup
        )

    except Exception as e:
        print(f"Auto-Formatter Error: {e}")
