import win32com.client as win32


class Email:

    def __init__(self):

        receivers_list = ['emilio.pardo@qiagen.com', 'ignacio.micolau@qiagen.com']

        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = receivers_list[0]
        mail.Subject = 'Report Cartuchos'

        mail.HTMLBody = """
        <p>Este correo se genera automáticamente.</p>
        <p>Los cartuchos fabricados por cada turno han sido:</p>
        <img src="TestFigure.png">
        """

        # # To attach a file to the email (optional):
        attachment = r'C:\Users\epardo\PycharmProjects\pythonProject\email_sender\TestFigure.png'
        mail.Attachments.Add(attachment)

        mail.Send()












