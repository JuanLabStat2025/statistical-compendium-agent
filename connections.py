import os
import json
import boto3
from botocore.config import Config
from typing import Dict, Any
import streamlit as st

session = boto3.Session()

if os.environ.get("ACCOUNT_ID") is None:
    os.environ["ACCOUNT_ID"] = session.client("sts").get_caller_identity().get("Account")
    os.environ["AWS_REGION"] = session.region_name

if os.environ.get("LAMBDA_FUNCTION_NAME") is None:
    try:
        os.environ["LAMBDA_FUNCTION_NAME"] = "getAgentResponse"
    except Exception:
        raise ValueError("LAMBDA_FUNCTION_NAME not found in environment")
else:
    os.environ["LAMBDA_FUNCTION_NAME"]


class OptimizedLambdaClient:
    """Cliente Lambda optimizado para Streamlit"""

    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self._client = None
        self._session = None

    @property
    def client(self):
        if self._client is None:
            config = Config(
                region_name=self.region_name,
                retries={"max_attempts": 3, "mode": "adaptive"},
                max_pool_connections=50,
                connect_timeout=5,
                read_timeout=30,
            )
            self._session = boto3.Session()
            self._client = self._session.client("lambda")

        return self._client

    def invoke_sync(
        self, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invocación síncrona optimizada"""
        try:
            response = self.client.invoke(
                FunctionName=os.environ["LAMBDA_FUNCTION_NAME"],
                InvocationType="RequestResponse",
                Payload=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            )

            # Leer respuesta
            payload_response = response["Payload"].read()
            result = json.loads(payload_response)

            # Agregar metadata
            result["_metadata"] = {
                "status_code": response["StatusCode"],
                "execution_time": response.get("ExecutedVersion"),
                "request_id": response["ResponseMetadata"]["RequestId"],
            }

            return result

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
                "_metadata": {"error": True},
            }

    def invoke_async(self, payload: Dict[str, Any]) -> str:
        """Invocación asíncrona (fire and forget)"""
        try:
            response = self.client.invoke(
                FunctionName=os.environ["LAMBDA_FUNCTION_NAME"],
                InvocationType="Event",  # Asíncrono
                Payload=json.dumps(payload, ensure_ascii=False),
            )

            return response["ResponseMetadata"]["RequestId"]

        except Exception as e:
            st.error(f"Error en invocación asíncrona: {e}")
            return None

@st.cache_resource
def get_lambda_client() -> OptimizedLambdaClient:
    return  OptimizedLambdaClient()