import webbrowser
import subprocess
import keyboard
import time
import requests
import platform
import os
GOOGLE_DOMAINS = ['google.com', 'google.ca', 'google.co.uk', 'google.de', 'google.fr']
WIKIPEDIA_LANGUAGES = ['en', 'es', 'fr', 'de', 'ja']
TRANSLATION_SERVICES = ['google', 'bing', 'yandex']


def translate_query(platform, query):
    translations = {
        'google': query,
        'youtube': f'inurl:"{query}"',
        'wikipedia': f'"{query}" site:en.wikipedia.org',
        'reddit': f'site:reddit.com {query}',
        'stackoverflow': f'site:stackoverflow.com {query}',
        'gmail': f'site:mail.google.com inurl:compose?hl={get_locale()} {query}',
        'ebay': f'site:ebay.com {query}',
        'amazon': f'site:amazon.com {query}',
    }

    return translations.get(platform.lower(), query)

# Open links in the background
def open_background(url):
    if platform.system() == 'Linux':
        subprocess.Popen(["xdg-open", url], creationflags=subprocess.DETACHED_PROCESS)
    else:
        webbrowser.open(url, new=2)

# Determine locale to use for searches
def get_locale():
    return requests.get('https://api.ipdata.co/?api-key=test').json()['region_code']

# Search in selected domains
def search_domains(query, domains):
    for domain in domains:
        search_web_for(f'{query} site:{domain}')

# Perform calculations
def perform_calculation(expression):
    calculation_services = ['google', 'wolframalpha']
    for service in calculation_services:
        translated_query = translate_query(service, expression)
        search_web_for(translated_query)
        time.sleep(1)

# Convert currencies
def convert_currency(amount, currency_from, currency_to):
    conversion_services = ['google', 'xe.com', 'oanda.com']
    for service in conversion_services:
        translated_query = translate_query(service, f'{amount} {currency_from} to {currency_to}')
        search_web_for(translated_query)
        time.sleep(1)

# Find similar images
def find_similar_images(image_url):
    reverse_image_search_engines = ['tineye.com', 'google.com']
    for engine in reverse_image_search_engines:
        translated_query = translate_query(engine, f'reverse image search {image_url}')
        search_web_for(translated_query)
        time.sleep(1)

# Generate QR codes
def generate_QR_code(content):
    qr_code_generators = ['goqr.me', 'qrcode.monster', 'qrstickers.at']
    for generator in qr_code_generators:
        translated_query = translate_query(generator, f'qr code {content}')
        search_web_for(translated_query)
        time.sleep(1)

# Clear cache for active tab in Chrome
def chrome_clear_cache():
    try:
        chromium_path = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'
        subprocess.call([chromium_path, "--remote-debugging-port=9222"])
        time.sleep(1)
        subprocess.call(["python", "-c",
                         """
import requests; \
session = requests.Session(); \
for cookie in session.cookies: \
print(cookie); \
requests.post('http://localhost:9222/session/1/cookie/Clear'); \
"""
                         ])
    except Exception as e:
        print(str(e))

# Play songs on Spotify
def spotify_play_song(song_name):
    subprocess.Popen(['spotify', '--play', song_name])

# Stop playing songs on Spotify
def spotify_stop_playback():
    subprocess.Popen(['spotify', '--stop'])

# Toggle dark mode on Twitter
def twitter_dark_mode():
    subprocess.Popen(['google-chrome', '--remote-debugging-port=9222', 'https://mobile.twitter.com'])
    time.sleep(1)
    requests.post('http://localhost:9222/session/1/executeScript',
                  json={'script': '''document.querySelector('#dark-mode-button').click();''',
                        'args': []})

# Switch Wikipedia languages
def switch_wikipedia_language(language):
    assert language in WIKIPEDIA_LANGUAGES
    current_language = ''
    for lang in WIKIPEDIA_LANGUAGES:
        if lang in webbrowser.get().get('new')._default_parser.parse_args('https://en.wikipedia.org')[0]:
            current_language = lang
            break

    search_web_for(translate_query('wikipedia', f'{current_language}:{language}'))

# Change translation services
def change_translation_service(service):
    global TRANSLATION_SERVICES
    assert service in TRANSLATION_SERVICES
    TRANSLATION_SERVICES = [service]

# Define search_web_for function
def search_web_for(query):
    webbrowser.open_new_tab(f'https://www.google.com/search?q={query}')

