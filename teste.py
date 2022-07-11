import os






caminho = os.path.dirname(os.path.abspath(__file__))+'\\server_files'


a = input('=')

a = a.split('\D:',1)
print(a)