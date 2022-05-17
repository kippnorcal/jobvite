import pandas as pd
import re


class Field_Transformations:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.possition_abbr()
        self.add_dept_codes()
        self.parse_pay_code()
        self.parse_location_code()
        self.create_jobcoastcode()

    """
    When paycom_job_title is formatted as "Academics Associate (0002/1005/ADASO)"", the following 
    method extracts the capitalized, abbreviated form of the position (i.e. ADASO). Not all field values are
    in this format so it first checks if "(" is included in the string
    """

    def possition_abbr(self):
        new_column = []
        for result in self.dataframe["paycom_job_title"]:
            if "(" in result:
                value = result.split("/")[2]
                new_column.append(value[:-1])
            else:
                new_column.append(None)
        self.dataframe["position"] = new_column

    """
    The following method first joins our Jobvite dataframe with the csv containing department codes, then it cleans it 
    by turning the float (ex. "1015.0") into a string and removing ".0" by only taking the first 4 characters ([:4])
    """

    def add_dept_codes(self):
        dept_codes = pd.read_csv("dept_codes.csv")
        self.dataframe = pd.merge(
            self.dataframe, dept_codes, on="department", how="left"
        )
        self.dataframe.drop(columns="Unnamed: 0", inplace=True)
        new_dept_column = []
        for result in self.dataframe["dept_code"]:
            if isinstance(result, float):
                new_value = str(result)[:4]
                new_dept_column.append(new_value)
            else:
                new_dept_column.append(None)

        self.dataframe["dept_code"] = new_dept_column

    def create_jobcoastcode(self):
        dept_code_string = []

        self.dataframe["jobcoastcode"] = (
            "("
            + self.dataframe["work_location_digit"]
            + "|"
            + self.dataframe["dept_code"]
            + "|"
            + self.dataframe["pay_location_digit"]
            + "|"
            + self.dataframe["position"]
            + "|"
            + "99|9999)"
        )

    """
    The next two methods simply extraxt the 3-digit code from both pay and work location (ex. takes 218 from "KIPP Bayview Elementary (218)"). Since
    not all field values are in this format, it first checks if "(" is in the string. I was getting a data type error so I also first checked
    if the value is a string
)
    """

    def parse_pay_location(self):
        pay_abbr_column = []
        for result in self.dataframe["assigned_pay_location"]:
            if isinstance(result, str) and "(" in result:
                new_value = re.sub("\D", "", result)
                pay_abbr_column.append(new_value)
            else:
                pay_abbr_column.append(None)
        self.dataframe["pay_location_digit"] = pay_abbr_column

    def parse_location_code(self):
        location_abbr_column = []
        for result in self.dataframe["assigned_work_location"]:
            if isinstance(result, str) and "(" in result:
                new_value = re.sub("\D", "", result)
                location_abbr_column.append(new_value)
            else:
                location_abbr_column.append(None)
        self.dataframe["work_location_digit"] = location_abbr_column
