import os
import shutil
import subprocess

commands_files = {
    # File management commands go here
    ('create', 'folder'): lambda folder, name: subprocess.Popen(['mkdir', '-p', f'{folder}/{name}'], shell=True),
    ('rename', 'file'): lambda old_name, new_name: subprocess.Popen(['mv', old_name, new_name], shell=True),
    ('move', 'file'): lambda source, destination: subprocess.Popen(['mv', source, destination], shell=True),
    ('copy', 'file'): lambda source, destination: shutil.copy(source, destination),
    ('delete', 'file'): lambda path: os.remove(path),
    ('compress', 'file'): lambda archive_type, file, destination: subprocess.Popen(['zip', f'-r{destination}/{file}.{archive_type}', file], shell=True),
    ('extract', 'file'): lambda archive_type, file, destination: subprocess.Popen(['unzip', file, '-d', destination], shell=True),
    ('find', 'file'): lambda file_extension, directory: subprocess.Popen(['find', directory, '-name', f'*.{file_extension}'], shell=True),
    ('diff', 'file'): lambda file1, file2: subprocess.Popen(['diff', file1, file2], shell=True),
    # Add more file management commands here
}

def match_command_files(tokens):
    for cmd_tokens, action in commands_files.items():
        if all(cmd_token.lower() in tokens for cmd_token in cmd_tokens):
            params = [token.lower() for token in tokens if token.lower() not in cmd_tokens]
            result = action(*params) if params else action()
            return result
    return None