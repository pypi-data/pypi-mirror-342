import ssl
import certifi
import os
import time
import json
import random
import threading
import warnings
import soundcard as sc
import soundfile as sf
from mtranslate import translate
import ollama
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import speech_recognition as sr

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

API_KEY = "374giayfaud738q"
kullanici_key = None
SETTINGS_PATH = "data.json"
MODEL_PATH = "model.json"
SYSTEM_PROMPT_PATH = "system_prompt.json"
PROFILS_PATH = "profils.json"
AKTIF_PATH = "aktif_profiller.json"

def set_api(key):
    global kullanici_key
    if key != API_KEY:
        raise ValueError("❌ Invalid API key!")
    kullanici_key = key
    print("✅ API key verified!")

def delay_sure_belirle():
    return random.randint(10, 45)

def kaydet_ayarlar(data):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)

def yukle_ayarlar():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def yukle_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("model", None)
    return None

def kaydet_model(model):
    with open(MODEL_PATH, "w", encoding="utf-8") as f:
        json.dump({"model": model}, f)

def oku_system_prompt():
    if os.path.exists(SYSTEM_PROMPT_PATH):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return " ".join(data.get("lines", []))
    return "You are an AI assistant in a Kick livestream. Speak like a human. Be brief, casual, realistic, and not robotic."

def kaydet_profil_sayaci(sayac):
    with open(PROFILS_PATH, "w", encoding="utf-8") as f:
        json.dump({"sayac": sayac}, f)

def yukle_profil_sayaci():
    if os.path.exists(PROFILS_PATH):
        with open(PROFILS_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("sayac", 1)
    return 1

def chrome_ile_baslat(profile_path, ayarlar, model, prompt_text):
    options = uc.ChromeOptions()
    options.user_data_dir = profile_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"❌ Chrome error: {e}")
        return

    driver.get(ayarlar["site"])
    print(f"🕒 AI will start in 60 seconds... ({profile_path})")

    def start_ai():
        SAMPLE_RATE = 48000
        RECORD_SEC = 10
        use_file_index = 1
        system_prompt = {"role": "system", "content": prompt_text}
        chat_history = []

        def build_prompt(user_input):
            chat_history.append({"role": "user", "content": user_input})
            return [system_prompt] + chat_history[-5:]

        while True:
            file_current = f"out{use_file_index}.wav"
            file_to_delete = f"out{(use_file_index % 3) + 1}.wav"

            try:
                with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
                    data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
                    sf.write(file_current, data[:, 0], samplerate=SAMPLE_RATE)
            except Exception as e:
                print(f"🎙️ Recording error: {e}")
                continue

            try:
                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)
            except Exception as e:
                print(f"🗑️ Delete error: {e}")

            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_current) as source:
                    audio = recognizer.record(source)
                turkish_text = recognizer.recognize_google(audio, language="tr-TR")
                print("🧑 (You):", turkish_text)
            except Exception as e:
                print(f"❌ Recognition error: {e}")
                use_file_index = (use_file_index % 3) + 1
                continue

            translated_text = translate(turkish_text, "en", "tr")
            prompt = build_prompt(translated_text)
            try:
                response = ollama.chat(model=model, messages=prompt)
                english_reply = response["message"]["content"].strip().split(".")[0].strip() + "."
                translated_reply = translate(english_reply, "tr", "en")
            except Exception as e:
                print(f"❌ AI response error: {e}")
                continue

            delay = delay_sure_belirle()
            print(f"⌛ Reply in {delay} sec...")
            time.sleep(delay)
            print("🤖 (AI):", translated_reply)
            chat_history.append({"role": "assistant", "content": english_reply})

            try:
                chat_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ayarlar["input_xpath"]))
                )
                chat_input.click()
                chat_input.send_keys(translated_reply)
                send_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ayarlar["buton_xpath"]))
                )
                send_button.click()
                print("📤 Sent!")
            except Exception as msg_err:
                print(f"❗ Send error: {msg_err}")

            use_file_index = (use_file_index % 3) + 1

    threading.Timer(60, start_ai).start()

def model_sec():
    print("\n🧠 Select AI Model:")
    print("1 - gemma:2b")
    print("2 - mistral")
    print("3 - llama3")
    secim = input("Your choice (1/2/3): ").strip()
    if secim == "1": kaydet_model("gemma:2b")
    elif secim == "2": kaydet_model("mistral")
    elif secim == "3": kaydet_model("llama3")
    else: print("❌ Invalid selection")

