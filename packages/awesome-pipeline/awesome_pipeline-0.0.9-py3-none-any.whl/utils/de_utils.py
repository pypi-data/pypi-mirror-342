from datetime import datetime
from dateutil.relativedelta import relativedelta
import xmltodict
import pandas as pd
import yaml
import os
import ast
from pathlib import Path
import shutil
import glob


def convert_and_format_date(date_input: str) -> str:
    """This function convert different date string from input into a unified format: YYYY-MM-DD
    This date pattern is customizeable and extendable, it can be applied to specific clinic date format
    that's unable to handle by general pythond date format.

    Args:
        date_input (str): the input format of data
    Raises:
        ValueError: is not an valid string format in our definition, it raised an exception

    Returns:
        str: formatted YYYY-MM-DD date str
    """
    formats = [
        "%Y-%m-%d",  # e.g., 2024-08-19
        "%d/%m/%Y",  # e.g., 19/08/2024
        "%m-%d-%Y",  # e.g., 08-19-2024
        "%d-%b-%Y",  # e.g., 19-Aug-2024
        "%d %B %Y",  # e.g., 19 August 2024
        "%d %b %Y",  # e.g., 19 Aug 2024
    ]
    date_string = str(date_input)
    for fmt in formats:
        try:
            date_object = datetime.strptime(date_string, fmt)
            # Convert to the desired format YYYY-MM-DD
            return date_object.strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date_string}' not recognized.")


def get_date_early(date_str: str, delta_year=1) -> str:
    """This function add a delta_year to a baseline date, and output the new date

    Args:
        date_str (str): the input date, as the baseline
        delta_year (int, optional): different date. Defaults to -1.

    Returns:
        str: adding delta_year years on top of date_str,
    """
    # Convert the string to a datetime object
    original_date = datetime.strptime(date_str, "%Y-%m-%d")
    year_earlier = original_date - relativedelta(years=delta_year)

    # Convert back to string if needed
    return year_earlier.strftime("%Y-%m-%d")


def read_XML(
    filename="data/raw/smokers_surrogate_train_all_version2.xml",
):

    with open(os.path.join(get_base_dir(), filename), "r") as file:
        xml_data = file.read()

    data_dict = xmltodict.parse(xml_data)
    data = []
    records = data_dict["ROOT"]["RECORD"]
    if isinstance(records, list):
        # If 'RECORD' is a list, iterate over each entry
        for record in records:
            record_id = record["@ID"]
            smoking_status = record["SMOKING"]["@STATUS"]
            text_content = record["TEXT"].strip()
            data.append((record_id, smoking_status, text_content))
    df = pd.DataFrame(data, columns=["record_id", "smoking_status", "text"])
    return df


def read_yaml(path):
    with open(path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def is_running_in_docker():
    """Check if the script is running inside a Docker container."""
    # This check relies on Docker-specific paths and environment variables.
    # One common method is to check for the existence of /.dockerenv.
    return os.path.exists("/.dockerenv")


def get_base_dir():
    current_file_path = os.path.abspath(__file__)
    # Find the index of the first occurrence of 'nlp_pipeline'
    first_occurrence_index = current_file_path.find("nlp_pipeline")

    if first_occurrence_index != -1:
        # Slice the path up to the end of the first 'nlp_pipeline' occurrence
        truncated_path = current_file_path[
            : first_occurrence_index + len("nlp_pipeline")
        ]
    else:
        # If 'nlp_pipeline' is not found, use the entire path
        truncated_path = current_file_path
    # adjust for docker path
    if truncated_path.startswith("/app/nlp_pipeline"):
        truncated_path = truncated_path.replace("/app/nlp_pipeline", "/app", 1)

    if is_docker():
        truncated_path = "/app"
    return truncated_path


def is_docker():
    cgroup = Path("/proc/self/cgroup")
    return (
        Path("/.dockerenv").is_file()
        or cgroup.is_file()
        and "docker" in cgroup.read_text()
    )


def read_text_content(relative_path: str):
    with open(
        os.path.join(
            get_base_dir(),
            relative_path,
        ),
        "r",
    ) as file:
        list_content = file.read()

    my_list = ast.literal_eval(list_content)
    return my_list


def move_csv(source_path, destination_path):
    source_folder = os.path.join(get_base_dir(), source_path)
    destination_folder = os.path.join(get_base_dir(), destination_path)

    # Ensure the destination folder exists, create if it doesn't
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get all CSV files in the source folder
    csv_files = glob.glob(os.path.join(source_folder, "*.csv"))

    # Move each CSV file to the destination folder
    for file in csv_files:
        destination_file = os.path.join(destination_folder, os.path.basename(file))
        shutil.move(file, destination_file)
