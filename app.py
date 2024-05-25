from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from io import BytesIO
from flask import send_file
import pandas as pd
from flask_migrate import Migrate
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from smtplib import SMTPAuthenticationError
from datetime import datetime
from flask import request
from flask import Flask, jsonify


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for production use
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'missyhelle345@gmail.com'
app.config['MAIL_PASSWORD'] = 'zerw yuhi ovzm lppu'
app.config['MAIL_DEFAULT_SENDER'] = 'missyhelle345@gmail.com'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password):
        self.email = email
        self.password = password


class FormSubmission(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('form_submission', lazy=True))
    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    birthdate = db.Column(db.String(100))
    residential_address = db.Column(db.String(100))
    place_of_birth = db.Column(db.String(100))
    civil_status = db.Column(db.String(100))
    sex = db.Column(db.String(100))
    spouse = db.Column(db.String(100))
    father = db.Column(db.String(100))
    mother = db.Column(db.String(100))
    elementary_school = db.Column(db.String(100))
    elementary_attendance = db.Column(db.String(100))
    elementary_honors = db.Column(db.String(100))
    secondary_school = db.Column(db.String(100))
    secondary_attendance = db.Column(db.String(100))
    secondary_honors = db.Column(db.String(100))
    vocational_school = db.Column(db.String(100))
    vocational_attendance = db.Column(db.String(100))
    vocational_honors = db.Column(db.String(100))
    college_school = db.Column(db.String(100))
    college_attendance = db.Column(db.String(100))
    college_honors = db.Column(db.String(100))
    graduate_school = db.Column(db.String(100))
    graduate_attendance = db.Column(db.String(100))
    graduate_honors = db.Column(db.String(100))
    position_title = db.Column(db.String(100))
    department = db.Column(db.String(100))
    inclusive_dates = db.Column(db.String(100))
    position_title2 = db.Column(db.String(100))
    department2 = db.Column(db.String(100))
    inclusive_dates2 = db.Column(db.String(100))
    issue1 = db.Column(db.String(100))
    issue2 = db.Column(db.String(100))
    issue3 = db.Column(db.String(100))
    wish1 = db.Column(db.String(100))
    wish2 = db.Column(db.String(100))
    wish3 = db.Column(db.String(100))

    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)
class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)



def is_valid_credentials(email, password):
    user = Users.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

def is_logged_in():
    return 'email' in session

