#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import time, threading
from ConfigParser import SafeConfigParser

# Reading configuration file  
parser = SafeConfigParser()
parser.read('config.ini')
parameters = {} 								# Dictionary for storing the parsed parameters

for section_name in parser.sections():			# Parsing the configuration file and reading it into the dictionary
	for name, value in parser.items(section_name):
		parameters[name] = value

# Automating your browser 
driver = webdriver.Chrome()						# Using the Chrome driver - there are 10 other drivers which you can use like Firefox, PhantomJS etc.
driver.get("http://www.quora.com")				# Quora home page url 
time.sleep(3)									# For Quora home page to load properly - adjust as per your requirement

# Logging into Quora using your email and password 
form = driver.find_element_by_class_name('regular_login')
email = form.find_element_by_name("email")
password = form.find_element_by_name("password")
email.send_keys(parameters["email_id"])
try:
	pass_word = parameters["pass_word"]
except:
	pass_word = getpass.getpass()				# In case you don't feel it safe to store your password in plaintext on your pc
password.send_keys(pass_word)
password.send_keys(Keys.RETURN)
time.sleep(2)									

# Getting to your crush's answers ;) 
answers_link = "https://www.quora.com/" + parameters["user_name"] + "/answers"		# Link to answers of your crush 
driver.get(answers_link)									# Retrieving the answers of your crush
time.sleep(2)

# Let's retrieve the whole page so that you don't miss a single answer of your crush 
while 1:
	a = driver.execute_script("return document.body.scrollHeight;")
	print a
	t_end = time.time() + int(parameters["timeout_seconds"])								
	while time.time() < t_end:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	b = driver.execute_script("return document.body.scrollHeight;")
	if(a==b):
		break;
	print b

print 'Yippeeee all answers are retrieved\n Let\'s upvote them now ;)\n'

# Time to upvote the answers ;) 
if parameters["up_vote"] == 'add':				# In case you want to get your crush's attention ;) 
	driver.execute_script("window.a = document.getElementsByClassName('add_upvote');")			# Retrieving all the upvote items in an array 
else:								# In case your ex is on Quora :P 
	driver.execute_script("window.a = document.getElementsByClassName('remove_upvote');")		# Retrieving all the upvote items in an array 
driver.execute_script("for(var i=0; i<a.length; i++) { a[i].click(); }")					# Clicking on each and every item one by one

if parameters["up_vote"] == 'add':
	print 'All answers upvoted :D\n'
else:
	print 'All upvotes removed :P\n'
