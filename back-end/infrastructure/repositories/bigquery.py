from infrastructure.client import client_manager

class BigQueryRepository:
    def __init__(self):
        self.client = client_manager.bigquery
    
    def _fetch_column_as_list(self, query: str, column_name: str) -> list:
        query_job = self.client.query(query)
        results = query_job.result()
        return [row[column_name] for row in results]