from requests_html import HTMLSession
import re
import os
session = HTMLSession()


class BQBspider(object):
    save_path = os.getcwd() + '/表情包/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    def __init__(self):
        self.url = 'https://adoutu.com/picture/list/{}'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        self.page = int(input('请输入爬取的表情页数/总共2777页，每页20个表情/:')) + 1

    def parse_request_url(self):
        for page in range(1, self.page):
            request_url = self.url.format(page)
            response = session.get(url=request_url, headers=self.headers)
            self.parse_response(response, page)

    def parse_response(self, response, page):
        html = response.content.decode()
        result_list = re.findall(r'<img.*?src="(.*?)".*?title="(.*?)"/>', html)
        for result in result_list:
            data = session.get(result[0]).content
            title = result[1] + result[0][-8:]
            self.save_data(data, title)

    def save_data(self, data, title):
        with open(self.save_path + title, 'wb') as f:
            f.write(data)
            print(f"{title}----保存完成---")


if __name__ == '__main__':
    B = BQBspider()
    B.parse_request_url()
