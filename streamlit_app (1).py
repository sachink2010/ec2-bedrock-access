import streamlit as st
import boto3
import json
from botocore.exceptions import ClientError

def initialize_bedrock_client():
    try:
        # Using instance profile credentials automatically
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'  # Change this to your region if needed
        )
        return bedrock_runtime
    except Exception as e:
        st.error(f"Failed to initialize Bedrock client: {str(e)}")
        return None

def get_model_response(client, model_id, prompt):
    try:
        # Base request body
        body = {
            "prompt": prompt,
            "max_tokens_to_sample": 1000,
            "temperature": 0.7,
        }
        
        # Model-specific request formatting
        if "claude" in model_id.lower():
            body = {
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 1000,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        elif "titan" in model_id.lower():
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1000,
                    "temperature": 0.7,
                    "topP": 0.9,
                }
            }

        # Make the API call
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        
        # Extract response based on model type
        if "claude" in model_id.lower():
            return response_body.get('completion', '')
        elif "titan" in model_id.lower():
            return response_body.get('results')[0].get('outputText', '')
        else:
            return str(response_body)
            
    except ClientError as error:
        return f"Error: {error.response['Error']['Message']}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="Amazon Bedrock Chat",
        page_icon="🤖",
        layout="wide"
    )
    
    # Application title and description
    st.title("🤖 Amazon Bedrock LLM Chat")
    st.markdown("""
    This application allows you to interact with various foundation models available through Amazon Bedrock.
    Select a model and enter your prompt to get started.
    """)
    
    # Initialize the Bedrock client
    client = initialize_bedrock_client()
    
    if client is None:
        st.error("Failed to initialize the application. Please check the instance profile configuration.")
        return
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Model selection
        models = [
            "anthropic.claude-v2",
            "anthropic.claude-instant-v1",
            "amazon.titan-text-express-v1"
        ]
        
        selected_model = st.selectbox(
            "Select a Foundation Model:",
            models
        )
        
        # Model parameters
        temperature = st.slider(
            "Temperature (randomness)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make the output more random, lower values make it more deterministic."
        )
        
        # User input
        user_input = st.text_area(
            "Enter your prompt:",
            height=200,
            placeholder="Type your message here..."
        )
        
        # Generate button
        generate_button = st.button("Generate Response", type="primary")
    
    with col2:
        # Response section
        st.subheader("Response")
        if generate_button and user_input:
            with st.spinner('Generating response...'):
                response = get_model_response(client, selected_model, user_input)
                st.markdown(response)
        elif generate_button:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()