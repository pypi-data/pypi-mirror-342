import os
import json
import pandas as pd
import tiktoken
from openai import OpenAI
from collections import defaultdict
import re
import textwrap
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

# Retrieve API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Error: OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_prompt(placeholders, user_prompt, system_prompt):
    """Generate the full prompt for GPT queries."""
    # Include the expected response format in the system message
    default_system_message = "You are a helpful assistant. You're a professional data analysis scientist." 
    identifier_placeholder_system = re.findall(r"{(.*?)}", system_prompt)
    if system_prompt:
        mapping = {key: placeholders.get(key, f"{{{key}}}") for key in identifier_placeholder_system}
        system_message = system_prompt.format_map(mapping)
    else:
        system_message = default_system_message
    # Fill the user_prompt with provided placeholders
    identifier_placeholder_user = re.findall(r"{(.*?)}", user_prompt)
    user_message = user_prompt.format_map({key: placeholders.get(key, f"{{{key}}}") for key in identifier_placeholder_user})
    return system_message, user_message

def count_tokens(text):
    """Calculate the number of tokens in a text"""
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(text))

def query_gpt(system_message, user_message):
    """Send a query to GPT and return the result"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

def execute_prompt(placeholders, user_prompt, system_prompt):
    """Encapsulate GPT query to maintain uniform invocation"""
    system_message, user_message = generate_prompt(placeholders, user_prompt, system_prompt)
    response = query_gpt(system_message, user_message)
    return response, system_message, user_message


def load_data(file_path):
    """Load CSV data"""
    try:
        water_data = pd.read_csv(file_path)
        print(f"Data loaded successfully! {water_data.shape[0]} rows, {water_data.shape[1]} columns.")
        return water_data
    except FileNotFoundError:
        print(f"Error: Data file not found at '{file_path}'. Ensure the file exists.")
        exit()

def extract_and_optionally_run_code(response: str, level: int = 0):
    """Extract code from GPT response and optionally run it"""
    try:
        response = response.encode().decode("unicode_escape")
    except Exception:
        pass  # fallback if already decoded

    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)

    if not code_blocks:
        print(f"{'  '*level}⚠ No code block found in response.")
        return

    code = code_blocks[0].strip()
    lines = code.splitlines()
    width = max(len(line) for line in lines) + 4

    # Draw pretty box
    print("╭" + "─" * (width - 2) + "╮")
    print("│ " + "Extracted Code:".ljust(width - 4) + " │")
    print("├" + "─" * (width - 2) + "┤")
    for line in lines:
        print("│ " + line.ljust(width - 4) + " │")
    print("╰" + "─" * (width - 2) + "╯")

    # Ask user if they want to run it
    run = inquirer.confirm(
        message="💡 Do you want to execute this code?",
        default=False
    ).execute()
    if run:
        print(f"{'  '*level}🧠 Executing code...")
        try:
            exec(code, globals())
        except Exception as e:
            print(f"{'  '*level}❌ Execution error: {e}")

def extract_options_and_insert_into_placeholders(response: str, placeholders: dict, input_file: str, level: int = 0):
    """
    Extract multiple choice options like [A] Option A [B] Option B...
    Let user choose insertion mode (single / multiple),
    insert selected options into placeholders,
    then update the original input JSON file on disk.
    """

    # Step 1: Extract options like [A] Apple, [B] Banana, ...
    option_pattern = re.findall(r"\[(\w+)\]\s*(.*?)(?=\s*\[\w+\]|$)", response, re.DOTALL)
    # if not option_pattern or len(option_pattern) < 2:
    if not option_pattern:
        print(f"{'  '*level}ℹ️ No multiple choice options detected.")
        return

    choices = [f"[{key}] {val.strip()}" for key, val in option_pattern]
    print(f"{'  '*level}ℹ️ Extracted options from response:")
    for c in choices:
        print(f"{'  '*level}  {c}")

    # Step 2: Ask for input mode (single / multiple / skip)
    mode = inquirer.select(
        message="❓ Choose input mode:",
        choices=[
            "Single choice",
            "Multiple choices",
            "[Skip this step]"
        ]
    ).execute()

    if mode == "[Skip this step]":
        print(f"{'  '*level}⏩ Skipped inserting any options.")
        return

    elif mode == "Single choice":
        # Single choice mode: select one option and insert into one placeholder
        selected = inquirer.select(
            message="📝 Choose one of the detected options:",
            choices=choices
        ).execute()
        selected_text = selected.split("] ", 1)[-1]

        field = inquirer.select(
            message="📌 Which placeholder field do you want to insert it into?",
            choices=list(placeholders.keys())
        ).execute()

        placeholders[field] = selected_text
        print(f"{'  '*level}✅ Inserted into placeholder '{field}': {selected_text}")

    elif mode == "Multiple choices":
        # Step 3: Build checkbox choices (add skip option, disabled by default)
        multiple_choices = [Choice(value="[Skip this step entirely]", enabled=False)] + [
            Choice(value=opt, enabled=False) for opt in choices
        ]

        # Let user select multiple options
        selected_options = inquirer.checkbox(
            message="📝 Select multiple options to insert:",
            choices=multiple_choices
        ).execute()

        # If only skip or nothing selected, exit early
        if not selected_options or selected_options == ["[Skip this step entirely]"]:
            print(f"{'  '*level}⏩ Skipped inserting any options.")
            return

        # Remove skip if it was selected together with other items
        selected_options = [opt for opt in selected_options if opt != "[Skip this step entirely]"]

        # For each selected option, ask user which placeholder to insert into
        remaining_placeholders = list(placeholders.keys())
        for selected in selected_options:
            selected_text = selected.split("] ", 1)[-1]

            field_choices = remaining_placeholders + ["[Skip this]"]
            field = inquirer.select(
                message=f"📌 Which placeholder to insert: {selected_text}",
                choices=field_choices
            ).execute()

            if field == "[Skip this]":
                print(f"{'  '*level}🔸 Skipped inserting '{selected_text}'")
                continue

            placeholders[field] = selected_text
            remaining_placeholders.remove(field)
            print(f"{'  '*level}✅ Inserted into placeholder '{field}': {selected_text}")

            if not remaining_placeholders:
                print(f"{'  '*level}⚠️ No more available placeholders. Stopping further insertions.")
                break

    # Step 4: Save updated JSON file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        config["placeholders"] = placeholders

        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        print(f"{'  '*level}💾 Input file '{input_file}' updated successfully.")
    except Exception as e:
        print(f"{'  '*level}❌ Failed to update input file: {e}")
