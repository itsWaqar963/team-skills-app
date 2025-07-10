import os

from flask import Flask, render_template, request, redirect
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 Function to write to Google Sheet
def write_to_google_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = json.loads(os.environ['GOOGLE_CREDS_JSON'])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)

    sheet = client.open("TeamSkillsData").sheet1  # Make sure this matches your Google Sheet name
    row = list(data.values())
    sheet.append_row(row)

app = Flask(__name__)

# 🔹 Route to show the form
@app.route('/')
def form():
    return render_template('form.html')

# 🔹 Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form['name'],
        'tech_stack': ', '.join(request.form.getlist('tech_stack')),
        'interest': request.form['interest'],
        'projects': request.form['projects'],
        'time': request.form['time'],
        'skills_to_learn': request.form['skills_to_learn'],
        'contribute': request.form['contribute']
    }

    # Save to CSV
    with open('responses.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

    # Save to Google Sheets
    write_to_google_sheet(data)

    return redirect('/')

# 🔹 Route to view responses in HTML table
@app.route('/responses')
def view_responses():
    try:
        with open('responses.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        return "No responses yet. Submit the form first."

    if not rows:
        return "No responses yet."

    headers = rows[0]
    data_rows = rows[1:]

    return render_template('responses.html', headers=headers, rows=data_rows)

# 🔹 Run the app
if __name__ == '__main__':
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

