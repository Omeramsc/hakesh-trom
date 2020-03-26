from flask import render_template, jsonify
from app_init import app
from models import Campaign


@app.route('/campaigns_test')
def campaigns_test():
    try:
        campaigns = Campaign.query.all()
        return jsonify([e.serialize() for e in campaigns])
    except Exception as e:
        return str(e)


@app.route('/')
def home():
    return render_template('/index.html')


@app.route('/first_steps')
def first_steps():
    return render_template('/first_steps.html')


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
