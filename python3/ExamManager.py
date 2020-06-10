# -*- coding: utf-8 -*-
# 作者：蓝一潇 20174899 电子1701
import sys  # 导入系统
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QCheckBox, QProgressBar, QLabel, QTextBrowser, QGridLayout, QComboBox
from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
import json
import time
# reload(sys)
# sys.setdefaultencoding('utf8')

class FirstUi(QMainWindow):  # 第一个窗口类
    def __init__(self):
        super(FirstUi, self).__init__()
        self.check_list = {}
        self.lock = False
        self.all_problem = 0
        self.user = ''
        self.host = HOST
        self.init_ui()

    def init_ui(self):
        self.biasY = -20
        self.biasX = -50
        min = 40

        self.now_problem_id = 1
        self.problem = self.get_basic_info()
        self.all_problem = len(self.problem)
        self.check_list = {}

        self.resize(1024, 900)  # 设置窗口大小

        self.combo = QComboBox(self)
        for i in range(1, len(self.problem)+1):
            self.combo.addItem(str(i))
        self.combo.activated[str].connect(self.onActivated)

        self.combo.move(50, 300)

        self.setWindowTitle('NEU-CSE专用考试系统')  # 设置窗口标题
        self.btn_back = QPushButton('退出系统', self)  # 设置按钮和按钮名称
        self.btn_back.setGeometry(30, 30, 100, 50)  # 前面是按钮左上角坐标，后面是窗口大小
        self.btn_back.clicked.connect(self._quit)  # 将信号连接到槽
        # self.username = QTextEdit()
        # self.username.setGeometry(20, 100, 100, 50)

        self.btn_handle = QPushButton('交卷', self)  # 设置按钮和按钮名称
        self.btn_handle.setGeometry(894, 30, 100, 50)  # 前面是按钮左上角坐标，后面是窗口大小
        self.btn_handle.clicked.connect(self.handle_problem)  # 将信号连接到槽


        self.btn_next = QPushButton('下一题', self)
        self.btn_next.setGeometry(680+self.biasX, 580, 100, 50)
        self.btn_next.clicked.connect(self.next_problem)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(390, 620, 200, 25)
        # self.pbar.setValue(int(1./self.all_problem*100))
        self.pbar.setValue(0)

        self.btn_last = QPushButton('上一题', self)
        self.btn_last.setGeometry(320+self.biasX, 580, 100, 50)
        self.btn_last.clicked.connect(self.last_problem)

        self.cb = QCheckBox('A', self)
        self.cb.move(440+self.biasX, 600+self.biasY)
        # self.cb.toggle()
        self.cb.stateChanged.connect(self.changeTitle)

        self.cb2 = QCheckBox('B', self)
        self.cb2.move(500+self.biasX, 600+self.biasY)
        # self.cb2.toggle()
        self.cb2.stateChanged.connect(self.changeTitle2)

        self.cb3 = QCheckBox('C', self)
        self.cb3.move(560+self.biasX, 600+self.biasY)
        # self.cb3.toggle()
        self.cb3.stateChanged.connect(self.changeTitle3)

        self.cb4 = QCheckBox('D', self)
        self.cb4.move(620+self.biasX, 600+self.biasY)
        # self.cb4.toggle()
        self.cb4.stateChanged.connect(self.changeTitle4)

        self.lable1 = QLabel('请选择题号：', self)
        self.lable1.setGeometry(50, 270, 100, 25)

        self.now = time.time()
        self.now = 60 * min + 16 * 60 * 60

        self.lcd = QLCDNumber(self)
        self.lcd.setGeometry(780, 300, 110, 30)
        self.lcd.setDigitCount(8)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%H:%M:%S", time.localtime(self.now)))



        # 新建一个QTimer对象
        self.timer = QBasicTimer()  # QTimer()貌似不行，不知何故？
        self.timer.start(1000, self)

        msg = """
    东北大学考生须知：
        一、考前40分钟，应试人员应到达本专业考试科目所指定的考点，凭本人准考证和东北大学学生证原件进入考点。

二、应试人员在每场考试前30分钟凭本人准考证和本人有效证件进入指定的考场参加考试，应试人员应如实在“考场签到表”上签到，经监考人员同意后进入考场，应试人员必须对号入座，并将准考证和有效证件放在考桌右上角，以备核对。应试人员应服从考试工作人员的管理，积极配合考场工作人员的各项监督和检查。

三、按照《东北大学考试守则》规定，开考5分钟后应试人员一律禁止入场。

四、上机考试结束前15分钟应试人员不能交卷出场。
        """


        self.lable2 = QTextBrowser(self)
        self.lable2.setText(str(msg))
        self.lable2.setGeometry(780, 480, 220, 150)

        self.lable3 = QLabel('剩余时间：', self)
        self.lable3.setGeometry(780, 270, 100, 25)

        self.lable4 = QLabel('开发者：蓝一潇20174899 魏景行20174782 陈绵健20174785 电子1701 东北大学计算机学院', self)
        self.lable4.setGeometry(10, 650, 1000, 25)
        try:
            with open('~tmp1.temp', 'r') as f:
                content = f.read()
                f.close()
        except:
            content = 'None'

        self.user = content

        self.lable5 = QLabel('亲爱的{}:\n欢迎进入考试，加油！'.format(content), self)
        self.lable5.setGeometry(50, 100, 150, 75)

        self.pl = QTextBrowser(self)
        self.pl.setText(str(self.problem[self.now_problem_id]['content']))
        self.pl.setGeometry(270, 60, 460, 500)

        self.setGeometry(300, 300, 1024, 900)

        self.check_list[1] = {}

    def _quit(self):
        if QMessageBox.question(self, '警告', '您还没有交卷！是否要退出？', QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
            self.close()
            self.deleteLater()
        else:
            return

    def changeTitle(self):
        if self.lock:
            return
        # self.cb.close()
        # del self.cb
        symbol = 'A'
        if symbol in self.check_list[self.now_problem_id]:
            self.check_list[self.now_problem_id][symbol] = not self.check_list[self.now_problem_id][symbol]
        else:
            self.check_list[self.now_problem_id][symbol] = True
        print('Check A')

    def changeTitle2(self):
        if self.lock:
            return
        # self.combo.setCurrentIndex(2)
        # self.cb.close()
        # del self.cb
        symbol = 'B'
        if symbol in self.check_list[self.now_problem_id]:
            self.check_list[self.now_problem_id][symbol] = not self.check_list[self.now_problem_id][symbol]
        else:
            self.check_list[self.now_problem_id][symbol] = True
        print('Check B')

    def changeTitle3(self):
        if self.lock:
            return
        # self.cb.close()
        # del self.cb
        symbol = 'C'
        if symbol in self.check_list[self.now_problem_id]:
            self.check_list[self.now_problem_id][symbol] = not self.check_list[self.now_problem_id][symbol]
        else:
            self.check_list[self.now_problem_id][symbol] = True
        print('Check C')

    def changeTitle4(self):
        if self.lock:
            return
        # self.cb.close()
        # del self.cb
        symbol = 'D'
        if symbol in self.check_list[self.now_problem_id]:
            self.check_list[self.now_problem_id][symbol] = not self.check_list[self.now_problem_id][symbol]
        else:
            self.check_list[self.now_problem_id][symbol] = True
        print('Check D')

    def next_problem(self):
        print(self.check_list)
        if self.now_problem_id == self.all_problem:
            print(self.now_problem_id, 'reach end!')
            QMessageBox.warning(self, "温馨提示", "已是最后一题！", QMessageBox.Ok)
            return
        self.switch_problem(self.now_problem_id+1)
        return

    def last_problem(self):
        print(self.check_list)
        if self.now_problem_id == 1:

            print(self.now_problem_id, 'reach the first!')
            QMessageBox.warning(self, "温馨提示", "已是第一题！", QMessageBox.Ok)
            return
        self.switch_problem(self.now_problem_id - 1)
        return

    def onActivated(self, text):
        print('combo', text)
        # self.combo.setCurrentIndex(int(text)-1)
        self.switch_problem(int(text))


    def switch_problem(self, problem_id):
        self.lock = True
        self.cb.setChecked(False)
        self.cb2.setChecked(False)
        self.cb3.setChecked(False)
        self.cb4.setChecked(False)
        self.now_problem_id = problem_id
        self.combo.setCurrentIndex(self.now_problem_id - 1)
        self.pbar.setValue(int(float(self.now_problem_id) / self.all_problem * 100))
        self.pl.setText(str(self.problem[self.now_problem_id]['content']))
        if self.now_problem_id not in self.check_list:
            self.check_list[self.now_problem_id] = {}
        else:
            for item in self.check_list[self.now_problem_id]:
                if self.check_list[self.now_problem_id][item]:
                    if item == 'A':
                        self.cb.setChecked(True)
                    if item == 'B':
                        self.cb2.setChecked(True)
                    if item == 'C':
                        self.cb3.setChecked(True)
                    if item == 'D':
                        self.cb4.setChecked(True)

        self.lock = False



        pass

    def get_basic_info(self):
        try:
            req = requests.get('http://{}/get-testpaper'.format(self.host))
            res = json.loads(req.content)
            _res = {}
            for i in res:
                _res[int(i)] = res[i]
            return _res
        except:
            QMessageBox.critical(self, "网络错误", "无法连接服务器{}，请检查网络设置！\n将打开默认试卷...".format(self.host), QMessageBox.Ok)
            return {1:{'content': '"CHINA!" 这个推特是谁发送的？ \n A.特朗普 B.希拉里 C.拜登 D.奥巴马', }, 2:{'content': '截至6月6日，美国死亡人数已经达到了？ \n A.10K B. 1k C.200K D.0'}}

    def handle_problem(self):
        print('will handle:{}'.format(self.check_list))
        EXIT = 0
        if QMessageBox.question(self, '温馨提示', '您确认要交卷吗？\n要仔细检查哦～', QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes) == QMessageBox.Yes:
            try:
                requests.post('http://{}/handin'.format(self.host), json={'user':self.user, 'check':self.check_list})
                QMessageBox.information(self, "恭喜", "试卷已经成功提交！\n即将退出系统～", QMessageBox.Ok)
                EXIT = 1
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "警告", "系统无法连接服务器！\n请稍后再试", QMessageBox.Ok)
                return
        else:
            return
        if EXIT == 1:
            sys.exit(0)


    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.lcd.display(time.strftime("%H:%M:%S", time.localtime(self.now)))
            self.now -= 1
            # print time.strftime("%m", time.localtime(self.now))
            if self.now == 16*60*60:
                self.handle_problem()
                QMessageBox.warning(self, "温馨提示", "考试结束！已自动交卷。\n  即将退出系统，\n  考完就不要想了~", QMessageBox.Ok)
                self.deleteLater()


