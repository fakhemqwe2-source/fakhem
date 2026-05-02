#!/usr/bin/env python3
import os
import sys
import json
import logging
from urllib.parse import quote
from datetime import datetime
import requests
import telebot
from telebot import types

# ================== الإعدادات الأساسية ==================
TOKEN = "8533945194:AAG_UskZav207apMlrfIBchapkVVJR13tK8"          # ضع توكن البوت هنا

# ================== قائمة الألعاب مع مفاتيح المصادقة الخاصة ==================
# 🔑 أضف المفتاح الحقيقي لكل لعبة في حقل "auth_key"
GAMES = {
    "Domino Dreams": {
        "platform": "ios",
        "ios_app_id": "id6444043291",
        "bundle_identifier": "com.superplaystudios.dominodreams",
        "user_agent": "DominoDreams/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "af_area_{number}_completed",
        "event_value_template": '{"af_area":{number}}',
        "auth_key": "Hn5qYjVAaRNJYDcwF4LaWF"   # 👈 ضع المفتاح هنا
    },
    "Coin Master": {
        "platform": "ios",
        "ios_app_id": "id406889139",
        "bundle_identifier": "com.coinmaster.game",
        "user_agent": "CoinMaster/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "village_{number}_complete",
        "event_value_template": '{"village":{number}}',
        "auth_key": "H3KjoCRVTiVgA5mWSAHtCe"     # 👈 ضع المفتاح هنا
    },
    "Coin Master Board Adventure": {
        "platform": "ios",
        "ios_app_id": "id6745761596",
        "bundle_identifier": "com.moonactive.cmboard",
        "user_agent": "CoinMasterBoardAdventure/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "village_{number}_complete",
        "event_value_template": '{"village":{number}}',
        "auth_key": "H3KjoCRVTiVgA5mWSAHtCe"
    },
    "Toon Blast": {
        "platform": "ios",
        "ios_app_id": "id1176027022",
        "bundle_identifier": "net.peakgames.toonblast",
        "user_agent": "ToonBlast/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "level_{number}_completed",
        "event_value_template": '{"level":{number}}',
        "auth_key": "F9M4SkdtH8WHcAt86ESrF3"
    },
    "Travel Town": {
        "platform": "ios",
        "ios_app_id": "id1521236603",
        "bundle_identifier": "io.randomco.travel",
        "user_agent": "TravelTown/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "reachedLevel{number}",
        "event_value_template": '{"Level":{number}}',
        "auth_key": "wizhvjciCuaDbAaR8KpZLn"
    },
    "Dice Dreams": {
        "platform": "ios",
        "ios_app_id": "id1484468651",
        "bundle_identifier": "com.dicedreams.game",
        "user_agent": "DiceDreams/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "af_kingdom_{number}_restored",
        "event_value_template": '{"kingdom":{number}}',
        "auth_key": "Hn5qYjVAaRNJYDcwF4LaWF"
    },
    "Disney Solitaire": {
        "platform": "ios",
        "ios_app_id": "id6475757306",
        "bundle_identifier": "com.superplaystudios.disneysolitairedreams",
        "user_agent": "DisneySolitaire/8618 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "af_area_{number}_completed",
        "event_value_template": '{"af_area":{number}}',
        "auth_key": "Hn5qYjVAaRNJYDcwF4LaWF"
    },
    "Empires": {
        "platform": "ios",
        "ios_app_id": "id1117841866",
        "bundle_identifier": "com.smallgiantgames.empires",
        "user_agent": "Empires/1974 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "xp_level_{number}",
        "event_value_template": '{\"af_level\":{number}}',
        "auth_key": "wStj8eCCuE84shUTkh7ZGc"
    },
    "Yarn loop": {
        "platform": "ios",
        "ios_app_id": "id6755183085",
        "bundle_identifier": "com.combo.yarnflow",
        "user_agent": "YarnLoop/1974 CFNetwork/1410.1 Darwin/22.6.0",
        "event_name_template": "level_complete_{number}",
        "event_value_template": '{\"level_complete\":{number}}',
        "auth_key": "TGm97uKTJF7qFCvREggWtf"
    },
    "family island": {
        "platform": "ios",
        "ios_app_id": "id1464689103",
        "bundle_identifier": "com.combo.yarnflow",
        "user_agent": "Family%20Island/2026010.6.88412 CFNetwork/1335.0.3.4 Darwin/21.6.0",
        "event_name_template": "level_{number}",
        "event_value_template": '{\"af_level\":{number}}',
        "auth_key": "H3KjoCRVTiVgA5mWSAHtCe"
    },
    "Merge Dragons": {
        "platform": "ios",
        "ios_app_id": "id1208952944",
        "bundle_identifier": "com.gramgames.mergedragons",
        "user_agent": "MergeDragons/1311 CFNetwork/1335.0.3.4 Darwin/21.6.0",
        "event_name_template": "event_{number}_dragon_power",
        "event_value_template": '{\"af_quantity\":{number}}',
        "auth_key": "fyKVEgAYzuD6jBZocaq3yh"
    },  
    "Match Masters": {
        "platform": "ios",
        "ios_app_id": "id1138264921",
        "bundle_identifier": "com.funtomic.matchmasters",
        "user_agent": "Match%20Masters/5405 CFNetwork/1335.0.3.4",
        "event_name_template": "trophies_{number}",
        "event_value_template": '{\"af_quantity\":{number}}',
        "auth_key": "EJcrH2pxmBbsWKHJHdrs3c"
    },  
    "Viking Rise": {
        "platform": "ios",
        "ios_app_id": "id6443577184",
        "bundle_identifier": "com.igg.vikingrise",
        "user_agent": "VikingRise/172347 CFNetwork/1335.0.3.4 ",
        "event_name_template": "castle_up_{number}",
        "event_value_template": '{\"af_level\":{number}}',
        "auth_key": "WEYqZmRBi6ZmFww2esj28Y"
    },
    "unerval master": {
        "platform": "ios",
        "ios_app_id": "id6744552355",
        "bundle_identifier": "com.mstudio.universemaster",
        "user_agent": "UNervalMaster/172347 CFNetwork/1335.0.3.4 ",
        "event_name_template": "af_level_achieved{number}",
        "event_value_template": '{\"af_level_achieved\":{number}}',
        "auth_key": "nYwfftoacbopmuszWBPGnd"
    },
    "screw guru": {
        "platform": "ios",
        "ios_app_id": "id6737529244",
        "bundle_identifier": "com.dcjnmed.jifqq",
        "user_agent": "ScrewGuru/172347 CFNetwork/1335.0.3.4 ",
        "event_name_template": "af_level_achieved{number}",
        "event_value_template": '{\"af_level\":{number}}',
        "auth_key": "nYwfftoacbopmuszWBPGnd"
    },
    "Match Factory": {
        "platform": "ios",
        "ios_app_id": "id6449094229",
        "bundle_identifier": "net.peakgames.match",
        "user_agent": "MatchFactory/172347 CFNetwork/1335.0.3.4 ",
        "event_name_template": "level_{number}_completed",
        "event_value_template": '{\"level\":{number}}',
        "auth_key": "F9M4SkdtH8WHcAt86ESrF3"
    },
}

