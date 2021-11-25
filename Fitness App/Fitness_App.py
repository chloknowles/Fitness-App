import os.path
import webbrowser
from guizero import App, Window, PushButton, info, Text, TextBox, ButtonGroup, ListBox, Picture, Box, CheckBox # Widgets used throughout the forms
import sqlite3		# Database
from sqlite3 import Error
import os
# Global variables
global stored_userid # The user that is currently logged in
global premium_user # This variable holds whether the user is a premium member or not
#
#	
#  This DDL creates my users table
sql = """
CREATE TABLE "fitness_users" (
	"UserID"	INTEGER NOT NULL,
	"Email_address"	TEXT,
	"User_name"	TEXT,
	"User_password"	TEXT,
	"Premium_member" INTEGER,
	PRIMARY KEY("UserID" AUTOINCREMENT)
);
Insert into fitness_users (Email_address, User_name, User_password, Premium_member) values ('chloe@me.com', 'chloe123', '12345', 1);
Insert into fitness_users (Email_address, User_name, User_password, Premium_member) values ('chloe123@me.com', 'chloe', '12345', 0);
"""


### MAIN PROGRAM ###

################################################
# Database name (global variable)
database_file = 'fitness_database.db'
# Delete the database
if os.path.exists(database_file):
    os.remove(database_file)

# Connect to the database
conn = sqlite3.connect(database_file)
# Get a cursor pointing to the database
cursor = conn.cursor()
# Create the tables
cursor.executescript(sql)
# Commit to save everything
conn.commit()
# Close the connection to the database
#################################################

def open_login():
    login_window.show()
    app.hide()

def open_signup():
    signup_window.show()
    app.hide()

def open_standard():
    login_window.hide()
    signup_window.hide()
    standard_window.show()

def open_premium():
    login_window.hide()
    signup_window.hide()
    premium_window.show()

def open_social_media():
    social_media_window()


def open_trainers():
    personal_trainer_window.show()

def open_healthyliving():
    healthyliving_window.show()

def open_fitnessadvice():
    fitnessadvice_window.show()

def open_workouts():
    workout_window.show()

def open_advice():
    advice_window.show()


### TITLE PAGE ###
app = App(title="Login or Sign up")
text_blank = Text(app, text=" ")
text_blank = Text(app, text=" Welcome to ToKa Fitness ")
text_blank = Text(app, text=" ")
picture = Picture(app, image="homepage.jpg", height = 200, width = 400)
text_blank = Text(app, text=" ")
text_blank = Text(app, text=" ")

box1 = Box(app, layout = "grid", border = False)

login_button = PushButton(box1, text="Login", command = open_login, height = 1, width = 13, grid = [0,0])
login_button.bg = "light grey"
text_blank = Text(box1, text="              ", grid = [1,0])

signup_button = PushButton(box1, text = "Sign up", command = open_signup, height = 1, width = 13, grid = [2,0])
signup_button.bg = "light grey"




### LOGIN PAGE ###

def login_process(): ### Login form validation and checks email and password ###
    global stored_userid ## variable needed in all forms ##
    global premium_user
    if username_textbox.value == " ":
        info("Error", "You must enter a valid username")
    elif password_textbox.value == " ":
        info("Error", "You must enter a password")

    else:
        username = username_textbox.value
        password = password_textbox.value
        ### set up SQL to find username on the database ###
        sqlselect = "SELECT * FROM fitness_users WHERE User_name = '"+username+"'"
        rows = query_database(database_file, sqlselect)
        if len(rows) == 0: ### This checks that the user was found ###
            info("Error","Error")
        else:
            ### Stored UserID is stored as rows[0,0]
            stored_userid = (rows[0][0])  # We need this as a foreign key
            storedusername = (rows[0][2])
            storedpassword = (rows[0][3])
            premium_user = (rows[0][4])
            if username == storedusername and password == storedpassword:
                info("Log in","Success")
                if premium_user == 1:
                    open_premium()
                elif premium_user == 0:
                    open_standard()
            else:
                info("Error","Incorrect")


