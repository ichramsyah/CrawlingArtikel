import requests
from bs4 import BeautifulSoup
import pandas as pd

# Ambil halaman web utama
url = 'https://ojs.unud.ac.id/index.php/jik/issue/view/5014'
response = requests.get(url)

# Cek apakah halaman berhasil diakses
if response.status_code == 200:
    print("Halaman berhasil diakses")
else:
    print("Terjadi kesalahan dalam mengakses halaman")

# Parsing halaman web
soup = BeautifulSoup(response.text, 'html.parser')

# Ambil semua artikel
articles = soup.find_all('div', class_='obj_article_summary')

# Siapkan list kosong untuk menyimpan data
data = []

# Loop untuk mengambil setiap artikel
for article in articles:
    # Cek apakah elemen title ada
    title_tag = article.find('div', class_='title').find('a')
    title = title_tag.text.strip() if title_tag else 'No title found'

    title = f"Judul: {title}"

    # Cek apakah elemen authors ada
    authors_tag = article.find('div', class_='authors')
    authors = authors_tag.text.strip() if authors_tag else 'No authors found'
    
    authors = f"Penulis: {authors}"

    # Cek apakah link DOI ada
    doi_link_tag = article.find('a', href=True)
    doi_link = doi_link_tag['href'] if doi_link_tag else None

    # Ambil abstrak dari halaman DOI jika ada link DOI
    abstract = 'No abstract found'
    if doi_link:
        doi_response = requests.get(doi_link)
        if doi_response.status_code == 200:
            doi_soup = BeautifulSoup(doi_response.text, 'html.parser')
            abstract_tag = doi_soup.find('div', class_='item abstract').find('p')
            abstract = abstract_tag.text.strip() if abstract_tag else 'No abstract found'

        abstract = f"Abstrak: {abstract}"

    # Simpan ke list
    data.append([title, authors, abstract])

# Buat DataFrame dari list data
df = pd.DataFrame(data, columns=['Judul Artikel', 'Nama Penulis', 'Abstrak'])

# Simpan ke CSV
df.to_csv('hasil crawl oleh ichram.csv', index=False)

print("Data berhasil disimpan ke CSV")
