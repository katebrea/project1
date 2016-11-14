#make sure that both the office and the home of someone like charlie weasley is displayed (for now it only shows his office)
#test sql injection
#!/usr/bin/env python2.7
#peng is going to check whether it's simple to change the dropdown on the html to display the relevant form.

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# two global variables: transmitting search information between functions
search_input = ''
search_type = 0

### login to google console command line: psql -U <your uni> postgres -h 104.196.175.120
### Kate: klb2180:6h42a
### Peng: pg2539:45nbd
DATABASEURI = "postgresql://klb2180:6h42a@104.196.175.120/postgres"  

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)





@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

########## NOTE ###############
# This bunch of funcitons below are very similar to one another. Each function corresponds to a query in a single table.
# In each function, inputs specifies the name and value of attribute we would like to search, 
# and the function returns an indicator which shows whether there is data in search result (0: query reutrns empty table; 1 otherwise), 
# as well as a list storing the search result.
#############################

def searchTable_characters(search_input, input_type = 'name'):
  print '\nquerying table Characters'
  cmd = 'SELECT * FROM characters WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_basic_info = 1
    raw_data = cursor.fetchone()
    uid = raw_data[0]
    data = []
    for n in raw_data[1: ]:
      data.append(n)
  else:
    print 'item not found'
    have_basic_info = 0
    uid = 0
    data = []

  cursor.close()
  return (have_basic_info, uid, data)

#Peng will change home name from a variable to a list so we can report both home and office
def searchTable_use(search_input, input_type = 'user_uid'):
  print '\nquerying table Use'
  cmd = 'SELECT * FROM use WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)
  have_use = 0
  have_home = 0
  home_name = ''
  have_office = 0
  office_name = ''

  # There may be up to 1 'home' & 'office' for each character 
  if cursor.rowcount > 0:
    print 'item found'
    have_use = 1
    raw_dataset = cursor.fetchall()
    for raw_data in raw_dataset:
      if raw_data[2] == 'home':
        have_home = 1
        home_name = raw_data[0]
      if raw_data[2] == 'office':
        have_office = 1
        office_name = raw_data[0]
  else:
    print 'item not found'

  cursor.close()
  return (have_use, have_home, home_name, have_office, office_name)


def searchTable_places(search_input, input_type = 'name'):
  print '\nquerying table Places'
  cmd = 'SELECT * FROM places WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_place = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data:
      data.append(n)
  else:
    print 'item not found'
    have_place = 0
    data = []

  cursor.close()
  return (have_place, data)


def searchTable_students(search_input, input_type = 'uid'):
  print '\nquerying table Students'
  cmd = 'SELECT * FROM students WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    is_student = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data[1: ]:
      data.append(n)
  else:
    print 'item not found'
    is_student = 0
    data = []

  cursor.close()
  return (is_student, data)


def searchTable_take(search_input, input_type = 'student_uid'):
  print '\nquerying table Take'
  cmd = 'SELECT * FROM take WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
  # it's possible that a student has taken more than one classes
    have_class = 1
    raw_data_list = cursor.fetchall()
    data = []
    for n in raw_data_list:
      data.append(n[2])
  else:
    print 'item not found'
    have_class = 0
    data = []

  cursor.close()
  return (have_class, data)


def searchTable_plays_for(search_input, input_type = 'player_uid'):
  print '\nquerying table Plays_for'
  cmd = 'SELECT * FROM plays_for WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    is_quidditch_plr = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data[ :-1]:
      data.append(n)
  else:
    print 'item not found'
    is_quidditch_plr = 0
    data = []

  return (is_quidditch_plr, data)


def searchTable_houses(search_input, input_type = 'name'):
  print '\nquerying table Houses'
  cmd = 'SELECT * FROM houses WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_house = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data[1: ]:
      data.append(n)
  else:
    print 'item not found'
    have_house = 0
    data = []

  return (have_house, data)


def searchTable_faculty(search_input, input_type = 'uid'):
  print '\nquerying table Faculty'
  cmd = 'SELECT * FROM faculty WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    is_faculty = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data[1: ]:
      data.append(n)
  else:
    print 'item not found'
    is_faculty = 0
    data = []

  return (is_faculty, data)


def searchTable_head_of(search_input, input_type = 'head_uid'):
  print '\nquerying relation Head_of'
  cmd = 'SELECT name FROM houses WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    is_head = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data:
      data.append(n)
  else:
    print 'item not found'
    is_head = 0
    data = []

  return (is_head, data)