def baslat():
    if kullanici_key != API_KEY:
        raise PermissionError("❌ API not verified!")

    if yukle_model() is None:
        print("⚠️ First launch: AI model not selected.")
        model_sec()

    while True:
        print("\n📋 Menu:")
        print("1 - Continue")
        print("2 - Configure")
        print("3 - Prompt Settings (DISABLED)")
        print("4 - Select AI Model")
        print("5 - System Prompt Settings")
        print("6 - Create New Chrome Profile")
        print("7 - Multi Launch Profiles")
        secim = input("Choose (1-7): ").strip()

        if secim == "2":
            site = input("🌐 Enter site URL: ").strip()
            xpath_input = input("✏️ Input XPath: ").strip()
            xpath_buton = input("📤 Send button XPath: ").strip()
            kaydet_ayarlar({"site": site, "input_xpath": xpath_input, "buton_xpath": xpath_buton})
            print("✅ Settings saved.")

        elif secim == "4":
            model_sec()

        elif secim == "5":
            print("⚙️ Edit system_prompt.json manually if needed.")

        elif secim == "6":
            sayac = yukle_profil_sayaci()
            yeni_profil = f"borsaiti-{sayac}"
            kaydet_profil_sayaci(sayac + 1)
            profile_path = os.path.join(os.getcwd(), yeni_profil)
            os.makedirs(profile_path, exist_ok=True)
            ayarlar = yukle_ayarlar()
            model = yukle_model()
            prompt_text = oku_system_prompt()
            chrome_ile_baslat(profile_path, ayarlar, model, prompt_text)

        elif secim == "7":
            if not os.path.exists(PROFILS_PATH):
                print("⚠️ No profiles found. Create with option 6.")
                continue
            with open(PROFILS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            mevcut_sayac = data.get("sayac", 1)
            profiller = [f"borsaiti-{i}" for i in range(1, mevcut_sayac)]
            print("🔢 Available profiles:")
            for idx, profil in enumerate(profiller):
                print(f"{idx + 1} - {profil}")
            secim_indexleri = input("Select profiles by number (e.g., 1,3): ").strip()
            secilenler = [s.strip() for s in secim_indexleri.split(",") if s.strip().isdigit()]
            secilen_profiller = []
            for secilen in secilenler:
                index = int(secilen) - 1
                if 0 <= index < len(profiller):
                    secilen_profiller.append(profiller[index])

            aktif_profiller = []
            if os.path.exists(AKTIF_PATH):
                with open(AKTIF_PATH, "r", encoding="utf-8") as f:
                    aktif_profiller = json.load(f).get("aktif", [])

            for profil in secilen_profiller:
                if profil not in aktif_profiller:
                    aktif_profiller.append(profil)

            with open(AKTIF_PATH, "w", encoding="utf-8") as f:
                json.dump({"aktif": aktif_profiller}, f)
            print(f"📂 Profiles saved: {aktif_profiller}")

            remove = input("Remove a profile from active list? (y/n): ").strip().lower()
            if remove == "y":
                print("🔢 Active profiles:")
                for idx, profil in enumerate(aktif_profiller):
                    print(f"{idx + 1} - {profil}")
                to_remove = input("Select profile numbers to remove (e.g., 2,3): ").strip()
                remove_indices = [int(i.strip()) - 1 for i in to_remove.split(",") if i.strip().isdigit()]
                aktif_profiller = [p for i, p in enumerate(aktif_profiller) if i not in remove_indices]
                with open(AKTIF_PATH, "w", encoding="utf-8") as f:
                    json.dump({"aktif": aktif_profiller}, f)
                print(f"🗑️ Updated active profiles: {aktif_profiller}")

        elif secim == "1":
            if os.path.exists(AKTIF_PATH):
                with open(AKTIF_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    profiller = data.get("aktif", [])
                for profil in profiller:
                    profile_path = os.path.join(os.getcwd(), profil)
                    os.makedirs(profile_path, exist_ok=True)
                    ayarlar = yukle_ayarlar()
                    model = yukle_model()
                    prompt_text = oku_system_prompt()
                    threading.Thread(target=chrome_ile_baslat, args=(profile_path, ayarlar, model, prompt_text)).start()
            else:
                profile_path = os.path.join(os.getcwd(), "borsaiti")
                os.makedirs(profile_path, exist_ok=True)
                ayarlar = yukle_ayarlar()
                model = yukle_model()
                prompt_text = oku_system_prompt()
                chrome_ile_baslat(profile_path, ayarlar, model, prompt_text)
            break

        else:
            print("❌ Invalid selection")