# ================== إعداد التسجيل العام ==================
LOG_FILE = "requests.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def log_request_global(username, user_id, game, level, request_payload, response_text, status_code):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_str = f"@{username}" if username else f"ID:{user_id}"
    log_line = (
        f"{timestamp} | User: {user_str} | Game: {game} | Level: {level}\n"
        f"--- Request: {json.dumps(request_payload, ensure_ascii=False)}\n"
        f"--- Response ({status_code}): {response_text[:500]}\n"
        f"--- End ---"
    )
    logger.info(log_line)

# ================== إدارة ملفات المستخدمين (JSON لكل مستخدم) ==================
USER_DATA_FOLDER = "users_data"
os.makedirs(USER_DATA_FOLDER, exist_ok=True)

def get_user_filename(username, user_id):
    if username:
        safe_name = "".join(c for c in username if c.isalnum() or c in '._-')
        return f"user_{safe_name}.json"
    else:
        return f"user_ID_{user_id}.json"

def load_user_json(user_id, username=None):
    filename = get_user_filename(username, user_id)
    filepath = os.path.join(USER_DATA_FOLDER, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "user_id": user_id,
        "username": username,
        "proxy": {"host": None, "port": None, "user": None, "pass": None, "ip": None},
        "game": None,
        "appsflyer_id": None,
        "device_id": None,
        "os_version": "16.7.12",
        "arch": "arm64",
        "app_version": "6.17.7",
        "device_model": "iPhone14,3",
        "requests_history": []
    }

