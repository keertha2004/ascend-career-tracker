from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import io
import base64
import psycopg2
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from collections import defaultdict, Counter
from psycopg2.extras import DictCursor

from utils.resume_parser import extract_resume_text
from utils.match_logic import calculate_match_score
from utils.db_config import get_db_connection
from utils.resume_improver import generate_improved_resume
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, flash
from utils.db_config import get_db_connection
from utils.auth import User
from flask import Flask, session, redirect, url_for



app = Flask(__name__)
app.secret_key = 'f9a8e1c59c3f44be929e7c81d45a11ccd'

import psycopg2
import psycopg2.extras

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    conn.autocommit = True
    return conn


# --- Config ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_chart_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# ===========================
# ROUTES
# ===========================

@app.route('/')
def home():
    return render_template("index.html")

# --- Resume Upload + Analysis ---
@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']
        job_desc = request.form['job_desc']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            resume_text = extract_resume_text(filepath)
            match_score = calculate_match_score(resume_text, job_desc)

            return render_template('result.html',
                                   resume_text=resume_text,
                                   job_desc=job_desc,
                                   match_score=match_score)
    return render_template('upload.html')

# --- Improve Resume ---
@app.route('/improve', methods=['POST'])
def improve_resume():
    resume_text = request.form['resume_text']
    job_desc = request.form['job_desc']

    improved_text = generate_improved_resume(resume_text, job_desc)
    return render_template("improved_resume.html", improved_text=improved_text)

# --- Download PDF ---
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    text = request.form['resume_text']
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    for line in text.split('\n'):
        p.drawString(40, y, line.strip())
        y -= 15
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='Improved_Resume.pdf', mimetype='application/pdf')

