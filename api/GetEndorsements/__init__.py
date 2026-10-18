import json
import os
import azure.functions as func
from azure.data.tables import TableClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    
    if not connection_string:
        return func.HttpResponse(json.dumps([]), mimetype="application/json")

    try:
        table_client = TableClient.from_connection_string(
            conn_str=connection_string, table_name="Endorsements"
        )
        entities = table_client.query_entities("is_approved eq true")
        
        endorsements = []
        for entity in entities:
            endorsements.append({
                "name": entity.get("name", "Anonymous"),
                "role": entity.get("role", "Professional Contact"),
                "message": entity.get("message", "")
            })

        return func.HttpResponse(
            json.dumps(endorsements),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
