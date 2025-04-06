# main.py (or pipeline.py)
import summarizer
import os


def summarize(text):
    # Replace this with actual LLM or LangChain logic
    return "This is a summary of the input text."


def extract_requirements(summary):
    # Extract requirements from the summary
    return "Functional requirements extracted from the summary."


def run_pipeline_from_file(user_input: str,file_path: str):
    # file_name = file_path.split("/")[-1]
    # file_dir = os.path.dirname(file_path)
    # if file_path.endswith(".pdf"):
    #     text = summarizer.extract_text_from_pdf(file_path)
    # elif file_path.endswith(".txt"):
    #     with open(file_path, "r", encoding="utf-8") as f:
    #         text = f.read()
    # else:
    #     raise ValueError("Unsupported file format. Please upload a PDF or TXT.")

    answer = summarizer.answer_query(
        user_query=user_input,
        file_path=file_path,
        # file_name=file_name,
        model_name="llama-3.3-70b-versatile",  # or whatever model
    )

    return {
        "summary": answer
    }
