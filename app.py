import hashlib # <--- Add this line
from flask import Flask, render_template, request
from database import get_db_connection
# Our clean import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form.get('applicant_name')
        nrc = request.form.get('nrc_number')
        category = request.form.get('cat')
        
        # 1. Create the Raw String (The data we want to lock)
        raw_data = f"{name}{nrc}{category}"
        
        # 2. Generate the SHA-256 Hash (The "Blockchain" part)
        # We turn the text into bytes, then hash it into a hex string
        data_hash = hashlib.sha256(raw_data.encode()).hexdigest()
        
        # 3. Create a readable Receipt ID (for humans)
        # We take the first 8 characters of the hash to make it look cool
        receipt_id = f"CDF-{data_hash[:8].upper()}"

        # 4. Save everything (including the full hash)
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO applications (name, nrc, category, receipt_id, data_hash) 
            VALUES (?, ?, ?, ?, ?)
        ''', (name, nrc, category, receipt_id, data_hash))
        conn.commit()
        conn.close()

        return render_template('success.html', receipt=receipt_id, hash=data_hash)

    return render_template('apply.html')

# ... Keep your other routes (Constituencies, LiveMap, etc.) below ...

#For the constituencies tab
@app.route('/Constituencies')
def constituencies():
    # This looks for constituencies.html inside your templates folder
    return render_template('constituencies.html')

@app.route('/reports')
def reports():
    # This looks for reports.html inside your templates folder
    return render_template('reports.html')

@app.route('/audits')  # This is the URL address
def audits():          # This is the name url_for looks for!
    return render_template('audits.html')

@app.route('/LiveMap') #This is the routing code for the map
def LiveMap():
    return render_template('LiveMap.html')

@app.route('/admin/applications')
def view_applications():
    conn = get_db_connection()
    # This pulls every row from your database
    apps = conn.execute('SELECT * FROM applications ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('admin_view.html', applications=apps)

if __name__ == '__main__':
    app.run(debug=True)