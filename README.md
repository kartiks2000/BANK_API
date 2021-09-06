# BANK API

### There are two apps built:

* *Django* based
* *Flask* based

### Django API

The application where the user will be calling API requests to. The main functions of this layer is to :

1. Works as main interface layer.
1. Parameter validation.
1. *Caching* of the *IFSC_Query* requests.
1. Intracting with the internal layer (Flask app).
1. Tracking *URL Hits* and *IFSC Hits*.

### Flask API

The application where the data is processed and stored (imported from a excel file). The main functions of this layer is to :

1. Works as the inner layer of the system.
1. Process and stores data of the bank.
1. Manages *BANK DATA,SEARCH HISTORYandLEADERBOARD* data.
1. Responds to the request send by django API in for of JSON.




#### We need to invoke the APIs from the REST Client (postman or CURL).

#### Use the provided POSTMAN collection for the django API.

## Install virtualenv

    python3 -m pip install --user virtualenv
    
## Create virtual Environment

    virtualenv --python=python3 venv    
    
## Activate virtual Environment

    source venv/bin/activate 
    
## Install dependencies from requirements.txt

    pip3 install -r requirements.txt 
    
## Change directory to django_API, and run server

    python3 manage.py runserver 
    
## Go back to main directory and change directory to Flask_API, and run server

    Python main.py
    
    
### Congrats, you are good to go. Both the servers are running and are ready to accept you API calls at:

    http://127.0.0.1:8000/ifsc_query/
    
    
## FIRST MAKE SURE FOR THE FLASK SERVER TO START COMPLETLY, ONLY START SENDING REQUESTS ONCE YOU RECIEVE THE BELOW MESSAGE IN THE CONSOLE :

    "======================== ***  Data Processing done, ready to take request *** =================================="
    
    
## IF A QUERY IS ALREADY CACHED AND ITS CACHED CACHED VALUE IS RESPONDED, YOU WILL RECIEVE THE BELOW RESPONSE :    

    "------------------- cached_Response_delivered-------------------"

    
    
# BANK REST API

The REST API to the example app is described below.



## Request Bank details for a given IFSC Code

### Request

`GET /ifsc_query/ifsc`

    curl --location --request GET 'http://127.0.0.1:8000/ifsc_query/ALLA0213505'
    
### Params

    TYPE : Path parameter
    parameter : ifsc (mandatory)

### Response

    {
        "BANK": "ALLAHABAD BANK",
        "IFSC": "ALLA0213505",
        "MICR_CODE": "NA",
        "BRANCH": "SAM LARGE",
        "ADDRESS": "17 PARLIAMENT STREET, NEW DELHI",
        "STD_CODE": 11,
        "CONTACT": 40230166,
        "CITY": "NEW DELHI",
        "DISTRICT": "NEW DELHI",
        "STATE": "DELHI"
    }



## Request LEADERBOARD

### Request

`GET leaderboard/`

    curl --location --request GET 'http://127.0.0.1:8000/leaderboard/'
    curl --location --request GET 'http://127.0.0.1:8000/leaderboard/?sortorder=ASC'
    curl --location --request GET 'http://127.0.0.1:8000/leaderboard/?fetchcount=6'
    curl --location --request GET 'http://127.0.0.1:8000/leaderboard/?sortorder=ASC&fetchcount=6'
    
### Params

    TYPE : Query parameter
    parameter : {
        sortorder : ASC, // (optional) (valid values = ASC, DESC || Default = DESC)
        fetchcount : 6 // (optional) (valid value = 1 to 225 || Default = 10)     
    }    

### Response

    {
        "THE ANDHRA PRADESH STATE COOPERATIVE BANK LIMITED": 4,
        "ABHYUDAYA COOPERATIVE BANK LIMITED": 3,
        "The Ajara Urban Co op Bank Ltd Ajara": 3,
        "AKOLA JANATA COMMERCIAL COOPERATIVE BANK": 3,
        "ALLAHABAD BANK": 3,
        "THE AKOLA DISTRICT CENTRAL COOPERATIVE BANK": 2,
        "ANDHRA BANK": 2,
        "AU SMALL FINANCE BANK LIMITED": 2,
        "BANK OF BARODA": 2,
        "EQUITAS SMALL FINANCE BANK LIMITED": 2
    }




## Request SEARCHHISTORY

### Request

`GET searchhistory/`

    curl --location --request GET 'http://127.0.0.1:8000/searchhistory/'
    curl --location --request GET 'http://127.0.0.1:8000/searchhistory/'
    curl --location --request GET 'http://127.0.0.1:8000/searchhistory/?fetchcount=4'
    curl --location --request GET 'http://127.0.0.1:8000/searchhistory/?fetchcount=4&sortorder=DESC'
    
### Params

    TYPE : Query parameter
    parameter : {
        sortorder : DESC, // (optional) (valid values = ASC, DESC || Default = ASC)
        fetchcount : 6 // (optional) (valid value = (1 to 10000) and all || Default = all)     
    }    

### Response

    [
        {
            "IFSC": "ALLA0213505",
            "TIMESTAMP": "04-Sep-2021 (12:52:38.512031)"
        },
        {
            "IFSC": "AUBL0002361",
            "TIMESTAMP": "04-Sep-2021 (13:02:16.625391)"
        },
        {
            "IFSC": "APBL0001021",
            "TIMESTAMP": "04-Sep-2021 (13:02:34.053493)"
        },
        {
            "IFSC": "ESFB0007029",
            "TIMESTAMP": "04-Sep-2021 (13:02:44.676998)"
        },
        {
            "IFSC": "APBL0004003",
            "TIMESTAMP": "04-Sep-2021 (13:03:02.818665)"
        },
        {
            "IFSC": "ANDB0000226",
            "TIMESTAMP": "04-Sep-2021 (13:03:11.205982)"
        },
        {
            "IFSC": "AJAR0000026",
            "TIMESTAMP": "04-Sep-2021 (13:03:31.001160)"
        }
    ]



## Request IFSC_Hit

### Request

`GET /ifsc_hit`

    curl --location --request GET 'http://127.0.0.1:8000/ifsc_hit'
    
### Params

    TYPE : NONE

### Response

    {
        "ALLA0213505": 5,
        "AUBL0002361": 3,
        "APBL0001021": 3,
        "ESFB0007029": 2,
        "APBL0004003": 1,
        "ANDB0000226": 1,
        "AJAR0000026": 1
    }
    
    
    
## Request URL_Hit

### Request

`GET /url_hit`

    curl --location --request GET 'http://127.0.0.1:8000/url_hit'
    
### Params

    TYPE : NONE

### Response

    {
      "IFSC_QUERY": 16,
      "LEADER_BOARD": 7,
      "SEARCH_HISTORY": 7
    }    




## Possible Response codes
    
    status = 400 // Bad request
    status = 404 // Not found
    
## Possible response messages

    Passing invalid IFSC code -:

    {
        "error": "Sorry, INVALID IFSC code."
    }
    
    Parameter passed out of the range of data -:
    eg-: there are 10 elements in Searchhistory and we pass fetchcount = 20.
    
    {
        "message": "Sorry, Exceeding range."
    }

    Passing not in described range of the api call -:
    eg-: 1 <= fetchcount <= 225, but we pass fetchcount = 700.

    "INVALID parameters passed"
    
    
# THANKS & REGARDS    
