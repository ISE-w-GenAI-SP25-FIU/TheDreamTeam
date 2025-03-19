from google.cloud import bigquery

PROJECT_ID = "dreamteamproject-449421"

client = bigquery.Client(project=PROJECT_ID)

QUERY = 'SELECT * from `ise-w-genai.CIS4993.Posts`'
query_job = client.query(QUERY)
rows = query_job.result()

for row in rows:
    print(row)
