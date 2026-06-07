# Email Assistant App

An AI powered email drafting web application built with Flask and LM Studio.

## Features
- Welcome popup explaining the app on first load
- Accepts input in any language or broken English
- Always generates professional English emails
- Personalised salutations using recipient's name
- Sign off with sender's name and role automatically
- Select tone - formal, casual or persuasive
- Editable email body - modify before copying
- Copy subject separately for Outlook
- Copy email body separately for Outlook
- Open directly in Outlook with one click
- Auto placeholders for missing details like date, time, location
- User details saved in browser - no login needed
- Deployed live on Render

## Tech Stack
- Python
- Flask
- LM Studio (local AI)
- HTML/JavaScript

## How to Run
1. Start LM Studio and load the Gemma-4 model
2. Start the local server in LM Studio
3. Run `python app.py` in terminal
4. Open `http://127.0.0.1:5000` in your browser