login_window = Window(app, title="Login")
login_window.hide()
text_blank = Text(app, text=" ")
text_blank = Text(app, text=" ")
login_title = Text(login_window, text ="Login")
login_title.text_size = 20
text_username = Text(login_window, text="Enter Username:")
text_username.text_color = "black"
username_textbox = TextBox(login_window, width = 20)
username_textbox.bg = "white"
text_password = Text(login_window, text="Enter Password:")
text_password.text_color = "black"
password_textbox = TextBox(login_window, hide_text=True, width = 20)
password_textbox.bg = "white"
button_login = PushButton(login_window, text = "Log in", command = login_process)


### Run a query to SELECT ###
def query_database(database, query):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows




### SIGN UP PAGE ###

### Creates an account ###
def sql_createacc(entities): #CREATE ACCOUNT
    conn = sqlite3.connect('fitness_database.db')
    cursorObj = conn.cursor()
    create_query = "INSERT INTO fitness_users (Email_address, User_name, User_password, Premium_member) VALUES (?,?,?,?)"
    cursorObj.execute(create_query, entities)
    conn.commit()

def signup_process(): ### Process for creating an account ###
    global stored_userid ## global variable used again
    global premium_user
    EmailA = signup_textbox_email.value
    NameUser = signup_textbox_username.value
    Pword = signup_password_textbox.value
    Prem = signup_premium_checkbox.value
    print (Prem)
    premium_user = 0
    if EmailA == "" or NameUser == "" : 
        info("ERROR","All details must be entered")
    elif len(Pword) < 5:
        info("ERROR","Pasword must be atleast 5 characters long")
    elif '@' not in EmailA:
        info("ERROR", "Please enter a valid email.")
    elif Prem == 1:
        premium_user = 1
    elif Prem == 0:
        premium_user = 0

    # insert user as all credential correct
    entities = (EmailA,NameUser, Pword, premium_user)
    sql_createacc(entities)
    info("INSERT USER","Account Created")
     ### set up SQL to find new user on the database ###
    sqlselect = "SELECT * FROM fitness_users WHERE Email_address = '"+ EmailA +"'"
    rows = query_database(database_file, sqlselect)
    if len(rows) == 0: ### This checks that the user was found ###
        info("Error","New user not found")
    else:
        ### Stored UserID is stored as rows[0,0]
        stored_userid = (rows[0][0])  
        storedemail = (rows[0][1])
        if premium_user == 1:
            open_premium()
        elif premium_user == 0:
            open_standard()
      

signup_window = Window(app, title="Sign Up")
signup_window.hide()
text_blank = Text(app, text=" ")
text_blank = Text(app, text=" ")
signup_title = Text(signup_window, text ="Sign Up")
signup_title.text_size = 20 
signup_text_email = Text(signup_window, text = "Enter an Email Address:")
signup_textbox_email = TextBox(signup_window, width = 20)
signup_text_username = Text(signup_window, text = "Enter a Username:")
signup_textbox_username = TextBox(signup_window, width = 20)
signup_textbox_username.bg = "white"
signup_text_password = Text(signup_window, text="Enter a Password:")
signup_text_password.text_color = "black"
signup_password_textbox = TextBox(signup_window, hide_text=True, width = 20)
signup_password_textbox.bg = "white"
signup_premium_checkbox = CheckBox(signup_window, text="Become a premium member")
signup_button_signup = PushButton(signup_window, text = "Sign up", command = signup_process)
signup_cookies_checkbox = CheckBox(signup_window, text = "Allow cookies")

