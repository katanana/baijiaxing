import pymysql
import requests
from lxml import etree
import json


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_first_name(html):
    etree_html=etree.HTML(html)
    all_first_name=etree_html.xpath('/html/body/div[3]/div/div/div[2]/a')
    surname_dict={}
    for item in all_first_name:
        surname_list=[]
        first_name_value=item.xpath('.//@href')[0]
        first_name=item.xpath('.//text()')[0]
        first_name1=str(first_name).split('姓名')[0]
        # surname_list.append(first_name_value)
        # surname_list.append(first_name1)
        surname_dict[first_name1]=first_name_value
    # print(surname_dict)
    with open('./surname.json','w',encoding='utf8')as f:
        json_file=json.dumps(surname_dict,ensure_ascii=False)
        f.write(json_file)
    return surname_dict


def parse_name(html):
    etree_html = etree.HTML(html)
    all_name=etree_html.xpath('/html/body/div[3]/div[2]/div[1]/div/a')
    name_dict = {}
    for item in all_name:
        name=item.xpath('.//text()')[0]
        name_url=item.xpath('.//@href')[0]
        name_dict[name]=name_url
    return name_dict


def insert_name(db,cursor,k,m,n):
    sql='insert into baijia(surname,name,name_url) value ("%s","%s","%s")' % (k,m,n)
    cursor.execute(sql)
    db.commit()




def main():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8',
                         database='baijiaxing')
    cur = db.cursor()
    url='http://www.resgain.net/xmdq.html'
    html=get_one_page(url)
    surname_dict=parse_first_name(html)
    for k,v in surname_dict.items():
        i=1
        for _ in range(10):
            list1=str(v).split('/')
            list2=list1[3].split('.')[0]
            url1='http://'+list1[2]+'/'+list2+'_'+str(i)+'.html'
            i +=1
            surname_html=get_one_page(url1)
            name_dict=parse_name(surname_html)
            print(name_dict)
            for m,n in name_dict.items():
                insert_name(db,cur,k,m,n)





if __name__ == '__main__':
    main()