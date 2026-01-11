import hashlib
import sqlite3
from flask import Flask, render_template, request, jsonify
from database import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Constituencies')
def constituencies():
    return render_template('constituencies.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/audits')
def audits():
    return render_template('audits.html')

@app.route('/LiveMap')
def LiveMap():
    return render_template('LiveMap.html')

@app.route('/api/projects')
def get_projects():
    """Returns GPS data and Inspection Photos for the map"""
    conn = get_db_connection()
    # Added image_url to the query
    query = 'SELECT title, constituency, category, lat, lng, image_url FROM applications WHERE lat IS NOT NULL'
    projects = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in projects])

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form.get('applicant_name')
        nrc = request.form.get('nrc_number')
        category = request.form.get('cat')
        
        raw_data = f"{name}{nrc}{category}"
        data_hash = hashlib.sha256(raw_data.encode()).hexdigest()
        receipt_id = f"CDF-{data_hash[:8].upper()}"

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO applications (name, nrc, category, receipt_id, data_hash) 
            VALUES (?, ?, ?, ?, ?)
        ''', (name, nrc, category, receipt_id, data_hash))
        conn.commit()
        conn.close()

        return render_template('success.html', receipt=receipt_id, hash=data_hash)

    return render_template('apply.html')

@app.route('/admin/applications')
def view_applications():
    conn = get_db_connection()
    apps = conn.execute('SELECT * FROM applications ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('admin_view.html', applications=apps)

if __name__ == '__main__':
    app.run(debug=True)