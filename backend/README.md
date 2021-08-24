# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

4. **Flask Environment Variables** - On Windows you can set flask environment variables for the app and environment so you don't need to specify them everytime you run the server:
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
```

5. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Endpoints
These are the endpoints of the API with the expected request and response bodies:

### Get Paginated Questions
```
GET '/questions?page=${page}'
- Fetches a paginated set of questions, all categories, total questions and current category.
- Request Arguments: page - integer.
- Returns: a dictionary that has at most 10 questions, all categories, total questions and current category.
{
    'success': True
    'questions': [
        {
            'id': 1,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 3,
            'category': 4
        },
        {
            'id': 2,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 20,
    'categories': 
        { 
            '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports" 
        },
    'currentCategory': None
}
```

### Get All Categories
```
GET '/categories'
- Fetches a dictionary that holds keys as category ids and values as category type.
- Request Arguments: None.
- Returns: dictionary of category ids as keys and category type as values.
{
    'success': True
    'categories': 
        { 
            '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports" 
        }
}
```

### Get Question by ID
```
GET '/questions/${id}'
- Fetches an object that holds the returned question and total number of questions.
- Request Arguments: id - integer.
- Returns: dictionary that has the returned question object and total number of questions.
{
    'success': True
    'question': 
        {
            'id': 5,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 3,
            'category': 4
        },
    'total_questions': 20
}
```

### Delete Question by ID
```
DELETE '/questions/${id}'
- Deletes a question by a given ID
- Request Arguments: id - integer.
- Returns: Only returns the HTTP success response and code.
```

### Add New Question
```
POST '/questions'
- Adds a new question from the provided request arguments from the client.
- Request Arguments: A question object that needs to be posted.
{
    'question':  'What?',
    'answer':  'Answer.',
    'difficulty': 3,
    'category': 5,
}
- Returns: Only HTTP response, status code and the total number of questions.
{
    'success': True,
    'total_questions': 20
}
```

### Search For Questions
```
POST '/questions'
- Searches for questions based on a given search term.
- Request Arguments: An object that has the search term.
{
    'searchTerm': 'What'
}
- Returns: All found questions, total number of questions and current category.
{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 1,
            'category': 1
        },
        {
            'id': 2,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 4,
            'category': 5
        },
        {
            'id': 3,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 20,
    'currentCategory': None
}
```

### Play Trivia Quiz
```
POST '/quizzes'
- Plays a quiz based on selected category and excluding previously asked questions.
- Request Arguments: An object that has the category of the quiz and the previously asked questions
{
    'previous_questions': [7, 2, 15, 12, 3]
    'quiz_category': 
        {
            'id': 1,
            'type': 'Science'
        }
}
- Returns: A random question that haven't been asked before.
{
    'success': True,
    'question': 
        {
            'id': 5,
            'question': 'What?',
            'answer': 'Answer.', 
            'difficulty': 5,
            'category': 2
        }
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
