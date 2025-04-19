import os
import pkg_resources

def read_file(relative_path):
    filepath = pkg_resources.resource_filename(__name__, f'slaveni/{relative_path}')
    with open(filepath, 'r') as file:
        return file.read()

# Пример использования
content1 = read_file('file1.txt')  # Чтение файла в корне slaveni
content2 = read_file('app/static/css/style.css')  # Чтение файла в подпапке
content3 = read_file('app/templates/template.html')  # Чтение файла в другой подпапке

print(content1)
print(content2)
print(content3)