from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/first_steps')
def first_steps():
    return render_template('/first_steps.html')

@app.route('/manage_campaign')
def manage_campaign():
    return render_template('/manage_campaign.html')


@app.route('/manage_campaign/campaign_control_panel')
def campaign_control_panel():
    return render_template('/campaign_control_panel.html')


@app.route('/donation', methods=['GET', 'POST'])
def donation():
    # if request.method == 'GET':
    # INSERT INTO DB / MOVE TO PP/bit
    # return render_template('/<---->.html')
    return render_template('/donation.html')


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    # GET REPORTS FROM DB
    return render_template('/reports.html')


@app.route('/create_report', methods=['GET', 'POST'])
def create_report():
    # if request.method == 'GET':
    # INSERT INTO DB
    # return redirect(url_for('report'))
    return render_template('/create_report.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
