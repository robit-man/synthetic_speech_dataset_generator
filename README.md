# Elevenlabs Synthetic Dataset Generator

### Place this python file in a directory alongside a metadata.csv file
the metadata.csv MUST contain only a single pipe per line
```csv
file_name|text content in the file
```

Then run the generator python script
```
python3 generate.py
```

Now you can convert the output mp3 files to wav
```
python3 convert.py
```


The script creates a venv, installs deps, activates venv, creates an output directory called output_audio, and begins populating it with the content of the csv, generating the dataset text and saving each file with the associated name.

clone this repo, and add your Elevenlabs API key and desired voice id, and test with the included numbers.csv.

The script will automatically pick up where it left off in the csv given a failure mode when you re-start the script.