def searchTable_teach(search_input, input_type = 'faculty_uid'):
  print '\nquerying table Teach'
  cmd = 'SELECT * FROM teach WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
  # it's possible that a student has taken more than one classes
    is_teaching = 1
    raw_data_list = cursor.fetchall()
    data = []
    for n in raw_data_list:
      data.append(n[2])
  else:
    print 'item not found'
    is_teaching = 0
    data = []

  cursor.close()
  return (is_teaching, data)


def searchTable_class(search_input, input_type = 'name'):
  print '\nquerying table class:'
  cmd = 'SELECT * FROM class WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_class = 1
    raw_data = cursor.fetchone()
    #print raw_data
    data = []
    # classroom_loc = data[2]
    for n in raw_data:
      data.append(n)
  else:
    print 'item not found'
    have_class = 0
    data = []

  cursor.close()
  return (have_class, data)


def searchTable_teach_join_characters(search_input, input_type = 'class_name'):
  print '\nquerying table teach_join_characters'
  cmd = 'SELECT * FROM teach t, characters c WHERE t.faculty_uid = c.uid and %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_teacher = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data:
      data.append(n)
  else:
    print 'item not found'
    have_teacher = 0
    data = []

  cursor.close()
  return (have_teacher, data)


def searchTable_take_join_characters(search_input, input_type = 'class_name'):
  print '\nquerying table take_join_characters'
  cmd = 'SELECT * FROM take t, characters c WHERE t.student_uid = c.uid and %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_student = 1
    raw_dataset = cursor.fetchall()
    data = []
    for n in raw_dataset:
      data.append(n)
  else:
    print 'item not found'
    have_student = 0
    data = []

  cursor.close()
  return (have_student, data)


def searchTable_textbook(search_input, input_type = 'class_name'):
  print '\nquerying table textbook'
  cmd = 'SELECT * FROM textbook WHERE %s = :si' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_textbook = 1
    raw_data = cursor.fetchone()
    data = []
    for n in raw_data:
      data.append(n)
  else:
    print 'item not found'
    have_textbook = 0
    data = []

  cursor.close()
  return (have_textbook, data)


def searchTable_plays_for_join_characters(search_input, input_type = 'house_name'):
  print '\nquerying table plays_for joining characters'
  cmd = 'SELECT p.h_from, p.h_to, p.position, c.name FROM plays_for p, characters c WHERE p.%s = :si and p.player_uid = c.uid' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_quidditch = 1
    raw_dataset = cursor.fetchall()
    data = []
    for n in raw_dataset:
      data.append(n)
  else:
    print 'item not found'
    have_quidditch = 0
    data = []

  cursor.close()
  return (have_quidditch, data)

def searchTable_students_join_characters(search_input, input_type = 'house_name'):
  print '\nquerying table students joining characters'
  cmd = 'SELECT s.date_join_hog, c.name FROM students s, characters c WHERE s.%s = :si and s.uid = c.uid' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_student = 1
    raw_dataset = cursor.fetchall()
    data = []
    for n in raw_dataset:
      data.append(n)
  else:
    print 'item not found'
    have_student = 0
    data = []

  cursor.close()
  return (have_student, data)

def searchTable_use_join_characters(search_input, input_type = 'place_name'):
  print '\nquerying table use joining characters'
  cmd = 'SELECT * FROM use u, characters c WHERE u.%s = :si and u.user_uid = c.uid' %(input_type)
  cursor = g.conn.execute(text(cmd), si = search_input)

  if cursor.rowcount > 0:
    print 'item found'
    have_user = 1
    raw_dataset = cursor.fetchall()
    data_home = []
    data_office = []

    for n in raw_dataset:
      print n
      if n[2] == 'home':
        data_home.append(n)
      if n[2] == 'office':
        data_office.append(n)

    if len(data_home) > 0:
      have_home = 1
    else:
      have_home = 0
    if len(data_office) > 0:
      have_office = 1
    else:
      have_office = 0

  else:
    print 'item not found'
    have_user = 0
    have_home = 0
    have_office = 0
    data_home = []
    data_office = []

  cursor.close()
  return (have_user, have_home, data_home, have_office, data_office)


@app.route('/')
def index():
  return render_template("proj1index.html")


