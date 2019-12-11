# Online Banking System - Team 1

This project provides an online web interface for creating accounts that can buy and sell stocks. Each account can access the current value of their account, the current value of all stocks, and the quantity of stocks they own.  
  
The bank has its own account from which stocks are sold to normal users. The bank account can view logs of all transactions. Use the admin account <admin,admin> to enter the bank account.

Team Members:
* Alain Garcia
* Georgia Hayes
* Spencer Wong
* Abhi Kante

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
