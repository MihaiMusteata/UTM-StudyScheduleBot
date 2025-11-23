from abc import ABC, abstractmethod

import requests


class PDFDownloader(ABC):

    def download(self):
        url = self.get_url()
        filename = self.get_filename()

        if not self.before_download(url):
            print("before_download blocked the process.")
            return False

        print(f"Downloading from {url} ...")
        ok = self._do_download(url, filename)

        if ok:
            self.after_download(filename)

        return ok

    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_filename(self) -> str:
        pass

    def before_download(self, url: str) -> bool:
        return True

    def after_download(self, filename: str):
        print(f"File saved as {filename}")

    def _do_download(self, url: str, filename: str, chunk_size=8192, timeout=10):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
            print(f"PDF downloaded successfully -> {filename}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF: {e}")
            return False