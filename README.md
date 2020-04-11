## Flask tutorial 
Example code from the official flask tutorial. 

https://flask.palletsprojects.com/en/1.1.x/tutorial/



### How to run 
Activate venv   

* pip install -r requirements.txt 
* export FLASK_APP=flaskr
* export FLASK_ENV=development
* flask init-db (only once)
* flask run

To clear database and initialize again run the following  
flask init-db 

### To run tests 
Install the flaskr first by using the following command. 
* pip install -e .

Now run the tests. 
* pytest 
* coverage run -m pytest
* coverage html 


### To learn 
* Find out what functools.wraps does
* Learn more about flask instance 
* Learn more about pytest - monkeypatch, dependency inject