import copy
import json
import os
import requests
import re
import csv


def sort_by_date(item):
    year_month = item['date']
    year, month = map(int, year_month.split('-'))
    return (year, month)


class TiobeSpider(object):
    def __init__(self):
        self.url = 'https://www.tiobe.com/tiobe-index/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36 Edg/81.0.416.58',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.table = 'test.csv'
        self.tablenew = 'data.csv'

    def run(self):
        response = requests.get(self.url, headers=self.headers)
        text = response.text
        # with open('test', 'w') as f:
        #     json.dump(text, f)
        total_content = ''.join(re.findall(r'series: (.*?)\}\);', text, re.DOTALL))  # re.DOTALL匹配到多行，包含换行符
        total_content = re.findall(r'({.*?})', total_content, re.DOTALL)

        # table 用于中间处理，tablenew 用于最终处理
        with open(self.table, 'w', newline='') as f, open(self.tablenew, 'w', newline='') as fnew:
            self.write = csv.DictWriter(f, ['date', 'value', 'name'])
            self.write.writeheader()
            self.writenew = csv.DictWriter(fnew, ['date', 'Python', 'C', 'C++', 'Java', 'C#', 'JS', 'Go', 'VB', 'SQL', 'Fortran'])
            self.writenew.writeheader()
            sum_data = []  # 存储字典数据的列表
            for content in total_content:
                name = ''.join(re.findall(r"{name : '(.*?)'", content, re.DOTALL))
                if name == 'Visual Basic':
                    name = 'VB'
                elif name == 'JavaScript':
                    name = 'JS'
                data = re.findall(r"Date.UTC(.*?)\]", content, re.DOTALL)
                for i in data:
                    i = i.replace(' ', '')  # 去掉空格
                    i = re.sub(r'[()]', '', i)  # 将小括号匹配为空
                    value = i.split(',')[-1]
                    date_list = i.split(',')[:2]

                    time = ''
                    for index, j in enumerate(date_list):
                        if index != 0:
                            if j == '0':
                                j = '12'
                            if len(j) == 1:
                                j = '0' + j
                            time = time + '-' + j
                        else:
                            time = time + j
                    dict_data = {'date': time, 'value': value, 'name': name}
                    if dict_data['date'] == '2024-12':
                        dict_data['date'] = '2023-12'
                    sum_data.append(dict_data)
            sum_data.sort(key=lambda item: item['date'])

            real_data = []
            real_dict = {}
            for i in range(len(sum_data)-1):
                cur = sum_data[i]['date']
                next = sum_data[i+1]['date']
                key = sum_data[i]['name']
                if cur == next:
                    real_dict['date'] = sum_data[i]['date']
                    if real_dict['date'] == '2024-03':
                        break
                    real_dict[key] = sum_data[i]['value']
                else:
                    real_dict[key] = sum_data[i]['value']
                    if real_dict.get('Go') is None:
                        real_dict['Go'] = '0'
                    if real_dict.get('VB') is None:  # 如果是空赋值为0
                        real_dict['VB'] = '0'

                    new_dict = copy.deepcopy(real_dict)  # 使用深拷贝解决字典可变的问题
                    real_data.append(new_dict)
            # print(real_data)
            for row in sum_data:  # 产生test.csv
                self.write.writerow(row)
            for row in real_data:
                self.writenew.writerow(row)
        os.remove('./test.csv')  # 删除中间文件
        print('爬取完成')


if __name__ == '__main__':
    tiobe = TiobeSpider()
    tiobe.run()