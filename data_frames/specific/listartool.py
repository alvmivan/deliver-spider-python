# lista en esta carpeta todos los archivos que tengan una sola linea (o ninguna) de texto (terminan en csv)

import os

listdir = [x for x in os.listdir()]
files_to_delete = []
for file in listdir:
    if file.endswith(".csv"):
        with open(file, "r", encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) <= 1:
                if lines == ['search_term,name,url,price,provider_id,photo,details,brand\n']:
                    files_to_delete.append(file)

print("will delete the following files:")
print(files_to_delete)
yes = input("are you sure? (y/n)")
if yes == "y":
    for file in files_to_delete:
        os.remove(file)
        print(file + " deleted")