# --- Job Tracker ---
@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if 'email' not in session:
        return redirect('/login')

    user_email = session['email']  # Get current user's email

    if request.method == 'POST':
        company = request.form['company']
        title = request.form['title']
        status = request.form['status']
        deadline = request.form['deadline']
        score = request.form['score']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(""" 
        INSERT INTO applications (company_name, job_title, status, deadline, match_score, user_email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,  (company, title, status, deadline, score, user_email))
        conn.commit()
        cur.close()
        conn.close()


        return redirect('/tracker')

    # ✅ Fetch only the jobs added by this user
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM applications WHERE user_email = %s", (user_email,))
    jobs = cur.fetchall()
    cur.close()
    conn.close()


    return render_template('tracker.html', jobs=jobs)


# --- Score Plot Dashboard ---


@app.route('/score-plot')
def score_plot():
    if 'email' not in session:
        return redirect('/login')

    user_email = session['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 🚀 Only fetch jobs for the current user
    cursor.execute("SELECT company_name, match_score, status, deadline FROM applications WHERE user_email = %s ORDER BY deadline", (user_email,))
    data = cursor.fetchall()
    conn.close()

   # Filter out rows that have None for required fields
    filtered_data = [row for row in data if row['match_score'] is not None and row['company_name'] and row['status'] and row['deadline']]

    companies = [row['company_name'] for row in filtered_data]
    scores = [row['match_score'] for row in filtered_data]
    statuses = [row['status'] for row in filtered_data]
    deadlines = [row['deadline'].strftime("%Y-%m") for row in filtered_data]


     # ✅ NEW: Summary statistics
    total_apps = len(data)
    low_score_count = sum(1 for score in scores if score is not None and score < 60)

    if scores:
       avg_score = round(sum(scores) / len(scores), 2)
    else:
       avg_score = 0


    # (your existing chart generation code continues here...)


    # 1. Match Score per Company
    fig1, ax1 = plt.subplots()
    ax1.bar(companies, scores, color="#71ACE0")  # Indigo-600
    ax1.set_title('Match Score per Company')
    ax1.set_xlabel('Company')
    ax1.set_ylabel('Score (%)')
    ax1.tick_params(axis='x', rotation=45)
    chart_url = generate_chart_image(fig1)

    # 2. Avg Match Score by Status
    status_score_map = defaultdict(list)
    for status, score in zip(statuses, scores):
        if score is not None and not (isinstance(score, float) and score != score):  # skip NaN
            status_score_map[status].append(score)
    avg_score_by_status = {s: sum(v)/len(v) for s, v in status_score_map.items() if v}
    fig2a, ax2a = plt.subplots()
    ax2a.bar(avg_score_by_status.keys(), avg_score_by_status.values(), color="#71A3DB")  # Blue-400
    ax2a.set_title("📊 Avg Match Score by Status")
    ax2a.set_ylabel("Avg Score (%)")
    skills_chart_url = generate_chart_image(fig2a)

    # 3. Most Applied Companies
    company_counts = Counter(companies)
    fig3a, ax3a = plt.subplots()
    ax3a.barh(list(company_counts.keys()), list(company_counts.values()), color="#C4C1E9D2")  # Blue-500
    ax3a.set_title("🏢 Companies You Applied to Most")
    ax3a.set_xlabel("No. of Applications")
    improvement_chart_url = generate_chart_image(fig3a)

    # 4. Application Status Distribution
    status_counts = Counter(statuses)
    pie_colors = ["#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD"]  # Dark to light blues
    fig4a, ax4a = plt.subplots()
    ax4a.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%', startangle=90, colors=pie_colors)
    ax4a.set_title("🧭 Application Status Distribution")
    status_chart_url = generate_chart_image(fig4a)

    # 5. Avg Resume Match Over Time
    timeline = defaultdict(list)
    for date, score in zip(deadlines, scores):
        timeline[date].append(score)
    months = sorted(timeline.keys())
    avg_scores = [sum(timeline[m])/len(timeline[m]) for m in months]
    fig5a, ax5a = plt.subplots()
    ax5a.plot(months, avg_scores, marker='o', color="#1E3A8A")  # Blue-600
    ax5a.set_title("📈 Avg Match Score Over Time")
    ax5a.set_xlabel("Month")
    ax5a.set_ylabel("Avg Score (%)")
    time_chart_url = generate_chart_image(fig5a)

    # 6. Top Companies by Match Score
    sorted_data = sorted(zip(companies, scores), key=lambda x: x[1], reverse=True)
    top_companies = [x[0] for x in sorted_data]
    top_scores = [x[1] for x in sorted_data]
    fig6a, ax6a = plt.subplots()
    ax6a.barh(top_companies, top_scores, color="#60A5FA")  # Blue-700
    ax6a.set_title("🏆 Top Companies by Resume Match")
    ax6a.invert_yaxis()
    top_chart_url = generate_chart_image(fig6a)

    # 7. Applications per Month
    month_counter = Counter(deadlines)
    months_applied = sorted(month_counter.keys())
    count_applied = [month_counter[m] for m in months_applied]
    fig7a, ax7a = plt.subplots()
    ax7a.bar(months_applied, count_applied, color="#73B9B9F6")  # Blue-200
    ax7a.set_title("📅 Applications per Month")
    ax7a.set_xlabel("Month")
    ax7a.set_ylabel("Applications")
    apps_chart_url = generate_chart_image(fig7a)

    return render_template('score_plot.html',
                           chart_url=chart_url,
                           skills_chart_url=skills_chart_url,
                           improvement_chart_url=improvement_chart_url,
                           status_chart_url=status_chart_url,
                           time_chart_url=time_chart_url,
                           top_chart_url=top_chart_url,
                           apps_chart_url=apps_chart_url,
                            total_apps=total_apps,
        low_score_count=low_score_count,
        avg_score=avg_score)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (int(user_id),))
    user = cursor.fetchone()
    conn.close()
    return User(user) if user else None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_hash = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()


        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']   # ✅ ADD THIS LINE
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')


@app.route('/blog')
def blog_home():
    return render_template('blog_home.html')  # You can list all blog articles here


@app.route('/blog/resume-mistakes')
def blog_resume_mistakes():
    return render_template('blog_resume_mistakes.html')

@app.route('/blog/ai-job-search')
def blog_ai_job_search():
    return render_template('blog_ai_job_search.html')


@app.route('/confirm_logout', methods=['GET', 'POST'])
def confirm_logout():
    if request.method == 'POST':
        # Optional: validate password here if needed
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for('home'))
    return render_template("confirm_logout.html")



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))



# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
