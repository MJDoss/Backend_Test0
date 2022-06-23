# Title : Backend_Test0
 Author : Matthew Doss

 Languages : Python, SQL
 
 Tools used : Flask, SQLite3

Notes :

    I wrote and tested this on a Windows machine.

    The version of Python I used for this is 3.8.7

    I also used Flask version 1.1.2, but the new version 2.1.x should run it fine.

    If not look for the older version.


Instructions :

    Step 0 : Installations
        To run this app you will need to have the following projects installed : 
        Flask and PySQLite
        
        If you are using a version of Python that came out after version 2.5, PySQLite is 
        already installed as part of the standard library and no installation is needed.

        For Flask you will need to install it. To do so go into the terminal and run the command:
        "pip install Flask"

    Step 1 : Initialize the database.
        To initialize the database go to the project directory in the terminal:
        "..\Backend_test0>"
        
        then change directory to Application_Backend_Test.
        "..\Backend_test0>cd Application_Backend_Test"

        Once in the directory use python's interpreter to run init_db.py with command:
        "..\Backend_test0\Application_Backend_Test>python init_db.py"

        You should now see a new file in the directory called "database.db"

    Step 2 : Setting up the Flask environment.
        This is different depending on whether you are using a Windows or Mac/Unix machine.
        For Windows users in the CMD prompt:
        "..\Backend_test0\Application_Backend_Test>set FLASK_APP=app.py"
        "..\Backend_test0\Application_Backend_Test>set FLASK_ENV=development"

        For Mac/Unix users in the bash terminal:
        "../Backend_test0/Application_Backend_Test
            $ export FLASK_APP=app.py "
        "../Backend_test0/Application_Backend_Test
            $ export FLASK_ENV=development "

        *NOTE : Here's a link for a better explanation or if you need a different command:
          https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/#run-the-application

    Step 3 : Run the app.
        To run the app you can use either of these two commands:
        "..\Backend_test0\Application_Backend_Test>flask run"

        or
        "..\Backend_test0\Application_Backend_Test>python app.py"

    Step 4 : Go into your browser and go to the address of http://127.0.0.1:5000/
        The nav bar will link you to all the tools you will need for testing.