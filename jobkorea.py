import requests
from bs4 import BeautifulSoup

URL = f"http://www.jobkorea.co.kr/Search/?stext=python&tabType=recruit"

def get_last_page():
  result = requests.get(URL)

  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("span", {"class": "pgTotal"}).string

  return int(pagination)

def extract_jobs(html):

  title = html.find("div", {"class": "post-list-info"}).find("a")  ##일자리 제목
  if title:
    title = title.get_text(strip = True)
  else:
    return 

  company = html.find("div", {"class": "post-list-corp"}).find("a")["title"]
  if company:
    company = company
  else:
    return

  location = html.find("div", {"class": "post-list-info"}).find("span", {"class": "loc long"})
  if location:
    location = location.string
  else:
    return

  job_id = html.find("div", {"class": "post-list-info"}).find("a")["href"]

  return {
    'title': title,
    'company': company,
    'location': location,
    'link': f"http://www.jobkorea.co.kr/{job_id}"
  }

def extract_jobkorea_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"JobKorea {page + 1}페이지에서 일자리 긁어오는 중...")

    result = requests.get(f"{URL}&Page_No={page + 1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "list-post"})

    for result in results:
      jobs.append(extract_jobs(result))

  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobkorea_jobs(last_page)
  return jobs