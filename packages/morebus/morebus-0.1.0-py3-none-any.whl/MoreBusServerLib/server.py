import subprocess
import os
import json

class Server:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()
        self.process = None

    def load_config(self):
        """ JSON dosyasını yükler """
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def start(self):
        """ Sunucuyu başlatır """
        try:
            command = f"morebus /server {self.config_file}"
            self.process = subprocess.Popen(command, shell=True)
            print(f"Sunucu başlatıldı: {command}")
        except Exception as e:
            print(f"Sunucu başlatılamadı: {str(e)}")

    def stop(self):
        """ Sunucuyu durdurur """
        if self.process:
            self.process.terminate()
            print("Sunucu durduruldu.")
        else:
            print("Sunucu zaten çalışmıyor.")
