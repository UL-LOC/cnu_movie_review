# Naver Movie에서 한 영화의리뷰를 페이지를 반복 돌면서
# 모든 리뷰를 수집하는 코드 작성

import math
import requests
from bs4 import BeautifulSoup

page = 1 # Start Page
count = 0 # Total Review Count

url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=206657&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1'
result = requests.get(url)
doc = BeautifulSoup(result.text, 'html.parser')
all_count = doc.select('strong.total > em')[0].get_text()
page = math.ceil(int(all_count) / 10)

for page in range(1, page+1):
    new_url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=206657&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={}'.format(page)

    # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    result = requests.get(new_url)
    doc = BeautifulSoup(result.text, 'html.parser')

    review_list = doc.select('div.score_result > ul > li')

    for one in review_list:
        count += 1
        print('## USER -> {} #####################################################################'.format(count))

        # 평점 정보 수집
        score = one.select('div.star_score > em')[0].get_text()

        # 리뷰 정보 수집
        review = one.select('div.score_reple > p > span')[-1].get_text().strip()

        # 작성자(닉네임) 정보 수집
        original_writer = one.select('div.score_reple dt em')[0].get_text().strip()

        idx_end = original_writer.find('(')
        writer = original_writer[:idx_end]

        # 날짜 정보 수집
        original_date = one.select('div.score_reple dt em')[1].get_text()
        date = original_date[:10] # yyyy.MM.dd 전처리 코드 작성

        print(':: REVIEW -> {}'.format(review))
        print(':: WRITER -> {}'.format(writer))
        print(':: SCORE -> {}'.format(score))
        print(':: DATE -> {}'.format(date))