def submit_form(user_id, personal_info, family_background, educational_attainment, work_experience, top_issues, top_wishes):
    existing_submission = FormSubmission.query.filter_by(user_id=user_id).first()
    if existing_submission:
        # Update the existing form submission
        existing_submission.first_name = personal_info['first_name']
        existing_submission.middle_name = personal_info['middle_name']
        existing_submission.last_name = personal_info['last_name']
        birthdate_parts = personal_info['birthdate'].split('-')
        existing_submission.birthdate_year = birthdate_parts[0]
        existing_submission.birthdate_month = birthdate_parts[1]
        existing_submission.birthdate_day = birthdate_parts[2]
        existing_submission.residential_address = personal_info['residential_address']
        existing_submission.place_of_birth = personal_info['place_of_birth']
        existing_submission.civil_status = personal_info['civil_status']
        existing_submission.sex = personal_info['sex']
        existing_submission.spouse = family_background['spouse']
        existing_submission.father = family_background['father']
        existing_submission.mother = family_background['mother']
        existing_submission.elementary_school = educational_attainment['elementary']['school']
        existing_submission.elementary_attendance = educational_attainment['elementary']['period_of_attendance']
        existing_submission.elementary_honors = educational_attainment['elementary']['academic_honors']
        existing_submission.secondary_school = educational_attainment['secondary']['school']
        existing_submission.secondary_attendance = educational_attainment['secondary']['period_of_attendance']
        existing_submission.secondary_honors = educational_attainment['secondary']['academic_honors']
        existing_submission.vocational_school = educational_attainment['vocational']['school']
        existing_submission.vocational_attendance = educational_attainment['vocational']['period_of_attendance']
        existing_submission.vocational_honors = educational_attainment['vocational']['academic_honors']
        existing_submission.college_school = educational_attainment['college']['school']
        existing_submission.college_attendance = educational_attainment['college']['period_of_attendance']
        existing_submission.college_honors = educational_attainment['college']['academic_honors']
        existing_submission.graduate_school = educational_attainment['graduate']['school']
        existing_submission.graduate_attendance = educational_attainment['graduate']['period_of_attendance']
        existing_submission.graduate_honors = educational_attainment['graduate']['academic_honors']
        existing_submission.position_title = work_experience['position_title']
        existing_submission.department = work_experience['department']
        existing_submission.inclusive_dates = work_experience['inclusive_dates']
        existing_submission.position_title2 = work_experience['position_title2']
        existing_submission.department2 = work_experience['department2']
        existing_submission.inclusive_dates2 = work_experience['inclusive_dates2']
        existing_submission.issue1 = top_issues[0]
        existing_submission.issue2 = top_issues[1]
        existing_submission.issue3 = top_issues[2]
        existing_submission.wish1 = top_wishes[0]
        existing_submission.wish2 = top_wishes[1]
        existing_submission.wish3 = top_wishes[2]

        db.session.commit()
        return True  # Return True to indicate that the form was updated
    else:
        # Create a new form submission
        new_submission = FormSubmission(
            user_id=user_id,
            first_name=personal_info['first_name'],
            middle_name=personal_info['middle_name'],
            last_name=personal_info['last_name'],
            birthdate=personal_info['birthdate'],
            residential_address=personal_info['residential_address'],
            place_of_birth=personal_info['place_of_birth'],
            civil_status=personal_info['civil_status'],
            sex=personal_info['sex'],
            spouse=family_background['spouse'],
            father=family_background['father'],
            mother=family_background['mother'],
            elementary_school=educational_attainment['elementary']['school'],
            elementary_attendance=educational_attainment['elementary']['period_of_attendance'],
            elementary_honors=educational_attainment['elementary']['academic_honors'],
            secondary_school=educational_attainment['secondary']['school'],
            secondary_attendance=educational_attainment['secondary']['period_of_attendance'],
            secondary_honors=educational_attainment['secondary']['academic_honors'],
            vocational_school=educational_attainment['vocational']['school'],
            vocational_attendance=educational_attainment['vocational']['period_of_attendance'],
            vocational_honors=educational_attainment['vocational']['academic_honors'],
            college_school=educational_attainment['college']['school'],
            college_attendance=educational_attainment['college']['period_of_attendance'],
            college_honors=educational_attainment['college']['academic_honors'],
            graduate_school=educational_attainment['graduate']['school'],
            graduate_attendance=educational_attainment['graduate']['period_of_attendance'],
            graduate_honors=educational_attainment['graduate']['academic_honors'],
            position_title=work_experience['position_title'],
            department=work_experience['department'],
            inclusive_dates=work_experience['inclusive_dates'],
            position_title2=work_experience['position_title2'],
            department2=work_experience['department2'],
            inclusive_dates2=work_experience['inclusive_dates2'],
            issue1=top_issues[0],
            issue2=top_issues[1],
            issue3=top_issues[2],
            wish1=top_wishes[0],
            wish2=top_wishes[1],
            wish3=top_wishes[2]
        )
        db.session.add(new_submission)
        db.session.commit()
        return True


def create_excel_file(form_data):
    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Form Submission"

    # Set column widths
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 30

    # Add headers
    headers = ['Field', 'Value']
    ws.append(headers)

    # Add form data
    for field, value in form_data.items():
        ws.append([field, value])

    # Apply styles
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal='center', vertical='center')
    for cell in ws[1]:
        cell.font = header_font
        cell.alignment = header_alignment

    # Save the workbook
    excel_file_path = 'form_submission.xlsx'
    wb.save(excel_file_path)

    return excel_file_path

# Define a function to check if a user is an admin
def is_admin(email, password):
    # Replace this with your admin authentication logic
    return email == 'admin@example.com' and password == 'admin_password'

def admin_submissions():
    if 'admin' in session:
        form_submissions = FormSubmission.query.all()
        return render_template('admin_submissions.html', form_submissions=form_submissions)
    else:
        return 'Unauthorized', 401  # Unauthorized status code
@app.route('/admin/calendar', methods=['POST'])
def add_calendar_event():
    if 'admin' in session:
        if request.method == 'POST':
            event_name = request.form['event_name']
            event_date_str = request.form['event_date']  # Get date string from form
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()  # Convert to Python date object
            description = request.form['description']

            # Create new CalendarEvent object and add to database
            new_event = CalendarEvent(event_name=event_name, event_date=event_date, description=description)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('admin_calendar'))
    else:
        return 'Unauthorized', 401

# Inside your Flask app

