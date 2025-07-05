# reset_db.py

from server import app, db, Student

with app.app_context():
    deleted = db.session.query(Student).delete()
    db.session.commit()
    print(f"✅ تم حذف {deleted} طالب(اً) من قاعدة البيانات.")
