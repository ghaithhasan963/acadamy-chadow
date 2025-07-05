from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'shadow_secret_123'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

socketio = SocketIO(app)

# 🎓 نموذج الطالب
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    session_code = db.Column(db.String(50), nullable=False)
    progress = db.Column(db.Text, default='[]')  # JSON list
    score = db.Column(db.Integer, default=0)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# 🏠 الصفحة الرئيسية (تسجيل الدخول)
@app.route('/')
def home():
    return render_template('login.html', now=datetime.utcnow())

# ✅ تسجيل الدخول
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('student_name')
    session_code = request.form.get('session_code')

    if not name or not session_code:
        return "يرجى إدخال الاسم ورمز الجلسة", 400

    student = Student(name=name.strip(), session_code=session_code.strip())
    db.session.add(student)
    db.session.commit()

    return render_template('index.html', student=student)

# 📚 لوحة الطالب
@app.route('/dashboard/<int:student_id>')
def dashboard(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('dashboard.html', student=student)

# 📈 تتبع التقدّم
@app.route('/track_progress/<int:student_id>/<page_name>', methods=['POST'])
def track_progress(student_id, page_name):
    student = Student.query.get_or_404(student_id)
    try:
        pages = json.loads(student.progress or "[]")
    except:
        pages = []
    if page_name not in pages:
        pages.append(page_name)
        student.progress = json.dumps(pages)
        db.session.commit()
    return jsonify({'status': 'saved', 'progress': pages})

# 🧪 حفظ النتيجة
@app.route('/submit_score/<int:student_id>', methods=['POST'])
def submit_score(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    student.score = int(data.get('score', 0))
    db.session.commit()
    return jsonify({'status': 'saved', 'score': student.score})

# 🔎 جلب النتيجة
@app.route('/get_score/<int:student_id>')
def get_score(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({'score': student.score})

# 🔍 جلب التقدّم
@app.route('/get_progress/<int:student_id>')
def get_progress(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        pages = json.loads(student.progress or '[]')
    except:
        pages = []
    return jsonify({'pages': pages})

# 📄 صفحة فردية لكل طالب
@app.route('/student/<int:student_id>')
def student_profile(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)

# 🔐 لوحة المعلم برمز دخول
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '4321':
            session['admin_access'] = True
            return redirect('/admin')
        return render_template('admin_login.html', error="رمز الدخول غير صحيح!")

    if not session.get('admin_access'):
        return render_template('admin_login.html')

    students = Student.query.order_by(Student.login_time.desc()).all()
    for student in students:
        try:
            pages = json.loads(student.progress or "[]")
        except:
            pages = []
        student.progress_display = ', '.join(pages) if pages else '–'

    return render_template('admin.html', students=students)

# 📣 بث الرسالة من المعلم
@socketio.on('admin_message')
def handle_admin_message(data):
    emit('show_message', data, broadcast=True)

# 🧭 عرض الصفحات التعليمية
 
@app.route('/cs50/<int:student_id>')
def cs50(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('cs50.html', student=student)

@app.route('/network/<int:student_id>')
def network(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('network.html', student=student)

@app.route('/kali/<int:student_id>')
def kali(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('kali.html', student=student)

@app.route('/kali-env/<int:student_id>')
def kalienv(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('kali-env.html', student=student)

@app.route('/about-tols/<int:student_id>')
def abouttols(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('about-tools.html', student=student)

@app.route('/terminal/<int:student_id>')
def terminal(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('terminal.html', student=student)

@app.route('/tools/<int:student_id>')
def tools(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('tools.html', student=student)

@app.route('/exploit/<int:student_id>')
def exploit(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('exploit.html', student=student)

@app.route('/lap/<int:student_id>')
def lap(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('lap.html', student=student)

@app.route('/sql-lap/<int:student_id>')
def skllap(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('sql-lap.html', student=student)

@app.route('/metasploit-lap/<int:student_id>')
def metasploitlap(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('metasploit-lap.html', student=student)

@app.route('/summary/<int:student_id>')
def sumary(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('summary.html', student=student)

@app.route('/final-test/<int:student_id>')
def finaltest(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('final-test.html', student=student)

# 🧱 عرض صفحات عادية
@app.route('/<path:page>')
def render_page(page):
    try:
        return render_template(page)
    except:
        return render_template('not-found.html'), 404

# 🚀 تشغيل السيرفر
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
