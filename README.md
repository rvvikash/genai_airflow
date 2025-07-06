📌 LLM Fix Suggestion DAG for Failing Tasks
This Airflow DAG demonstrates how to automatically collect exceptions from multiple failing tasks, send those error tracebacks to an LLM (via OpenRouter API), and log back the suggested code fixes. It's useful for observability, debugging, and AI-powered development workflows.

📁 Project Structure
Copy
Edit
airflow/
├── dags/
│   └── llm_fix_suggestion_multi_failure.py
├── README.md
Make sure the DAG file is saved as:
airflow/dags/llm_fix_suggestion_multi_failure.py

🚀 Setup & Run Instructions
1. Set Up Airflow (if not already)
bash
Copy
Edit
pip install apache-airflow==2.7.3
Initialize the Airflow metadata DB:

bash
Copy
Edit
airflow db init
Create a user to access the Airflow web UI:

bash
Copy
Edit
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
2. Start the Scheduler and Webserver
bash
Copy
Edit
airflow scheduler
In another terminal/tab:

bash
Copy
Edit
airflow webserver --port 8080
Visit: http://localhost:8080

🧪 Run the DAG
List available DAGs:

bash
Copy
Edit
airflow dags list
Trigger this DAG manually:

bash
Copy
Edit
airflow dags trigger llm_fix_suggestion_multi_failure
Check DAG status:

bash
Copy
Edit
airflow dags list-runs -d llm_fix_suggestion_multi_failure
🛠️ How This DAG Works
🔹 Purpose
This DAG intentionally fails multiple tasks to simulate real-world bugs. It captures those errors and sends them to an LLM, which returns suggestions to fix the issues.

🔹 Components
failing_division_by_zero: Triggers a ZeroDivisionError

failing_name_error: Triggers a NameError

failing_type_error: Triggers a TypeError

failing_syntax_error: Triggers a SyntaxError via exec

llm_suggestion: Collects all XCom errors, formats them, sends to OpenRouter API, and logs suggestions.

🔹 LLM Integration
API: https://openrouter.ai

Model: openai/gpt-4o

Output is logged like:

bash
Copy
Edit
========== ✅ BEGIN LLM SUGGESTIONS ==========
# Fix 1: ...
# Fix 2: ...
========== ❌ END LLM SUGGESTIONS ==========
🔐 Security Notice
Make sure to store your OpenRouter API key securely. This demo uses it directly in the DAG file for simplicity. In production:

Use Airflow Connections

Or use Variables

📦 Dependencies
Python 3.7+

Apache Airflow 2.7+

jq (for JSON formatting in Bash)

curl (for API calls)

OpenRouter API Key

