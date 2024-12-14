import os
import sys
import subprocess
from pathlib import Path

# Configurations
VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
NEEDED_PACKAGES = ["ffmpeg-python"]
MP3_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_audio")
WAV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wav")

#############################################
# Step 1: Setup Virtual Environment         #
#############################################
def in_venv():
    """
    Check if the script is already running inside a virtual environment.
    """
    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )


def setup_venv():
    """
    Create a virtual environment if it doesn't exist.
    Install required packages.
    """
    if not os.path.isdir(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

    pip_path = os.path.join(
        VENV_DIR, "bin", "pip"
    ) if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "pip.exe")
    subprocess.check_call([pip_path, "install", "--upgrade", "pip"])
    subprocess.check_call([pip_path, "install"] + NEEDED_PACKAGES)


def relaunch_in_venv():
    """
    Relaunch the script using the Python interpreter from the virtual environment.
    """
    python_path = os.path.join(
        VENV_DIR, "bin", "python"
    ) if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "python.exe")
    os.execv(python_path, [python_path] + sys.argv)


def check_ffmpeg_installed():
    """
    Check if ffmpeg is installed and available in the system PATH.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not found in the system PATH.")
        print("Please install ffmpeg and ensure it is available in your PATH.")
        sys.exit(1)


if not in_venv():
    setup_venv()
    relaunch_in_venv()

#############################################
# Step 2: Imports after venv setup          #
#############################################
import ffmpeg

#############################################
# Step 3: Main Logic                        #
#############################################
def convert_mp3_to_wav(mp3_file, wav_file):
    """
    Convert an MP3 file to WAV format using ffmpeg.
    """
    try:
        print(f"Converting: {mp3_file} -> {wav_file}")
        ffmpeg.input(mp3_file).output(wav_file, format="wav").run(overwrite_output=True)
        print(f"Conversion successful: {wav_file}")
    except Exception as e:
        print(f"Error converting {mp3_file}: {e}")


def process_mp3_files():
    """
    Process all MP3 files in the 'mp3' directory and convert them to WAV files in the 'wav' directory.
    """
    if not os.path.exists(MP3_DIR):
        print(f"MP3 directory '{MP3_DIR}' not found. Exiting.")
        sys.exit(1)

    # Ensure WAV directory exists
    os.makedirs(WAV_DIR, exist_ok=True)

    for mp3_file in os.listdir(MP3_DIR):
        if mp3_file.endswith(".mp3"):
            mp3_path = os.path.join(MP3_DIR, mp3_file)
            wav_filename = os.path.splitext(mp3_file)[0] + ".wav"
            wav_path = os.path.join(WAV_DIR, wav_filename)

            # Skip conversion if the WAV file already exists
            if os.path.exists(wav_path):
                print(f"Skipping already converted file: {wav_path}")
                continue

            convert_mp3_to_wav(mp3_path, wav_path)


def main():
    """
    Main script logic.
    """
    check_ffmpeg_installed()  # Ensure ffmpeg is available
    process_mp3_files()


if __name__ == "__main__":
    main()
