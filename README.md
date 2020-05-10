## Flask tutorial 
Flask example code I've written while following the official flask tutorial. 

https://flask.palletsprojects.com/en/1.1.x/tutorial/

This implementation also covers the self assignments given in the following link, except search functionality. 

https://flask.palletsprojects.com/en/1.1.x/tutorial/next/

One notable difference with the official tutorial here is that after completing the tutorial with raw sql, I have converted this project to use SQLAlchemy. 

### How to run locally
Activate venv   

* $ pip install -r requirements.txt 
* $ export FLASK_APP=flaskr
* $ export FLASK_ENV=development
* $ flask init-db (only once)
* $ flask run

To clear database and initialize again run the following  

$ flask init-db 

To load some test data please run the following. 

$ flask load-test-data 

### To run tests 
Install the flaskr first by using the following command. 
* pip install -e .

Now run the tests. 
* pytest 
* coverage run -m pytest
* coverage html 

### Future enhancements 
* Implement the search using sqlite FTS
* Limit upload file size 
* Improve style 
* Most read, most commented 
* Provide a Dockerfile 

