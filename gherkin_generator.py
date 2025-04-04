from groq import Groq
import config

llm = Groq(api_key=config.GROQ_API_KEY)

def generate_gherkin(summary):
    gherkin_prompt = f"""
    Based on the following requirement summary, generate a Gherkin feature file:
    {summary}
    Format:
    Feature: <Feature name>
      Scenario: <Test case>
        Given <precondition>
        When <action>
        Then <expected result>
    """
    
    response = llm.invoke([{"role": "user", "content": gherkin_prompt}])
    return response
