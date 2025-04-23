"""Helper file functions"""

import os
import re
import readline  # pylint: disable=unused-import
import sys

from dataclasses import dataclass
from enum import Enum

from datetime import datetime
from pymongo import MongoClient


def get_width() -> int:
    """Get width"""

    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def prompt_preview(prompt: str):
    """Prompt preview"""

    width = get_width()

    start = "[ PROMPT ] "
    end = "[ / PROMPT ] "

    asterisks_start = "*" * (width - len(start))
    asterisks_end = "*" * (width - len(end))

    sys.stderr.write(
        "\n".join([start + asterisks_start, prompt, end + asterisks_end + "\n\n"])
    )


def process_file_tags(s):
    """Process file tags"""

    def replace_tag(match):
        filename = match.group(1).strip()
        try:
            return read_file_contents(filename)
        except FileNotFoundError:
            print("Error: File not found", file=sys.stderr)
            return ""

    return re.sub(r"<file>(.*?)</file>", replace_tag, s, flags=re.DOTALL)


def strip_thinking(response: str) -> str:
    """String thinking"""

    return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()


def read_file_contents(filename: str):
    """Read system description."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def get_child_folders(directory):
    """Get the child folders of a given directory."""
    try:
        contents = os.listdir(directory)
        for item in contents:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                print(item)
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
    except PermissionError:
        print(f"Permission denied: {directory}")


def search_file_type(directory, extension):
    """Search files ending with a specific extension"""
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files


def find_full_input_output_folder(folder_path, input_filename, output_filename):
    """Find conversation folder"""
    results = []
    for root, _, files in os.walk(folder_path):
        if output_filename in files and input_filename in files:
            with open(
                os.path.join(root, output_filename), "r", encoding="utf-8"
            ) as file:
                assistant_content = file.read()
            with open(
                os.path.join(root, input_filename), "r", encoding="utf-8"
            ) as file:
                user_content = file.read()
            if assistant_content != "" and user_content != "":
                results.append(root)
    return results


def get_latest_folder(root, directories) -> str:
    """Get latest directories"""
    latest_folder = ""
    latest_time = 0

    for directory in directories:
        full = os.path.join(root, directory)
        if os.path.isdir(full):
            folder_time = os.path.getmtime(full)
            if folder_time > latest_time:
                latest_time = folder_time
                latest_folder = directory

    return latest_folder


def generate_next_folder_name(
    root: str,
    latest_folder: str,
    input_filename: str = "input",
    output_filename: str = "output",
):
    """Generate unique sequenced folder"""
    if (not os.path.exists(os.path.join(root, latest_folder, input_filename))) and (
        not os.path.exists(os.path.join(root, latest_folder, output_filename))
    ):
        return latest_folder

    match = re.search(r"\d+", latest_folder)
    if match:
        start_index = match.start()
        end_index = match.end()
        number = int(latest_folder[start_index:end_index])

        new_number = str(number + 1).zfill(end_index - start_index)

        new_string = (
            latest_folder[:start_index] + new_number + latest_folder[end_index:]
        )
    else:
        new_string = latest_folder + ".1"

    if os.path.exists(os.path.join(root, new_string)):
        return generate_next_folder_name(
            root, new_string, input_filename, output_filename
        )
    return new_string


def is_question_the_same_as_last(
    root: str, question: str = "", input_filename: str = "input"
) -> bool:
    """Get history's latest question"""
    os.makedirs(root, exist_ok=True)
    directories = next(os.walk(root))[1]
    if len(directories) == 0:
        return False
    latest_folder = get_latest_folder(
        root,
        directories,
    )
    if (
        read_file_contents(os.path.join(root, latest_folder, input_filename))
        == question
    ):
        return True
    return False


def get_new_export_directory_under(
    root: str, input_filename: str = "input", output_filename: str = "output"
):
    """Get new export directory"""
    directories = next(os.walk(root))[1]
    if len(directories) == 0:
        os.makedirs(os.path.join(root, "1"))
        directories = next(os.walk(root))[1]
    return generate_next_folder_name(
        root,
        get_latest_folder(
            root,
            directories,
        ),
        input_filename,
        output_filename,
    )


def get_database_connection():
    """Get database connection"""
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["model"]


def write_training_data(collection: str, date: datetime, entry: dict):
    """Save to MongoDB database"""
    db = get_database_connection()
    col = db[collection]
    col.insert_one({"date": date, "entry": entry})


def retrieve_conversations_together(slug: str) -> list[dict[str, str]]:
    """Structure conversation"""

    collection = get_database_connection()[slug]
    results = collection.find({}, {"_id": 0, "entry": 1}).sort("date", 1)

    conversations = [
        {"role": doc["entry"]["role"], "content": doc["entry"]["content"]}
        for doc in results
    ]

    return conversations


def retrieve_conversations_date(slug: str):
    """Structure conversation"""

    collection = get_database_connection()[slug]
    return collection.find_one(sort=[("date", -1)])


def get_question() -> str:
    """Get question"""

    question: str = ""

    if not sys.stdin.isatty():
        question = sys.stdin.read()
    else:
        sys.stderr.write("Press Ctrl+D to submit\n\n")
        while True:
            try:
                ask = input()
                question += ask + "\n"
            except EOFError:
                break
        question = question.strip()
        sys.stderr.write("\n")

    return question


def read_file_content(filename: str) -> str | None:
    """Read file content"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(
            f'{BColors.WARNING}[Warning]{
            BColors.END_C} File "{filename}" not found '
        )
    return None


@dataclass
class BColors:
    """BColors"""

    HEADER = "\033[95m"
    OK_BLUE = "\033[94m"
    OK_CYAN = "\033[96m"
    OK_GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END_C = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CloudProvider(Enum):
    """Cloud Provider Enumeration"""

    AMAZON_BEDROCK = 1
    GOOGLE_VERTEX_AI = 2
    ANTHROPIC = 3
    GEMINI = 4


class OpenAILibraryEndpoint(Enum):
    """Cloud Provider Enumeration"""

    NVIDIA = 1
    GROQ = 2
    VERTEX_LLAMA = 3
    OPENAI = 4