### STANDARD PAGE ###
standard_window = Window(app, title = "Standard users")
standard_window.hide()
standard_window.bg = "#59bfff"
standard_title1 = Text(standard_window, text = "Welcome to the standard")
standard_title1.font = "britannic bold"
standard_title1.text_size = 20
standard_title2 = Text(standard_window, text = "ToKa Fitness page")
standard_title2.font = "britannic bold"
standard_title2.text_size = 20
standard_picture = Picture(standard_window, image="standard.jpeg", height = 200, width = 400)
choose_trainer_button = PushButton(standard_window, text = "Choose a personal trainer", command = open_trainers)
fitness_advice_button = PushButton(standard_window, text = "Free fitness advice", command = open_fitnessadvice)
healthy_living_advice_button = PushButton(standard_window, text = "Free healthy living advice", command = open_healthyliving)

# Personal trainer window #
personal_trainer_window = Window(app,title = "Personal trainers")
personal_trainer_window.hide()
trainers_title = Text(personal_trainer_window, text = "Meet our personal trainers")
trainers_title.font = "britannic bold"
trainers_title.text_size = 20
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
box2 = Box(personal_trainer_window, layout = "grid", border = False)
box3 = Box(box2, border = False, grid = [0,3])
box4 = Box(box2, border = False, grid = [1,3])
box5 = Box(box2, border = False, grid = [2,3])
box6 = Box(box2, border = False, grid = [0,4])
box7 = Box(box2, border = False, grid = [1,4])
box8 = Box(box2, border = False, grid = [2,4])
marlon_picture = Picture(box3, image="marlonbetter.jpg", height = 150, width = 150)
ash_picture = Picture(box4, image="ashbetter.jpg", height = 150, width = 150)
jack_picture = Picture(box5, image="jackbetter.jpg", height = 150, width = 150)
marlontitle = Text(box6, text = "Lomk")
marlontitle.text_size = 15
ashtitle = Text(box7, text = "Gub")
ashtitle.text_size = 15
jacktitle = Text(box8, text = "Phil")
jacktitle.text_size = 15
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
text_blank = Text(personal_trainer_window, text=" ")
contact = Text(personal_trainer_window, text = "Contact 07895743037 to arrange a free session")
contact.font = "britannic bold"

# Healthy living advice page #
healthyliving_window = Window(app, title = "Healthy living")
healthyliving_window.hide()
healthyliving_window.bg = "#62BD69"
healthy_title = Text (healthyliving_window, text = "Healthy living and advice")
healthy_title.font = "britannic bold"
healthy_title.text_size = 20
healthy_title.text_size = 20
plate = Picture(healthyliving_window, image="healthyplate.jpg", height = 200, width = 300)
healthylive = Picture(healthyliving_window, image="healthylive.jpg", height = 250, width = 300)

# Fitness advice page #
fitnessadvice_window = Window(app, title = "Fitness advice")
fitnessadvice_window.hide()
fitnesstitle = Text(fitnessadvice_window, text = "Fitness advice")
tips = Picture(fitnessadvice_window, image="fitnesstips.jpg", height = 240, width = 300)
advice = Picture(fitnessadvice_window, image="fitnessadvice.jfif", height = 240, width = 300)



### PREMIUM PAGE ###
premium_window = Window(app, title = "Premium users")
premium_window.hide()
premium_window.bg = "#c69e3c"
premium_title1 = Text (premium_window, text = "Welcome to the premium")
premium_title2 = Text (premium_window, text = "ToKa Fitness page")
premium_title1.font = "algerian"
premium_title1.text_color = "white"
premium_title1.text_size = 20
premium_title2.font = "algerian"
premium_title2.text_color = "white"
premium_title2.text_size = 20
premium_picture = Picture(premium_window, image="premium.jpg", height = 200, width = 400)
go_to_standard_button = PushButton(premium_window, text = "Click here to go to the standard users page", command = open_standard)
view_workout_button = PushButton(premium_window, text = "View a workout", command = open_workouts)
def social_media_window():
    webbrowser.open('https://www.fitnessblender.com/', new=2)
social_media_button = PushButton(premium_window, text = "Go to our social media page", command = open_social_media)
eating_plan_button = PushButton(premium_window, text = "See food advice", command = open_advice)

# Workout page #
def open_lunges():
    lunge_window.show()
    
def open_squats():
    squat_window.show()

