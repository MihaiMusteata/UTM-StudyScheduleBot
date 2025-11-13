import requests

schedule_url = 'https://fcim.utm.md/wp-content/uploads/sites/24/2025/11/orar-master-2025-2026-sem-1-anul-1_final.pdf'
schedule_filename = 'master-lessons.pdf'

exam_url = 'https://fcim.utm.md/wp-content/uploads/sites/24/2025/10/Sesiuni-de-examinare-Anul-II-sem-3-toamna_2025-2026_P2-1.pdf'
exam_filename = 'master-exams.pdf'

def download_pdf(url, filename, chunk_size=8192, timeout=10):
    try:
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
        print(f"PDF downloaded successfully to {filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF from {url}: {e}")
        return False

download_pdf(schedule_url, schedule_filename)
download_pdf(exam_url, exam_filename)