#### search type 1 ####
@app.route('/search_result_characters/')
def search_result_characters():

  print "searching for characters..."
  global search_input  # content that is typed into text box when searching
  global search_type   # kind of entity we would like to search: character, location, course, house, or textbooks
  print 'search_input:', search_input
  print 'search_type:', search_type

  # Get the 'first name' of search object
  if len(search_input) != 0:
    search_input_fn = search_input.split()[0]
  else:
    search_input_fn = ''

  # Initializing variables
  have_basic_info = 0
  basic_info_data = []
  have_use = 0
  have_home = 0
  home_name = ''
  home_data = []
  have_office = 0
  office_name = ''
  office_data = []
  is_student = 0
  student_data = []
  have_house = 0
  house_data = []
  have_class = 0
  class_data = []
  is_quidditch_plr = 0
  quidditch_data = []
  is_faculty = 0
  faculty_info = []
  is_head = 0
  head_info = []
  is_teaching = 0
  teaching_info = []

  # calling query functions 
  (have_basic_info, uid, basic_data) = searchTable_characters(search_input)

  if have_basic_info == 1: 
    (have_use, have_home, home_name, have_office, office_name) = searchTable_use(uid)
    (is_student, student_data) = searchTable_students(uid)
    (is_faculty, faculty_info) = searchTable_faculty(uid)

    if have_use == 1:
      if have_home == 1:
        (idx, home_data) = searchTable_places(home_name)
      if have_office == 1:
        (idx, office_data) = searchTable_places(office_name)
    
    if is_student == 1:
      (have_class, class_data) = searchTable_take(uid)
      (is_quidditch_plr, quidditch_data) = searchTable_plays_for(uid)
    
    if is_faculty == 1:  
      (is_head, head_info) = searchTable_head_of(uid)
      (is_teaching, teaching_info) = searchTable_teach(uid)
  
  # generating a dictionary which contains all the indicators and search results

  context = dict(s_input = search_input, s_input_fn = search_input_fn,
    hbi = have_basic_info, u = uid, bd = basic_data, 
    hu = have_use, hhom = have_home, hn = home_name, ho = have_office, officen = office_name, 
    homed = home_data, od = office_data,
    istu = is_student, sd = student_data,
    hc = have_class, cd = class_data,
    iqp = is_quidditch_plr, qd = quidditch_data,
    hh = have_house, hd = house_data,
    ifa = is_faculty, fi = faculty_info,
    ih = is_head, hi = head_info,
    it = is_teaching, ti = teaching_info)

  # passing the indicators and search results to the webpage
  return render_template("search_result_characters.html", **context)
  

#### search type 2 ####
@app.route('/search_result_class/')
def search_result_class():
  
  print "searching for class..."
  global search_input  # content that is typed into text box when searching
  global search_type   # kind of entity we would like to search: character, location, course, house, or textbooks
  print 'search_input:', search_input
  print 'search_type:', search_type  

  # Initializing veriables:
  have_class = 0
  class_info = []
  classroom_loc = ''
  have_teacher = 0
  teacher_info = []
  have_student = 0
  student_info = []
  have_textbook = 0
  textbook_info = []
  have_classroom = 0
  classroom_info = []

  # Querying database
  (have_class, class_info) = searchTable_class(search_input)
  
  if have_class == 1:
    classroom_name = class_info[2]
    (have_teacher, teacher_info) = searchTable_teach_join_characters(search_input)
    (have_student, student_info) = searchTable_take_join_characters(search_input)
    (have_textbook, textbook_info) = searchTable_textbook(search_input)
    (have_classroom, classroom_info) = searchTable_places(classroom_name)

  context = dict(s_input = search_input,
    hc = have_class, ci = class_info,
    ht = have_teacher, ti = teacher_info,
    hs = have_student, si = student_info,
    htx = have_textbook, txi = textbook_info,
    hcr = have_classroom, cri = classroom_info
    )
  
  return render_template("search_result_class.html", **context)


#### search type 3 ####  
@app.route('/search_result_houses/')
def search_result_houses():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  
  print "searching for houses..."
  global search_input  # content that is typed into text box when searching
  global search_type   # kind of entity we would like to search: character, location, course, house, or textbooks
  print 'search_input:', search_input
  print 'search_type:', search_type

  # Initializing variables:
  have_house = 0
  house_info = []
  have_quidditch = 0
  quidditch_info = []
  have_student = 0
  student_info = []
  have_head = 0
  head_faculty_info = []
  head_basic_info = []

  # Querying Database:
  (have_house, house_info) = searchTable_houses(search_input)
  if have_house == 1:
    head_uid = house_info[4]
    (have_quidditch, quidditch_info) = searchTable_plays_for_join_characters(search_input)
    (have_student, student_info) = searchTable_students_join_characters(search_input)
    (have_head, head_faculty_info) = searchTable_faculty(head_uid)
    (have_head, head_uid, head_basic_info) = searchTable_characters(head_uid, 'uid')


  context = dict(s_input = search_input,
    hh = have_house, hi = house_info,
    hq = have_quidditch, qi = quidditch_info,
    hs = have_student, si = student_info,
    hhead = have_head, hfi = head_faculty_info, hbi = head_basic_info
    )
  return render_template("search_result_houses.html", **context)


