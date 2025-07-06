from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 7, 5),
    "retries": 0,
}

with DAG(
    dag_id="llm_fix_suggestion_multi_failure",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="DAG that captures failing tasks and gets LLM suggestions",
) as dag:

    # Failing Task 1: Division by zero
    failing_division_by_zero = PythonOperator(
        task_id="failing_division_by_zero",
        python_callable=lambda: 1 / 0,
        on_failure_callback=lambda context: context['ti'].xcom_push(
            key="error_traceback", value=str(context['exception'])
        ),
    )

    # Failing Task 2: NameError
    failing_name_error = PythonOperator(
        task_id="failing_name_error",
        python_callable=lambda: print(undefined_variable),
        on_failure_callback=lambda context: context['ti'].xcom_push(
            key="error_traceback", value=str(context['exception'])
        ),
    )

    # Failing Task 3: TypeError
    failing_type_error = PythonOperator(
        task_id="failing_type_error",
        python_callable=lambda: "2" + 2,
        on_failure_callback=lambda context: context['ti'].xcom_push(
            key="error_traceback", value=str(context['exception'])
        ),
    )

    # Failing Task 4: SyntaxError (in eval)
    failing_syntax_error = PythonOperator(
        task_id="failing_syntax_error",
        python_callable=lambda: exec("for in range(5): print(i)"),
        on_failure_callback=lambda context: context['ti'].xcom_push(
            key="error_traceback", value=str(context['exception'])
        ),
    )

    # Task to collect all error tracebacks and request LLM suggestions
    llm_suggestion = BashOperator(
        task_id="llm_suggestion",
        trigger_rule=TriggerRule.ALL_DONE,
        bash_command="""
echo "========== START COLLECTING ERRORS =========="

ERRORS=""
for task in failing_division_by_zero failing_name_error failing_type_error failing_syntax_error; do
  TRACE=$(airflow tasks xcom pull -d llm_fix_suggestion_multi_failure -t $task -k error_traceback 2>/dev/null)
  if [ ! -z "$TRACE" ]; then
    ERRORS="$ERRORS\n------------------\nError from $task:\n$TRACE\n"
  fi
done

# Escape the collected errors for JSON
ESCAPED_ERRORS=$(echo -e "$ERRORS" | python3 -c 'import json,sys; print(json.dumps("Give only code fix suggestions for these errors:\\n" + sys.stdin.read()))')

# Create request body
cat <<EOF > /tmp/llm_request.json
{
  "model": "openai/gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": $ESCAPED_ERRORS
    }
  ],
  "max_tokens": 600
}
EOF

# Make the API call
RESPONSE=$(curl -s --location --request POST 'https://openrouter.ai/api/v1/chat/completions' \
--header 'Authorization: Bearer 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' \
--header 'Content-Type: application/json' \
--header 'Referer: http://localhost' \
--header 'X-Title: LLM Token Validator' \
--data @/tmp/llm_request.json)

# Pretty print output from the model
echo "========== ✅ BEGIN LLM SUGGESTIONS =========="
echo "$RESPONSE" | jq -r '.choices[0].message.content'
echo "========== ❌ END LLM SUGGESTIONS ============"
        """,
    )

    # Set task dependencies
    [
        failing_division_by_zero,
        failing_name_error,
        failing_type_error,
        failing_syntax_error,
    ] >> llm_suggestion
