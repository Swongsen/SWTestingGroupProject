# Online Banking System - Team 1

This project provides an online web interface for creating accounts that can buy and sell stocks. Each account can access the current value of their account, the current value of all stocks, and the quantity of stocks they own.  
  
The bank has its own account from which stocks are sold to normal users. The bank account can view logs of all transactions. Use the admin account <admin,admin> to enter the bank account.

Team Members:
* Alain Garcia
* Georgia Hayes
* Spencer Wong
* Abhi Kante

Deployed [here](http://fa2019obs.herokuapp.com/), thought it is less stable than the localhost build.

Video for milestone 3 in the root directory and is named milestone3.mp4.

## Installation
* Install [Python 3.x](https://www.python.org/downloads/)
* Use the `requirements.txt` file and package manager [pip](https://pip.pypa.io/en/stable/) to install the following Python 3 packages:
	* pytest
	* pylint
	* mysql-connector-python
	* flask
	* pandas
	* gunicorn
```bash
pip install -r requirements.txt
```

## Usage

```bash
python webclient.py
```

The web service should then be hosted on localhost using port 5000.

## Setup Overview
We used Python for this entire project. The `flask` library was used to set up the web service. We used MySQL databases hosted by Google Cloud to store the web application's data. We interface with those databases through the `mysql-connector-python` library. The `pandas` library was used very briefly for CSV handling. The `gunicorn` library was used for heroku integration.

Testing was done with the help of the `pytest` library. Linting was done with the help of the `pylint` library. Authentication was completed by using a custom module which very simply checks for plain text user data.

## Resources Used
Continuous Integration Service: [Travis CI](https://travis-ci.com/)
Version Control: [Github](https://github.com/)
MySQL Server Hosting: [Google Cloud](https://cloud.google.com/)
Deployment: [Heroku](https://www.heroku.com/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
