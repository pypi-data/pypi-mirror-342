import os
import shutil

class ModLoader:
    def __init__(self, mod_directory):
        self.mod_directory = mod_directory

    def install_mod(self, mod_path):
        """ Mod yükler """
        try:
            # Mod dosyasını hedef klasöre kopyalar
            if os.path.exists(mod_path):
                shutil.copytree(mod_path, os.path.join(self.mod_directory, os.path.basename(mod_path)))
                print(f"Mod başarıyla yüklendi: {mod_path}")
            else:
                print("Mod dosyası bulunamadı.")
        except Exception as e:
            print(f"Mod yüklenirken hata oluştu: {str(e)}")

    def list_installed_mods(self):
        """ Yüklenen modları listeler """
        mods = os.listdir(self.mod_directory)
        print("Yüklenen modlar:")
        for mod in mods:
            print(mod)
