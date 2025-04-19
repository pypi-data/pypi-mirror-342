import json

def save_config(config, config_file):
    """ Konfigürasyonu JSON dosyasına kaydeder """
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def load_config(config_file):
    """ Konfigürasyonu JSON dosyasından yükler """
    with open(config_file, 'r') as f:
        return json.load(f)
