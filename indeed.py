import requests
from bs4 import BeautifulSoup

LIMIT = 50  ##페이지당 불러오는 일자리 개수
URL = f"https://kr.indeed.com/취업?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

def extract_indeed_pages():
  result = requests.get(URL)

  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("ul", {"class": "pagination-list"})  ##총 페이지 개수 찾기

  links = pagination.find_all("span", {"class": "pn"})
  
  pages = []

  for link in links[0:-2]:
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page   ##페이지 최대 개수 반환

def extract_jobs(html):
  title = html.find("h2", {"class": "title"}).find("a")["title"]  ##일자리 제목
  
  company = html.find("span", {"class": "company"})   ##기업 이름
  if company:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = str(company_anchor.string)
    else:
      company = str(company.string)
    company = company.strip()
  else:
    company = None

  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]  ##기업 위치정보
  ##location = html.find("span", {"class": "location"})

  job_id = html["data-jk"]  ##일자리 정보 ID

  return {
    'title': title,
    'company': company,
    'location': location,
    'link': f"https://kr.indeed.com/채용보기?&jk={job_id}"
  }

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(extract_indeed_pages()):
    print(f"indeed {page + 1}페이지에서 일자리 긁어오는 중...")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

    for result in results:
      jobs.append(extract_jobs(result))
  return jobs

def get_jobs():
  jobs = extract_indeed_jobs(extract_indeed_pages())
  return jobs