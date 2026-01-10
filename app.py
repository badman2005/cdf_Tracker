from flask import Flask, render_template

# This creates the 'App' object
app = Flask(__name__)

# This tells the 'Brain' what to do when someone visits the home page
@app.route('/')
def home():
    return render_template('index.html')

#For the constituencies tab
@app.route('/constituencies')
def constituencies():
    # This looks for constituencies.html inside your templates folder
    return render_template('constituencies.html')

@app.route('/reports')
def reports():
    # This looks for reports.html inside your templates folder
    return render_template('reports.html')


# This starts the server
if __name__ == '__main__':
    app.run(debug=True)