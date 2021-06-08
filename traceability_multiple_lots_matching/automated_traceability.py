from functools import reduce
import re
import xlwings as xw
import pandas as pd
import numpy as np
import logging

# Configure base logger object
logging.basicConfig(filename='logfile.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w',
                    level=logging.ERROR
                    )

# Create a logging object
logger = logging.getLogger()



class SelectedCell:
    """  Class: SelectedCell
         Attributes:
         - row: [str] Letter that represents the cell vertical location in Excel. F.Ex: 'A'
         - column: [str] Number that represents the cell horizontal location in Excel. F.Ex: '1'
         - value: [str] Value contained in the cell. F.Ex: '2011712 / 2011726 (233)'
         - split_lots: [list of str] List of lots in string format. F.Ex: ['2011712', '2011726']
    """

    # Constructor
    def __init__(self):
        app = xw.apps.active
        location = app.selection
        # Location: "$A$1"

        # Get location value
        self.value = location.value

        # Remove first character (first "$")
        location = location.address[1:]

        # Split to get the attributes row and column
        # "A$1" => split("$") => ['A', '1']
        (self.column, self.row) = location.split('$')

        # Removes the text between brackets and the brackets itselves
        try:
            filtered = re.sub("[\(\[].*?[\)\]]", "", self.value)
            # Also remove the remaing last space
            self.split_lots = filtered[:-1].split(' / ')
        except TypeError as e:
            # If the selected cell does not have a parenthesis, then do save it in a list of one entry as an integer
            print('This cell does not contain any parenthesis')
            self.split_lots = [int(self.value)]
            pass

    def change_adyacent_value(self, value):

        # Convert current letter position to integer
        current_column = chr_to_int(self.column)
        # Get next column: n + 1
        next_column = current_column + 1
        print('La siguiente columns es: ', next_column)

        # Change value with xlwings from continuous cell
        xw.Range((self.row, next_column)).value = value

def chr_to_int(letters):
    # Function to convert a position in letters to numeric posiion
    # Letters can be: from 'A' to 'Z' and then 'AAA' to 'XFD' [str]
    # Note: ord(A) = 65 => it should be 1 (so substract 64 to become 1)
    print('Letters entering: ', letters)

    # transform each character into a number from 1  ('A') to 26 ('Z') and add it into a vector
    # Ex: 'A' => [1]
    # Ex: 'AA' => [1, 1]
    # Ex: 'ZZZ' => [26, 26, 26]
    numbers = list(map(lambda x: ord(x) - 64, letters))

    # Add all the list numbers to get a total number. F.Ex: [26, 26, 26] => 26 * 26^2 + 26 * 26^1 + 26 * 26^0 = 18278
    # Ex: [23] => 23 * 26^0 = 23
    # Ex: [24, 25] => 24 * 26^1 + 25 * 26^0 = 649

    # First create the exponents list
    exponents = list(range(len(letters) - 1, -1, -1))
    # Ex: letters = len(letters) = 5 => [4, 3, 2, 1, 0]
    # Multiply each exponent by 26:
    values = [26 ** x for x in exponents]
    # Ex: Values = [26^4 26^3 26^2 26 1]

    # Add the respective value from the numbers
    multiplied = (np.array(values) * np.array(numbers)).tolist()
    print('Multiplied: ', multiplied)

    position = reduce(lambda x, y: int(x) + int(y), multiplied)
    print('Position: ', position)

    # return the absolute position
    return position

def int_to_chr(number):
    # Converts a number [int] to an Excel column [str]. F.Ex: 1 => 'A'
    # Example: 712 =>

    # Note: 712 = 1*25^2 + 1*25^1 + 10*25^0

    # Since: 712 // 25 = 27
    # remainder (rest): 712 % 26 = 10 (LSB)
    # Step 2: 27 // 25 = 1 (middle B)
    # remainder (rest): 27 % 25 = 1 (MSB)

    # Division in python: quotient, remainder = divmod(a, b)
    # Letters quantity in alphabet
    q_letters_alphabet = 25

    remainders = []

    dividend = number

    while dividend > 0:
        # perform a regular division with 25 and get the remainder
        print('Dividend (aka new Position): ', dividend)
        quotient, remainder = divmod(dividend, q_letters_alphabet)
        print('Quotient: ', quotient)
        print('Remainder: ', remainder)
        remainders += [remainder]
        # Now the quotient becomes the new number (dividend)
        dividend = quotient

    # Reverse the list to get ordered from MSB to LSB
    # Ex: 712 = [10, 1, 1] (remainders) , as 712 = 1*25^2 + 1*25^1 + 10*25^0 = [1, 1, 10] * [26^2 26^1 26^0], the vector
    # the remainders vector must be reversed
    remainders.reverse()
    print('Remainders: ', remainders)

    # Vector to get the letter for each value. Ex: As 1 = 'A', 2 ='B', ... : [1, 1, 10] = ['A', 'A', 'J']
    column = [chr(n + 64) for n in remainders]
    print('Columns ', column)

    # Return all the values wrapped together. Ex: ['A', 'A', 'J'] = 'AAJ'
    letter_position = reduce(lambda x, y: x + y, column)
    print('Letter position: ', letter_position)
    return letter_position


# =========== Executable method ==================
if __name__ == '__main__':

    try:
        # Create the Data Frame where supplier lots are stored
        df = pd.read_excel("J:\\48 Documentation\\Traceability_XJ.xlsx", sheet_name='PO')

        while True:
            input('Press any key to execute the code')
            # Selected Cell datas
            sel_cell = SelectedCell()
            values = sel_cell.value
            print(sel_cell.column)
            list_lots = sel_cell.split_lots
            # Converting each entry into int (if there are more than one entry to avoid raising error)
            if len(list_lots) > 1:
                list_lots = list(map(lambda x: int(x), list_lots))

            # Get the match in the PO Sheet
            try:
                matches = [df['Supplier Lot'].loc[(df['Lot/Serial'] == lot)].matrix_days_quantities[0] for lot in list_lots]
            except IndexError:
                # When there is no match with the Sheet Data Source, the returned value will be "#N/D"
                print('main.py, Line 151: Not Found item on Data Source')
                matches = ['#N/D']
            # print(matches)

            # Convert to the format: 'SupplierLot1 / SupplerLot2'
            supplier_lots = reduce(lambda x, y: str(x) + ' / ' + str(y), matches)
            print(supplier_lots)

            # Changing the value in the opposite cell with the suppliers lot values
            sel_cell.change_adyacent_value(supplier_lots)

    except Exception as e:
        # Save Error in a text file to improve
        logger.error('Found Error: %s' % (e))

