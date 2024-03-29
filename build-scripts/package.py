#!/usr/bin/env python3

import sys
import os
import shutil
import zipfile
import subprocess
import tempfile
import atexit
import pathlib


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


godot_bin_path = sys.argv[1]
platform_name = sys.argv[2]
source_directory = sys.argv[3]
output_directory = sys.argv[4]
print(f"output directory: {output_directory}")
game_name = sys.argv[5]
editor_settings_path = os.path.expanduser(sys.argv[6])
library_paths = sys.argv[7].split('\n')[:-1] # last element is empty, newline at end

def ensure_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

if not os.path.exists(editor_settings_path):
    os.mknod(editor_settings_path)

# copy build outputs
for l in library_paths:
    shutil.copy2(l, output_directory)

editor_settings_cache_directory = tempfile.TemporaryDirectory()
editor_settings_cache_path = os.path.join(
    editor_settings_cache_directory.name, "editor-settings-cache.tres"
)
shutil.copy2(editor_settings_path, editor_settings_cache_path)


def cleanup_editor_settings():
    shutil.copy2(editor_settings_cache_path, editor_settings_path)
    editor_settings_cache_directory.cleanup()


atexit.register(cleanup_editor_settings)

exporting_process = subprocess.Popen(
    [
        godot_bin_path,
        "--export-debug",
        platform_name,
        "--path",
        os.path.join(source_directory),
        os.path.join(output_directory, game_name),
    ]
)
exporting_process.wait()
if exporting_process.returncode != 0:
    raise Exception("Failed to export godot game")
