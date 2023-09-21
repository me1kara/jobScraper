from extractors.jobkorea import extract_jobkorea_jobs

keyword = input('원하는 직업 검색하기!')

#잡코리아, 잡플래닛에서 데이터 가져옴
my_jobs = extract_jobkorea_jobs(keyword)

#쓰기모드, 덮어쓰기 모드로 파일엶
file = open(f"jobkorea.csv", "w", encoding="utf-8-sig")
file.write("Position,Company,Location,URL,Rate,Date\n")

#파일작성
for job in my_jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']},{job['rate']},{job['date']}\n")

file.close()