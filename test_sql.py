from google.cloud import bigquery

# required field for authentication
project_id = "dreamteamproject-449421"

client = bigquery.Client(project=project_id)

QUERY = 'SELECT * from `ise-w-genai.CIS4993.Posts`'
query_job = client.query(QUERY)
rows = query_job.result()

for row in rows:
    print(row)
