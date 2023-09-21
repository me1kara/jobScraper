from requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#잡코리아 페이지갯수구하기 
def get_page_count(keyword) :
    base_url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}&local=I000&careerType=1%2C4&edu=3%2C0"
    response = get(base_url)
    if response.status_code != 200:
        print("can't request website")
    else : 
        soup = BeautifulSoup(response.text,"html.parser")
        item_count = soup.find('p',class_='filter-text').find('strong').string
        print(item_count)
        
        if item_count != None :
            page_count = 0
            item_c = int(item_count)
            if item_c % 20 ==0 :
                page_count = item_c/20
            else : 
                page_count = int((item_c/20)+1)
            return page_count

#잡코리아 직업 구하기
def extract_jobkorea_jobs(keyword) :
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    your_pages = int(input(f'총 {pages} 중 몇 페이지까지 원해?'))

    if your_pages>pages :
        your_pages = pages
    
    results = []
    page_list = range(your_pages)
    for page in page_list:
        url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}&local=I000&careerType=1%2C4&edu=3%2C0&tabType=recruit&Page_No={page+1}"
        response = get(url)
        if response.status_code != 200:
            print("can't request website")
        else : 
            soup = BeautifulSoup(response.text, "html.parser")
            #여기 고쳐야됨 
            jobs = soup.find_all('div',class_='list-default')
            job_list = jobs[0].find_all('li')
            for job in job_list:
                option = job.find('p',class_='option')
                company = job.select_one('.post-list-corp>a').string.replace(',',' ')
                location = option.find('span', class_='long')
                date = option.find('span', class_='date')
                link = job.select_one('.post-list-info>a')['href']
                title = job.select_one('.post-list-info>a')
                rate = get_rate(company)

                job_data = {
                    "link" : f"https://www.jobkorea.co.kr{link}",
                    "company" : company,
                    "location" : location.string.replace(',',' '),
                    "position" : title.get_text().replace('\r\n','').replace(',',' ').strip(),
                    "date" : date.string.replace(',',' '),
                    "rate" : rate
                }
                results.append(job_data)
            
    return results


        # for job_section in jobs:
        #     job_posts = job_section.find_all('li')
        #     job_posts.pop(-1)
        #     for post in job_posts:
        #         anchors = post.find_all('a')
        #         anchor = anchors[1]
        #         link = anchor['href']
        #         company, kind, region = anchor.find_all('span', class_="company")
        #         title = anchor.find('span', class_="title")
        #         job_data = {
        #             "link" : f"https://weworkremotely.com{link}",
        #             "company" : company.string.replace(',',' '),
        #             "position" : region.string.replace(',',' '),
        #             "location" : title.string.replace(',',' ')
        #         }
        #         results.append(job_data)
        # return results



#잡플래닛 점수 구하기봇
def get_rate(keyword) :
    url = f'https://www.jobplanet.co.kr/search?query={keyword}'    
    response = get(url)
    if(response.status_code != 200) :
        print('fail')
    else :
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("headless")
        options.add_argument('--log-level=3') # 브라우저 로그 레벨을 낮춤
        options.add_argument('--disable-loging') # 로그를 남기지 않음
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        coms = soup.select_one('.is_company_card')
        if coms != None :
            divs = coms.find_all('div')
            for company in divs :
                title = company.find('a',class_='tit')
                if title != None :
                    bold = title.find('b')
                    text = title.get_text()
                    if bold!=None :
                        if bold.string == keyword :
                            rate_point = company.find('span',class_='rate_ty02')                        
                            return float(rate_point.string)
                    elif text!=None :
                         print(text)
                         print(keyword)
                         text = text.replace('㈜','').replace('(주)','').strip()
                         keyword = keyword.replace('㈜','').replace('(주)','').strip()
                         if text == keyword :
                            print('일치확인')
                            rate_point = company.find('span',class_='rate_ty02')                        
                            return float(rate_point.string)
            return 0
        else:
            return 0


