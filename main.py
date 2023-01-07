import sqlite3
import datetime
from flask import Flask, request, send_file

try:
    conn = sqlite3.connect('share.db', check_same_thread=False)
    curs = conn.cursor()

    curs.execute('CREATE TABLE IF NOT EXISTS shares (id TEXT PRIMARY KEY, route TEXT, pw TEXT, expire TEXT)')
    conn.commit()
except Exception as e:
    print(e)
    exit()

app = Flask(__name__)


@app.route('/download/<file_id>')
def download(file_id):
    curs.execute('SELECT route, pw, expire FROM shares WHERE id=?', (file_id,))
    result = curs.fetchone()
    if not result:
        return '파일 없음'
    route, pw, expire = result

    if datetime.datetime.strptime(expire, '%Y-%m-%d %H:%M:%S') < datetime.datetime.today():
        return '만료됨'

    if pw:
        if pw != request.args.get('pw', ''):
            return '비밀번호 틀림'

    return send_file(route, as_attachment=True, download_name=route.split('/')[-1])


app.run(host="0.0.0.0", port=8818)
