import os
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_mail import Mail, Message

app = Flask(__name__)
is_prod = os.environ.get('IS_HEROKU', None)

if os.path.isfile('settings.cfg'):
    app.config.from_pyfile('settings.cfg')
else:
    values = ['MAIL_USERNAME','MAIL_PASSWORD', 'MAIL_PORT', 'MAIL_SERVER', 'MAIL_USE_SSL'] 
    for val in values:
        app.config[val] = os.environ[val]
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
mail = Mail(app)

@app.route('/')
@app.route('/landing.html')
def index():
    return render_template('landing.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/portfolio-link')
def download_portfolio():
    return send_from_directory(os.path.join(app.root_path, 'static/files'),
                               'Malcolm LeClair Portfolio.pdf')

@app.route('/contact_me', methods=['POST'])
def contact():
    form_data = request.form.to_dict()
    msg = Message('[malcolmleclair.com] New Message from {}'.format(form_data['name']),
            sender='info@malcolmleclair.com',
            recipients=['malcolmleclair@gmail.com'])
    msg.html = render_template('contact_form.html', form=form_data)
    mail.send(msg)
    return jsonify({'success': True}) 


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
