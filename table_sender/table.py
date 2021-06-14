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
        colors_week_days = np.array(['ghostwhite'] * 7).reshape(7, 1)
        colors_quantities = self.convert_to_colors(quantities_by_shift)
        print(colors_quantities)
        color_matrix = np.concatenate((colors_week_days, colors_quantities), 1).transpose()
        print(color_matrix)

        # Headers_colors
        headers_colors = np.array([['white'] + ['lightcyan'] * 5 + ['lightskyblue'] * 5,
                                  ['white'] + ['lightcyan'] * 5 + ['lightskyblue'] * 5]).transpose()

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
                line_color=headers_colors,
                fill_color=headers_colors,
                align='center',
                font=dict(color='black', size=18)
            ),
            cells=dict(
                values=matrix_days_quantities,
                line_color='black',
                fill_color=color_matrix,
                align='center',
                font=dict(color='black', size=16),
                height=45
            ))
        ])

        # Save the table
        path = r'J:\98_Scaling up plan\14-Proyectos 2021\13_Lean Box\20_Objetivo y Producciones\ObjectivesTable.png'
        fig.write_image(path, height=680, width=1500, scale=0.8)

    def convert_to_colors(self, matrix):

        # Objectives dictionary
        objectives_dict = {
            'SSL1': dict(week=(dict(max=648, min=611)), weekend=(dict(max=1162, min=932))),
            'SSL3': dict(week=(dict(max=577, min=544)), weekend=(dict(max=1035, min=830)))
        }

        # Preallocate the matrix
        colors_matrix = np.chararray(matrix.shape, itemsize=6)

        # Fulfill the matrix with the values based on the value
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                day = 'week' if i < 5 else 'weekend'
                line = 'SSL1' if j < 5 else 'SSL3'

                val = matrix[i][j]
                min = objectives_dict[line][day]['min']
                max = objectives_dict[line][day]['max']

                color = 'black' if np.isnan(val) else 'white' if val == 0 else \
                        'red' if val < min else 'green' if val > max else 'orange'

                position = j + i * len(matrix[0])
                print(position, i, j, val, line, day, min, max, color)

                np.put(colors_matrix, position, color)

        return colors_matrix
