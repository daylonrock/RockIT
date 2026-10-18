import json
import os
import uuid
import azure.functions as func
from azure.data.tables import TableClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        name = req_body.get('name')
        role = req_body.get('role', 'Professional Contact')
        message = req_body.get('message')

        if not name or not message:
            return func.HttpResponse(
                json.dumps({"error": "Missing name or message"}),
                status_code=400
            )

        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        table_client = TableClient.from_connection_string(
            conn_str=connection_string, table_name="Endorsements"
        )

        entity = {
            "PartitionKey": "EndorsementsPartition",
            "RowKey": str(uuid.uuid4()),
            "name": name,
            "role": role if role.strip() != "" else "Professional Contact",
            "message": message,
            "is_approved": False
        }

        table_client.create_entity(entity=entity)

        return func.HttpResponse(
            json.dumps({"status": "Success"}),
            mimetype="application/json",
            status_code=201
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500
        )