def save_user_json(user_id, username, data):
    filename = get_user_filename(username, user_id)
    filepath = os.path.join(USER_DATA_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_user_field(user_id, username, field, value):
    data = load_user_json(user_id, username)
    data[field] = value
    save_user_json(user_id, username, data)

def add_request_to_history(user_id, username, game, level, request_payload, response_text, status_code, success, headers):
    data = load_user_json(user_id, username)
    # إخفاء مفتاح المصادقة في السجل لأسباب أمنية
    safe_headers = headers.copy()
    if "Authentication" in safe_headers:
        safe_headers["Authentication"] = "HIDDEN"
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "game": game,
        "level": level,
        "success": success,
        "status_code": status_code,
        "request": request_payload,
        "headers": safe_headers,
        "response": response_text[:500]
    }
    data.setdefault("requests_history", []).append(history_entry)
    save_user_json(user_id, username, data)

# ================== دوال فحص البروكسي ==================
def test_proxy(proxy_dict):
    try:
        r = requests.get("https://api.ipify.org", proxies=proxy_dict, timeout=15)
        if r.status_code == 200:
            return True, r.text
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)

# ================== إرسال الحدث إلى AppsFlyer (مع مفتاح خاص لكل لعبة) ==================
def send_appsflyer_event(user_id, username, state, level_number):
    proxy = state["proxy"]
    if not all([proxy["host"], proxy["port"], proxy["user"], proxy["pass"]]):
        return False, "لم يتم إعداد البروكسي بعد", None, None

    game_name = state["game"]
    game = GAMES[game_name]
    
    # بناء اسم الحدث وقيمته
    event_name = game["event_name_template"].replace("{number}", str(level_number))
    event_value = game["event_value_template"].replace("{number}", str(level_number))
    
    # إعداد البروكسي
    proxy_url = f"socks5://{quote(proxy['user'])}:{quote(proxy['pass'])}@{proxy['host']}:{proxy['port']}"
    proxies = {"http": proxy_url, "https": proxy_url}
    
    # اختبار البروكسي وجلب IP
    proxy_ok, proxy_ip = test_proxy(proxies)
    if not proxy_ok:
        return False, f"البروكسي لا يعمل: {proxy_ip}", None, None
    # تحديث IP البروكسي في بيانات المستخدم
    update_user_field(user_id, username, "proxy", {**proxy, "ip": proxy_ip})
    
    # تجهيز البيانات المرسلة (الجسم)
    payload = {
        "appsflyer_id": state["appsflyer_id"],
        "eventName": event_name,
        "eventValue": event_value,
        "ip": proxy_ip,
        "idfa": state["device_id"],
        "customer_user_id": "4KMB4-YDMUU-62ZWY-FZ50B-5A31Z",   # ثابت
        "bundleIdentifier": game["bundle_identifier"],
        "os": state.get("os_version", "16.7.12"),
        "arch": state.get("arch", "arm64"),
        "app_version_short": state.get("app_version", "6.17.7"),
        "device_model": state.get("device_model", "iPhone14,3"),
        "platform": game["platform"]
    }
    
    # رؤوس الطلب - استخدام مفتاح المصادقة الخاص باللعبة
    auth_key = game.get("auth_key")
    if not auth_key:
        # إذا لم يتم تعيين مفتاح لهذه اللعبة، يمكنك إما رفع خطأ أو استخدام مفتاح عام
        auth_key = "DEFAULT_FALLBACK_KEY"   # يمكنك تغيير هذا أو جعله إلزامياً
    headers = {
        "Authentication": auth_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": game["user_agent"]
    }
    
    endpoint = f"https://api2.appsflyer.com/inappevent/{game['ios_app_id']}"
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, proxies=proxies, timeout=25)
        success = response.status_code == 200
        response_text = response.text
        status_code = response.status_code
    except Exception as e:
        success = False
        response_text = str(e)
        status_code = 0
    
    # تسجيل في الملف العام
    log_request_global(username, user_id, game_name, level_number, payload, response_text, status_code)
    # تسجيل في ملف المستخدم الخاص
    add_request_to_history(user_id, username, game_name, level_number, payload, response_text, status_code, success, headers)
    
    return success, response_text, status_code, payload

# ================== واجهة البوت ==================
bot = telebot.TeleBot(TOKEN)

def get_user_state_from_json(user_id, username):
    data = load_user_json(user_id, username)
    return {
        "proxy": data["proxy"],
        "game": data["game"],
        "appsflyer_id": data["appsflyer_id"],
        "device_id": data["device_id"],
        "os_version": data.get("os_version", "16.7.12"),
        "arch": data.get("arch", "arm64"),
        "app_version": data.get("app_version", "6.17.7"),
        "device_model": data.get("device_model", "iPhone14,3"),
        "username": username
    }