# Update the reset_password function to dynamically fetch user email and password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = Users.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='email-confirm')
            link = url_for('reset_with_token', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Your link is {link}'
            
            # Use user-specific email and password for sending the email
            mail.username = user.email
            mail.password = user.password
            try:
                mail.send(msg)
                return 'A password reset link has been sent to your email.'
            except SMTPAuthenticationError:
                return 'Failed to send email. Incorrect email credentials.'
            except Exception as e:
                # General exception handling for debugging
                return f'An error occurred: {e}'
        else:
            return 'Email not found. Please try again.'

    return render_template('reset_password.html')



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # Token is valid for 1 hour
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        user = Users.query.filter_by(email=email).first()
        if user:
            try:
                user.password = generate_password_hash(new_password)
                db.session.commit()
                return 'Your password has been updated! <a href="/">Click here to return to the website page</a>'
            except Exception as e:
                print(f"Error updating password: {e}")
                db.session.rollback()  # Rollback changes in case of an error
                return 'An error occurred while updating your password. Please try again.'
        else:
            return 'User not found. Unable to update password.'
    
    return render_template('reset_with_token.html', token=token)

@app.route('/admin_home')
def admin_home():
    if 'admin' in session:
        return render_template('admin_home.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin_submissions')
def admin_submissions():
    if 'admin' in session:
        form_submissions = FormSubmission.query.all()
        return render_template('admin_submissions.html', form_submissions=form_submissions)
    else:
        return 'Unauthorized', 401  # Unauthorized status code
@app.route('/events')
def get_events():
    # Query events from your database
    events = CalendarEvent.query.all()
    
    # Convert events to a list of dictionaries
    event_list = []
    for event in events:
        event_data = {
            'event_name': event.event_name,
            'event_date': event.event_date.strftime('%Y-%m-%d'),  # Convert date to string
            'description': event.description
        }
        event_list.append(event_data)
    
    # Return JSON response
    return jsonify(event_list)


# Admin Calendar route
# Admin Calendar route
@app.route('/admin/calendar', methods=['GET', 'POST'])
def admin_calendar():
    if request.method == 'POST':
        # Handle form submission to add a new event
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        description = request.form['description']
        new_event = CalendarEvent(event_name=event_name, event_date=event_date, description=description)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('admin_calendar'))
    else:
        # Display existing events
        events = CalendarEvent.query.all()
        return render_template('admin_calendar.html', events=events)
   

# Calendar of Events route
@app.route('/calendar')
def calendar():
    events = CalendarEvent.query.all()
    return render_template('calendar.html', events=events)
from datetime import datetime

