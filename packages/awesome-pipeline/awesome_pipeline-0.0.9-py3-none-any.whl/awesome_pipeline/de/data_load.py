import pandas as pd
from ..utils.de_utils import *
from .configuration import Configuration
from .data_quality_checker import DataQualityChecker
from fpdf import FPDF


class DataLoad:
    def __init__(self, config: Configuration = None):
        self.data = None
        self.configuration = config

    def load_csv(self, file_path):
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            print(f"Failed to load data: {e}")
        return None

    def quality_check_in_folder(self, log_filename=None):
        folder_path = os.path.join(
            self.configuration.get("global.project.path"),
            self.configuration.get("quality_checking.file_source.path"),
        )
        if log_filename is None:
            from datetime import datetime

            # Get the current timestamp
            current_timestamp = datetime.now()
            # Convert to a string in a desired format
            timestamp_str = current_timestamp.strftime("%Y%m%d_%H%M%S")
            log_filename = "data_quality_report_" + timestamp_str + ".pdf"

        output_pdf_path = os.path.join(
            self.configuration.get("global.project.path"),
            self.configuration.get("quality_checking.output.path"),
            log_filename,
        )
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set font for the PDF
        pdf.set_font("Arial", size=12)

        # Iterate over all CSV files in the specified folder
        for filename in os.listdir(folder_path):
            print(folder_path + " ----------" + filename)
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                self.configuration.logging.info(f"Processing file: {filename}")

                # Load the CSV file into a DataFrame
                try:
                    df = pd.read_csv(file_path)
                    checker = DataQualityChecker(df)
                    report = checker.generate_report()

                    # Add file name to PDF
                    pdf.cell(
                        200,
                        10,
                        txt=f"Data Quality Report for {filename}",
                        ln=True,
                        align="C",
                    )
                    pdf.ln(10)

                    # Add report details to PDF
                    for check_name, check_result in report.items():
                        pdf.cell(200, 10, txt=f"{check_name}:", ln=True)
                        if isinstance(check_result, pd.DataFrame):
                            # Add DataFrame details
                            for row in check_result.itertuples():
                                pdf.cell(200, 10, txt=str(row), ln=True)
                        else:
                            # Add simple result (text)
                            pdf.cell(200, 10, txt=str(check_result), ln=True)
                        pdf.ln(5)

                    pdf.add_page()  # Add a new page for the next file

                except Exception as e:
                    self.configuration.logging.error(
                        f"Error processing file {filename}: {e}"
                    )
                    pdf.cell(200, 10, txt=f"Error processing {filename}: {e}", ln=True)
                    pdf.add_page()  # Add a new page after error

        # Output the PDF
        pdf.output(output_pdf_path)
        self.configuration.logging.info(f"PDF report saved to {output_pdf_path}")

    def quality_check_file(self, single_file, log_filename=None):
        folder_path = os.path.join(
            self.configuration.get("global.project.path"),
            self.configuration.get("quality_checking.file_source.path"),
        )
        if log_filename is None:
            from datetime import datetime

            # Get the current timestamp
            current_timestamp = datetime.now()
            # Convert to a string in a desired format
            timestamp_str = current_timestamp.strftime("%Y%m%d_%H%M%S")
            log_filename = "data_quality_report_" + timestamp_str + ".pdf"

        output_pdf_path = os.path.join(
            self.configuration.get("global.project.path"),
            self.configuration.get("quality_checking.output.path"),
            log_filename,
        )
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set font for the PDF
        pdf.set_font("Arial", size=12)

        # Iterate over all CSV files in the specified folder
        for filename in os.listdir(folder_path):
            if filename.endswith(single_file + ".csv"):
                file_path = os.path.join(folder_path, filename)
                self.configuration.logging.info(f"Processing file: {filename}")

                # Load the CSV file into a DataFrame
                try:
                    df = pd.read_csv(file_path)
                    checker = DataQualityChecker(df)
                    report = checker.generate_report()

                    # Add file name to PDF
                    pdf.cell(
                        200,
                        10,
                        txt=f"Data Quality Report for {filename}",
                        ln=True,
                        align="C",
                    )
                    pdf.ln(10)

                    # Add report details to PDF
                    for check_name, check_result in report.items():
                        pdf.cell(200, 10, txt=f"{check_name}:", ln=True)
                        if isinstance(check_result, pd.DataFrame):
                            # Add DataFrame details
                            for row in check_result.itertuples():
                                pdf.cell(200, 10, txt=str(row), ln=True)
                        else:
                            # Add simple result (text)
                            pdf.cell(200, 10, txt=str(check_result), ln=True)
                        pdf.ln(5)

                    pdf.add_page()  # Add a new page for the next file

                except Exception as e:
                    self.configuration.logging.error(
                        f"Error processing file {filename}: {e}"
                    )
                    pdf.cell(200, 10, txt=f"Error processing {filename}: {e}", ln=True)
                    pdf.add_page()  # Add a new page after error

        # Output the PDF
        pdf.output(output_pdf_path)
        self.configuration.logging.info(f"PDF report saved to {output_pdf_path}")
        return report

    def load_dummy(self):
        # this is a function that used for preparing dummy testing data,set lable:
        self.labels = ["historical", "current"]
        # Sample dataset
        data = {
            "text": [
                "The patient was diagnosed with diabetes in 2010.",
            ],
            "label": self.labels,
        }

        df = pd.DataFrame(data)
        # Map labels to integers
        self.label_map = {item: index for index, item in enumerate(self.labels)}
        df["label"] = df["label"].map(self.label_map)
        self.data = df
