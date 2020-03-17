import os
import shutil
import time

"""
set FLASK_APP=app.py
SET FLASK_ENV=development
flask run -h iphere -p 8080
"""

# function - Camera takes picture and downloads
def snap_a_pic(): 
    os.system('gphoto2 --capture-image-and-download')

# function - Move camera image from root directory to images directory 
def move_the_snap():
    # date and time variables
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m-%d-%Y" + "-" "%H:%M:%S", named_tuple)

     # searches images folder for images and then adds an img tag for each
    for filename in os.listdir(os.getcwd()):
     if filename.endswith(".jpg"):
      # do something with any .jpg found
      shutil.move(filename, 'static/images/' + time_string + filename)
      continue
     else:
      continue

# function - Creates html image tag for each image in images folder and appends to images.html
def add_images_to_feed():

    # delete existing imaages html file to avoid duplication
    os.remove("templates/images.html") 

    # searches images folder for images and then adds an img tag for each
    for filename in os.listdir('static/images'):

     if filename.endswith(".jpg"):
      imageItemTemplate = "<!-- photo booth embeded image -->" + "<article class=" + "\"" + "animated flipInY" + "\"" + "><img src=" + "\"" + "/static/images/" + filename + "\"" + " alt=\"Photobooth moment\"/></article><!-- / photo booth embeded image -->" + "\n" 
      
      # write tags to images.html file
      f = open("templates/images.html", "a")
      f.write(imageItemTemplate)
      f.close() 

      # open index.html file and add all components 
      continue
     else:
      continue

# function - Combines all three template html files into single index.html to create photo feed
def build_webpage():

    # Creating a list of filenames 
    filenames = ['templates/prepend.html', 'templates/images.html', 'templates/append.html'] 
    
    # Open file3 in write mode 
    with open('templates/photowall.html', 'w') as outfile: 
    
        # Iterate through list 
        for names in filenames: 
    
            # Open each file in read mode 
            with open(names) as infile: 
    
                # read the data from files and write to index.html 
                outfile.write(infile.read()) 
     
            # from next line 
            outfile.write("\n") 

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photowall')
def photowall():
    print('Reloading photo wall page')
    return render_template('photowall.html')

@app.route('/my-link')
def my_link():

    # initial 3 secons await before image is taken
    # time.sleep(3)

    print('Picture script now running')
    # takes snap
    print('Taking a snap!')
    snap_a_pic()

    # moves snap
    print('Moving snap to images folder')
    move_the_snap()
    time.sleep(5)

    # adds snap to webpage
    print('adding images folder to feed')
    add_images_to_feed()

    # rebuilds webpage with new snap
    print('updating website feed')
    time.sleep(5)
    build_webpage()

    print('Process complete, check out the pic on the feed website')
    return render_template('timer.html')

if __name__ == '__main__':
    app.run(debug=True)
