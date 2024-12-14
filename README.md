# Elevenlabs Synthetic Dataset Generator

### Place this python file in a directory alongside a metadata.csv file
the metadata.csv MUST contain only a single pipe per line
```csv
file_name|text content in the file
```

The script creates a venv, installs deps, activates venv, creates an output directory called output_audio, and begins populating it with the content of the csv, generating the dataset text and saving each file with the associated name.

clone this repo, and add your keys to test with the included numbers.csv

Just enter your Elevenlabs API key and desired voice id, place the script next to your metadata.csv and let her rip!
