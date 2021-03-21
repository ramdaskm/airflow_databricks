##### Ubuntu 18.04
* sudo apt-get update

* sudo apt-get install software-properties-common
* sudo apt-add-repository universe
* sudo apt-get update
* sudo apt-get install python-setuptools
* sudo apt-get install libmysqlclient-dev
* sudo apt-get install libssl-dev
* sudo apt-get install libkrb5-dev
* source airflow/bin/activate
* sudo apt install sqlite3

* sudo apt-get install virtualenv
* virtualenv airflow -p python3

#### requirements.txt
`sqlalchemy < 1.4.0`
* pip install -r requirements.txt

* export AIRFLOW_HOME=~/airflow
* pip install apache-airflow
* pip install typing_extensions
* airflow db init
* airflow users create  --username ramdaskm  --firstname ramdas --lastname murali --role Admin --email ramdas.murali@databricks.com
* airflow webserver -p 8096
* airflow scheduler

* mkdir ~airflow/dags
* cp databricks.py dags
* pip install "apache-airflow[databricks]"
* pip install apache-airflow['cncf.kubernetes']
* pip install apache-airflow-providers-slack

##### Airflow Connections
* Databricks-default
* Slack