def open_russians():
    russian_window.show()


def open_crunches():
    crunches_window.show()

def open_burpees():
    burpees_window.show()

def open_dumbellcurl():
    dumbellcurl_window.show()

def open_shoulderpress():
    shoulderpress_window.show()

def open_chestfly():
    chestfly_window.show()

def open_deadlift():
    deadlift_window.show()

def open_barbell():
    barbell_window.show()

lunge_window = Window(app, title = "Lunge")
lunge_window.hide()
lunge_gif = Picture(lunge_window, image="lunge.gif")

squat_window = Window(app, title = "Squats")
squat_window.hide()
squat_gif = Picture(squat_window, image="squats.gif")

russian_window = Window(app, title = "Russian twists")
russian_window.hide()
russian_gif = Picture(russian_window, image="russian.gif")

crunches_window = Window(app, title = "crunches")
crunches_window.hide()
crunches_gif = Picture(crunches_window, image="crunches.gif", height = 250, width = 440)

burpees_window = Window(app, title = "Burpees")
burpees_window.hide()
burpees_gif = Picture(burpees_window, image="burpees.gif")

dumbellcurl_window = Window(app, title = "Dumbell curls")
dumbellcurl_window.hide()
dumbellcurl_gif = Picture(dumbellcurl_window, image="dumbellcurl.gif", height = 400, width = 440)

shoulderpress_window = Window(app, title = "Shoulder press")
shoulderpress_window.hide()
shoulderpress_gif = Picture(shoulderpress_window, image="shoulderpress.gif", height = 400, width = 400)

chestfly_window = Window(app, title = "Chest fly")
chestfly_window.hide()
chestfly_gif = Picture(chestfly_window, image="chestfly.gif")

deadlift_window = Window(app, title = "Deadlift")
deadlift_window.hide()
deadlift_gif = Picture(deadlift_window, image="deadlift.gif")

barbell_window = Window(app, title = "Barbell rows")
barbell_window.hide()
barbell_gif = Picture(barbell_window, image="barbell.gif")


workout_window = Window(app, title = "View a workout")
workout_window.hide()
workout_title = Text(workout_window, text = "Click on a workout")
workout_title.text_size = 20
workout_title.font = "algerian"
lunges = PushButton(workout_window, text = "Lunges", command = open_lunges, height = 1, width = 13)
squats = PushButton(workout_window, text = "Squats", command = open_squats, height = 1, width = 13)
russian = PushButton(workout_window, text = "Russian twists", command = open_russians, height = 1, width = 13)
crunches = PushButton(workout_window, text = "Bicycle crunches", command = open_crunches, height = 1, width = 13)
burpees = PushButton(workout_window, text = "Burpees", command = open_burpees, height = 1, width = 13)
dumbellcurl = PushButton(workout_window, text = "Dumbell curls", command = open_dumbellcurl, height = 1, width = 13)
shoulderpress = PushButton(workout_window, text = "Shoulder press", command = open_shoulderpress, height = 1, width = 13)
chestfly = PushButton(workout_window, text = "Chest fly", command = open_chestfly, height = 1, width = 13)
deadlift =  PushButton(workout_window, text = "Deadlifts", command = open_deadlift, height = 1, width = 13)
barbell = PushButton(workout_window, text = "Barbell rows", command = open_barbell, height = 1, width = 13)


advice_window = Window(app, title = "Advice")
advice_window.hide()
advice_title = Text(advice_window, text = "Food advice")
advice_title2 = Text(advice_window, text = "Please choose a selection of foods to show interesting advice")
### Food advice ###
def clearitems():
    listbox_advice.clear()
    advice_list.clear()
    chicken.value = 0
    fish.value = 0
    tofu.value = 0
    broccoli.value = 0
    carrots.value = 0
    leafs.value = 0
    pasta.value = 0
    rice.value = 0
    bread.value = 0
    avocado.value = 0
    nuts.value = 0
    olives.value = 0

