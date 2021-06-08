import plotly.graph_objects as go
import numpy as np


class Table:
    def __init__(self, numpy_ordered_matrixes):
        np.random.seed(1)
        # Note: Transposes are performed to keep the print format with the plot format
        # as plotly methods plot columns, not rows

        # Values matrix: [week_days, quantiites_from_databases]
        week_days_array = np.array(['Lunes', 'Martes', 'Miércoles', 'Jueves',
                                    'Viernes', 'Sábado', 'Domingo']).reshape(7, 1)
        quantities_by_shift = numpy_ordered_matrixes
        matrix_days_quantities = np.concatenate((week_days_array, quantities_by_shift), 1).transpose()

        # Colors matrix: [week_days, quantities_from_database]
        colors_week_days = np.array(['white'] * 7).reshape(7, 1)
        colors_quantities = self.convert_to_colors(quantities_by_shift)
        print(colors_quantities)
        color_matrix = np.concatenate((colors_week_days, colors_quantities), 1).transpose()
        print(color_matrix)

        # Headers_colors
        headers_colors = np.array([['white'] * 11, ['white'] + ['#00ffff'] * 5 + ['#ffff00'] * 5]).transpose()

        # Table
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=[['', '<b>Día</b>'],
                        ['', '<b>Noche</b>'],
                        ['', '<b>Mañana</b>'],
                        ['<b>SSL1</b>', '<b>Tarde</b>'],
                        ['', '<b>Noche finde</b>'],
                        ['', '<b>Mañana finde</b>'],
                        ['', '<b>Noche</b>'],
                        ['', '<b>Mañana</b>'],
                        ['<b>SSL3</b>', '<b>Tarde</b>'],
                        ['', '<b>Noche finde</b>'],
                        ['', '<b>Mañana finde</b>']],
                line_color='white',
                fill_color=headers_colors,
                align='center',
                font=dict(color='black', size=12)
            ),
            cells=dict(
                values=matrix_days_quantities,
                line_color='black',
                fill_color=color_matrix,
                align='center',
                font=dict(color='black', size=11)
            ))
        ])

        # Save the table
        path = r'C:\Users\epardo\PycharmProjects\pythonProject\email_sender\TestFigure.png'
        fig.write_image(path, height=450, width=1000)

    def convert_to_colors(self, matrix):

        objectives_dict = {
            'SSL1': dict(week=(719, 762), weekend=(1097, 1162)),
            'SSL3': dict(week=(640, 679), weekend=(977, 1035))
        }

        colors_matrix = np.chararray(matrix.shape, itemsize=6)

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i <= 5 and j <= 5:
                    line = 'SSL1'
                    day = 'week'
                elif i > 5 and j <= 5:
                    line = 'SSL1'
                    day = 'weekend'
                elif i <= 5 and j > 5:
                    line = 'SSL3'
                    day = 'week'
                else:
                    line = 'SSL3'
                    day = 'weekend'

                val = matrix[i][j]

                if np.isnan(val):
                    color = 'grey'
                elif val == 0:
                    color = 'white'
                elif val > objectives_dict[line][day][1]:
                    color = 'green'
                elif objectives_dict[line][day][0] <= val < objectives_dict[line][day][1]:
                    color = 'orange'
                else:
                    color = 'red'

                position = j + i*len(matrix[0])
                print(position, val, color)

                np.put(colors_matrix, position, color)

        return colors_matrix


