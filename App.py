# Import necessary libraries
import streamlit as st  # For creating the web interface
import os               # For accessing environment variables
from groq import Groq   # To interact with the Groq API
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from the .env file into the environment
load_dotenv()

# Retrieve the Groq API key from environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

# If API key is not found, display an error and stop the app
if not groq_api_key:
    st.error("Groq API Key is missing! Ensure `.env` is correctly loaded.")
    st.stop()

# Optional print statement for debugging to confirm key is loaded
print("Groq API Key Loaded Successfully.")

# Initialize the Groq API client with the retrieved API key
client = Groq(api_key=groq_api_key)

# Configure the Streamlit page
st.set_page_config(page_title="MRI Scan Chatbot", layout="centered")
st.title("🧠 MRI Scan Explanation Chatbot")

# Create a text area input for users to paste their MRI report
report  = st.text_area("Paste your MRI Report Below", height=300)

# Optional input field for users to ask a question about the MRI report
user_question = st.text_input("❓ Ask a question about your MRI report (optional):")

# When the "Explain Report" button is clicked
if st.button("Explain Report"):
    # Check if the report is empty
    if not report.strip():
        st.warning("Please enter an MRI report.")  # Warn user if report is missing
    else:
        with st.spinner("Analyzing and report..."):  # Show a spinner while processing
            try:
                # Build the prompt based on whether a user question is provided
                if user_question.strip():
                    # Prompt for answering a specific user question using context from the MRI report
                    prompt = (
                        "You are a helpful medical assistant. A user has provided an MRI report and asked a question about it. "
                        "Please answer their question based on the MRI report. If helpful, explain it in simple terms.\n\n"
                        f"MRI Report:\n{report}\n\n"
                        f"User Question: {user_question}\n\n"
                        "Answer:"
                    )
                else:
                    # Prompt for general explanation of the MRI report
                    prompt = (
                        "You are a friendly medical assistant. A user has pasted an MRI scan report. "
                        "Explain it in simple, easy-to-understand language. Be clear, avoid jargon, and highlight anything that might be abnormal.\n\n"
                        f"MRI Report:\n{report}\n\nExplanation:"
                    )
                
                # Call the Groq API to generate a response based on the prompt
                chat_completion = client.chat.completions.create(
                    model="gemma2-9b-it",  # Model to use for generating the response
                    messages=[
                        {"role": "system", "content": "You explain MRI reports and answer questions in layman's terms."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,  # Controls the creativity of the response
                )

                # Extract the generated content from the response
                output = chat_completion.choices[0].message.content

                # Display the result in the UI
                st.success("Here's the response:")
                st.write(output)

            # Catch and display any errors during processing
            except Exception as e:
                st.error(f"Error: {e}")
