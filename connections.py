import logging
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
    os.environ["ACCOUNT_ID"] = (
        session.client("sts").get_caller_identity().get("Account")
    )
    os.environ["AWS_REGION"] = session.region_name


class OptimizedAWSClient:
    """
    Optimized AWS Client for Streamlit.
    Handles connection pooling and retries.
    """

    def __init__(
        self,
        aws_resource_name: str,
        aws_resource_type: str,
        region_name: str = "us-east-1",
    ):
        """
        Initialize the OptimizedAWSClient.

        Args:
            region_name (str): AWS region name. Defaults to "us-east-1".
            aws_resource_name (str): Name of the AWS resource.
            aws_resource_type (str): Type of the AWS resource.

        Raises:
            ValueError: If the resource type is not 'lambda' or 'dynamodb'.
        """
        self.region_name = region_name
        self._aws_resource_name = aws_resource_name
        self._aws_resource_type = aws_resource_type
        if self._aws_resource_type == "lambda":
            self._client = boto3.Session(region_name=self.region_name).client("lambda")
        elif self._aws_resource_type == "dynamodb":
            self._client = boto3.resource("dynamodb").Table(self._aws_resource_name)
        else:
            raise ValueError("Invalid resource type.")

    @property
    def client(self) -> Any:
        """
        Lazy initialization of the boto3 Lambda client.
        """
        return self._client

    def invoke_sync(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous invocation of the Lambda function.

        Args:
            payload (Dict[str, Any]): The payload to send to the Lambda function.

        Returns:
            Dict[str, Any]: The response from the Lambda function.

        Raises:
            ValueError: If the resource type is not 'lambda'.
        """
        if self._aws_resource_type != "lambda":
            raise ValueError(
                "Resource type must be 'lambda' for synchronous invocation."
            )
        try:
            response = self.client.invoke(
                FunctionName=self._aws_resource_name,
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

        Raises:
            ValueError: If the resource type is not 'lambda'.
        """
        if self._aws_resource_type != "lambda":
            raise ValueError(
                "Resource type must be 'lambda' for asynchronous invocation."
            )
        try:
            response = self.client.invoke(
                FunctionName=self._aws_resource_name,
                InvocationType="Event",  # Asynchronous
                Payload=json.dumps(payload, ensure_ascii=False),
            )

            return response["ResponseMetadata"]["RequestId"]

        except Exception as e:
            logging.error(f"Error in asynchronous invocation: {e}")
            return None

    def write_row(self, item: Dict[str, Any]) -> None:
        """
        Write a single row to the DynamoDB table.

        Args:
            item (Dict[str, Any]): The item to write to the DynamoDB table.
        """
        try:
            self._client.put_item(Item=item)
        except Exception as e:
            logging.error(f"Error writing row to DynamoDB: {e}")


@st.cache_resource
def get_lambda_client_bedrock(lambda_function_name: str) -> OptimizedAWSClient:
    """
    Get a cached instance of OptimizedAWSClient for Bedrock.

    Args:
        lambda_function_name (str): Name of the Lambda function.

    Returns:
        OptimizedAWSClient: The client instance.
    """
    return OptimizedAWSClient(
        aws_resource_name=lambda_function_name,
        aws_resource_type="lambda",
    )


@st.cache_resource
def get_lambda_client_feedback(lambda_function_name: str) -> OptimizedAWSClient:
    """
    Get a cached instance of OptimizedAWSClient for Feedback.

    Args:
        lambda_function_name (str): Name of the Lambda function.

    Returns:
        OptimizedAWSClient: The client instance.
    """
    return OptimizedAWSClient(
        aws_resource_name=lambda_function_name,
        aws_resource_type="lambda",
    )


@st.cache_resource
def get_dynamodb_client(dynamodb_table_name: str) -> OptimizedAWSClient:
    """
    Get a cached instance of OptimizedAWSClient for DynamoDB.

    Args:
        dynamodb_table_name (str): Name of the DynamoDB table.

    Returns:
        OptimizedAWSClient: The client instance.
    """
    return OptimizedAWSClient(
        aws_resource_name=dynamodb_table_name,
        aws_resource_type="dynamodb",
    )
