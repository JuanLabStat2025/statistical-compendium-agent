import os
import json
import boto3
from botocore.config import Config
from typing import Dict, Any, Optional
import streamlit as st

# Initialize session
session = boto3.Session()

# Set environment variables if not present
if os.environ.get("ACCOUNT_ID") is None:
    os.environ["ACCOUNT_ID"] = session.client("sts").get_caller_identity().get("Account")
    os.environ["AWS_REGION"] = session.region_name

class OptimizedLambdaClient:
    """
    Optimized Lambda Client for Streamlit.
    Handles connection pooling and retries.
    """

    def __init__(self, region_name: str = "us-east-1", lambda_function_name: str = "getAgentResponse"):
        """
        Initialize the OptimizedLambdaClient.

        Args:
            region_name (str): AWS region name. Defaults to "us-east-1".
            lambda_function_name (str): Name of the Lambda function. Defaults to "getAgentResponse".
        """
        self.region_name = region_name
        self._client = None
        self._session = None
        self._lambda_function_name = lambda_function_name

    @property
    def client(self) -> Any:
        """
        Lazy initialization of the boto3 Lambda client.
        """
        if self._client is None:
            config = Config(
                region_name=self.region_name,
                retries={"max_attempts": 3, "mode": "adaptive"},
                max_pool_connections=50,
                connect_timeout=5,
                read_timeout=30,
            )
            self._session = boto3.Session()
            self._client = self._session.client("lambda", config=config)

        return self._client

    def invoke_sync(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous invocation of the Lambda function.

        Args:
            payload (Dict[str, Any]): The payload to send to the Lambda function.

        Returns:
            Dict[str, Any]: The response from the Lambda function.
        """
        try:
            response = self.client.invoke(
                FunctionName=self._lambda_function_name,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            )

            # Read response
            payload_response = response["Payload"].read()
            result = json.loads(payload_response)

            # Add metadata
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

    def invoke_async(self, payload: Dict[str, Any]) -> Optional[str]:
        """
        Asynchronous invocation (fire and forget) of the Lambda function.

        Args:
            payload (Dict[str, Any]): The payload to send to the Lambda function.

        Returns:
            Optional[str]: The RequestId if successful, None otherwise.
        """
        try:
            response = self.client.invoke(
                FunctionName=self._lambda_function_name,
                InvocationType="Event",  # Asynchronous
                Payload=json.dumps(payload, ensure_ascii=False),
            )

            return response["ResponseMetadata"]["RequestId"]

        except Exception as e:
            st.error(f"Error in asynchronous invocation: {e}")
            return None

@st.cache_resource
def get_lambda_client_bedrock(lambda_function_name: str) -> OptimizedLambdaClient:
    """
    Get a cached instance of OptimizedLambdaClient for Bedrock.

    Args:
        lambda_function_name (str): Name of the Lambda function.

    Returns:
        OptimizedLambdaClient: The client instance.
    """
    return OptimizedLambdaClient(lambda_function_name=lambda_function_name)

@st.cache_resource
def get_lambda_client_feedback(lambda_function_name: str) -> OptimizedLambdaClient:
    """
    Get a cached instance of OptimizedLambdaClient for Feedback.

    Args:
        lambda_function_name (str): Name of the Lambda function.

    Returns:
        OptimizedLambdaClient: The client instance.
    """
    return OptimizedLambdaClient(lambda_function_name=lambda_function_name)