#### search type 4 ####
@app.route('/search_result_textbooks/')
def search_result_textbooks():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  
  print "searching for textbooks..."
  global search_input  # content that is typed into text box when searching
  global search_type   # kind of entity we would like to search: character, location, course, house, or textbooks
  print 'search_input:', search_input
  print 'search_type:', search_type

  # Initializing variables:
  have_textbook = 0
  textbook_info = []
  have_class = 0
  class_info = []

  # Querying database:
  (have_textbook, textbook_info) = searchTable_textbook(search_input, 'name')
  if have_textbook == 1:
    class_name = textbook_info[3]
    (have_class, class_info) = searchTable_class(class_name)

  context = dict(s_input = search_input,
    ht = have_textbook, ti = textbook_info,
    hc = have_class, ci = class_info
    )
  return render_template("search_result_textbooks.html", **context)


#### search type 5 ####
@app.route('/search_result_places/')
def search_result_places():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  
  print "searching for places..."
  global search_input  # content that is typed into text box when searching
  global search_type   # kind of entity we would like to search: character, location, course, house, or textbooks
  print 'search_input:', search_input
  print 'search_type:', search_type

  # Initializing Data:
  have_place = 0
  place_info = []
  have_class = 0
  class_info = []
  have_user = 0
  have_home = 0
  data_home = []
  have_office = 0
  data_office = []

  # Querying database:
  (have_place, place_info) = searchTable_places(search_input)
  if have_place == 1:
    (have_class, class_info) = searchTable_class(search_input, 'classroom_loc')
    (have_user, have_home, data_home, have_office, data_office) = searchTable_use_join_characters(search_input)

  context = dict(s_input = search_input,
    hp = have_place, pi = place_info,
    hc = have_class, ci = class_info,
    hu = have_user, hh = have_home, dh = data_home, ho = have_office, do = data_office
    )
  return render_template("search_result_places.html", **context)


#### search type unknown ####
@app.route('/search_result_unknown/')
def search_result_unknowntype():
  return render_template("search_result_unknowntype.html")



@app.route('/search', methods=['POST'])
def search():
  global search_input
  global search_type
  search_input = request.form['name']
  search_type = int(request.form['search_type'])
  print 'search input:', search_input
  print 'search type:', search_type

  if search_type == 1:
    return redirect('/search_result_characters/')
  elif search_type == 2:
    return redirect('/search_result_class/')
  elif search_type == 3:
    return redirect('/search_result_houses/')
  elif search_type == 4:
    return redirect('/search_result_textbooks/')
  elif search_type == 5:
    return redirect('search_result_places/')
  else:
    return redirect('/search_result_unknown/')
  

