import pysftp

host = 'sfr0bu6xdb03.odqad.com'
user = 'manfu'
password = 'Qwerty@12345'

if __name__ == '__main__':
    with pysftp.Connection(host=host, port=22, username=user, password=password) as sftp:
        print('Connection succesfully stablished ....')
        sftp.cwd('/tmp/Sys/Outbound')
        directory_structure = sftp.listdir_attr()