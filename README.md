# Amazon Bedrock Streamlit Chat Application on EC2 

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

# Setup Instructions
1. Clone this repository on your EC2 instance:
```
git clone &lt;repository-url&gt;
cd ec2-streamlit
```
2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:

``` 
pip install -r requirements.txt
```
4. Run the application:
``` 
streamlit run streamlit_app.py --server.port 8501
```

# EC2 Configuration Requirements
Ensure your EC2 instance has an instance profile attached with the necessary Bedrock permissions
Configure your EC2 security group to allow inbound traffic:
- Port 8501 (Streamlit default port)
- Source: Your IP address or appropriate CIDR range
