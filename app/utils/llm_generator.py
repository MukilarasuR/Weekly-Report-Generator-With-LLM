import os
import trace
import traceback
import openai
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load and render prompt template
def render_llm_prompt(template_path: str, context: dict) -> str:
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = Template(file.read())
            return template.render(**context)
    except Exception as e:
        return f"❌ Prompt Rendering Error: {str(e)}"

# Generate LLM-based report from prompt
def generate_llm_report(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional project analyst writing structured weekly reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1200
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.error.OpenAIError as e:
        return f"❌ LLM Error: {str(e)}"
    except Exception as e:
        print(str(e), traceback.format_exc())
