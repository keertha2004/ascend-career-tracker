import pymysql
import pandas as pd
from utils.db_config import get_db_connection

conn = get_db_connection()
query = "SELECT * FROM applications"
df = pd.read_sql(query, conn)
df.to_csv("job_applications.csv", index=False)
conn.close()

print("✅ Exported to job_applications.csv")
