## 📌 LLM Fix Suggestion DAG for Failing Tasks

This Airflow DAG demonstrates how to automatically collect exceptions from multiple failing tasks, send those error tracebacks to an LLM (via OpenRouter API), and log back the suggested code fixes. It's useful for **observability, debugging, and AI-powered development workflows**.

---

### 📁 Project Structure

```
airflow/
├── dags/
│   └── llm_fix_suggestion_multi_failure.py
├── README.md
```

> Make sure the DAG file is saved as:
> `airflow/dags/llm_fix_suggestion_multi_failure.py`

---

### 🚀 Setup & Run Instructions

#### 1. Set Up Airflow (if not already)

```bash
pip install apache-airflow==2.7.3
```

Initialize the Airflow metadata DB:

```bash
airflow db init
```

Create a user to access the Airflow web UI:

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

#### 2. Start the Scheduler and Webserver

```bash
airflow scheduler
```

In another terminal/tab:

```bash
airflow webserver --port 8080
```

Visit: [http://localhost:8080](http://localhost:8080)

---

### 🧪 Run the DAG

List available DAGs:

```bash
airflow dags list
```

Trigger this DAG manually:

```bash
airflow dags trigger llm_fix_suggestion_multi_failure
```

Check DAG status:

```bash
airflow dags list-runs -d llm_fix_suggestion_multi_failure
```

---

### 🛠️ How This DAG Works

#### 🔹 Purpose

This DAG intentionally fails multiple tasks to simulate real-world bugs. It captures those errors and sends them to an LLM, which returns suggestions to fix the issues.

#### 🔹 Components

* `failing_division_by_zero`: Triggers a `ZeroDivisionError`
* `failing_name_error`: Triggers a `NameError`
* `failing_type_error`: Triggers a `TypeError`
* `failing_syntax_error`: Triggers a `SyntaxError` via `exec`
* `llm_suggestion`: Collects all XCom errors, formats them, sends to OpenRouter API, and logs suggestions.

#### 🔹 LLM Integration

* API: [https://openrouter.ai](https://openrouter.ai)
* Model: `openai/gpt-4o`
* Output is logged like:

```
========== ✅ BEGIN LLM SUGGESTIONS ==========
# Fix 1: ...
# Fix 2: ...
========== ❌ END LLM SUGGESTIONS ==========
```

---

### 🔐 Security Notice

Make sure to **store your OpenRouter API key securely**. This demo uses it directly in the DAG file for simplicity. In production:

* Use Airflow [Connections](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection/index.html)
* Or use [Variables](https://airflow.apache.org/docs/apache-airflow/stable/howto/use-variables.html)

---

### 📦 Dependencies

* Python 3.7+
* Apache Airflow 2.7+
* `jq` (for JSON formatting in Bash)
* `curl` (for API calls)
* OpenRouter API Key

---

### ✅ What This Covers

| Feature                        | Included ✅ |
| ------------------------------ | ---------- |
| Multiple task failure handling | ✅          |
| XCom error tracebacks          | ✅          |
| LLM fix suggestions via API    | ✅          |
| Pretty print logs              | ✅          |
| `TriggerRule.ALL_DONE` usage   | ✅          |
| Token config for large output  | ✅          |

---

### 📌 Future Improvements

* Auto-fix and re-run failed tasks
* Email/Slack LLM suggestions
* Use Airflow secrets manager for API keys
* Deploy to production Airflow on ECS/Kubernetes

