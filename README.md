# Amazon Bedrock Streamlit Chat Applicationon EC2 

This is a Streamlit application that allows users to interact with various foundation models available through Amazon Bedrock using EC2 instance profile authentication.

## Prerequisites

- An EC2 instance with an instance profile that has the necessary permissions to access Amazon Bedrock
- Python 3.8+
- Required IAM permissions:
  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "bedrock:InvokeModel"
              ],
              "Resource": "*"
          }
      ]
  }