commands_browser = {
    # Browser commands go here
    ('open', 'new', 'tab'): lambda *args: webbrowser.open_new_tab('https://www.google.com'),
    ('new', 'tab'): lambda *args: webbrowser.open_new_tab('https://www.google.com'),
    ('add', 'new', 'tab'): lambda *args: webbrowser.open_new_tab('https://www.google.com'),
    ('launch', 'new', 'tab'): lambda *args: webbrowser.open_new_tab('https://www.google.com'),
    ('search', 'web', 'for'): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search', 'for'): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search', 'web'): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search',): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('google',): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search', 'video', 'for'): lambda query: webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={query}'),
    ('launch', 'youtube'): lambda *args: webbrowser.open_new_tab('https://www.youtube.com'),
    ('youtube',): lambda query, *args: webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={query}'),
    ('open', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('play', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('launch', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('start', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('access', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('visit', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('go', 'to', 'spotify'): lambda *args: webbrowser.open_new_tab('https://open.spotify.com'),
    ('spotify',): lambda query: webbrowser.open_new_tab(f'https://open.spotify.com/search/{query}'),
    ('open', 'facebook'): lambda *args: webbrowser.open_new_tab('https://www.facebook.com'),
    ('facebook',): lambda *args: webbrowser.open_new_tab('https://www.facebook.com'),
    ('open', 'whatsapp'): lambda *args: webbrowser.open_new_tab('https://web.whatsapp.com'),
    ('whatsapp',): lambda *args: webbrowser.open_new_tab('https://web.whatsapp.com'),
    ('open', 'instagram'): lambda *args: webbrowser.open_new_tab('https://www.instagram.com'),
    ('instagram',): lambda *args: webbrowser.open_new_tab('https://www.instagram.com'),
    ('close', 'tab'): lambda *args: webbrowser.close(),
    ('close', 'all', 'tabs'): lambda *args: webbrowser.get().open('about:blank', new=0),
    ('facebook',): lambda *args: webbrowser.open_new_tab('https://www.facebook.com'),
    ('fb',): lambda *args: webbrowser.open_new_tab('https://www.facebook.com'),
    ('instagram',): lambda *args: webbrowser.open_new_tab('https://www.instagram.com'),
    ('ig',): lambda *args: webbrowser.open_new_tab('https://www.instagram.com'),
    ('twitter',): lambda *args: webbrowser.open_new_tab('https://www.twitter.com'),
    ('tw',): lambda *args: webbrowser.open_new_tab('https://www.twitter.com'),
    ('linkedin',): lambda *args: webbrowser.open_new_tab('https://www.linkedin.com'),
    ('ln',): lambda *args: webbrowser.open_new_tab('https://www.linkedin.com'),
    ('youtube',): lambda *args: webbrowser.open_new_tab('https://www.youtube.com'),
    ('yt',): lambda *args: webbrowser.open_new_tab('https://www.youtube.com'),
    ('wikipedia',): lambda *args: webbrowser.open_new_tab('https://www.wikipedia.org'),
    ('wiki',): lambda *args: webbrowser.open_new_tab('https://www.wikipedia.org'),
    ('refresh', 'current', 'tab'): lambda *args: keyboard.press_and_release('f5'),
    ('clear', 'cache', 'of', 'active', 'tab'): lambda *args: chrome_clear_cache(),
    ('incognito', 'mode'): lambda *args: chrome_toggle_private_browsing(),
    ('switch', 'to', 'previous', 'tab'): lambda *args: keyboard.press_and_release('<ctrl>+shift+tab'),
    ('next', 'tab'): lambda *args: keyboard.press_and_release('<ctrl>+tab'),
    ('previous', 'tab'): lambda *args: keyboard.press_and_release('<ctrl>+shift+tab'),
    ('switch', 'to', 'next', 'tab'): lambda *args: keyboard.press_and_release('<ctrl>+tab'),
    ('search', 'in', 'multiple', 'platforms'): lambda query: search_domains(query, GOOGLE_DOMAINS),
    ('calculate',): lambda query: perform_calculation(query),
    ('convert', 'currency', 'from', 'to'): lambda amount, curr1, curr2: convert_currency(amount, curr1, curr2),
    ('find', 'similar', 'images'): lambda img_url: find_similar_images(img_url),
    ('generate', 'QR', 'code'): lambda content: generate_QR_code(content),
    ('change', 'translation', 'service'): lambda service: change_translation_service(service),
    ('play', 'spotify', 'song'): lambda song: spotify_play_song(song),
    ('stop', 'spotify'): lambda *args: spotify_stop_playback(),
    ('enable', 'night', 'mode', 'on', 'twitter'): lambda *args: twitter_dark_mode(),
    ('switch', 'lang', 'wiki', 'to'): lambda lang: switch_wikipedia_language(lang),
}


def match_command_browser(tokens):
    for cmd_tokens, action in commands_browser.items():
        if all(cmd_token.lower() in tokens for cmd_token in cmd_tokens):
            params = [token.lower() for token in tokens if token.lower() not in cmd_tokens]
            result = action(*params) if params else action()
            return result
    return None

def chrome_toggle_private_browsing():
    subprocess.Popen(['google-chrome', '--incognito'])

def chrome_clear_cache():
    try:
        chromium_path = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"'
        subprocess.call([chromium_path, "--remote-debugging-port=9222"])
        time.sleep(1)
        subprocess.call(["python", "-c",
                         """
import requests; \
session = requests.Session(); \
for cookie in session.cookies: \
print(cookie); \
requests.post('http://localhost:9222/session/1/cookie/Clear'); \
"""])
    except Exception as e:
        print(str(e))