@app.route('/deleteCharacter', methods=['POST'])
def deleteCharacter():
  print "\nenter function deleteCharacter"
  uid= str(request.form['uid'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM characters WHERE uid= :ui'
  g.conn.execute(text(cmd), ui = uid)
  print "\ndeleted data from database successfully"
  return redirect('/')

@app.route('/deleteFaculty', methods=['POST'])
def deleteFaculty():
  print "\nenter function deleteFaculty"
  uid= str(request.form['uid'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM faculty WHERE uid= :ui'
  g.conn.execute(text(cmd), ui = uid)
  print "\ndeleted data from database successfully"
  return redirect('/')


@app.route('/deleteStudent', methods=['POST'])
def deleteStudent():
  print "\nenter function deleteStudent"
  uid= str(request.form['uid'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM students WHERE uid= :ui'
  g.conn.execute(text(cmd), ui = uid)
  print "\ndeleted data from database successfully"
  return redirect('/')

@app.route('/deleteTextbook', methods=['POST'])
def deleteTextbook():
  print "\nenter function deleteTextbook"
  isbn= str(request.form['isbn'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM textbook WHERE isbn= :isb'
  g.conn.execute(text(cmd), isb = isbn)
  print "\ndeleted data from database successfully"
  return redirect('/')


@app.route('/deleteClass', methods=['POST'])
def deleteClass():
  print "\nenter function deleteClass"
  name= str(request.form['name'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM class WHERE name= :n'
  g.conn.execute(text(cmd), n = name)
  print "\ndeleted data from database successfully"
  return redirect('/')


@app.route('/deletePlace', methods=['POST'])
def deletePlace():
  print "\nenter function deletePlace"
  name= str(request.form['name'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM Places WHERE name= :n'
  g.conn.execute(text(cmd), n = name)
  print "\ndeleted data from database successfully"
  return redirect('/')

@app.route('/deletePlayer', methods=['POST'])
def deletePlayer():
  print "\nenter function deletePlayer"
  h_from= str(request.form['h_from'])
  house_name= str(request.form['house_name'])
  player_uid= str(request.form['player_uid'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM plays_for WHERE house_name= :n AND h_from= :h AND player_uid= :pid'
  g.conn.execute(text(cmd), h = h_from, n = house_name, pid = player_uid)
  print "\ndeleted data from database successfully"
  return redirect('/')

@app.route('/deleteTeach', methods=['POST'])
def deleteTeach():
  print "\nenter function deleteTeacher"
  faculty_uid= str(request.form['faculty_uid'])
  class_name= str(request.form['class_name'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM Teach WHERE faculty_uid= :ui AND class_name= :cn'
  g.conn.execute(text(cmd), ui= faculty_uid, cn = class_name)
  print "\ndeleted data from database successfully"
  return redirect('/')

@app.route('/deleteTake', methods=['POST'])
def deleteTake():
  print "\nenter function deleteTake"
  student_uid= str(request.form['student_uid'])
  class_name= str(request.form['class_name'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM Take WHERE student_uid= :ui AND class_name= :cn'
  g.conn.execute(text(cmd), ui= student_uid, cn = class_name)
  print "\ndeleted data from database successfully"
  return redirect('/')


@app.route('/deleteUse', methods=['POST'])
def deleteUse():
  print "\nenter function deleteUse"
  place_name= str(request.form['place_name'])
  user_uid= str(request.form['user_uid'])
  print "\ngethered data from webpage"
  # g.conn.execute("DELETE FROM characters WHERE uid= %s", uid)
  cmd = 'DELETE FROM use WHERE place_name= :pn AND user_uid = :ui'
  g.conn.execute(text(cmd), pn=place_name, ui = user_uid)
  print "\ndeleted data from database successfully"
  return redirect('/')

# @app.route("/", methods=["GET"])
# def hello():
#     return render_template('TEMP.html')

# @app.route('/delete', methods=["GET"])
# def delete():
#     uid= str(request.form['uid'])
#     g.conn.execute("DELETE FROM characters WHERE uid= '%s'" %(uid))
#   #g.conn.execute(characters.delete().where(characters.uid=VALUES('%s'), uid))
#     return redirect('/')


# @app.route('/deleteFaculty', methods=['POST'])
# def deleteFaculty():
#   uid= str(request.form['uid'])
#   g.conn.execute('DELETE FROM Faculty WHERE uid=VALUES (%s)', uid)
#   # cmd = 'DELETE FROM Faculty WHERE uid = VALUES (:ui)'
#   # g.conn.execute(text(cmd), ui = uid)
#   return redirect('/')

#   @app.route('/deleteCharacter', methods=['POST'])
# def deleteCharacter():
#   uid= str(request.form['uid'])
#   g.conn.execute('DELETE FROM characters WHERE uid=VALUES (%s)', uid)
#   return redirect('/')

#   @app.route('/deleteCharacter', methods=['POST'])
# def deleteCharacter():
#   uid= str(request.form['uid'])
#   g.conn.execute('DELETE FROM characters WHERE uid=VALUES (%s)', uid)
#   return redirect('/')

#   @app.route('/deleteCharacter', methods=['POST'])
# def deleteCharacter():
#   uid= str(request.form['uid'])
#   g.conn.execute('DELETE FROM characters WHERE uid=VALUES (%s)', uid)
#   return redirect('/')

#   @app.route('/deleteCharacter', methods=['POST'])
# def deleteCharacter():
#   uid= str(request.form['uid'])
#   g.conn.execute('DELETE FROM characters WHERE uid=VALUES (%s)', uid)
#   return redirect('/')

#   @app.route('/deleteCharacter', methods=['POST'])
# def deleteCharacter():
#   uid= str(request.form['uid'])
#   g.conn.execute('DELETE FROM characters WHERE uid=VALUES (%s)', uid)
#   return redirect('/')

###  The Insert Section


  # def updateTable_characters(search_input, input_type = 'name'):
  # print '\nquerying table Characters'
  # cmd = 'SELECT * FROM characters WHERE %s = :si' %(input_type)
  # cursor = g.conn.execute(text(cmd), si = search_input)


#methods include push, put, get. checks for method defined in html.

@app.route('/addCharacter', methods=['POST'])
def addCharacter():
  print "\nBegin adding data to table 'characters'"
  uid= str(request.form['uid'])
  name = request.form['name'] #request is a form 
  dob = str(request.form['dob'])
  blood_type=request.form['blood_type']
  gender=request.form['gender']
  print "\ncollected data from webpage"

  # g.conn.execute('INSERT INTO characters VALUES (%s,%s,%s,%s,%s)', uid, name, dob, blood_type, gender)
  cmd = 'INSERT INTO characters VALUES (:ui, :na, :do, :bl, :ge)'
  g.conn.execute(text(cmd), ui = uid, na = name, do = dob, bl = blood_type, ge = gender)
  print "\ninserted data to table 'characters'"
  return redirect('/')

#methods include push, put, get. checks for method defined in html.
@app.route('/addFaculty', methods=['POST'])
def addFaculty():
  uid= request.form['uid']
  date_join_hog = str(request.form['date_join_hog'])
  # head_of=request.form['head_of']

  # g.conn.execute('INSERT INTO faculty VALUES (%s,%s)', uid, date_join_hog)
  cmd = "INSERT INTO faculty VALUES (:ui, :da)"
  g.conn.execute(text(cmd), ui = uid, da = date_join_hog)
  return redirect('/')

@app.route('/addClass', methods=['POST'])
def addClass():
  name= request.form['name']
  department = request.form['department']
  classroom_loc=request.form['classroom_loc']
  
  # g.conn.execute('INSERT INTO Class VALUES (%s,%s, %s)', name, department, classroom_loc)
  cmd = "INSERT INTO class VALUES (:na, :de, :cl)"
  g.conn.execute(text(cmd), na = name, de = department, cl = classroom_loc)
  return redirect('/')

@app.route('/addPlace', methods=['POST'])
def addPlace():
  name= request.form['name']
  street_number = request.form['street_number']
  street_name = request.form['street_name']
  zippy=str(request.form['zippy'])
  city=request.form['city']
  country=request.form['country']
  be_classroom_for=request.form['be_classroom_for']
  # g.conn.execute('INSERT INTO Places VALUES (%s,%s,%s,%s,%s,%s)', name, street_number, street_name, zippy, city, country)
  cmd = "INSERT INTO places VALUES (:na, :stnu, :stna, :zi, :ci, :co)"
  g.conn.execute(text(cmd), na = name, stnu = street_number, stna = street_name, zi = zippy, ci = city, co = country)
  return redirect('/')

@app.route('/addStudent', methods=['POST'])
def addStudent():
  uid= str(request.form['uid'])
  date_join_hog = str(request.form['date_join_hog'])
  pet=request.form['pet']
  house_name=request.form['house_name']
  # g.conn.execute('INSERT INTO students VALUES (%s,%s,%s,%s)', uid, date_join_hog, pet, house_name)
  cmd = 'INSERT INTO students VALUES (:ui, :da, :pe, :ho)'
  g.conn.execute(text(cmd), ui = uid, da = date_join_hog, pe = pet, ho = house_name)
  return redirect('/')

# @app.route('/addTeam', methods=['POST'])
# def addTeam():
#   year= str(request.form['year'])
#   #name = request.form['name'] #request is a form 
#   # g.conn.execute('INSERT INTO Quidditch_teams VALUES (%s)', year)
#   cmd = 'INSERT INTO Quidditch_teams VALUES (:ye)'
#   g.conn.execute(text(cmd), ye = year)
#   return redirect('/')

@app.route('/addPlaysFor', methods=['POST'])
def addPlaysFor():
  h_from = str(request.form['h_from'])
  h_to = str(request.form['h_to'])
  house_name = request.form['house_name'] 
  position = request.form['position']
  player_uid=request.form['player_uid']
  # g.conn.execute('INSERT INTO Plays_for VALUES (%s,%s,%s,%s,%s)', h_from, h_to, house_name, position, player_uid)
  cmd = "INSERT INTO plays_for VALUES (:hf, :ht, :ho, :po, :pl)"
  g.conn.execute(text(cmd), hf = h_from, ht = h_to, ho = house_name, po = position, pl = player_uid)
  return redirect('/')

@app.route('/addTextbook', methods=['POST'])
def addTextbook():
  isbn= request.form['isbn']
  name = request.form['name'] 
  author = request.form['author']
  class_name=request.form['class_name']

  # g.conn.execute('INSERT INTO Textbook VALUES (%s,%s,%s,%s)', isbn, name, author, class_name)
  cmd = "INSERT INTO textbook VALUES (:isb, :na, :au, :cl)"
  g.conn.execute(text(cmd), isb = isbn, na = name, au = author, cl = class_name)
  return redirect('/')

@app.route('/addDeed', methods=['POST'])
def addDeed():
  place_name= request.form['place_name']
  user_uid = str(request.form['user_uid'])
  types = request.form['types']
  # g.conn.execute('INSERT INTO Use VALUES (%s,%s,%s)', place_name, user_uid, types)
  cmd = "INSERT INTO use VALUES (:pl, :us, :ty)"
  g.conn.execute(text(cmd), pl = place_name, us = user_uid, ty = types)
  return redirect('/')

@app.route('/addTake', methods=['POST'])
def addTake():
  student_uid= request.form['student_uid']
  since = str(request.form['since'])
  class_name = request.form['class_name']
  # g.conn.execute('INSERT INTO Take VALUES (%s,%s,%s)', student_uid, since, class_name)
  cmd = 'INSERT INTO take VALUES (:st, :si, :cl)'
  g.conn.execute(text(cmd), st = student_uid, si = since, cl = class_name)
  return redirect('/')

@app.route('/addTeach', methods=['POST'])
def addTeach():
  faculty_uid= request.form['faculty_uid']
  since = str(request.form['since'])
  class_name = request.form['class_name']
  # g.conn.execute('INSERT INTO Teach VALUES (%s,%s,%s)', faculty_uid, since, class_name)
  cmd = 'INSERT INTO Teach VALUES (:fa, :si, :cl)'
  g.conn.execute(text(cmd), fa = faculty_uid, si = since, cl = class_name)
  return redirect('/')
#with the put method you have to include both request.args and request.form. 
#pass the character id in the URL and have the new detais in the form. 


# <h2>Updating Records<h2>
# @app.route('/updateCharacter', methods=['POST'])
# def updateCharacter():
#   print "\nBegin updating data to table 'characters'"
#   uid= str(request.form['uid'])
#   name = request.form['name'] #request is a form 
#   dob = str(request.form['dob'])
#   blood_type=request.form['blood_type']
#   gender=request.form['gender']
#   print "\ncollected data from webpage"

#   # g.conn.execute('INSERT INTO characters VALUES (%s,%s,%s,%s,%s)', uid, name, dob, blood_type, gender)
#   cmd = 'UPDATE characters SET uid, name, dob, blood_type, gender = VALUES (:ui, :na, :do, :bl, :ge)'
#   g.conn.execute(text(cmd), ui = uid, na = name, do = dob, bl = blood_type, ge = gender)
#   print "\ninserted data to table 'characters'"
#   return redirect('/')

# #methods include push, put, get. checks for method defined in html.
# @app.route('/addFaculty', methods=['POST'])
# def addFaculty():
#   uid= request.form['uid']
#   date_join_hog = str(request.form['date_join_hog'])
#   # head_of=request.form['head_of']

#   # g.conn.execute('INSERT INTO faculty VALUES (%s,%s)', uid, date_join_hog)
#   cmd = "INSERT INTO faculty VALUES (:ui, :da)"
#   g.conn.execute(text(cmd), ui = uid, da = date_join_hog)
#   return redirect('/')

# @app.route('/addClass', methods=['POST'])
# def addClass():
#   name= request.form['name']
#   department = request.form['department']
#   classroom_loc=request.form['classroom_loc']
  
#   # g.conn.execute('INSERT INTO Class VALUES (%s,%s, %s)', name, department, classroom_loc)
#   cmd = "INSERT INTO class VALUES (:na, :de, :cl)"
#   g.conn.execute(text(cmd), na = name, de = department, cl = classroom_loc)
#   return redirect('/')

# @app.route('/addPlace', methods=['POST'])
# def addPlace():
#   name= request.form['name']
#   street_number = request.form['street_number']
#   street_name = request.form['street_name']
#   zippy=str(request.form['zippy'])
#   city=request.form['city']
#   country=request.form['country']
#   be_classroom_for=request.form['be_classroom_for']
#   # g.conn.execute('INSERT INTO Places VALUES (%s,%s,%s,%s,%s,%s)', name, street_number, street_name, zippy, city, country)
#   cmd = "INSERT INTO places VALUES (:na, :stnu, :stna, :zi, :ci, :co)"
#   g.conn.execute(text(cmd), na = name, stnu = street_number, stna = street_name, zi = zippy, ci = city, co = country)
#   return redirect('/')

# @app.route('/addStudent', methods=['POST'])
# def addStudent():
#   uid= str(request.form['uid'])
#   date_join_hog = str(request.form['date_join_hog'])
#   pet=request.form['pet']
#   house_name=request.form['house_name']
#   # g.conn.execute('INSERT INTO students VALUES (%s,%s,%s,%s)', uid, date_join_hog, pet, house_name)
#   cmd = 'INSERT INTO students VALUES (:ui, :da, :pe, :ho)'
#   g.conn.execute(text(cmd), ui = uid, da = date_join_hog, pe = pet, ho = house_name)
#   return redirect('/')

# # @app.route('/addTeam', methods=['POST'])
# # def addTeam():
# #   year= str(request.form['year'])
# #   #name = request.form['name'] #request is a form 
# #   # g.conn.execute('INSERT INTO Quidditch_teams VALUES (%s)', year)
# #   cmd = 'INSERT INTO Quidditch_teams VALUES (:ye)'
# #   g.conn.execute(text(cmd), ye = year)
# #   return redirect('/')

# @app.route('/addPlaysFor', methods=['POST'])
# def addPlaysFor():
#   h_from = str(request.form['h_from'])
#   h_to = str(request.form['h_to'])
#   house_name = request.form['house_name'] 
#   position = request.form['position']
#   player_uid=request.form['player_uid']
#   # g.conn.execute('INSERT INTO Plays_for VALUES (%s,%s,%s,%s,%s)', h_from, h_to, house_name, position, player_uid)
#   cmd = "INSERT INTO plays_for VALUES (:hf, :ht, :ho, :po, :pl)"
#   g.conn.execute(text(cmd), hf = h_from, ht = h_to, ho = house_name, po = position, pl = player_uid)
#   return redirect('/')

# @app.route('/addTextbook', methods=['POST'])
# def addTextbook():
#   isbn= request.form['isbn']
#   name = request.form['name'] 
#   author = request.form['author']
#   class_name=request.form['class_name']

#   # g.conn.execute('INSERT INTO Textbook VALUES (%s,%s,%s,%s)', isbn, name, author, class_name)
#   cmd = "INSERT INTO textbook VALUES (:isb, :na, :au, :cl)"
#   g.conn.execute(text(cmd), isb = isbn, na = name, au = author, cl = class_name)
#   return redirect('/')

# @app.route('/addDeed', methods=['POST'])
# def addDeed():
#   place_name= request.form['place_name']
#   user_uid = str(request.form['user_uid'])
#   types = request.form['types']
#   # g.conn.execute('INSERT INTO Use VALUES (%s,%s,%s)', place_name, user_uid, types)
#   cmd = "INSERT INTO use VALUES (:pl, :us, :ty)"
#   g.conn.execute(text(cmd), pl = place_name, us = user_uid, ty = types)
#   return redirect('/')

# @app.route('/addTake', methods=['POST'])
# def addTake():
#   student_uid= request.form['student_uid']
#   since = str(request.form['since'])
#   class_name = request.form['class_name']
#   # g.conn.execute('INSERT INTO Take VALUES (%s,%s,%s)', student_uid, since, class_name)
#   cmd = 'INSERT INTO take VALUES (:st, :si, :cl)'
#   g.conn.execute(text(cmd), st = student_uid, si = since, cl = class_name)
#   return redirect('/')

# @app.route('/addTeach', methods=['POST'])
# def addTeach():
#   faculty_uid= request.form['faculty_uid']
#   since = str(request.form['since'])
#   class_name = request.form['class_name']
#   # g.conn.execute('INSERT INTO Teach VALUES (%s,%s,%s)', faculty_uid, since, class_name)
#   cmd = 'INSERT INTO Teach VALUES (:fa, :si, :cl)'
#   g.conn.execute(text(cmd), fa = faculty_uid, si = since, cl = class_name)
#   return redirect('/')
# #with the put method you have to include both request.args and request.form. 
# #pass the character id in the URL and have the new detais in the form. 




if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
