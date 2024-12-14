import os
import sys
import subprocess
from pathlib import Path

# Configurations
VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
NEEDED_PACKAGES = ["elevenlabs"]
OUTPUT_DIR = "./output_audio"

# ElevenLabs Config
API_KEY = "ELEVENLABS_API_KEY"
VOICE_ID = "ELEVENLABS_VOICE_ID"
MP3_OUTPUT_FORMAT = "mp3_22050_32"

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


if not in_venv():
    setup_venv()
    relaunch_in_venv()

#############################################
# Step 2: Imports after venv setup          #
#############################################
import csv
from elevenlabs import ElevenLabs

#############################################
# Step 3: Main Logic                        #
#############################################
def process_csv_and_generate_audio(csv_file):
    """
    Process a CSV file and generate audio for each row using ElevenLabs API.
    """
    client = ElevenLabs(api_key=API_KEY)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Processing CSV: {csv_file}")
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="|")

        for row in reader:
            if len(row) < 2:
                print(f"Skipping malformed row: {row}")
                continue

            # Extract filename and text
            base_filename = row[0].strip()
            text = row[1].strip()
            mp3_filename = os.path.join(OUTPUT_DIR, f"{base_filename}.mp3")

            # Skip if the file already exists
            if os.path.exists(mp3_filename):
                print(f"Skipping {base_filename}, file already exists.")
                continue

            print(f"Generating audio for: {base_filename} with text: {text}")

            try:
                # Generate speech using ElevenLabs API
                audio_generator = client.text_to_speech.convert(
                    voice_id=VOICE_ID,
                    model_id="eleven_multilingual_v2",
                    text=text,
                    output_format=MP3_OUTPUT_FORMAT,
                )

                # Consume generator and write audio as bytes
                with open(mp3_filename, "wb") as audio_file:
                    for chunk in audio_generator:
                        audio_file.write(chunk)

                print(f"MP3 saved to: {mp3_filename}")

            except Exception as e:
                print(f"Error generating audio for {base_filename}: {e}")
                continue


def find_csv_files():
    """
    Finds all CSV files in the current directory.
    """
    import glob

    return glob.glob("*.csv")


def main():
    """
    Main script logic.
    """
    # Find CSV files in the current directory
    csv_files = find_csv_files()
    if not csv_files:
        print("No CSV files found in the current directory.")
        sys.exit(1)

    for csv_file in csv_files:
        process_csv_and_generate_audio(csv_file)


if __name__ == "__main__":
    main()
