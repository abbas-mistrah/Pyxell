import requests
import subprocess
import time
import re
import random
import yfinance as yf
import xml.etree.ElementTree as ET
import os

commands_other = {
    # Other commands go here
    ('send', 'http', 'request'): lambda method, url: getattr(requests, method)(url).json(),
    ('count', 'words', 'in', 'sentence'): lambda sentence: len(sentence.split()),
    ('encrypt',): lambda algorithm, data, password: subprocess.Popen(['openssl', 'enc', f'-{algorithm}', '-in', data, '-out', 'encrypted_data', '-pass', f'pass:{password}'], shell=True),
    ('decrypt',): lambda algorithm, data, password: subprocess.Popen(['openssl', 'enc', f'-d', f'-{algorithm}', '-in', data, '-out', 'decrypted_data', '-pass', f'pass:{password}'], shell=True),
    # Add more other commands here
    # system.py commands
   ('kill', 'process'): lambda names: kill_processes([name.strip() for name in names.split(',')]),
    ('check', 'running', 'processes'): lambda: jsonify(psutil.pids()),
    ('details', 'process'): lambda pid: jsonify(psutil.Process(int(pid)).as_dict()),
    
    # Network Operations
    ('show', 'network', 'interfaces'): lambda: jsonify(dict(psutil.net_if_stats())),
    
    # Disk Operations
    ('format', 'drive'): lambda drive_letter, partition_scheme, fs_type: subprocess.Popen(['diskutil', 'eraseDisk', fs_type, partition_scheme, f'jhd{drive_letter}-0', f'/dev/{drive_letter}1'], shell=True),
    
    # Other Utilities
    ('sleep', 'now'): lambda: subprocess.run(['pmset', 'displaysleepnow'], check=False),
    ('wake', 'display'): lambda: subprocess.run(['pmset', 'awake'], check=False),
    ('lock', 'screen'): lambda: subprocess.run(['/System/Library/CoreServices/"Menu Extras"/User.menu/Contents/Resources/CGSession', '-suspend'], check=False),
    ('empty', 'trash'): lambda: subprocess.run(['osascript', '-e', 'tell application "Finder" to empty trash'], shell=True),
    # Commands for opening websites
    ('open', 'new', 'tab'): lambda: webbrowser.open_new_tab('https://www.google.com'),
    ('new', 'tab'): lambda: webbrowser.open_new_tab('https://www.google.com'),
    ('add', 'new', 'tab'): lambda: webbrowser.open_new_tab('https://www.google.com'),
    ('launch', 'new', 'tab'): lambda: webbrowser.open_new_tab('https://www.google.com'),
    ('search', 'web', 'for'): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search', 'for'): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search', 'web'): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search',): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('google',): lambda query: webbrowser.open_new_tab(f'https://www.google.com/search?q={query}'),
    ('search', 'video', 'for'): lambda query: webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={query}'),
    ('launch', 'youtube'): lambda: webbrowser.open_new_tab('https://www.youtube.com'),
    ('youtube',): lambda query: webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={query}'),
    ('open', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('play', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('launch', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('start', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('access', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('visit', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('go', 'to', 'spotify'): lambda: webbrowser.open_new_tab('https://open.spotify.com'),
    ('spotify',): lambda query: webbrowser.open_new_tab(f'https://open.spotify.com/search/{query}'),
    ('open', 'facebook'): lambda: webbrowser.open_new_tab('https://www.facebook.com'),
    ('facebook'): lambda: webbrowser.open_new_tab('https://www.facebook.com'),
    ('open', 'whatsapp'): lambda: webbrowser.open_new_tab('https://web.whatsapp.com'),
    ('whatsapp',): lambda: webbrowser.open_new_tab('https://web.whatsapp.com'),
    ('open', 'instagram'): lambda: webbrowser.open_new_tab('https://www.instagram.com'),
    ('instagram',): lambda: webbrowser.open_new_tab('https://www.instagram.com'),
    
    # Commands for opening Notepad and writing something
    ('open', 'editor'): lambda: subprocess.Popen(['gedit']),  # Adjusted for Linux
    ('write', 'in', 'editor'): lambda content: open('notes.txt', 'w').write(content),  # Adjusted for Linux
    
    # Commands for closing websites
    ('close', 'tab'): lambda: webbrowser.close(),
    ('close', 'all', 'tabs'): lambda: webbrowser.get().open('about:blank', new=0),
    ('close', 'facebook'): lambda: webbrowser.get().open('javascript:window.close();', new=0),
    ('close', 'whatsapp'): lambda: webbrowser.get().open('javascript:window.close();', new=0),
    ('close', 'instagram'): lambda: webbrowser.get().open('javascript:window.close();', new=0),
    
    # Commands for listing files in a directory
    ('list', 'files', 'in', 'directory'): lambda directory: os.listdir(directory),
    ('list', 'files'): lambda: os.listdir('.'),
    
    # Commands for getting information about the computer
    ('show', 'memory'): lambda: jsonify({'total': round(psutil.virtual_memory().total / (1024 * 1024 * 1024)),
                                         'available': round(psutil.virtual_memory().available / (1024 * 1024 * 1024)),
                                         'used': round((psutil.virtual_memory().total -
                                          psutil.virtual_memory().available) / (1024 * 1024 * 1024)),
                                         'percentage': psutil.virtual_memory().percent}),
    ('show', 'cpu'): lambda: jsonify({'model': psutil.cpuinfo().brand,
                                'cores': psutil.cpu_count(),
                                'frequency': psutil.cpu_freq().max}),
    ('show', 'disk'): lambda: jsonify({'free': round(psutil.disk_usage('/').free / (1024 * 1024 * 1024)),
                             'total': round(psutil.disk_usage('/').total / (1024 * 1024 * 1024)),
                             'used': round(((psutil.disk_usage('/').total -
                              psutil.disk_usage('/').free) / (1024 * 1024 * 1024))) }),
    
    # Command for downloading a file from the internet
    ('download', 'file', 'from', 'url'): lambda url, destination: requests.get(url).saveas(destination),
    
    # Commands for shutting down or restarting the computer
    ('shutdown', 'computer'): lambda: subprocess.run(['shutdown', '/s', '/t', '1']),
    ('reboot', 'computer'): lambda: subprocess.run(['shutdown', '/r', '/t', '1']),
    ('logoff'): lambda: subprocess.run(['shutdown', '/l']),
    
    # Commands for taking screenshots
    ('take', 'screenshot'): lambda: subprocess.Popen(['powershell', f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("%{{PRTSC}}"); $image = [System.Windows.Forms.Clipboard]::GetImage(); $image.Save("{os.path.join(os.path.expanduser("~"), "Pictures", "screenshot.png")}")'], shell=True),
     
    # Commands for converting units
    ('convert', 'unit', 'of', 'length'): lambda length, unit: {'cm': round(float(length)*0.01, 2),
                                   'm': round(float(length)*0.001, 2),
                                   'km': round(float(length)*0.000001, 2),
                                   'inch': round(float(length)*39.3701, 2),
                                   'feet': round(float(length)*3.28084, 2),
                                   'yard': round(float(length)*1.09361, 2),
                                   'mile': round(float(length)*0.000621371, 2)}[request.args.get('to')],
    ('convert', 'unit', 'of', 'weight'): lambda weight, unit: {'kg': float(weight)/1000,
                                   'g': float(weight),
                                   'lb': float(weight)*2.20462,
                                   'oz': float(weight)*35.274,
                                   'tonne': float(weight)*0.001}[request.args.get('to')],
    ('convert', 'unit', 'of', 'volume'): lambda volume, unit: {'ml': float(volume)/1000,
                                   'cl': float(volume)/100,
                                   'dl': float(volume)/10,
                                   'l': float(volume),
                                   'quart': float(volume)*0.000219969,
                                   'gallon': float(volume)*0.0000264172}[request.args.get('to')],
    
    # Command for sending HTTP requests
    ('send', 'http', 'request'): lambda method, url: getattr(requests, method)(url).json(),
    
    # Commands for counting words in a sentence
    ('count', 'words', 'in', 'sentence'): lambda sentence: len(sentence.split()),

    # Commands for file management
    ('create', 'folder'): lambda folder, name: subprocess.Popen(['mkdir', '-p', f'{folder}/{name}'], shell=True),
    ('rename', 'file'): lambda old_name, new_name: subprocess.Popen(['mv', old_name, new_name], shell=True),
    ('move', 'file'): lambda source, destination: subprocess.Popen(['mv', source, destination], shell=True),
    ('copy', 'file'): lambda source, destination: shutil.copy(source, destination),
    ('delete', 'file'): lambda path: os.remove(path),
    ('compress', 'file'): lambda archive_type, file, destination: subprocess.Popen(['zip', f'-r{destination}/{file}.{archive_type}', file], shell=True),
    ('extract', 'file'): lambda archive_type, file, destination: subprocess.Popen(['unzip', file, '-d', destination], shell=True),
    ('find', 'file'): lambda file_extension, directory: subprocess.Popen(['find', directory, '-name', f'*.{file_extension}'], shell=True),
    ('diff', 'file'): lambda file1, file2: subprocess.Popen(['diff', file1, file2], shell=True),
    ('encrypt',): lambda algorithm, data, password: subprocess.Popen(['openssl', 'enc', f'-{algorithm}', '-in', data, '-out', 'encrypted_data', '-pass', f'pass:{password}'], shell=True),
    ('decrypt',): lambda algorithm, data, password: subprocess.Popen(['openssl', 'enc', f'-d', f'-{algorithm}', '-in', data, '-out', 'decrypted_data', '-pass', f'pass:{password}'], shell=True),
    ('open', 'word'): lambda: subprocess.Popen(['start', 'WINWORD.EXE'], shell=True),
    ('open', 'excel'): lambda: subprocess.Popen(['start', 'EXCEL.EXE'], shell=True),
    ('open', 'powerpoint'): lambda: subprocess.Popen(['start', 'POWERPNT.EXE'], shell=True),
    ('open', 'play', 'control', 'panel'): lambda: subprocess.Popen(['explorer', 'shell:::{21EC2020-3AEA-1069-A2DD-08002B30309D}'], shell=True),
    ('open', 'my', 'computer'): lambda: subprocess.Popen(['explorer', 'shell:::{20D04FE0-3AEA-1069-A2D8-08002B30309D}', '::{00000000-0000-0000-0000-000000000000}'], shell=True),
    ('open', 'folder'): lambda folder_path: subprocess.Popen(['explorer', folder_path], shell=True),
    ('open', 'my', 'computer'): lambda: subprocess.Popen(['explorer', 'shell:::{20D04FE0-3AEA-1069-A2D8-08002B30309D}', '::{00000000-0000-0000-0000-000000000000}'], shell=True),
    ('open', 'folder'): lambda folder_path: subprocess.Popen(['explorer', folder_path], shell=True),
    ('open', 'notepad'): lambda: subprocess.Popen(['explorer', 'notepad.exe'], shell=True),
    ('open', 'calendar'): lambda: subprocess.Popen(['explorer', 'shell:::{2DF6FAED-9BE0-4CF3-8EA3-58ACFDCA2E93}'], shell=True),
        # Time & Date Management
    ('set', 'alarm'): lambda: subprocess.Popen(['open', 'Clock.app'], shell=True),
    ('cancel', 'alarm'): lambda: subprocess.Popen(['open', 'Clock.app'], shell=True),
    ('set', 'timer'): lambda: subprocess.Popen(['open', 'Clock.app'], shell=True),
    ('cancel', 'timer'): lambda: subprocess.Popen(['open', 'Clock.app'], shell=True),
    ('set', 'reminder'): lambda: subprocess.Popen(['open', 'Calendar.app'], shell=True),
    ('cancel', 'reminder'): lambda: subprocess.Popen(['open', 'Calendar.app'], shell=True),
    ('timezone',): lambda country_or_city: subprocess.Popen(['tzutil', '/g', f'"{country_or_city}"'], shell=True),
    ('date',): lambda format: subprocess.Popen(['date', f'+{format}'], shell=True),
    ('calendar',): lambda year_or_month_or_day: subprocess.Popen(['cal', year_or_month_or_day], shell=True),

    # Web Browsing
    ('bookmark',): lambda site_URL, title: webbrowser.open_new_tab(f'https://www.google.com/bookmarks/mark?op=edit&output=popup&bkmk={site_URL}&title={title}'),
    ('history',): lambda action: subprocess.Popen(['open', 'chrome://history'], shell=True) if action == 'view' else subprocess.Popen(['rm', '~/.config/google-chrome/Default/History'], shell=True),
    ('cache',): lambda action: subprocess.Popen(['open', 'chrome://settings/clearBrowserData'], shell=True) if action == 'clear' else subprocess.Popen(['open', 'chrome://view-http-cache'], shell=True),
    ('cookies',): lambda action: subprocess.Popen(['open', 'chrome://settings/siteData'], shell=True) if action == 'manage' else None,

    # Communication
    ('email',): lambda subject, body, recipient: webbrowser.open_new_tab(f'mailto:{recipient}?subject={subject}&body={body}'),
    ('chat',): lambda contact, message: subprocess.Popen(['open', f'https://web.whatsapp.com/send?phone={contact}&text={message}'], shell=True),
    ('voice',): lambda phone_number: subprocess.Popen(['open', f'tel:{phone_number}'], shell=True),
    ('video',): lambda contact: subprocess.Popen(['open', f'https://web.whatsapp.com/send?phone={contact}&text=&source=&data=&app_absent='], shell=True),

    # Music & Video Players
    ('play',): lambda song_name: subprocess.Popen(['open', f'https://www.youtube.com/results?search_query={song_name}'], shell=True),
    ('pause',): lambda: subprocess.Popen(['pause'], shell=True),
    ('resume',): lambda: subprocess.Popen(['play'], shell=True),
    ('stop',): lambda: subprocess.Popen(['killall', 'VLC'], shell=True),
    ('next',): lambda: subprocess.Popen(['next'], shell=True),
    ('previous',): lambda: subprocess.Popen(['previous'], shell=True),
    ('vol',): lambda level: subprocess.Popen(['osascript', '-e', f'set volume output volume {level}'], shell=True),
    ('seek',): lambda seconds: subprocess.Popen(['osascript', '-e', f'tell application "VLC" to set current time to current time + {seconds}'], shell=True),
  
}

def match_command_other(tokens):
    for cmd_tokens, action in commands_other.items():
        if all(cmd_token.lower() in tokens for cmd_token in cmd_tokens):
            params = [token.lower() for token in tokens if token.lower() not in cmd_tokens]
            result = action(*params) if params else action()
            return result
    return None