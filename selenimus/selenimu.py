import os
import os.path
import re
import time
import sys

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from loggings import Loggingyaml
from yamls import Selenimu_Yaml

logs=Loggingyaml().loggerin()

class webdrivers(object):
    def __init__(self,webbrowser):
        self.webbrowser=webbrowser
        self.default_yaml=Selenimu_Yaml().file_judge

    #加载配置
    def evns_infos(self):
        try:
            Environment=self.default_yaml['Environment']
            return Environment
        except BaseException as be:
            logs.error(be)
            logs.error('配置未正确，已退出。请确认配置后运行')
            sys.exit(0)

    @property
    def starts(self):
        yamls=self.evns_infos()
        for i in range(0,len(yamls)):
            env=list(yamls.keys())[i]
            env_infos=yamls[env]
            self.webseleimus(env,env_infos)

    #关闭
    @property
    def close(self):
        if self.webbrowser=='-c':
            return self.chrome_webseleimus().close()
        elif self.webbrowser=='-s':
            return self.safari_webseleimus().close()

    def directory(self):
        floder=r'./Screenshots'
        isExists=os.path.exists(floder)
        if not isExists:
            try:
                os.mkdir(floder)
            except BaseException as be:
                logs.error(be)
        return floder

    def webseleimus(self,env,infos):
        if self.webbrowser=='-c':
            drivers=self.chrome_webseleimus()
        elif self.webbrowser=='-s':
            drivers=self.safari_webseleimus()
        
        try:
            drivers.get(infos['Https'])
        except BaseException as be:
            logs.error('网址参数错误。%s ',(be))
            logs.info('执行关闭退出')
            drivers.close()
            return None
        
        #键入用户名和密码
        try:
            username=drivers.find_element_by_name('username')
            username.send_keys(userinfo['name'])
            password=drivers.find_element_by_id('inputPassword')
            password.send_keys(userinfo['pw'])
            drivers.find_element_by_id('inputPassword').send_keys(Keys.ENTER)

            time.sleep(5)
        except BaseException as be:
            logs.error('selenium.common.exceptions.NoSuchElementException:%s,未能找到相关页面元素，只截当前图',be)

        #设置大小
        width=drivers.execute_script('return document.documentElement.scrollWidth')
        height=drivers.execute_script('return document.documentElement.scrollHeight')
        drivers.set_window_size(width,height)
        time.sleep(1)

        times=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    
        directorys=self.directory()

        scren=r'%s/%s-%s.png' % (directorys,env,times)
        logs.info('已获取截图:%s',scren)
        drivers.save_screenshot(scren)
        # drivers.get_screenshot_as_file(abc)
        drivers.close()    
        
    #chrome模式
    def chrome_webseleimus(self):
        # chrome模式
        chromedriver_path=r'./chromedriver'
        chromedriver=r'./chromedriver/chromedriver'
        if not os.path.exists(chromedriver_path):
            try:
                os.mkdir(chromedriver_path)
            except BaseException as be:
                logs.error(be)
        if  not os.path.exists(chromedriver):
            logs.info('未发现Chrome驱动，并确保存在chromedriver目录下且名为chromedriver')
            return None

        #无界面模式
        chrome_options=Options()
        chrome_options.add_argument('headless')
        drivers=webdriver.Chrome(chromedriver,chrome_options=chrome_options)

        return drivers

    #safari模式
    def safari_webseleimus(self):
        drivers=webdriver.Safari()
        return drivers

# try:
# webdrivers(webbrowser='-s').starts
# except BaseException as be:
#     logs.error(be)