import win32com.client as win32

if __name__ == '__main__':

    # receivers_list = ['marialaura.marinelli@contractor.qiagen.com', 'georgina.mitjansdomenech@qiagen.com']

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'emilio.pardo@qiagen.com'
    mail.Subject = 'mensaje de prueba'
    # mail.Body = """
    # Jodeos: Ahora puedo hacer spam a todo el mundo.
    #
    # os lo envío a las dos al mismo tiempo.
    #
    # Firmado:
    #
    # El nuevo spammer de la empresa
    #
    # """
    mail.HTMLBody = """<p>Mensaje de prueba para testear que puedo enviar la información"""

    # # To attach a file to the email (optional):
    attachment = r'C:\Users\epardo\PycharmProjects\pythonProject\email_sender\table_report'
    mail.Attachments.Add(attachment)

    mail.Send()












