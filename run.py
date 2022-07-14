# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures from the user.
    Run a while loop to collect valid data from the user
    via the terminal, must be 6 values, comma seperated.
    Loop ends when data entered is valid,
    """
    while True:
        print("Please enter the sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid')
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values are required, you entered {len(values)}'
            )
    except ValueError as error:
        print(f'Invalid data: {error}, please try again.\n')
        return False

    return True


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print('Update sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    print(sales_worksheet)
    sales_worksheet.append_row(data)
    print('Sales worksheet updated successfully.\n')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales minus the stock:
    -Positive values indicates waste
    -Negative values indicate added stock when main stock ran out
    """
    print('Calculating surplus data ...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print('Welcome to Love Sandwiches Data Automation')
main()
