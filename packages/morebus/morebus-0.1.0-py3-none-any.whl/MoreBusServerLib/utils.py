import os

def ensure_directory_exists(directory):
    """ Eğer dizin yoksa oluşturur """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"{directory} dizini oluşturuldu.")
    else:
        print(f"{directory} dizini zaten var.")
