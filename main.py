import streamlit as st
import os
import time
import summarizer
import gherkin_generator
import selenium_generator

# st.title("AI-Powered Test Automation Agent with RAG")
st.subheader("🚀 **AI-Powered Test Automation Agent with RAG** 🎉")
st.write("---")


with st.sidebar:
    st.header("Upload & Select Model")
    
    # File uploader inside the sidebar
    uploaded_file = st.file_uploader("Upload Requirement Document", type=["pdf", "txt"])

    # Model selection inside the sidebar
    selected_model = st.selectbox(
        "Select an AI Model:",
        ["gemma2-9b-it", "llama-3.3-70b-versatile","deepseek-r1-distill-llama-70b"]
    )


if uploaded_file:
    file_path = os.path.join("./uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.upload_success = True
    st.success(f"📂 File '{uploaded_file.name}' uploaded successfully!")

    
    # st.rerun()
    # with st.spinner("Summarizing requirement..."):
        
    #     summary = summarizer.summarize_requirement("./uploads",uploaded_file.name)
    #     st.subheader("Requirement Summary")
    #     st.text_area("", summary, height=400)

    # 🔹 Allow User to Ask Queries Based on the Uploaded Document
    user_query = st.text_input("Ask a question about the document:")
    
    if user_query:
        with st.spinner("Retrieving answer..."):
            answer = summarizer.answer_query(user_query, "./uploads", uploaded_file.name,selected_model)
            if not answer:
               answer = "❌ No answer found for your question." 
            st.subheader("Answer")
            st.markdown(f"```{answer}```")

    # with st.spinner("Generating Gherkin test scenarios..."):
    #     gherkin_scenario = gherkin_generator.generate_gherkin(summary)
    #     st.subheader("Generated Gherkin Feature File")
    #     st.text_area("", gherkin_scenario, height=200)

    # with st.spinner("Generating Selenium test script..."):
    #     selenium_script = selenium_generator.generate_selenium_script()
    #     st.subheader("Generated Selenium Test Script")
    #     st.text_area("", selenium_script, height=200)

    # st.download_button("Download Selenium Script", selenium_script, file_name="test_script.py")