class SecondUi(QWidget):  # 建立第二个窗口的类
    def __init__(self):
        super(SecondUi, self).__init__()
        self.host = HOST
        self.init_ui()

    def init_ui(self):
        self.resize(500, 350)  # 设置第二个窗口代码
        self.setWindowTitle('登录考试系统')  # 设置第二个窗口标题

        self.btn = QPushButton('登录', self)  # 设置按钮和按钮名称
        self.btn.setGeometry(200, 250, 100, 50)  # 前面是按钮左上角坐标，后面是按钮大小
        self.btn.clicked.connect(self.slot_btn_function)  # 将信号连接到槽

        self.lable4 = QLabel('作者：\n蓝一潇20174899 \n魏景行20174782 \n陈绵健20174785 \n电子1701 \n东北大学计算机学院', self)
        self.lable4.setGeometry(10, 130, 150, 300)

        self.lable3 = QLabel('学生请输入学号密码登录，教师请输入用户名以及密码登录', self)
        self.lable3.setGeometry(70, 5, 400, 50)

        self.lable2 = QLabel('学号/用户名:', self)
        self.lable2.setGeometry(100, 100, 100, 50)

        self.lable = QLabel('密码:', self)
        self.lable.setGeometry(142, 150, 100, 50)

        self.lable0 = QLabel('欢迎使用NEU-CES考试系统！', self)
        self.lable0.setGeometry(175, 50, 300, 50)

        self.username = QLineEdit(self)
        self.username.setGeometry(190, 110, 200, 30)

        self.passowrd = QLineEdit(self)
        self.passowrd.setGeometry(190, 165, 200, 30)
        self.passowrd.setEchoMode(QLineEdit.Password)

    def slot_btn_function(self):

        if self.passowrd.text() == '1234' and self.username.text() == 'shelaoshi':
            print('Admin mode!')
            self.close()  # 关闭窗口
            self.deleteLater()
            self.f = ThirdUI()  # 将第一个窗口换个名字
            self.f.show()  # 将第一个窗口显示出来

        elif self.check_student(self.username.text(), self.passowrd.text()):
            with open('~tmp1.temp', 'w') as f:
                f.write(self.username.text())
                f.close()
            self.close()  # 关闭窗口
            self.deleteLater()
            self.f = FirstUi()  # 将第一个窗口换个名字
            self.f.show()  # 将第一个窗口显示出来
        else:
            QMessageBox.warning(self, "温馨提示", "您输入的用户名或密码有误，请重试！", QMessageBox.Ok)
            return


    def check_student(self, username, password):
        try:
            req = requests.get('http://{}/verify/{}/{}'.format(self.host, username, password))
            print(req.content)
            if req.content == b'200':
                return True
            else:
                return False
        except Exception as e:
            print(e)
            if QMessageBox.question(self, "警告", "无法连接到服务器，\n是否进入离线模式？", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
                with open('~tmp1.temp', 'w') as f:
                    f.write('离线模式')
                    f.close()
                self.close()  # 关闭窗口
                self.deleteLater()
                self.f = FirstUi()  # 将第一个窗口换个名字
                self.f.show()  # 将第一个窗口显示出来
            else:
                return


class ThirdUI(QWidget):
    def __init__(self):
        super(ThirdUI, self).__init__()
        self.host = HOST
        self.content = ''
        self.init_ui()

    def init_ui(self):
        self.resize(1024, 768)  # 设置第二个窗口代码
        self.setWindowTitle('考试系统 管理面板')  # 设置第二个窗口标题
        self.setGeometry(200, 0, 1024, 768)

        self.lable0 = QLabel('欢迎使用NEU-CES考试系统后台管理器', self)
        self.lable0.setGeometry(400, 25, 300, 50)

        self.lable4 = QLabel('开发者：蓝一潇20174899 魏景行20174782 陈绵健20174785 电子1701 东北大学计算机学院', self)
        self.lable4.setGeometry(10, 630, 1000, 25)

        self.lable3 = QLabel('添加学生：', self)
        self.lable3.setGeometry(170, 250, 100, 25)

        self.lable5 = QLabel('学号：', self)
        self.lable5.setGeometry(50, 280, 100, 25)

        self.lable5 = QLabel('姓名：', self)
        self.lable5.setGeometry(50, 310, 100, 25)

        self.lable5 = QLabel('密码：', self)
        self.lable5.setGeometry(50, 340, 100, 25)

        self.username = QLineEdit(self)
        self.username.setGeometry(100, 280, 200, 30)

        self.no = QLineEdit(self)
        self.no.setGeometry(100, 310, 200, 30)

        self.pwd = QLineEdit(self)
        self.pwd.setGeometry(100, 340, 200, 30)

        self.btn = QPushButton('添加', self)  # 设置按钮和按钮名称
        self.btn.setGeometry(150, 380, 100, 30)  # 前面是按钮左上角坐标，后面是按钮大小
        self.btn.clicked.connect(self.add_user)  # 将信号连接到槽

        self.lable5 = QLabel('学生成绩查询', self)
        self.lable5.setGeometry(600, 75, 100, 25)

        msg = '请点击"查询成绩"进行查询'

        self.lable2 = QTextBrowser(self)
        self.lable2.setText(str(msg))
        self.lable2.setGeometry(600, 100, 400, 440)

        self.btn2 = QPushButton('查询成绩', self)  # 设置按钮和按钮名称
        self.btn2.setGeometry(750, 570, 100, 30)  # 前面是按钮左上角坐标，后面是按钮大小
        self.btn2.clicked.connect(self.get_grade)  # 将信号连接到槽

        self.lable5 = QLabel('更新试卷', self)
        self.lable5.setGeometry(400, 150, 100, 25)

        self.btn3 = QPushButton('选择新的试卷', self)  # 设置按钮和按钮名称
        self.btn3.setGeometry(350, 240, 100, 30)  # 前面是按钮左上角坐标，后面是按钮大小
        self.btn3.clicked.connect(self.upload)  # 将信号连接到槽

        self.btn4 = QPushButton('上传试卷', self)  # 设置按钮和按钮名称
        self.btn4.setGeometry(460, 240, 75, 30)  # 前面是按钮左上角坐标，后面是按钮大小
        self.btn4.clicked.connect(self._upload)  # 将信号连接到槽

        msg2 = """试卷编写规则：
        每一行为一道题。题目与选项与正确答案之间，使用-***-进行分割。最后一行没有换行。
        示例：
"CHINA!" 这个推特是谁发送的?-***-A.特朗普 B.希拉里 C.拜登 D.奥巴马-***-A
美国死亡人数已经达到了-***-A.10K B. 1k C.200K D.全死了-***-A
被警察杀害的黑人叫做?-***-A.乔治弗洛伊德 B.马丁路德金 C.奥巴马 D.迪卡普里奥莱昂纳多-***-A
东北大学的英文缩写是?-***-A.NEU B.BEU C.CEU D.DEU-***-A
        
        """

        self.lable0 = QTextBrowser(self)
        self.lable0.setText(str(msg2))
        self.lable0.setGeometry(350, 300, 200, 300)


    def add_user(self):
        username = self.username.text()
        password = self.pwd.text()
        print(username, password)
        try:
            requests.get('http://{}/add-user/{}/{}'.format(self.host, username, password))
            QMessageBox.warning(self, "温馨提示", "成功添加了新的用户！", QMessageBox.Ok)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "温馨提示", "无法连接到服务器，请稍后再试！", QMessageBox.Ok)
        return




    def get_grade(self):
        try:
            req = requests.get('http://{}/get-grade'.format(self.host))
            self.lable2.setText(str(req.content, encoding="utf-8"))
            print(req.content)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "温馨提示", "无法连接到服务器{}，请稍后再试！".format(self.host), QMessageBox.Ok)


        return

    def upload(self):
        try:
            openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'TXT files(*.txt)')
            path = openfile_name[0]
            with open(path, 'r') as f:
                content = f.read()
                f.close()
            if content == '':
                QMessageBox.warning(self, "警告", "该文件为空！", QMessageBox.Ok)
                return
            self.lable0.setText(str('试卷预览：\n{}'.format(content)))
            self.content = content
        except Exception as e:
            print(e)
            return

    def _upload(self):
        if self.content == '':
            QMessageBox.warning(self, "警告", "该文件为空！", QMessageBox.Ok)
            return
        js = {'content':self.content}
        try:
            requests.post('http://{}/update-paper'.format(self.host), json=js)
            QMessageBox.warning(self, "温馨提示", "试卷上传成功！", QMessageBox.Ok)
            return

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "温馨提示", "无法连接到服务器，请稍后再试！", QMessageBox.Ok)
            return











HOST = '114.115.130.28:7000'

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = SecondUi()  # 将第一和窗口换个名字
    w.show()  # 将第一和窗口换个名字显示出来
    sys.exit(app.exec_())  # app.exet_()是指程序一直循环运行直到主窗口被关闭终止进程（如果没有这句话，程序运行时会一闪而过）


if __name__ == '__main__':  # 只有在本py文件中才能用，被调用就不执行
    main()

