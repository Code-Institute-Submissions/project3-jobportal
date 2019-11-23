# Install the various required library
from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo	
from bson.objectid import ObjectId

app = Flask(__name__)
	
# Setting up the MONGODB DATABASES to be link up	
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'jobPortal'
COLLECTION_NAME = 'jobListing'

# set up the connection to MONGO_URI which we set up in bashrc
conn = pymongo.MongoClient(MONGO_URI)
# set 'data' to represent the database link
data = conn[DATABASE_NAME][COLLECTION_NAME]

# Landing page 
@app.route('/') # map the root route to the index function
def index():
    return render_template('index.html')

# Display listing for the job-listing for employee to apply
@app.route('/employee')
def employee():
    result = data.find({})
    return render_template('employee.html', data = result)

# Display listing and allow Employer to Create / Edit / Delete the listing
@app.route('/employer')
def employer():
    result = data.find({})
    return render_template('employer.html', data = result)

# Redirect to form HTML for user to enter data
@app.route('/new_post')
def new_post():
    return render_template('new_post.html')
# Inserting new data into database    
@app.route('/new_post', methods=["POST"])
def insert_post():
    position = request.form.get('position')
    company = request.form.get('company')
    description = request.form.get('description')
    salary = int(request.form.get('salary'))
    nationality = request.form.get('nationality')
    professional_license = request.form.get('professional_license')
    working_experience = request.form.get('working_experience')
    
    data.insert({
        'position':position,
        'company':company,
        'description':description,
        'salary':salary,
        'requirement':{
            'nationality': nationality,
            'professional_license':professional_license,
            'working_experience':working_experience
        }
    })
    return redirect(url_for('employer'))
 
# Pass the reference id to extract the data to be edited    
@app.route('/edit_post/<task_id>')
def edit_post(task_id):
    # Find the data using the task_id
    data_to_be_edited = data.find_one({
        '_id':ObjectId(task_id)
    })
    return render_template('edit_post.html', data = data_to_be_edited)
# Update the database with the new data   
@app.route('/edit_post/<task_id>', methods=["POST"])
def update_post(task_id):
    position = request.form.get('position')
    company = request.form.get('company')
    description = request.form.get('description')
    salary = int(request.form.get('salary'))
    nationality = request.form.get('nationality')
    professional_license = request.form.get('professional_license')
    working_experience = request.form.get('working_experience')
    
    data.update({
        '_id':ObjectId(task_id)
        }, {
        '$set': {
                'position':position,
                'company':company,
                'description':description,
                'salary':salary,
                'requirement':{
                    'nationality': nationality,
                    'professional_license':professional_license,
                    'working_experience':working_experience
                }
                }
        })    
    return redirect(url_for('employer'))

# Link to check if user confirm wants to delete the post
@app.route('/remove_post/<task_id>')
def remove_post(task_id):
    task = data.find_one({
        '_id':ObjectId(task_id)
    })
    return render_template('remove_post.html', d=task)
# Proceed to delete from database and return to employer.html
@app.route('/confirm_remove_post/<task_id>')
def confirm_remove_post(task_id):
    data.delete_one({
        '_id':ObjectId(task_id)
    })
    result = data.find({})
    return render_template('employer.html', data = result)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)