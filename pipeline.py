# main.py (or pipeline.py)
import summarizer

def summarize(text):
    # Replace this with actual LLM or LangChain logic
    return "This is a summary of the input text."

def extract_requirements(summary):
    # Extract requirements from the summary
    return "Functional requirements extracted from the summary."



# Final pipeline function
def run_pipeline(text):
    summary = summarize(text)
    requirements = extract_requirements(summary)
    # gherkin = generate_gherkin(requirements)
    # selenium_code = generate_selenium_code(gherkin)

    return {
        "summary": summary,
        "requirements": requirements
        # "gherkin": gherkin,
        # "selenium_code": selenium_code
    }
def run_pipeline_from_file(file_path: str) -> dict:
    if file_path.endswith(".pdf"):
        text = summarizer.extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT.")

    return run_pipeline(text)