def food_options():
    global advice_list
    if chicken.value == 1:
        advice_list.append("Chicken is a lean meat with high nutritional value, and eating it regularly will help you stay healthy.")
    if fish.value == 1:
        advice_list.append("Fish is rich in calcium and phosphorus and a great source of minerals, such as iron, zinc, iodine, magnesium, and potassium.")
    if tofu.value == 1:
        advice_list.append("Tofu contains several anti-inflammatory, antioxidant phyto-chemicals making it a great addition to an anti-inflammatory diet.")
    if broccoli.value == 1:
        advice_list.append("Broccoli is a good carb and is high in fiber")
    if carrots.value == 1:
        advice_list.append("Carrots have calcium and vitamin K, both of which are important for bone health.")
    if leafs.value == 1:
        advice_list.append("Leafy greens are packed with vitamins, minerals and fiber but low in calories.")
    if pasta.value == 1:
        advice_list.append("Pasta has sustained energy which provides glucose, the crucial fuel for your brain and muscles.")
    if rice.value == 1:
        advice_list.append("Rice helps maintain a healthy weight, supports energy and restores glycogen levels after exercise.")
    if bread.value == 1:
        advice_list.append("The whole grains in wholemeal bread can boost overall health and help reduce the risk of obesity and various other complications and diseases.")
    if avocado.value == 1:
        advice_list.append("Avocados are an excellent source of potassium, folate and fibre, all of which benefit the heart and cardiovascular system.")
    if nuts.value == 1:
        advice_list.append("Nuts are loaded with antioxidants, aid with weightloss, and are high in beneficial fibre.")
    if olives.value == 1:
        advice_list.append("Olives are very high in vitamin E and other powerful antioxidants. They are good for the heart and may protect against osteoporosis and cancer.")



# after list is completed, add to list box
    
    for line in range (0,len(advice_list)):
        listbox_advice.append(advice_list[line])

advice_list = []

mainbox = Box(advice_window, layout = "grid", border = False)
proteinbox = Box(mainbox, border = True, grid = [0,0], width = 200, height = 100)
text_blank = Text(mainbox, text="  ", grid = [1,0])
text_blank = Text(mainbox, text="  ", grid = [1,1])
text_blank = Text(mainbox, text="  ", grid = [0,1])
text_blank = Text(mainbox, text="  ", grid = [2,1])
text_blank = Text(mainbox, text="  ", grid = [1,2])
veggiebox = Box(mainbox, border = True, grid = [2,0], width = 200, height = 100)
carbbox = Box(mainbox, border = True, grid = [0,2], width = 200, height = 100)
fatbox = Box(mainbox, border = True, grid = [2,2], width = 200, height = 100)

proteintitle = Text(proteinbox, text = "Protein options")

chicken = CheckBox(proteinbox, text="Chicken", command= None)
fish = CheckBox(proteinbox,    text="Fish   ", command= None)
tofu = CheckBox(proteinbox,    text="Tofu   ", command= None)

vegtitle = Text(veggiebox, text = "Vegetable options")

broccoli = CheckBox(veggiebox, text="Broccoli    ", command= None)
carrots = CheckBox(veggiebox,  text="Carrots     ", command= None)
leafs = CheckBox(veggiebox,    text="Leafy greens", command= None)

carbtitle = Text(carbbox, text = "Carbohydrate options")

pasta = CheckBox(carbbox, text="Pasta", command= None)
rice = CheckBox(carbbox,  text="Rice ", command= None)
bread = CheckBox(carbbox, text="Bread", command= None)

fattitle = Text(fatbox, text = "Healthy fats options")

avocado = CheckBox(fatbox, text="Avocado", command= None)
nuts = CheckBox(fatbox,    text="Nuts   ", command= None)
olives = CheckBox(fatbox, text= "Olives ", command= None)

listbox_advice = ListBox(advice_window, items=[""], height = 200, width= 1500)
done_button = PushButton (advice_window, text = "Show advice", command = food_options)
clear_button = PushButton(advice_window, text = "Clear advice", command = clearitems)




app.display()


