from functools import reduce
import re
import xlwings as xw
import pandas as pd


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

        # Get the cell value (in string format)
        try:
            # Avoid the single lot float error
            self.value = str(int(location.value))
        except ValueError:
            # Avoid the multiple lots string error
            self.value = str(location.value)

        # Save the selected row and column
        self.row = location.row
        self.column = location.column

        # Removes the text between brackets and the brackets
        filtered = self.remove_values_brackets(self.value)

        # In case that there are many values in the same cell, splits them into a list
        try:
            self.split_lots = filtered.split(' / ')
        except TypeError as e:
            # If the selected cell only has one value, then save it in a list of one entry
            print('This cell does not contain any parenthesis', e)
            self.split_lots = [str(int(self.value))]
            print('Single value. List created: ', self.split_lots)
            pass

    def remove_values_brackets(self, cell_value: str) -> str:
        """
        Removes the text between brackets and the brackets. Moreover, removes the remaining space if necessary.
        '210234 / 2104532 (234)' =>  '210234 / 2104532'
        :param cell_value: [str] Raw cell value. F.Ex: '210234 / 2104532 (234)'
        :return:  [str] Only the lots numbers. F.Ex: '210234 / 2104532'
        """
        filtered = re.sub("[\(\[].*?[\)\]]", "", cell_value)

        # In case that the last value is a space, return the string without the last space
        return filtered if filtered[:-1] != ' ' else filtered[:-1]

    def change_adjacent_value(self, value):

        # Convert current letter position to integer
        current_column = self.column
        # Get next column: n + 1
        next_column = current_column + 1
        print('Column modified: ', next_column)

        # Change value with xlwings from continuous cell
        xw.Range((self.row, next_column)).value = value


# =========== Executable method ==================
if __name__ == '__main__':

    # Create the Data Frame where supplier lots are stored
    df = pd.read_excel("J:\\48 Documentation\\14. Georgina\\Traceability_XJ.xlsx", sheet_name='PO', engine='openpyxl')

    # Change the "Lot/Serial" column is string type
    df['Lot/Serial'] = df['Lot/Serial'].astype(str)

    while True:
        input('Press any key to execute the code')

        # Selected Cell data
        sel_cell = SelectedCell()

        print('Cell column: ', sel_cell.column)

        list_lots = sel_cell.split_lots
        print('Cell values split: ', list_lots)

        # Converting each entry into strings
        list_lots = [str(entry) for entry in list_lots]

        # Get the match in the PO Sheet
        matches = [] * len(list_lots)
        for lot in list_lots:
            print('Searching lot: ', lot)
            try:
                matches += [df['Supplier Lot'].loc[(df['Lot/Serial'] == lot)].tolist()[0]]
            except IndexError:
                # When there is no match with the PO Sheet, return a "#N/D"
                print('main.py, Line 80: Not Found item on Data Source ', lot)
                matches += ['#N/D']
        # print(matches)

        # Convert to the format: 'SupplierLot1 / SupplerLot2' if there are more than one lot
        supplier_lots = reduce(lambda x, y: str(x) + ' / ' + str(y), matches)
        print('Supplier lots: ', supplier_lots)

        # Changing the value in the opposite cell with the suppliers lot values
        sel_cell.change_adjacent_value(supplier_lots)


