# Dump Azure Transcriptions
Iterates over Microsoft Azure Speech to Text Transcriptions and saves combinedRecognizedPhrases as transcriptions.json file.

## Installation 
Clone repo into desired directory and run
```
pip install -r requirements.txt
```

## Configuration
Provide API Key, Region and Transcription ID in .env file. Like this:
```
KEY=x6e646jd7f8tri45d
REGION=westus
ID=b4rt6590-9v3da-3m21-8c27-x444c406m2a4
```

Script may cache all successful remote responses in **cache** directory if you create it.

## Run
```
python azure-fetch-transcriptions.py
```
