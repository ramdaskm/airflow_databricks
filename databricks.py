"""
This is an example DAG which uses the DatabricksSubmitRunOperator.
In this example, we create two tasks which execute sequentially.
The first task is to run a notebook at the workspace path "/test"
and the second task is to run a JAR uploaded to DBFS. Both,
tasks use new clusters.

Because we have set a downstream dependency on the notebook task,
the spark jar task will NOT run until the notebook task completes
successfully.

The definition of a successful run is if the run has a result_state of "SUCCESS".
For more information about the state of a run refer to
https://docs.databricks.com/api/latest/jobs.html#runstate
"""

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.utils.dates import days_ago
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

SLACK_CONN_ID = 'slack'

def task_fail_slack_alert(context):
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    slack_msg = """
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
        )

    failed_alert = SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='slack',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow')
    return failed_alert.execute(context=context)


default_args = {
    'owner': 'ramdaskm',
    'email': ['airflow@example.com'],
    'depends_on_past': False,
    'on_failure_callback': task_fail_slack_alert
}

with DAG(
    dag_id='example_databricks_operator',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    new_cluster = {
        'spark_version': '6.4.x-scala2.11',
        'node_type_id': 'r3.xlarge',
        'aws_attributes': {'availability': 'ON_DEMAND'},
        'num_workers': 2,
    }

    notebook_task_params1 = {
        'new_cluster': new_cluster,
        'notebook_task': {
            'notebook_path': '/Users/ramdas.murali@databricks.com/temp/nb1',
        },
    }
    # Example of using the JSON parameter to initialize the operator.
    notebook_task1 = DatabricksSubmitRunOperator(task_id='notebook_task1', json=notebook_task_params1)

    notebook_task_params2 = {
        'new_cluster': new_cluster,
        'notebook_task': {
            'notebook_path': '/Users/ramdas.murali@databricks.com/temp/nb2',
        },
    }
    # Example of using the JSON parameter to initialize the operator.
    notebook_task2 = DatabricksSubmitRunOperator(task_id='notebook_task2', json=notebook_task_params2)

    notebook_task_params3 = {
        'new_cluster': new_cluster,
        'notebook_task': {
            'notebook_path': '/Users/ramdas.murali@databricks.com/temp/nb3',
        },
    }
    # Example of using the JSON parameter to initialize the operator.
    notebook_task3 = DatabricksSubmitRunOperator(task_id='notebook_task3', json=notebook_task_params3)    
    
    
notebook_task1 >> [notebook_task2, notebook_task3] 
