# Import the app from our package
from gradedisplay import app
# Also import this LoginForm object
from gradedisplay.form import LoginForm
# Import some built in functions of flask
from flask import render_template, url_for, request, flash, redirect, make_response, session
# Import sessions 
from flask_session import Session
# Import other useful stuff
import requests, lxml.html, json, os, time

# Create an instance of a request object
s = requests.session()
# Use a get request to the portal login page, then we get the hidden feilds in the form that we will need to copy and post back to the server
# This code was borrowed from Stephen Brennan at https://brennan.io/2016/03/02/logging-in-with-requests/
login = s.get('https://portal.mcpsmd.org/public/')
login_html = lxml.html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

# Create a session object and initilize it
sess = Session()
sess.init_app(app)

# Load data function 
def load_data(form):
    '''This function handles the data loading of the program, the input "form" is what the user entered on the login form. All the data is loaded as soon as the user enters vaild credentials'''
    # Try to post the data, which is a collection of what we get with the get request at the top of the page and the users credentials
    # Sometimes the portal page glitches out, you enter in valid credentials and nothing happens, you may have experienced this yourself, so I created a loop to conteract this
    # However, we don't want the loop to interate too much because if the user entered invalid credentials, it could end up locking their account as that is how MCPS deals with brute force attacks
    for i in range(3):
        # Keep posting
        response = s.post('https://portal.mcpsmd.org/guardian/home.html', data=form)
        # Check if it is valid by tring to find something that is there when the user enters valid credentials
        if response.text.find('root.schoolId') != -1:
            # Exit this loop if it is proved that the user entered valid credentials
            break
    # If even after the 3 attempts, it is found the credentials are invalid, exit this function (return None)
    if response.text.find('root.schoolId') == -1:
        return
    # However, if it is found that the user entered valid data, we need to get that data and format in a way that suits us
    else:
        # We first get the school id and the guardian id which are needed later, also initilize a variable called specialData which we will only use in specific cases
        gradeInfo, specialData = [[response.text[response.text.find('root.schoolId')+26:response.text.find('root.schoolId')+29],response.text[response.text.find('root.guardianId')+19: response.text.find('root.guardianId')+24]]],[]
        # Here we use the guardian id as well as the school id to get data of all the classes that the student has taken in the school year and we store it in loginData
        # This data includes the course and teacher name, the marking period, the overall grade, the class period and more 
        loginData = s.get('https://portal.mcpsmd.org/guardian/prefs/gradeByCourseSecondary.json?schoolid='+gradeInfo[0][0]+'&student_number='+form['account']+'&studentId='+gradeInfo[0][1]).json()
        # Now we need to keep only the data that we want, so we will loop through the loginData that we just got
        for quarter in range(len(loginData)-1):
            # Here we filter the login data to match only the marking period that we want to show
            if loginData[quarter]['termid'] == 'MP4':
                # Now we are looping through each class, we get the more specific information here such as the percent that the user has in the class, and storing it so that we can filter it later
                basicInfo = s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_CourseDetail.json?secid='+loginData[quarter]['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP4').json()  
                # Now with that information that we received, we want to only store the following - the name of the course, the overall grade, the percent the user has in the class, etc
                gradeInfo.append([basicInfo['courseName'], basicInfo['overallgrade'], float(basicInfo['percent']),basicInfo['teacher'],basicInfo['email_addr'], basicInfo['sectionid'], basicInfo['period']])
                # Now that we have added that info to grade data, we also want to add the actual grades such as the grade categories (for example the formative category with a weight of 40) and the percent that the user has in each category
                # We also get the individual grades, for example a 30/40 on a formative project or 10/10 on a homework, we save these both in our gradeInfo variable 
                gradeInfo.append([s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_CategoryDetail.json?secid='+basicInfo['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP4').json(),s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_AssignmentDetail.json?secid='+basicInfo['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP3').json()])
            # However, we also want to keep track of unlisted marking periods because due to how  MyMCPS works, if a grade isnt entered for a class, there will be no marking period assigned to that class
            # If the class isnt included, it will cause our program to crash later, therefore it is necesary that we add the classes without grades
            elif loginData[quarter]['termid'] == '':
                # Add the course name, and everthing else, this is the same thing we did with the other data
                specialData.append([loginData[quarter]['courseName'], '', '', loginData[quarter]['teacher'],loginData[quarter]['email_addr'], loginData[quarter]['sectionid'],loginData[quarter]['period']])
        # If we found special data, this is usually allways true because MCPS usually sends the classes counselor and homeroom along with the grade data, so we need to check the special data to find if it is actually a real class
        if specialData:
            # Here we look at all the users classes again, we look at the data 4 before the end because the last one is usually blank, the two before that are usually counselor and homeroom
            # This could be prone to error however, so I may need to fix it 
            for period in range(int(loginData[-4]['period'])-1):
                # Due to how I stored the data, I know how to perform calculations on it to check for certian things, the first clause checks to see that the period isnt outside of the amount of classes stored in gradeInfo, if it is,
                # then that class might need to be added, also I check to see if the class in gradeInfo isnt matching up with the period, for example, if the period I'm looking for is 1 (meaning period is 0 since I am interating through 
                # a list that starts from 0 and goes to the last period), then I check to see if the period at the index that should correspond to 1 is in fact 1, and if it is not, then we need to proceed
                if (period)*2+1 > len(gradeInfo)-2 or gradeInfo[(period)*2+1][6] != "0"+str(period+1):
                    # Enumerate through all the special data 
                    for data in range(len(specialData)):
                        # If the data is the one that we are looking for (we got this from the if loop) then we will proceed
                        if specialData[data][6] == "0"+str(period+1):
                            # We want to then insert that data at the specific location, this is the class data, as I said before this includes things such as the course name, and everthing else
                            gradeInfo.insert(period*2+1, specialData[data]) 
                            # Since there are no grades, just put in a list with blank dictionaries to server sort of as a place holder 
                            gradeInfo.insert(period*2+2, [{},{}])
        # After everything, return the grade data 
        return gradeInfo
        # We now have all the grade data that we will need for the entire program, the format is as such:
        '''
        [[schoolId, gardianId], [class1Attr1, class1Attr2, *this is filled with class attributes that include the teachers name, period number, grade in the class, etc*], [{class1GradeHeader1, class1GradeHeader2, *this is filled with the class grade headers*},{class1Grade1, class1Grade2, *this is filled with the individual grades*}], *and here we would place our second class followed by its grades*]
        '''
        # So as you can see, we have a large list which begins with a small list containing the school and guardian id (which are actually useless after we have gathered the data but I'm to remove them because I would have to change the rest of the program and I'm too lazy to change everything, maybe I will later)
        # After that list, we have a class which is a list that has some attributes of the class, with another list is followed by another list which has two dictionaries containing grade data 
        # Then we would have more classes following that class, meaning two lists (per class), the first with class attributes the second with dictionaries with grade data
        # Thats it for the data gathering/formatting part which I think was one of the hardest parts of this program 

