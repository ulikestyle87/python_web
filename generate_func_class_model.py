import pandas as pd


class Newsapp():

    def format_data(self, data):
        datas = {
            'url': data.get('url'),
            'funcName': data.get('funcName'),
            'method': data.get('method'),
            'params': data.get('params')
        }
        return datas

    def get_data(self):
        df_content = pd.read_excel(r'file.xlsx', sheet_name='file_name')
        # inplace为False时创建新的对象，inplace为True时不创建新对象直接在原有数据上修改
        df_content = df_content.fillna('None', inplace=False)
        data_list = [self.format_data(df_content.iloc[i, :]) for i in range(len(df_content))]
        return data_list

    # 生成模板函数
    def generate_model(self, datas):
        if datas.get('method') == 'POST':
            model = f'''
    def {datas['funcName']}(self):
        method = "{datas['method']}"
        url = "{datas['url']}"
        params = {datas['params']}
        headers = configs.GetHeaders().get_headers(method=method)
        resp = requests.request(method=method,url=url,data=json.dumps(params),headers=headers,verify=False)
        resp = json.loads(resp.text)
        print(resp)
        assert 200 == int(resp.get("code"))
        '''
        elif datas['method'] == 'GET':
            model = f'''
    def {datas['funcName']}(self):
        method = "{datas['method']}"
        url = "{datas['url']}"
        params = {datas['params']}
        headers = configs.GetHeaders().get_headers(method=method)
        resp = requests.request(method=method,url=url,params=params,headers=headers,verify=False)
        resp = json.loads(resp.text)
        print(resp)
        assert 200 == int(resp.get("code"))
                    '''
        else:
            model = ''''''
        return model

    # 生成模板类
    def generate_classmodel(self, models):
        strmodel = '\n'.join(models)

        classmodel = f'''
import requests, unittest, json, HTMLTestRunner
from config import configs


class NewsappTest(unittest.TestCase):
    {strmodel}

if __name__ == '__main__':
    report_dir = r'test.html'
    re_open = open(report_dir,'wb')
    suite = unittest.TestLoader().loadTestsFromTestCase(NewsappTest)
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=re_open,
        title=u'测试报告',
        description=u'测试详情'
    )
    # print(suite)
    runner.run(suite)
        '''
        return classmodel


if __name__ == '__main__':
    datas = Newsapp().get_data()
    models = [Newsapp().generate_model(_) for _ in datas]
    classmodel = Newsapp().generate_classmodel(models)
    with open(r'NewsappScript.py', 'w', encoding='utf8') as f:
        f.write(classmodel)


