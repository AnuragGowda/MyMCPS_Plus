from gradedisplay import app
from gradedisplay.form import LoginForm
from flask import render_template, url_for, request, flash, redirect, make_response, session
from flask_session import Session
import requests, lxml.html, json, os, time
from datetime import datetime
s = requests.session()
login = s.get('https://portal.mcpsmd.org/public/')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
sess = Session()
sess.init_app(app)
def load_data(form):
    response = s.post('https://portal.mcpsmd.org/guardian/home.html', data=form)
    for i in range(3):
        response = s.post('https://portal.mcpsmd.org/guardian/home.html', data=form)
        if response.text.find('root.schoolId') != -1:
            break
    if response.text.find('root.schoolId') == -1:
        return
    else:
        gradeInfo, specialData = [[response.text[response.text.find('root.schoolId')+26:response.text.find('root.schoolId')+29], response.text[response.text.find('root.guardianId')+19: response.text.find('root.guardianId')+24]]],[]
        loginData = s.get('https://portal.mcpsmd.org/guardian/prefs/gradeByCourseSecondary.json?schoolid='+gradeInfo[0][0]+'&student_number='+form['account']+'&studentId='+gradeInfo[0][1]).json()
        for quarter in range(len(loginData)-1):
            if loginData[quarter]['termid'] == 'MP4':
                basicInfo = s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_CourseDetail.json?secid='+loginData[quarter]['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP4').json()  
                gradeInfo.append([basicInfo['courseName'], basicInfo['overallgrade'], float(basicInfo['percent']), basicInfo['teacher'], basicInfo['email_addr'], basicInfo['sectionid'], basicInfo['period']])
                gradeInfo.append([s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_CategoryDetail.json?secid='+basicInfo['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP4').json(), s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_AssignmentDetail.json?secid='+basicInfo['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP3').json()])
            elif loginData[quarter]['termid'] == '':
                specialData.append([loginData[quarter]['courseName'], '', '', loginData[quarter]['teacher'], loginData[quarter]['email_addr'], loginData[quarter]['sectionid'], loginData[quarter]['period']])
        if specialData:
            for period in range(int(loginData[-3]['period'])-1):
                if (period)*2+1 > len(gradeInfo)-1 or gradeInfo[(period)*2+1][6] != "0"+str(period+1):
                    for data in range(len(specialData)):
                        if specialData[data][6] == "0"+str(period+1):
                            gradeInfo.insert(period*2+1, specialData[data]) 
                            gradeInfo.insert(period*2+2, [{},{}])
        return gradeInfo

@app.before_request
def cleanSessionData():
    try:
        for filename in os.listdir(os.getcwd()+'//flask_session'):
            if time.time() - os.path.getmtime(os.getcwd()+'//flask_session//'+filename) > 900:
                os.remove(os.getcwd()+'//flask_session//'+filename+'//asd')
    except Exception as e:
        flash('An error occured: '+e+'. The developer will be notified', 'danger')

@app.route('/', methods=['GET', 'POST'])
def getInfo():
    if session.get('login', False):
        flash('You are already logged in!', 'success')
        return redirect(url_for('grades'))
    login = LoginForm(request.form)
    if request.method == 'POST':
        if login.validate_on_submit():
            form['account'], form['ldappassword'], form['pw'] = request.form['username'], request.form['password'], '0'
            data = load_data(form)
            if data:
                session['gradeData'] = data
                session['login'] = True
                flash('You have been logged in!', 'success')
                return redirect(url_for('grades'))
            else:
                flash('Login Unsuccessful, Try Again.', 'danger')
    return render_template('home.html', title = 'Login', formData=form['contextData'], formPassword=form['ldappassword'], form=login)

@app.route('/grades')
def grades():
    if not session.get('login', False):
        flash('You haven\'t logged in, please log in first!', 'danger')
        return redirect(url_for('getInfo'))
    overallInfo = []
    for i in range(int(session.get('gradeData', '')[-2][-1])):
        overallInfo.append(session.get('gradeData', '')[(i+1)*2-1])
    return render_template('grades.html', title = 'Grades', data=overallInfo, periods=range(int(session.get('gradeData', '')[-2][-1])))

@app.route('/gradePage/<classData>')
def gradePage(classData):
    if not session.get('login', False):
        flash('You haven\'t logged in, please log in first', 'danger')
        return redirect(url_for('getInfo'))
    return render_template('gradePage.html', title = session.get('gradeData', '')[(int(classData)+1)*2-1][0], data = session.get('gradeData', '')[(int(classData)+1)*2], info = session.get('gradeData', '')[(int(classData)+1)*2-1])

@app.route('/about')
def about():
    return render_template('about.html', title = 'About Page')

@app.route('/contact')
def contact():
    return render_template('contact.html', title = 'Contact Page')

@app.route('/logout')
def logout():
    session['login'] = False
    flash('You have been logged out!', 'info')
    return redirect(url_for('getInfo'))

@app.errorhandler(404)
def pageNotFound(e):
    flash('You have entered a url that does not exist! You have been redirected.', 'warning')
    return redirect(url_for('getInfo'))

@app.errorhandler(500)
def crash():
    return render_template('crash.html', title = 'Crash Page')

@app.errorhandler(410)
def deletedInfo():
    flash('It seems that the data you are trying to access has been mysteriously deleted or changed! If this problem persists, contact the creator of this website.', 'danger')
    return redirect(url_for('getInfo'))
