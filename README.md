# 🧾 Transaction Summary API (Django + MongoDB + Docker)

---

## 🚀 Endpoints

### 1. 📦 Read from Cache Only
```http request
GET /transactions/cache/?mode=monthly&type=count
```
- Fetches precomputed summary data directly from the `transaction_summary` collection.
- Fastest response: no aggregation is executed.
- If cache is not found, it returns:
  - `204 No Content`, or
  - an empty list `[]` (based on implementation).

---

### 2. 📊 Generate & Cache Report
```http request
GET /transactions/?mode=monthly&type=count
```
- Checks if the result exists in cache.
- If **found**: returns cached result ✅
- If **not found**:
  - Executes aggregation on `transaction` collection using MongoDB pipeline.
  - Generates the formatted response (in Jalali calendar).
  - Caches the result in `transaction_summary`.
  - Then returns it to the client.

This view is **slower on first call** but **fast on subsequent requests** thanks to caching.

---

## 🔧 Query Parameters

| Parameter     | Values                            | Description                                           |
|---------------|------------------------------------|-------------------------------------------------------|
| `mode`        | `daily`, `weekly`, `monthly`       | Time interval for grouping the results                |
| `type`        | `count`, `amount`                  | Aggregate by transaction count or total amount        |
| `merchantId`  | *(optional)* MongoDB ObjectId      | Filter report by a specific merchant (if provided)    |

---

## 🐳 Running the Project with Docker
### Data Initialization
The mongo-setup service will automatically load  initial database state from the backup files under ./mongo-init.
No manual data import is required—as soon as you run docker-compose, MongoDB will be seeded from the provided backup scripts.

    docker compose up --build 


## 🧠 Generate Cache via Command
To pre-generate all combinations of reports for all merchants and summary types:

```python
python3 manage.py generate_summary_cache
```
This will:

- Loop over all combinations of mode and type
- Generate and store summaries in transaction_summary
- For each merchant and also globally (no merchant filter)