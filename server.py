# coding:utf8
# author:蓝一潇 20174899
from flask import Flask, jsonify, request
import sqlite3
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/get-testpaper')
def get_test_paper():
    with open('paper', 'rb') as f:
        p = f.readlines()
        f.close()
        res = {}
        for idx in range(len(p)):
            temp = p[idx].split('-***-')
            res[idx+1] = {'content': temp[0]+'\n'+temp[1]}
    # return jsonify({1:{'content': '"CHINA!" 这个推特是谁发送的？ \n A.特朗普 B.希拉里 C.拜登 D.奥巴马', }, 2:{'content': '美国死亡人数已经达到了？ \n A.10K B. 1k C.200K D.全死了'}, 3:{'content': '被警察杀害的黑人叫做？ \nA.乔治弗洛伊德 B.马丁路德金 C.奥巴马 D.迪卡普里奥莱昂纳多'}, 4:{'content': '东北大学的英文缩写是？\n A.NEU B.BEU C.CEU D.DEU'}}), 200
    return jsonify(res), 200

@app.route('/handin', methods=['POST'])
def handin():

    with open('paper', 'rb') as f:
        p = f.readlines()
        f.close()
        ans = {}
        for idx in range(len(p)):
            temp = p[idx].split('-***-')
            ans[idx+1] = {'A':'A' in temp[2], 'B':'B' in temp[2], 'C':'C' in temp[2], 'D':'D' in temp[2]}
    all_ans = len(ans)
    print('ans', ans)
    data = json.loads(request.get_data(as_text=True))
    score = 0
    print('data check', data['check'])
    for i in data['check']:
        print('here')
        FLAG = True
        for symbol in 'ABCD':
            if symbol in data['check'][i]:
                if data['check'][i][symbol] != ans[int(i)][symbol]:
                    FLAG = False
                    break
        if FLAG:
            score += 100./all_ans
    score = int(score)
    print(score)
    db = sqlite3.connect('USER.DB')
    c = db.cursor()
    c.execute("""UPDATE USER SET GRADE=? WHERE USERNAME=?""", (score, data['user']))
    db.commit()
    db.close()
    return jsonify({'status': 200}), 200

@app.route('/verify/<username>/<password>')
def verify(username, password):
    if check_user(username, password):
        return '200'
    else:
        return '500'

@app.route('/get-grade')
def get_grade():
    # return '20174899 100\n20174885 0\n'
    return getgrade()

@app.route('/update-paper', methods=['post'])
def update_paper():
    data = json.loads(request.get_data(as_text=True))
    print(data['content'])
    with open('paper', 'wb') as f:
        f.write(data['content'])
        f.close()
    return '200'

@app.route('/add-user/<username>/<password>')
def adduser(username, password):
    add_user(username, password)
    return '200'

def check_user(username, password):
    db = sqlite3.connect('USER.DB')
    c = db.cursor()
    res = c.execute("""SELECT * FROM USER WHERE USERNAME=? AND PASSWORD=?""", (username, password))
    for _ in res:
        return True
    return False

def add_user(username, password):
    db = sqlite3.connect('USER.DB')
    c = db.cursor()
    c.execute("""INSERT INTO USER (USERNAME, PASSWORD, GRADE) VALUES (?, ?, 0)""", (username, password))
    db.commit()
    return

def getgrade():
    g = '序号 学号 成绩\n'
    db = sqlite3.connect('USER.DB')
    c = db.cursor()
    res = c.execute("""SELECT ID, USERNAME, GRADE FROM USER""")
    for i in res:
        g += '{} {} {}\n'.format(i[0], i[1], i[2])
    return g


def sql_handler():
    db = sqlite3.connect('USER.DB')
    c = db.cursor()
    c.execute("""CREATE TABLE USER (
ID INTEGER PRIMARY KEY AUTOINCREMENT ,
USERNAME VARCHAR(255),
PASSWORD VARCHAR(255),
GRADE INT
)""")
    # c.execute("""INSERT INTO USER (USERNAME, PASSWORD) VALUES (20174899, 123456)""")
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run(port=5000)
    # sql_handler()