@app.route('/admin/calendar/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    if request.method == 'POST':
        # Update event details based on form submission
        event.event_name = request.form['event_name']
        
        # Convert the event date string to a Python date object
        event_date_str = request.form['event_date']
        event.event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        
        event.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin_calendar'))
    else:
        return render_template('edit_event.html', event=event)

@app.route('/admin/calendar/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('admin_calendar'))









@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if is_admin(email, password):
            session['admin'] = True
            return redirect(url_for('admin_home'))
        elif is_valid_credentials(email, password):
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password. Please try again.'

    return render_template('login.html')




@app.route('/export', methods=['GET'])
def export_data():
    if 'admin' in session:
        form_submissions = FormSubmission.query.all()
        data = []
        for submission in form_submissions:
            data.append({
                'First Name': submission.first_name,
                'Middle Name': submission.middle_name,
                'Last Name': submission.last_name,
                'Birthdate': submission.birthdate,
                'Residential Address': submission.residential_address,
                'Place of Birth': submission.place_of_birth,
                'Civil Status': submission.civil_status,
                'Sex': submission.sex,
                'Spouse': submission.spouse,
                'Father': submission.father,
                'Mother': submission.mother,
                'Elementary School': submission.elementary_school,
                'Elementary Attendance': submission.elementary_attendance,
                'Elementary Honors': submission.elementary_honors,
                'Secondary School': submission.secondary_school,
                'Secondary Attendance': submission.secondary_attendance,
                'Secondary Honors': submission.secondary_honors,
                'Vocational School': submission.vocational_school,
                'Vocational Attendance': submission.vocational_attendance,
                'Vocational Honors': submission.vocational_honors,
                'College School': submission.college_school,
                'College Attendance': submission.college_attendance,
                'College Honors': submission.college_honors,
                'Graduate School': submission.graduate_school,
                'Graduate Attendance': submission.graduate_attendance,
                'Graduate Honors': submission.graduate_honors,
                'Position Title': submission.position_title,
                'Department': submission.department,
                'Inclusive Dates': submission.inclusive_dates,
                'Position Title2': submission.position_title2,
                'Department2': submission.department2,
                'Inclusive Dates2': submission.inclusive_dates2,
                'Issue1': submission.issue1,
                'Issue2': submission.issue2,
                'Issue3': submission.issue3,
                'Wish1': submission.wish1,
                'Wish2': submission.wish2,
                'Wish3': submission.wish3
            })

        df = pd.DataFrame(data)

        # Export DataFrame to Excel
        excel_file = 'form_submissions.xlsx'
        df.to_excel(excel_file, index=False)

        # Send the Excel file as a response
        return send_file(excel_file, as_attachment=True)
    else:
        return 'Unauthorized', 401  # Unauthorized status code



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if Users.query.filter_by(email=email).first():
            return 'Email already exists. Please choose another one.'
        else:
            hashed_password = generate_password_hash(password)
            new_user = Users(email, hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return "Signup successful. You can now login. Click <a href='/login'>here</a> to go back to log in."
    return render_template('signup.html')

@app.route('/home')
def home():
    if is_logged_in():
        email = session['email']
        return render_template('home.html', email=email)
    else:
        return redirect(url_for('login'))
# Add this route to your Flask application
@app.route('/sk_officials')
def sk_officials():
    # Define SK officials data (replace this with your actual data)
    sk_officials_data = {
        'chairman': 'Zul Fiqar Ali',
        'secretary': 'Irish Mae Novem Gutierez',
        'treasurer': 'Ellen Mae Olegario',
        'kagawad1': 'Kim Hesham Kautin',
        'kagawad2': 'Alyssa Udik',
        'kagawad3': 'Johaimin Hadjimanan',
        'kagawad4': 'Sohaira Marohom',
        'kagawad5': 'Norjana Diragen',
        'kagawad6': 'Muslimen Madidis',
        'kagawad7': 'Fatma Mae Tomawis',
    }
    return render_template('sk_officials.html', sk_officials=sk_officials_data)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/hello', methods=['GET', 'POST'])
def form():
    if not is_logged_in():
        return redirect(url_for('login'))

    user_email = session['email']
    user = Users.query.filter_by(email=user_email).first()

    # Fetch existing form submission data if it exists
    existing_submission = FormSubmission.query.filter_by(user_id=user._id).first()

    if request.method == 'POST':
        birthdate_month = request.form['birthdate_month']
        birthdate_day = request.form['birthdate_day']
        birthdate_year = request.form['birthdate_year']
        birthdate = f"{birthdate_year}-{birthdate_month}-{birthdate_day}"

        personal_info = {
            'first_name': request.form['first_name'],
            'middle_name': request.form['middle_name'],
            'last_name': request.form['last_name'],
            'birthdate': birthdate,
            'residential_address': request.form['residential_address'],
            'place_of_birth': request.form['place_of_birth'],
            'civil_status': request.form['civil_status'],
            'sex': request.form['sex']
        }
        family_background = {
            'spouse': request.form['spouse'],
            'father': request.form['father'],
            'mother': request.form['mother']
        }

        educational_attainment = {
            'elementary': {
                'school': request.form['elementary_school'],
                'period_of_attendance': request.form['elementary_attendance'],
                'academic_honors': request.form['elementary_honors']
            },
            'secondary': {
                'school': request.form['secondary_school'],
                'period_of_attendance': request.form['secondary_attendance'],
                'academic_honors': request.form['secondary_honors']
            },
            'vocational': {
                'school': request.form['vocational_school'],
                'period_of_attendance': request.form['vocational_attendance'],
                'academic_honors': request.form['vocational_honors']
            },
            'college': {
                'school': request.form['college_school'],
                'period_of_attendance': request.form['college_attendance'],
                'academic_honors': request.form['college_honors']
            },
            'graduate': {
                'school': request.form['graduate_school'],
                'period_of_attendance': request.form['graduate_attendance'],
                'academic_honors': request.form['graduate_honors']
            }
        }

        work_experience = {
            'position_title': request.form['position_title'],
            'department': request.form['department'],
            'inclusive_dates': request.form['inclusive_dates'],
            'position_title2': request.form['position_title2'],
            'department2': request.form['department2'],
            'inclusive_dates2': request.form['inclusive_dates2']
        }

        top_issues = [
            request.form['issue1'],
            request.form['issue2'],
            request.form['issue3']
        ]

        top_wishes = [
            request.form['wish1'],
            request.form['wish2'],
            request.form['wish3']
        ]

        form_submission = {
            'personal_info': personal_info,
            'family_background': family_background,
            'educational_attainment': educational_attainment,
            'work_experience': work_experience,
            'top_issues': top_issues,
            'top_wishes': top_wishes
        }

        if submit_form(user._id, personal_info, family_background, educational_attainment, work_experience, top_issues, top_wishes):
            return render_template('form_submission.html', message="Your form has been submitted.", form_submission=form_submission)
        else:
            return 'You have already submitted a form.'

    # If there's an existing submission, populate the form with the existing data
    if existing_submission:
        return render_template('form.html', existing_data=existing_submission)

    return render_template('form.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 