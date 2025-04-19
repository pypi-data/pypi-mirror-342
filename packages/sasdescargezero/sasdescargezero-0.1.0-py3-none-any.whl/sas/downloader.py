import requests
from bs4 import BeautifulSoup
import os
import time
import base64
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SASDownloader:
    HOST = base64.b64decode(b"aHR0cHM6Ly9jaWVuY2ltZWQuc2xkLmN1L2luZGV4LnBocC9jaWVuY2ltZWQ=").decode("utf-8")
    USERNAME = base64.b64decode(b"cmV2aXQwMDEw").decode("utf-8")
    PASSWORD = base64.b64decode(b"1YhHZXJvMTIz").decode("utf-8")
    
    def __init__(self):
        self.session = requests.Session()
        self.total_downloaded = 0
        self.start_time = 0
        self.current_file = "INDEFINIDO"
        self.directory = "./SASDownloads"
        self._initialize_session()

    def _initialize_session(self):
        """Inicializa la sesión autenticándose en el host."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
        }
        try:
            response = self.session.get(f"{self.HOST}/login", headers=headers, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            token = soup.find('input', {'name': 'csrfToken'})['value']
            login_data = {
                "password": self.PASSWORD,
                "remember": 1,
                "source": "",
                "username": self.USERNAME,
                "csrfToken": token
            }
            login_response = self.session.post(f"{self.HOST}/login/signIn", data=login_data, headers=headers, verify=False)
            if login_response.status_code != 200:
                raise Exception("Fallo en el login")
        except Exception as e:
            print(f"\033[31mError durante el login: {e}\033[0m")
            sys.exit(1)

    def sizeof_fmt(self, num, suffix='B'):
        """Formatea el tamaño del archivo en un formato legible."""
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return f"{num:3.2f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.2f}Yi{suffix}"

    def clear_console(self):
        """Limpia la consola."""
        os.system("clear" if os.name == "posix" else "cls")

    def download_file(self, url, name, total_size):
        """Descarga un archivo desde la URL proporcionada."""
        downloaded = 0
        try:
            with self.session.get(url, headers={"User-Agent": "Mozilla/5.0"}, stream=True) as r:
                r.raise_for_status()
                with open(name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            downloaded += 8192
                            self.total_downloaded += 8192
                            percentage = (self.total_downloaded / int(total_size)) * 100
                            elapsed = round(time.time() - self.start_time)
                            spaces = 17
                            rest = 100 / spaces
                            bar = f"  \033[32m|\033[0m\033[1m\033[30m\033[42m•{round(percentage/rest)}\033[40m•{round((100-percentage)/rest)}\033[0m\033[1m {percentage:.1f}% | {self.sizeof_fmt(self.total_downloaded)}     "
                            print(bar, end="\r")
                            f.write(chunk)
        except Exception as e:
            print(f"\n  \033[31m\033[1m|\033[41m\033[30m\033[1m + ERROR - CONEXIÓN PERDIDA + \033[0m: {e}")
            sys.exit(1)

    def process_urls(self, urls):
        """Procesa y descarga archivos desde las URLs proporcionadas."""
        if self.directory and not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        urls = urls.replace(" ", "_").split("_&&_")
        for url in urls:
            self.clear_console()
            print("  \033[1m\033[33m|\033[30m\033[43m + PREPARANDO + \033[0m")
            self.current_file = url.split("/")[-1]
            surl = url.split("/")[-4]
            key = url.split("/")[-2].split("-")
            repo = base64.b64decode(key[3].replace("@", "==").replace("#", "=")).decode("utf-8")
            size = url.split("/")[-5].split("-")[0]
            ide = url.split("/")[-5].split("-")[1]
            bitzero = url.split("/")[-3]

            url_list = surl.split("-") if "-" in surl else [surl]
            download_urls = [f"{self.HOST}/$$$call$$$/api/file/file-api/download-file?submissionFileId={u}&submissionId={repo}&stageId=1" for u in url_list]

            self.start_time = time.time()
            self.clear_console()
            display_name = self.current_file[:7] + "..." if len(self.current_file) > 10 else self.current_file
            print(f"  \033[32m|\033[0m\033[1m\033[42m\033[30m + DESCARGANDO + \033[0m {display_name} | {self.sizeof_fmt(int(size))}")

            files = []
            for idx, dl_url in enumerate(download_urls):
                if dl_url:
                    temp_file = f"index_{ide}_{idx}"
                    self.download_file(dl_url, temp_file, size)
                    files.append(temp_file)

            print("\n")
            output_path = os.path.join(self.directory, self.current_file)
            with open(output_path, "wb") as outfile:
                for f in files:
                    with open(f, "rb" if bitzero == '1' else "r") as infile:
                        if bitzero == '1':
                            data = infile.read().replace(
                                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82",
                                b''
                            )
                        elif bitzero == '2':
                            data = base64.b64decode(infile.read().replace('<!DOCTYPE html>\n<html lang="es">\n<bytes>', '').replace('</bytes></html>', ''))
                        outfile.write(data)
                    os.unlink(f)

            self.clear_console()
            print(f"\033[32mGUARDADO:\033[0m {output_path}")
            self.total_downloaded = 0
