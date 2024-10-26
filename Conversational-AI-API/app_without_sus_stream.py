import os
import openai
from docx import Document
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
#openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = st.secrets["open_ai_key"]

if openai.api_key is None:
    st.error("OpenAI API key not found. Please check your .env file.")
else:
    st.success("OpenAI API key loaded successfully.")

# Load resource files
def load_resources():
    resources = {}
    for root, dirs, files in os.walk('Sample_Training_Documents'):
        for file in files:
            if file.endswith('.docx'):
                doc = Document(os.path.join(root, file))
                content = ''
                referral_links = []
                link_flag = False
                for para in doc.paragraphs:
                    if para.text.strip():
                        content += para.text + '\n'
                        if "http" in para.text:  # Check for URLs
                            referral_links.append(para.text)
                            link_flag = True
                if not link_flag:
                    referral_links.append(f"https://vbnreddy/resources/{file}")

                resources[file] = {
                    "content": content.strip(),
                    "links": referral_links
                }
    return resources

resources = load_resources()
st.success("resources_data": resources)

# Suggest files and links based on user input
def suggest_files(issue):
    suggestions = []
    referral_links = []
    for file_name, resource in resources.items():
        content = resource["content"]
        links = resource["links"]
        
        if issue.lower() in content.lower() or file_name.lower().startswith(issue.lower()):
            suggestions.append(file_name)
            referral_links.extend(links)
    st.success("suggested_files return")
    return suggestions, referral_links

# Streamlit UI
st.title("Conversational AI Chat-3")
user_input = st.text_input("Please describe your issue:")

if st.button("Submit"):
    if user_input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_response = response.choices[0].message['content']
        st.success("suggested_files going")
        suggested_files, referral_links = suggest_files(user_input)

        st.subheader("Response from AI:")
        st.write(bot_response)
        # st.subheader("Suggested Resources:")
        # if suggestions:
        #     suggested_file = suggestions[0][0]  # Get the file name of the top suggestion
        #     referral_link = suggestions[0][2]    # Get the links of the top suggestion
        # else:
        #     suggested_file = None
        #     referral_link = None
        # st.write(f"File: {suggested_file}")
        # st.write(f"Links: {referral_link[0]}")
        st.success(suggested_files)
        st.success(referral_links)
        if suggested_files:
            st.subheader("Suggested Files:")
            for file in suggested_files:
                st.write(file)
            st.subheader("Referral Links:")
            for link in referral_links:
                st.write(link)
        else:
            st.write("No suggestions found.")
    else:
        st.warning("Please provide some input.")
