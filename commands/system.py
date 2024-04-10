import psutil
import subprocess
import os
from flask import jsonify

commands_system = {
    # System commands go here
    ('kill', 'process'): lambda names: kill_processes([name.strip() for name in names.split(',')]),
    ('check', 'running', 'processes'): lambda: jsonify(psutil.pids()),
    ('details', 'process'): lambda pid: jsonify(psutil.Process(int(pid)).as_dict()),
    ('show', 'memory', 'statistics'): lambda: jsonify(get_memory_statistics()),
    ('show', 'cpu', 'statistics'): lambda: jsonify(get_cpu_statistics()),
    ('show', 'disk', 'space'): lambda mountpoint: jsonify(get_disk_space(mountpoint)),
    ('restart', 'machine'): lambda: restart_machine(),
    ('shutdown', 'machine'): lambda: shutdown_machine(),
    ('list', 'environment', 'variables'): lambda: jsonify(get_env_variables()),
    # Additional system commands can be included below
    # System and browser commands
    ('lauch', 'edge'): lambda: subprocess.Popen(['start', 'MicrosoftEdge.exe'], shell=True),
    ('launch', 'edge'): lambda: subprocess.Popen(['start', 'MicrosoftEdge.exe'], shell=True),
    ('laun', 'edge'): lambda: subprocess.Popen(['start', 'MicrosoftEdge.exe'], shell=True),
    ('chrome'): lambda: subprocess.Popen(['start', 'chrome.exe'], shell=True),
    ('ffox', 'launch'): lambda: subprocess.Popen(['start', 'firefox.exe'], shell=True),
    ('mozilla', 'launch'): lambda: subprocess.Popen(['start', 'firefox.exe'], shell=True),
    ('fmusic', 'launch'): lambda: subprocess.Popen(['start', 'GrooveMusic.exe'], shell=True),
    ('gpics', 'launch'): lambda: subprocess.Popen(['start', 'Photos.exe'], shell=True),
    ('movies', 'launch'): lambda: subprocess.Popen(['start', 'FilmsAndTV.exe'], shell=True),
    ('mail', 'app'): lambda: subprocess.Popen(['start', 'Mail.exe'], shell=True),
    ('mails'): lambda: subprocess.Popen(['start', 'Mail.exe'], shell=True),
    ('ms teams'): lambda: subprocess.Popen(['start', 'Teams.exe'], shell=True),
    ('team'): lambda: subprocess.Popen(['start', 'Teams.exe'], shell=True),
    ('skypes'): lambda: subprocess.Popen(['start', 'Skype.exe'], shell=True),
    ('sky'): lambda: subprocess.Popen(['start', 'Skype.exe'], shell=True),
    ('documents'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Documents'], shell=True),
    ('dochome'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Documents'], shell=True),
    ('downloads'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Downloads'], shell=True),
    ('dwnld'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Downloads'], shell=True),
    ('pics'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Pictures'], shell=True),
    ('pic'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Pictures'], shell=True),
    ('music'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Music'], shell=True),
    ('vid'): lambda: subprocess.Popen(['explorer', '%USERPROFILE%\\Videos'], shell=True),
    ('tsk'): lambda: subprocess.Popen(['start', 'taskmgr.exe'], shell=True),
    ('powrshell'): lambda: subprocess.Popen(['start', 'powershell.exe'], shell=True),
    ('pwrshell'): lambda: subprocess.Popen(['start', 'powershell.exe'], shell=True),
    ('codes'): lambda: subprocess.Popen(['start', 'Code.exe'], shell=True),
    ('vditor'): lambda: subprocess.Popen(['start', 'VisualStudio.exe'], shell=True),
    ('visual studio'): lambda: subprocess.Popen(['start', 'VisualStudio.exe'], shell=True),
    ('vs'): lambda: subprocess.Popen(['start', 'VisualStudio.exe'], shell=True),
    ('slacks'): lambda: subprocess.Popen(['start', 'Slack.exe'], shell=True),
    ('wa'): lambda: subprocess.Popen(['start', 'WhatsApp.exe'], shell=True),
    ('ws'): lambda: subprocess.Popen(['start', 'Steam.exe'], shell=True),
    ('sglauncher'): lambda: subprocess.Popen(['start', 'LauncherInternal.exe'], shell=True),
    ('origi'): lambda: subprocess.Popen(['start', 'Origin.exe'], shell=True),
    ('bat'): lambda: subprocess.Popen(['start', 'Battle.net.exe'], shell=True),
    ('gotomtg'): lambda: subprocess.Popen(['start', 'GoToOpener.exe'], shell=True),
    # Internet Browsers
    ('open', 'edge'): lambda: subprocess.Popen(['start', 'MicrosoftEdge.exe'], shell=True),
    ('open', 'chrome'): lambda: subprocess.Popen(['start', 'chrome.exe'], shell=True),
    ('open', 'firefox'): lambda: subprocess.Popen(['start', 'firefox.exe'], shell=True),
    # Multimedia Applications
    ('open', 'groove', 'music'): lambda: subprocess.Popen(['start', 'GrooveMusic.exe'], shell=True),
    ('open', 'photos'): lambda: subprocess.Popen(['start', 'Photos.exe'], shell=True),
    ('open', 'videos'): lambda: subprocess.Popen(['start', 'FilmsAndTV.exe'], shell=True),
    # Email Clients
    ('open', 'mail'): lambda: subprocess.Popen(['start', 'Mail.exe'], shell=True),
    # Communication Apps
    ('open', 'teams'): lambda: subprocess.Popen(['start', 'Teams.exe'], shell=True),
    ('open', 'skype'): lambda: subprocess.Popen(['start', 'Skype.exe'], shell=True),
    # Storage Services
    ('open', 'onedrive'): lambda: subprocess.Popen(['start', 'OneDrive.exe'], shell=True),
    # Settings
    ('open', 'settings'): lambda: subprocess.Popen(['start', 'Settings.exe'], shell=True),
    # File Explorer
    ('open', 'file', 'explorer'): lambda folder_path: subprocess.Popen(['explorer', folder_path], shell=True),
    # Task Manager
    ('open', 'task', 'manager'): lambda: subprocess.Popen(['start', 'taskmgr.exe'], shell=True),
    # Store
    ('open', 'store'): lambda: subprocess.Popen(['start', 'ms-windows-store://'], shell=True),
    # PowerShell
    ('open', 'powershell'): lambda: subprocess.Popen(['start', 'powershell.exe'], shell=True),
    # Command Prompt
    ('open', 'cmd'): lambda: subprocess.Popen(['start', 'cmd.exe'], shell=True),
    # Visual Studio Code
    ('open', 'vs', 'code'): lambda: subprocess.Popen(['start', 'Code.exe'], shell=True),
    # GitHub Desktop
    ('open', 'github', 'desktop'): lambda: subprocess.Popen(['start', 'git-credential-manager.exe'], shell=True),
    # Slack
    ('open', 'slack'): lambda: subprocess.Popen(['start', 'Slack.exe'], shell=True),
    # Discord
    ('open', 'discord'): lambda: subprocess.Popen(['start', 'Discord.exe'], shell=True),
    # WhatsApp Desktop
    ('open', 'whatsapp', 'desktop'): lambda: subprocess.Popen(['start', 'WhatsApp.exe'], shell=True),
    # Steam
    ('open', 'steam'): lambda: subprocess.Popen(['start', 'Steam.exe'], shell=True),
    # Epic Games Launcher
    ('open', 'epic', 'games', 'launcher'): lambda: subprocess.Popen(['start', 'LauncherInternal.exe'], shell=True),
    # Origin
    ('open', 'origin'): lambda: subprocess.Popen(['start', 'Origin.exe'], shell=True),
    # Battle.net
    ('open', 'battle', 'net'): lambda: subprocess.Popen(['start', 'Battle.net.exe'], shell=True),
    # Blizzard Battle.net
    ('open', 'blizzard', 'battle', 'net'): lambda: subprocess.Popen(['start', 'Battle.net.exe'], shell=True),
    # GoToMeeting
    ('open', 'goto', 'meeting'): lambda: subprocess.Popen(['start', 'GoToOpener.exe'], shell=True),
    # New Command
    ('brightness', 'up'): lambda: subprocess.Popen(['powershell', '(Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(100)', '&& exit'], shell=True),
    ('brightness', 'down'): lambda: subprocess.Popen(['powershell', '(Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(-100)', '&& exit'], shell=True),
    # New Command
    ('play', 'media'): lambda media_name: subprocess.Popen(['powershell', f'(New-Object -ComObject wmpds.axWindowsMediaPlayer).URL=\'{media_name}\'; (New-Object -ComObject wmpds.axWindowsMediaPlayer).controls.play()', '&& exit'], shell=True),
    ('wireless', 'scan'): lambda: subprocess.Popen(['netsh', 'wlan', 'show', 'profile', 'key=clear'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8'),
    ('connect', 'wifi'): lambda ssid, key: connect_wifi(ssid, key),
    ('disconnect', 'wifi'): lambda: disconnect_wifi(),
    ('wifi', 'connections'): lambda: jsonify(check_wifi_connection()),
    # Display Commands
    ('monitor', 'turn', 'off'): lambda: turn_off_monitor(),
    ('monitor', 'turn', 'on'): lambda: turn_on_monitor(),
    # Lighting Commands
    ('keyboard', 'illuminate', 'on'): lambda: toggle_keyboard_illumination('on'),
    ('keyboard', 'illuminate', 'off'): lambda: toggle_keyboard_illumination('off'),
    # Sound Commands
    ('mute', 'sound'): lambda: mute_sound(),
    ('unmute', 'sound'): lambda: unmute_sound(),
    # CPU Stress Test
    ('stress', 'test', 'cpu'): lambda duration: stress_test_cpu(duration),
    # Backup Commands
    ('backup', 'database', 'mysql'): lambda database, backup_path: backup_mysql_db(database, backup_path),
    # Download Commands
    ('download', 'file', 'direct'): lambda url, save_path: download_file_direct(url, save_path),
    ('open', 'voice', 'recorder'): lambda: subprocess.Popen(['start', 'soundrecorder:']),
    ('open', 'calendar'): lambda: subprocess.Popen(['start', 'outlookcal:']),
    ('open', 'calculator'): lambda: subprocess.Popen(['calc']),
    ('open', 'camera'): lambda: subprocess.Popen(['start', 'camera:']),
    ('show', 'battery', 'status'): lambda: webbrowser.open('ms-settings:privacy-batterysaver'),
    ('open', 'wi-fi', 'settings'): lambda: webbrowser.open('ms-settings:network-wifi'),
    ('open', 'color', 'picker'): lambda: subprocess.Popen(['start', 'control color']),
    ('open', 'paint'): lambda: subprocess.Popen(['mspaint']),
    ('open', 'notepad'): lambda: subprocess.Popen(['notepad']),
}

def kill_processes(names):
    """Terminate processes whose names match the input arguments."""
    killed_pids = []
    for name in names:
        try:
            pids = [proc.pid for proc in psutil.process_iter(['name']) if name.lower() in proc.info['name'].lower()]
            for pid in pids:
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                    killed_pids.append(pid)
                except Exception as e:
                    print(f"Couldn't terminate PID '{pid}'. Reason: {str(e)}")
        except Exception as e:
            print(f"Couldn't retrieve PIDs for '{name}'. Reason: {str(e)}")
    return killed_pids

def get_memory_statistics():
    """Return memory usage statistics as a JSON object."""
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    stats = {
        'total': round(virtual_mem.total / (1024 ** 3)),
        'available': round(virtual_mem.available / (1024 ** 3)),
        'used': round((virtual_mem.total - virtual_mem.available) / (1024 ** 3)),
        'percentage': virtual_mem.percent,
        'swap_total': round(swap_mem.total / (1024 ** 3)),
        'swap_used': round(swap_mem.used / (1024 ** 3)),
        'swap_free': round(swap_mem.free / (1024 ** 3)),
        'swap_percentage': swap_mem.percent
    }
    return stats

def get_cpu_statistics():
    """Return CPU information as a JSON object."""
    cpu_info = psutil.cpu_info()
    cpu_freq = psutil.cpu_freq()
    cpu_times = psutil.cpu_times()
    stats = {
        'model': cpu_info.get('model'),
        'cores': psutil.cpu_count(),
        'frequency': round(cpu_freq.max / 1000, 2),
        'user_time': str(timedelta(seconds=cpu_times.user)),
        'nice_time': str(timedelta(seconds=cpu_times.nice)),
        'sys_time': str(timedelta(seconds=cpu_times.system)),
        'idle_time': str(timedelta(seconds=cpu_times.idle)),
        'irq_time': str(timedelta(seconds=cpu_times.irq)),
        'soft_irq_time': str(timedelta(seconds=cpu_times.soft_irq)),
        'guest_time': str(timedelta(seconds=cpu_times.guest)),
        'guest_nice_time': str(timedelta(seconds=cpu_times.guest_nice))
    }
    return stats

def get_disk_space(mountpoint):
    """Return disk space statistics for a given mount point as a JSON object."""
    disk_partitions = psutil.disk_partitions()
    target_partition = next(filter(lambda part: part.mountpoint == mountpoint, disk_partitions), None)
    if target_partition:
        disk_usage = psutil.disk_usage(target_partition.mountpoint)
        stats = {
            'device': target_partition.device,
            'mountpoint': target_partition.mountpoint,
            'fstype': target_partition.fstype,
            'options': target_partition.opts,
            'free': round(disk_usage.free / (1024 ** 3)),
            'total': round(disk_usage.total / (1024 ** 3)),
            'used': round(disk_usage.used / (1024 ** 3)),
            'percentage': disk_usage.percent
        }
        return stats
    else:
        return {"error": "Mount point not found"}

def restart_machine():
    """Restart the machine."""
    subprocess.call(['shutdown', '/r', '/t', '0'])

def shutdown_machine():
    """Shut down the machine."""
    subprocess.call(['shutdown', '/s', '/t', '0'])

def get_env_variables():
    """Return environment variables as a JSON object."""
    env_vars = {}
    for var in os.environ:
        env_vars[var] = os.environ[var]
    return env_vars

def match_command_system(tokens):
    for cmd_tokens, action in commands_system.items():
        if all(cmd_token.lower() in tokens for cmd_token in cmd_tokens):
            params = [token.lower() for token in tokens if token.lower() not in cmd_tokens]
            result = action(*params) if params else action()
            return result
    return None