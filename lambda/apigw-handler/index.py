# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Import necessary libraries
import boto3  # AWS SDK for Python (Boto3)
import os     # Module providing a way to interact with the operating system
import json   # Module to work with JSON data
import logging  # Module to log messages
import uuid   # Module to generate unique identifiers

# Configure logger
logger = logging.getLogger()  # Get the root logger
logger.setLevel(logging.INFO)  # Set logging level to INFO

# Create a DynamoDB client
dynamodb_client = boto3.client("dynamodb")

# Define the Lambda function handler
def handler(event, context):
    # Get the DynamoDB table name from the environment variable
    table = os.environ.get("TABLE_NAME")
    logging.info(f"## Loaded table name from environment variable DDB_TABLE: {table}")

    # Check if the request body is present
    if event["body"]:
        # Parse JSON payload from the request body
        item = json.loads(event["body"])
        logging.info(f"## Received payload: {item}")

        # Extract data from the payload
        year = str(item["year"])
        title = str(item["title"])
        id = str(item["id"])

        # Put item into DynamoDB table
        dynamodb_client.put_item(
            TableName=table,
            Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
        )

        # Prepare response
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
    else:
        # If no payload is present, insert a default item into the DynamoDB table
        logging.info("## Received request without a payload")
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "year": {"N": "2012"},
                "title": {"S": "The Amazing Spider-Man 2"},
                "id": {"S": str(uuid.uuid4())},  # Generate a unique identifier
            },
        )

        # Prepare response
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
