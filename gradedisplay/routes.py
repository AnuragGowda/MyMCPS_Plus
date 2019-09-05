# Import the app from our package
from gradedisplay import app
# Also import this LoginForm object
from gradedisplay.form import LoginForm, ErrorForm
# Import some built in functions of flask
from flask import render_template, url_for, request, flash, redirect, make_response, session
# Import sessions 
from flask_session import Session
# Import other useful stuff
import requests, lxml.html, json, os, time, smtplib
# Other stuff that will be used later, this is to keep the password hidden
import platform
import os, base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

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

# I could probably do this in a differnt way where I figure out if its summer based on the result from the sever, but I think that this is probably simpler, its just that I will have to manually edit it (only once a year tho)
summer_break = False
# Same with this, I think that I could figure out how to automate this, but im fine with having to manually edit it each quarter
marking_period = 'MP1'

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
            if loginData[quarter]['termid'] == marking_period:
                # Now we are looping through each class, we get the more specific information here such as the percent that the user has in the class, and storing it so that we can filter it later
                basicInfo = s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_CourseDetail.json?secid='+loginData[quarter]['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid='+marking_period).json()  
                # Now with that information that we received, we want to only store the following - the name of the course, the overall grade, the percent the user has in the class, etc
                gradeInfo.append([basicInfo['courseName'], basicInfo['overallgrade'], float(basicInfo['percent']),basicInfo['teacher'],basicInfo['email_addr'], basicInfo['sectionid'], basicInfo['period']])
                # Now that we have added that info to grade data, we also want to add the actual grades such as the grade categories (for example the formative category with a weight of 40) and the percent that the user has in each category
                # We also get the individual grades, for example a 30/40 on a formative project or 10/10 on a homework, we save these both in our gradeInfo variable 
                gradeInfo.append([s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_CategoryDetail.json?secid='+basicInfo['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid='+marking_period).json(),s.get('https://portal.mcpsmd.org/guardian/prefs/assignmentGrade_AssignmentDetail.json?secid='+basicInfo['sectionid']+'&student_number='+form['account']+'&schoolid='+gradeInfo[0][0]+'&termid=MP3').json()])
            # However, we also want to keep track of unlisted marking periods because due to how  MyMCPS works, if a grade isnt entered for a class, there will be no marking period assigned to that class
            # If the class isnt included, it will cause our program to crash later, therefore it is necesary that we add the classes without grades, also we need to check that these aren't "fake classes" like counselor
            elif loginData[quarter]['termid'] == '' and loginData[quarter]['courseName'] not in ['HOMEROOM', 'COUNSELOR', 'MYP RESEARCH SEM']:
                # Add the course name, and everthing else, this is the same thing we did with the other data
                specialData.append([loginData[quarter]['courseName'], '', '', loginData[quarter]['teacher'],loginData[quarter]['email_addr'], loginData[quarter]['sectionid'],loginData[quarter]['period']])
        # If we found special data, this is only run when you have a class that doesn't have grades entered, because MCPS won't assign a marking period to them when sending the json over
        if specialData:
            # Here we look at all the users classes again, and we sort them
            # I fixed this so this shouldn't be able to crash
            # Get the higest period we have of the special data
            lastSpecialData = int(specialData[-1][6]) if len(specialData) > 0 and isinstance(specialData[-1][6], str) and specialData[-1][6].isdigit() else 0
            # Get the highest period we have of the actual grade data
            lastGradeData = int(gradeInfo[-2][6]) if len(gradeInfo) >= 2 and isinstance(gradeInfo[-2][6], str) and gradeInfo[-2][6].isdigit() else 0
            # Get the max of these, and run through the range to make sure we have all the periods in between
            for period in range(max(lastSpecialData,lastGradeData,1)):
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
        # Thats it for the data gathering/formatting part which I think was one of the hardest parts of this program , honestly I think by organizing the data this way I made it harder for myself

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

# Decorator which makes the following function run when the user goes to the default page, hence the "/", also allow both get and post requests since we have a form
@app.route('/', methods=['GET', 'POST'])
# The actual function that handles what to do when the user gets on the website
def getInfo():
    '''login page for the website'''
    # Before doing anything, we check to see if there is already current session data, we check to see if the user has already logged in
    if session.get('login', False):
        # Tell the user that they have already logged in
        flash('You are already logged in!', 'success')
        # Redirect the user to the grade page 
        return redirect(url_for('grades'))
    # Check if its summer break
    if summer_break:
        return redirect(url_for('summer'))
    # Create an instance of the class login form and feed it the login form on the page 
    login = LoginForm()
    # If they credentials that they entered into the form are valid then we can do stuff with them
    if login.validate_on_submit():
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
    # This section here tells the app to send the user the home page when they connect to our website
    return render_template('home.html', title = 'Login', form=login)

# Decorator to make the following function handle the /summer 
@app.route('/summer')
# Actual function
def summer():
    # Check if it's actually summer, the use could've just entered it into the url
    if not summer_break:
        # If its not summer, we return them to the login screen
        return redirect(url_for('getInfo'))
    # Return the html template if it is
    return render_template('break.html')

# I just made a demonstrate feature for summer since I disabled the login feature, so normally, dutring the school year to see this, you would have to actually type in the keywords
@app.route('/dem')
# This is the function, and honestly, I'm going to allow the user to go here just by typing it in the url, so it'l be easier
def dem():
    # Set the session login to true so that we can tell the user has logged on while the session is still active
    session['login'] = True
    # Also in the session, create a grade data variable and assign it the dummy example data 
    session['gradeData'] = [['0','0'],['Class1','A',100.0,'Teacher1','teacher1@mcpsmd.org','0','01'],[[{'Id':0,'CategoryGrade':'A','Description':'Category1(34)','OrganizationId':0,'Percent':100.0,'PointsEarned':'100.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'A','Missing':'0','Percent':'','Points':'100.0'},{}]],['Class2','B',80.0,'Teacher2','teacher2@mcpsmd.org','0','02'],[[{'Id':0,'CategoryGrade':'B','Description':'Category1(34)','OrganizationId':0,'Percent':80.0,'PointsEarned':'80.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'B','Missing':'0','Percent':'','Points':'80.0'},{}]],['Class3','C',70.0,'Teacher3','teacher3@mcpsmd.org','0','03'],[[{'Id':0,'CategoryGrade':'C','Description':'Category1(34)','OrganizationId':0,'Percent':70.0,'PointsEarned':'70.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'C','Missing':'0','Percent':'','Points':'70.0'},{}]],['Class4','D',60.0,'Teacher4','teacher4@mcpsmd.org','0','04'],[[{'Id':0,'CategoryGrade':'A','Description':'Category1(34)','OrganizationId':0,'Percent':60.0,'PointsEarned':'60.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'D','Missing':'0','Percent':'','Points':'60.0'},{}]],['Class5','E',50.0,'Teacher5','teacher5@mcpsmd.org','0','05'],[[{'Id':0,'CategoryGrade':'E','Description':'Category1(34)','OrganizationId':0,'Percent':50.0,'PointsEarned':'50.0','PointsPossible':'100.0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'34.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category2(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{'Id':0,'CategoryGrade':'NG','Description':'Category3(33)','OrganizationId':0,'Percent':0,'PointsEarned':'0','PointsPossible':'0','SectionId':'0','StudentId':0,'TermId':'MP4','Weight':'33.000'},{}],[{'Id':0,'AssignedDate':'2019-04-1100:00:00.0','AssignmentId':'0','AssignmentType':'Category1(34)','Description':'ExampleDescription','DueDate':'2019-04-1100:00:00.0','Note':'','Possible':'100','SectionId':'77373202','Weight':'','Grade':'E','Missing':'0','Percent':'','Points':'50.0'},{}]]]
    # Redirect them to the grades page 
    return redirect(url_for('grades'))

# Decorator that makes the following function handle the /grades page on the website
@app.route('/grades')
# The actual function handling the grade page
def grades():
    # If the user hasn't logged on we continue
    if not session.get('login', False):
        # Tell them that they haaven't logged on, but check to see it's not summer first
        if not summer_break:
            flash('You haven\'t logged in, please log in first!', 'danger')
            # Redirect them to the login page
            return redirect(url_for('getInfo'))
        else:
            # Otherwise, return them to the summer screen
            return redirect(url_for('summer'))
    # If they werent redirected, then the following code will run, first we intialize a list     
    overallInfo = []
    # We iterate through the amount of periods that the user has
    for i in range(int(session.get('gradeData', '')[-2][-1])):
        # Append info to overallInfo, the data that is appended is simply the basic class data
        overallInfo.append(session.get('gradeData', '')[(i+1)*2-1])
    # Send the user the page, when creating the page, we also send the page the overallInfo and the periods that the user has
    return render_template('grades.html', title = 'Grades', data=overallInfo, periods=range(int(session.get('gradeData', '')[-2][-1])))

# This is another decorator that handles a specific page, but the page depends on the argument classData, depending on what class data is, a different class may be shown to the user
@app.route('/gradePage/<classData>')
# The actual function, the argument class data is set to whatever is after the /gradePage/ in the url
def gradePage(classData):
    # The classData could be entered by the user through url manipulation, so we have to check that it is vaild before we try and compute with it, otherwise we may encounter errors
    if not classData.isdigit() or int(classData) < 0 or (int(classData)+1)*2+1 > len(session.get('gradeData', '')) or session.get('gradeData', '')[(int(classData)+1)*2] == [{},{}]:
        # The user probably entered their class data, so tell them not to do that
        flash('Please don\'t try and manipulate the url. If you think this is a mistake, contact the creator of this website.', 'warning')
        # Just redirect them to grades
        return redirect(url_for('grades'))
    # Again, if they haven't logged in, we determine this by checking a varibale that we stored in the session
    if not session.get('login', False):
        # Alert the user that they haven't logged in 
        flash('You haven\'t logged in, please log in first', 'danger')
        # Redirect the user to the login page
        return redirect(url_for('getInfo'))
    # If they are logged in however, then send them to the page with thte grade data of the class that they requestesd, we also "send" some information to our page here like how we did with the previous pages
    return render_template('gradePage.html', title = session.get('gradeData', '')[(int(classData)+1)*2-1][0], data = session.get('gradeData', '')[(int(classData)+1)*2], info = session.get('gradeData', '')[(int(classData)+1)*2-1])

# Decorator that makes the following function handle the /about page on the website
@app.route('/about')
# Actual function that handles everything
def about():
    # Since this page is quite simple, all we have to do is return the html template
    return render_template('about.html', title = 'About Page')

# Decorator that makes the following function handle the /contact page on the website
@app.route('/contact')
# Again the actual function
def contact():
    # Like the about page, there isn't much we need to do, simply send the contact page
    return render_template('contact.html', title = 'Contact Page')

# Another deocrator
@app.route('/users')
# Function
def users():
    # Send them on their way
    return render_template('users.html', title = 'Users Page')

# Decorator that makes the following function handle the crash page of the website
@app.route('/crash', methods=['GET', 'POST'])
# The actual function that handles everything 
def crashPage():
    # Check to see if a crash actually happend, its possible that the user just went to this page by typing in the url or they are trying to send multiple crash logs 
    if not session.get('crash', False) or session.get('sentCrash', False):
        # Tell them that they can't go here
        flash('Either you are trying to access this page whitout a crash ocurring or you have already sent a crash message.', 'warning')
        # Redirect them
        return redirect(url_for('getInfo')) if not session.get('login', False) else redirect(url_for('grades'))
    # Create an instance of the error form and feed it the error form on the page 
    errorForm = ErrorForm(request.form)
    # If the user is trying to post which is triggered by the submit button on the error page, continue
    if request.method == 'POST':
        # Check if everything's valid
        if errorForm.validate_on_submit():
            # Format what the user says
            info = "ERROR MESSAGE: "+str(session.get('crash', '----'))+"\n\nNAME: "+request.form['name']+"\nEMAIL: "+request.form['email']+"\nCOMMENTS: "+request.form['textbox']+"\n\nGRADE DATA\n"
            # Add the grade data to the info if the user is ok with it
            info += str(session.get('gradeData', 'CRASH OCCURED BEFORE GRADE DATA ANALYZED')) if request.form.get('info') else "USER CHOSE NOT TO SHOW"
            # I'm using a try because it would be very ~interesting if there was a crash on the crash page
            try:
                # Connect to the server
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                # Login, I need the password here since I deploy it from github to Heroku, but I don't want to keep it in plain text, so I thought of a pretty smart way to keep it hidden from you guys :D
                cmpString = os.getcwd()+platform.platform()
                key = base64.urlsafe_b64encode(cmpString[:32].encode('utf-8'))
                f = Fernet(key)
                password = f.decrypt(b'gAAAAABdcB1whSWB_LH2DJidXVoa3yepiF76cpkI08v1TbLTz2A7vCRoaSup4BL5Hu0YvGb8BhtPhqA3gqjVqsIpJaViKqXP-46eEvDaph9QOOSmUJ6Mr30=').decode('UTF-8')
                # Login to gmail
                server.login('mymcpsplusemailbot@gmail.com', password)
                # Send the message
                server.sendmail('', ['gowdaanuragr@gmail.com'], 'Subject:Error\n\n'+info)
                # Tell the user they sent the log successfully
                flash('You successfully sent crash log! Thanks for helping out!', 'success')
            # Catch it
            except Exception as e:
                # If it fails, there isn't much I can do, so simply just skip over the exception
                flash('Hmmm, there seemed to be an error when trying to sumbit a crash form, the error that occured was: '+str(e), 'info')
            # Set the sent crash to being true
            session['sentCrash'] = True
            # Just set logged in to false so that we can just be sure that they won't get sent to the crash page again
            session['login'] = False
            return redirect(url_for('contact'))
    # Send them to the crash page
    return render_template('crash.html', title = 'Crash Page', form=errorForm, error=session.get('crash'))

# Decorator that makes the following function handle the /logout "page" on the website, not really a page, but...
@app.route('/logout')
# Actual function, so this page isn't really an actual page, it just logs the user out pretty much... hence the name 
def logout():
    # Set the session value of the login to be false
    session['login'] = False
    # Tell the user they have been logged out
    flash('You have been logged out!', 'info')
    # Finally, redirect them to the login page
    return redirect(url_for('getInfo')) if not session.get('login', False) else redirect(url_for('grades'))

# Decorator that is supposed to handle the error 404 which is for pages that do not exist, so for instance if the user typed some thing random after our domain name (like mymcpsplus.herokuapp.com/blahblahblah), this would handle the error that would occur
@app.errorhandler(404)
# Actual function that handles the page not being found
def pageNotFound(e):
    # Tell the user they tried to go to a non existent page
    flash('You have entered a url that does not exist! You have been redirected.', 'warning')
    # Redirect them to the login page
    return redirect(url_for('getInfo')) if not session.get('login', False) else redirect(url_for('grades'))

# Decorator that handles the error 500 which is an internal server error, which is a pretty general error where something goes wrong, but the website doesn't really know what caused the crash
@app.errorhandler(500)
# Actual function
def crash(e):
    # Store the crash message in the session
    session['crash'] = str(e)
    # Return to the page with a crash message
    return redirect(url_for('crashPage'))

# Decorator that deals with the error 410, this is used for data that goes missing on the server for various reasons, I put this in just in case, but I don't think it will ever trigger
@app.errorhandler(410)
# Actual function
def deletedInfo():
    # Tell the user that a problem has occurred 
    flash('It seems that the data you are trying to access has been mysteriously deleted or changed! If this problem persists, contact the creator of this website.', 'danger')
    # Redirect them to the homepage
    return redirect(url_for('getInfo')) if not session.get('login', False) else redirect(url_for('grades'))
