from openai import OpenAI

from models import Questions

client = OpenAI()
model = "gpt-4.1-nano"

# ------------------------------------------------------------
# Instructions for the question extraction assistant
# ------------------------------------------------------------
assistant_instructions = """
You are a specialized assistant for extracting exam questions from PDF files.

TASK:
- You will be provided with a file ID for a PDF.
- Your job is to extract all exam questions from it, structure them according to the Questions schema, and return them.

LIMITATIONS:
- Skip images and non-text content.
- Only focus on exam-related questions and subparts.
"""


def extract_questions(file_path: str) -> Questions:
    # ------------------------------------------------------------
    # Step 1: Upload file to OpenAI
    # ------------------------------------------------------------
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose="user_data",
    )

    # ------------------------------------------------------------
    # Step 2: Extract questions from the PDF
    # ------------------------------------------------------------
    response = client.responses.parse(
        model=model,
        instructions=assistant_instructions,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_file", "file_id": file.id},
                    {
                        "type": "input_text",
                        "text": "Extract the questions from the PDF",
                    },
                ],
            }
        ],
        text_format=Questions,
    )

    return response.output[0].content[0].parsed.questions
