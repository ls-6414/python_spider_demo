import re
from requests_html import HTMLSession
session = HTMLSession()
from lxml import etree
import pandas as pd


class WZRY_Spider(object):

    def __init__(self):
        self.start_url = 'https://pvp.qq.com/web201605/herolist.shtml'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    def get_request(self):
        response = session.get(self.start_url, headers=self.headers).content.decode('gbk')
        hero_detail_rule = re.compile(r'<a href="herodetail/(\d*).shtml" target="_blank">')
        hero_detail_list = re.findall(hero_detail_rule, response)
        hero_unfinished_url = 'https://pvp.qq.com/web201605/herodetail/{}.shtml'
        for hero_id in hero_detail_list:
            hero_detail_url = hero_unfinished_url.format(hero_id)
            hero_detail_response = session.get(hero_detail_url).content.decode('gbk')
            self.parse_response(hero_detail_response)
            break

    def parse_response(self, hero_detail):
        hero_name_rule = re.compile('<h2 class="cover-name">(.*?)</h2>')
        hero_name_list = re.findall(hero_name_rule, hero_detail)[0]
        dom = etree.HTML(hero_detail)
        hero_skill_name_list = dom.xpath('//p[@class="skill-name"]/b/text()')
        hero_skill_desc_list = dom.xpath('//p[@class="skill-desc"]/text()')

        passive_skill_name = hero_skill_name_list[0]
        passive_skill_desc = hero_skill_desc_list[0]
        passive_skill = passive_skill_name + "----" + passive_skill_desc

        skill_one_name = hero_skill_name_list[1]
        skill_one_desc = hero_skill_desc_list[1]
        skill_one = skill_one_name + "----" + skill_one_desc

        skill_two_name = hero_skill_name_list[2]
        skill_two_desc = hero_skill_desc_list[2]
        skill_two = skill_two_name + "----" + skill_two_desc

        skill_three_name = hero_skill_name_list[3]
        skill_three_desc = hero_skill_desc_list[3]
        skill_three = skill_three_name + "----" + skill_three_desc

        columns = ['英雄', '被动', '技能1', '技能2', '技能3']
        save_list = []
        b = save_list.append([hero_name_list, passive_skill, skill_one, skill_two, skill_three])
        self.save_data(save_list, columns)

    def save_data(self, save_list, columns):
        final_content = pd.DataFrame(save_list, columns=columns)
        print(final_content)
        final_content.to_excel("王者荣耀英雄与技能.xlsx", index=False)


if __name__ == '__main__':
    W = WZRY_Spider()
    W.get_request()