@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    username = message.from_user.username
    load_user_json(uid, username)
    show_main_menu(message)

def show_main_menu(message):
    uid = str(message.from_user.id)
    username = message.from_user.username
    state = get_user_state_from_json(uid, username)
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    proxy_status = "✅ مضاف" if state["proxy"]["host"] else "❌ غير مضاف"
    markup.add(types.InlineKeyboardButton(f"🔧 إضافة بروكسي ({proxy_status})", callback_data="add_proxy"))
    
    game_name = state["game"] if state["game"] else "❌ لم تختر"
    markup.add(types.InlineKeyboardButton(f"🎮 اختيار اللعبة ({game_name})", callback_data="choose_game"))
    
    markup.add(types.InlineKeyboardButton("⚙️ إعدادات الجهاز", callback_data="device_settings"))
    
    if state["proxy"]["host"] and state["game"] and state["appsflyer_id"] and state["device_id"]:
        markup.add(types.InlineKeyboardButton("🚀 إرسال الطلب الآن", callback_data="send_request"))
    else:
        markup.add(types.InlineKeyboardButton("⏳ أكمل البيانات أولاً", callback_data="noop"))
    
    markup.add(types.InlineKeyboardButton("🔄 إعادة تعيين", callback_data="reset"))
    
    text = (
        "🤖 *بوت AppsFlyer*\n\n"
        "1️⃣ أضف بروكسي (SOCKS5)\n"
        "2️⃣ اختر اللعبة\n"
        "3️⃣ أدخل معرف AppsFlyer\n"
        "4️⃣ أدخل معرف الجهاز (IDFA)\n"
        "5️⃣ أرسل الرقم\n\n"
        f"📡 البروكسي: {proxy_status}\n"
        f"🎲 اللعبة: {game_name}\n"
        f"🆔 AppsFlyer ID: {state['appsflyer_id'] or 'لم يدخل'}\n"
        f"📱 Device ID: {state['device_id'] or 'لم يدخل'}"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = str(call.from_user.id)
    username = call.from_user.username
    state = get_user_state_from_json(uid, username)
    
    if call.data == "add_proxy":
        msg = bot.send_message(
            call.message.chat.id,
            "📨 أرسل بيانات البروكسي *SOCKS5*:\n`host:port:user:pass`\nمثال: `185.199.96.148:1080:myuser:mypass`",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler(msg, process_proxy)
    
    elif call.data == "choose_game":
        markup = types.InlineKeyboardMarkup(row_width=2)
        for g in GAMES.keys():
            markup.add(types.InlineKeyboardButton(g, callback_data=f"setgame_{g}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
        bot.edit_message_text("اختر اللعبة:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data.startswith("setgame_"):
        game = call.data.replace("setgame_", "")
        update_user_field(uid, username, "game", game)
        bot.answer_callback_query(call.id, f"تم اختيار {game}")
        msg = bot.send_message(call.message.chat.id, "📱 أرسل الآن معرف AppsFlyer (appsflyer_id):")
        bot.register_next_step_handler(msg, process_appsflyer_id)
    
    elif call.data == "device_settings":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("📱 موديل الجهاز", callback_data="set_device_model"))
        markup.add(types.InlineKeyboardButton("🔄 إصدار iOS", callback_data="set_os_version"))
        markup.add(types.InlineKeyboardButton("💾 نسخة التطبيق", callback_data="set_app_version"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
        bot.edit_message_text("إعدادات الجهاز:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "set_device_model":
        msg = bot.send_message(call.message.chat.id, "أرسل موديل الجهاز (مثل: iPhone14,3):")
        bot.register_next_step_handler(msg, lambda m: update_device_field(m, "device_model"))
    elif call.data == "set_os_version":
        msg = bot.send_message(call.message.chat.id, "أرسل إصدار iOS (مثل: 16.7.12):")
        bot.register_next_step_handler(msg, lambda m: update_device_field(m, "os_version"))
    elif call.data == "set_app_version":
        msg = bot.send_message(call.message.chat.id, "أرسل نسخة التطبيق (مثل: 6.17.7):")
        bot.register_next_step_handler(msg, lambda m: update_device_field(m, "app_version"))
    
    elif call.data == "send_request":
        if not state["proxy"]["host"]:
            bot.answer_callback_query(call.id, "أضف بروكسي أولاً!", show_alert=True)
            return
        if not state["game"]:
            bot.answer_callback_query(call.id, "اختر لعبة أولاً!", show_alert=True)
            return
        if not state["appsflyer_id"]:
            bot.answer_callback_query(call.id, "أدخل معرف AppsFlyer أولاً!", show_alert=True)
            return
        if not state["device_id"]:
            bot.answer_callback_query(call.id, "أدخل معرف الجهاز (IDFA) أولاً!", show_alert=True)
            return
        msg = bot.send_message(call.message.chat.id, "🔢 أرسل الرقم (المستوى/القرية):")
        bot.register_next_step_handler(msg, process_level_number)
    
    elif call.data == "reset":
        filename = get_user_filename(username, uid)
        filepath = os.path.join(USER_DATA_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        load_user_json(uid, username)
        bot.answer_callback_query(call.id, "تم إعادة تعيين جميع بياناتك")
        show_main_menu(call.message)
    
    elif call.data == "back_main":
        show_main_menu(call.message)
    
    elif call.data == "noop":
        bot.answer_callback_query(call.id, "أكمل البيانات أولاً")

def update_device_field(message, field):
    uid = str(message.from_user.id)
    username = message.from_user.username
    new_value = message.text.strip()
    # منع إدخال بيانات تشبه البروكسي
    if ':' in new_value or '@' in new_value or new_value.count('.') >= 3:
        bot.reply_to(
            message,
            f"❌ قيمة غير صالحة لـ `{field}`.\nلا يمكن استخدام `:` أو `@` أو IP.\nمثال: `iPhone14,3`",
            parse_mode="Markdown"
        )
        return
    update_user_field(uid, username, field, new_value)
    bot.reply_to(message, f"✅ تم تحديث {field} إلى `{new_value}`", parse_mode="Markdown")
    show_main_menu(message)

def process_proxy(message):
    uid = str(message.from_user.id)
    username = message.from_user.username
    try:
        parts = message.text.strip().split(':')
        if len(parts) != 4:
            raise ValueError("يجب أن تكون 4 أجزاء")
        host, port, user, pwd = parts
        test_proxies = {
            "http": f"socks5://{quote(user)}:{quote(pwd)}@{host}:{port}",
            "https": f"socks5://{quote(user)}:{quote(pwd)}@{host}:{port}"
        }
        works, result = test_proxy(test_proxies)
        if works:
            proxy_data = {"host": host, "port": port, "user": user, "pass": pwd, "ip": result}
            update_user_field(uid, username, "proxy", proxy_data)
            bot.reply_to(message, f"✅ تم حفظ البروكسي!\nعنوان IP الظاهر: `{result}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ البروكسي لا يعمل: {result}\nتأكد من أنه SOCKS5 والبيانات صحيحة.")
            return
        show_main_menu(message)
    except Exception as e:
        bot.reply_to(message, f"❌ صيغة خاطئة: {e}\nاستخدم: host:port:user:pass", parse_mode="Markdown")

def process_appsflyer_id(message):
    uid = str(message.from_user.id)
    username = message.from_user.username
    update_user_field(uid, username, "appsflyer_id", message.text.strip())
    msg = bot.reply_to(message, "🆔 تم حفظ AppsFlyer ID. أرسل الآن معرف الجهاز (IDFA):")
    bot.register_next_step_handler(msg, process_device_id)

def process_device_id(message):
    uid = str(message.from_user.id)
    username = message.from_user.username
    update_user_field(uid, username, "device_id", message.text.strip())
    bot.reply_to(message, "✅ تم حفظ معرف الجهاز. يمكنك الآن إرسال الطلب.")
    show_main_menu(message)

def process_level_number(message):
    level_num = message.text.strip()
    if not level_num.isdigit():
        bot.reply_to(message, "❌ الرجاء إرسال رقم صحيح")
        return
    
    uid = str(message.from_user.id)
    username = message.from_user.username
    state = get_user_state_from_json(uid, username)
    
    bot.send_message(message.chat.id, "⏳ جاري إرسال الطلب عبر البروكسي ...")
    success, resp_text, status_code, _ = send_appsflyer_event(uid, username, state, level_num)
    
    if success:
        reply = f"✅ *تم الإرسال بنجاح!*\nكود الاستجابة: `{status_code}`"
    else:
        reply = f"❌ *فشل الإرسال*\nكود الاستجابة: `{status_code}`\nالتفاصيل: `{resp_text[:200]}`"
    
    bot.reply_to(message, reply, parse_mode="Markdown")
    show_main_menu(message)

if __name__ == "__main__":
    print("🚀 بوت AppsFlyer يعمل الآن (نسخة مع Authentication خاص لكل لعبة)")
    bot.infinity_polling()