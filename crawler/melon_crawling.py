## 크롤링 코드

import requests
from bs4 import BeautifulSoup
import json
import time
import os

# 멜론 차트 100을 크롤링 하는 함수
# 타입힌팅 : 해당 변수의 데이터타입을 지정 

def crawl_melon_chart(url : str) -> list[dict] :
    
    # 브라우저 헤더 설정 (멜론은 User-Agent 체크함)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    # 웹페이지 요청
    response = requests.get(url,headers=headers)
    print(response)
    
    # 데이터 추출(파싱)
    soup = BeautifulSoup(response.content, 'lxml')

    # id,순위,제목,가수,앨범

    song_row_tags = soup.select('tbody tr')
    
    # 차트 데이터
    chart_data = []

    for row_tags in song_row_tags:
    
        # id 추출
        id = int(row_tags.get('data-song-no'))

        # 순위 추출
        rank_tag = row_tags.select_one('.rank')
        rank = int(rank_tag.text.strip())

        # 곡명 추출
        title_tag = row_tags.select_one('.ellipsis.rank01 a')
        title = title_tag.text.strip() if title_tag else "정보 없음"

        # 가수 추출
        artist_tags = row_tags.select(".ellipsis.rank02 > a")
        if artist_tags:
            # 여러 아티스트가 있을 경우 쉼표로 연결
            artists = [tag.text.strip() for tag in artist_tags]
            artist = ", ".join(artists)
        else:
            artist = "정보 없음"        

        # 앨범명 추출
        album_tag = row_tags.select_one('.ellipsis.rank03 a')
        album = album_tag.text.strip() if album_tag else '정보 없음'

        # 데이터 가공
        song_info = {
                    "id": int(id) if id else 0,
                    "rank": int(rank) if rank else 0,
                    "title": title,
                    "artist": artist,
                    "album": album,}

        chart_data.append(song_info)
    
    return chart_data

# 데이터를 json 파일로 저장하는 함수
def save_to_json(data, filename="melon_chart_top100.json"):

    # 실행 위치 (터미널에서 실행한 폴더)
    base_dir = os.getcwd()
    
    # app 폴더 (없으면 생성)
    data_dir = os.path.join(base_dir, "app","data")
    os.makedirs(data_dir, exist_ok=True)

    # 파일 경로
    file_path = os.path.join(data_dir, filename)
    
    '''

    # 현재 파일 위치
    current_dir = os.path.dirname(__file__)  # crawler 폴더

    # 프로젝트 루트
    project_root = os.path.dirname(current_dir)  # playlist-api 폴더

    # data 폴더 경로
    data_dir = os.path.join(project_root, "app", "data")

    # 폴더 생성
    os.makedirs(data_dir, exist_ok=True)

    # 파일 경로
    file_path = os.path.join(data_dir, filename)

    '''

    # 파일 생성
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 파일 저장 완료: {file_path}")
    except Exception as e:
        print(f"❌ JSON 파일 저장 실패: {e}")
    


if __name__ == '__main__':

    # 멜론 차트 크롤링
    melon_chart = crawl_melon_chart('https://www.melon.com/chart/index.htm')
    
    # JSON 파일로 저장
    if melon_chart:
        save_to_json(melon_chart)
    else:
        print("❌ 크롤링 실패! 데이터를 수집하지 못했습니다.")

    print(f'갯수: {len(melon_chart)}')
    print(melon_chart[:1])