# Decorator before_request, makes the following function run when they are fetching the website
@app.before_request
# Function that delete old session information so that the server won't run out of memory with useless session info
def cleanSessionData():
    '''clean the old session data on the server'''
    # Im using an exception just in case I'm not able to find the data or something weird happens so that it doesn't crash 
    try:
        # Here we search through all the files in the current directory under the file flask session which is where flask sessions are stored
        for filename in os.listdir(os.getcwd()+'//flask_session'):
            # If the current time minus the time the file was made, which is how long the file was "alive", exceeds 900 seconds, which is 15 minutes, proceed
            if time.time() - os.path.getmtime(os.getcwd()+'//flask_session//'+filename) > 900:
                # Delete this file, 15 minutes seems like a long enough time to check grades, we don't want it to be too long 
                os.remove(os.getcwd()+'//flask_session//'+filename)
    # If an error occurs when trying to get rid of files store it in e
    except Exception as e:
        # Display an error message to the user, the developer actually wont be notified, but if there was a recurring problem, I would already know about it
        flash('An error occured: '+str(e)+'. The developer will be notified', 'danger')

# Decorator which makes the followin function run when the user goes to the default page, hence the "/", also allow both get and post requests since we have a form
@app.route('/', methods=['GET', 'POST'])
# The actual function that handles what to do when the user gets on the website
def getInfo():
    '''login page for the website'''
    # A variable that will be used in case the user would like to enter dummy data just to see what the app looks like 
    checkValid = True
    # Before doing anything, we check to see if there is already current session data, we check to see if the user has already logged in
    if session.get('login', False):
        # Tell the user that they have already logged in
        flash('You are already logged in!', 'success')
        # Redirect the user to the grade page 
        return redirect(url_for('grades'))
    # Create an instance of the class login form and feed it the login form on the page 
    login = LoginForm(request.form)
    # If the user is trying to post which is triggered by the submit button on the login page, continue
    if request.method == 'POST':
        # If they entered the special login that allows them to just see a "demo" we continue
        if request.form['username'] == 'example' and request.form['password'] == 'password':
            # Set the session login to true so that we can tell the user has logged on while the session is still active
            session['login'] = True
            # Also in the session, create a grade data variable and assign it the dummy example data 
            session['gradeData'] = [['0','0'],['Class1','A',100.0,'Teacher1','teacher1@mcpsmd.org','0','01'],[[{'Id':0,'CategoryGrade':'A','Description':'Category1(34)','OrganizationId':0,'Percent':100.0,'PointsEarned':'100.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'A','Missing':'0','Percent':'','Points':'100.0'},{}]],['Class2','B',80.0,'Teacher2','teacher2@mcpsmd.org','0','02'],[[{'Id':0,'CategoryGrade':'B','Description':'Category1(34)','OrganizationId':0,'Percent':80.0,'PointsEarned':'80.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'B','Missing':'0','Percent':'','Points':'80.0'},{}]],['Class3','C',70.0,'Teacher3','teacher3@mcpsmd.org','0','03'],[[{'Id':0,'CategoryGrade':'C','Description':'Category1(34)','OrganizationId':0,'Percent':70.0,'PointsEarned':'70.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'C','Missing':'0','Percent':'','Points':'70.0'},{}]],['Class4','D',60.0,'Teacher4','teacher4@mcpsmd.org','0','04'],[[{'Id':0,'CategoryGrade':'A','Description':'Category1(34)','OrganizationId':0,'Percent':60.0,'PointsEarned':'60.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'D','Missing':'0','Percent':'','Points':'60.0'},{}]],['Class5','E',50.0,'Teacher5','teacher5@mcpsmd.org','0','05'],[[{'Id':0,'CategoryGrade':'E','Description':'Category1(34)','OrganizationId':0,'Percent':50.0,'PointsEarned':'50.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'A','Missing':'0','Percent':'','Points':'50.0'},{}]]]
            # Check valid is false, we don;t need to validate credentials anymore 
            checkValid = False
        # If they credentials that they entered into the form are valid then we can do stuff with them
        if login.validate_on_submit() and checkValid:
            # Fill in some of the form fields of the form that we created at the beginning of the program, so that the form is complete when we post the data to MyMCPS
            form['account'], form['ldappassword'], form['pw'] = request.form['username'], request.form['password'], '0'
            # Store the output of the load_data function in data when we send the form to the fucntion
            data = load_data(form)
            # If there actually is data, remember that the function returns none when the credentials are invalid, we need to set up some things
            if data:
                # Set the session grade data to the data returned by the function
                session['gradeData'] = data
                # Set the session login variable to true
                session['login'] = True
                # Tell the user they logged in successfully 
                flash('You have been logged in!', 'success')
                # Redirect them to the grades page
                return redirect(url_for('grades'))
            # However, if the function returns none, this code runs
            else:
                # Simply tell the user that the login was unsuccessful
                flash('Login Unsuccessful, Try Again.', 'danger')
    # This section here tells the app to send the user the home page when they connect to our website, it also sets up some things  
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
