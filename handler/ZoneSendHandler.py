# -*- coding: utf-8 -*-

from pyrestful.rest import post
from pyrestful import mediatypes
from pyrestful.rest import RestHandler
from log import logger
import traceback
from database import make_mysql_session
from modals import *
import urllib, time, re
from selenium import webdriver


class ZoneSendHandler(RestHandler):
    """
    QQ空间说说发送 handler
    """
    class ReceivedZoneSend:
        get_content = str

    @post(_path="/api/zoneSend/", _types=[ReceivedZoneSend], _consumes=mediatypes.APPLICATION_JSON, _produces=mediatypes.APPLICATION_JSON)   
    def zoneSend(self, ReceivedZoneSend):
        """
        QQ空间说说发送 handler
        """
        sendContent=ReceivedZoneSend.content
        qq_num = "2804505287"
        qq_psw = "*************"

        res = make_request(qq_num,qq_psw,sendContent)
        
        print (res)


        return {"res": ReceivedZoneSend.content}
    """
        get_content = received_feedback.get_content
        if DEVELOPMENG:
            self.set_secure_cookie("qq", str(2972822179))
        mysql_session = make_mysql_session()
        qq = self.get_secure_cookie("qq")
        if qq is None:
            return {"res": 1}
        logger.info(str(qq) + " send feedback")
        try:
            new_feedback = FeedbackModal(getContent=get_content,
                                         getPersonQQ=qq,
                                         getTime=int(time.time()),
                                         subType=0)
            mysql_session.add(new_feedback)
            mysql_session.commit()
            feedback = mysql_session.query(FeedbackModal).filter(
                FeedbackModal.getContent == get_content).first()
        except Exception as e:
            # logger.error(e.message)
            logger.error(traceback.format_exc())
            mysql_session.rollback()
            return {"res": 1}
        else:
            return {"res": 0, "data": feedback.make_response()}
        finally:
            mysql_session.close()

        except Exception as e:
            logger.error(traceback.format_exc())
            # logger.error(e.message)
            response = {
                "code": 500,
                "message": "Internal Server Error",
                "errors": {
                    "code": 5001,
                    "message": "MySQL Server Error"
                },
                "relationships": {
                    "author": "MLT"
                },
                "jsonapi": {
                    "version": "1.0"
                }
            }
            return response
        """

    def get_cookie(qq_num,qq_psw):
        url = 'http://user.qzone.qq.com/'
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)

        #切换到登录的frame上
        driver.switch_to.frame('login_frame')
        time.sleep(3)
        #点击“帐号密码登录”按钮
        driver.find_element_by_id('switcher_plogin').click()
        #定位帐号输入框
        
        time.sleep(3)
        username = driver.find_element_by_id('u')
        #清空帐号输入框内容
        
        time.sleep(2)
        username.clear()
        #填写帐号

        time.sleep(5)
        username.send_keys(qq_num)

        
        time.sleep(2)
        password = driver.find_element_by_id('p')

        time.sleep(3)
        password.clear()
        
        time.sleep(5)
        password.send_keys(qq_psw)
        #点击“登录”按钮
        
        time.sleep(2)
        driver.find_element_by_id('login_button').click()

        time.sleep(50)
        getCookie=driver.get_cookies()
        pageSource = driver.page_source
        driver.quit()
        return getCookie,pageSource
    

    def make_g_tk(p_skey):
        tk = 5381
        for c in p_skey:
            tk += (tk<<5) + ord(c)
        tk &= 0x7fffffff
        return tk

    def make_cookie(getCookie):
        for i in getCookie:
            if i['name']=='Loading':
                Loading = i['value']
            if i['name']=='ptcz':
                ptcz = i['value']
            if i['name']=='pgv_pvid':
                pgv_pvid = i['value']
            if i['name']=='ptisp':
                ptisp = i['value']
            if i['name']=='p_uin':
                p_uin = i['value'] 
            if i['name']=='pgv_info':
                pgv_info = i['value']
            if i['name']=='_qpsvr_localtk':
                _qpsvr_localtk = i['value']
            if i['name']=='pgv_pvi':
                pgv_pvi = i['value']
            if i['name']=='ptui_loginuin':
                ptui_loginuin = i['value']
            if i['name']=='pgv_si':
                pgv_si = i['value']
            if i['name']=='RK':
                RK = i['value']
            if i['name']=='uin':
                uin = i['value']
            if i['name']=='skey':
                skey = i['value']
            if i['name']=='pt2gguin':
                pt2gguin = i['value']
            if i['name']=='pt4_token':
                pt4_token = i['value'] 
            if i['name']=='p_skey':
                p_skey = i['value']
            if i['name']=='qz_screen':
                qz_screen = i['value']
        return 'zzpaneluin=; zzpanelkey=; _qpsvr_localtk='+str(_qpsvr_localtk)+'; pgv_pvi='+str(pgv_pvi)+'; pgv_si='+str(pgv_si)+'; ptui_loginuin='+str(ptui_loginuin)+'; ptisp='+str(ptisp)+'; RK='+str(RK)+'; ptcz='+str(ptcz)+'; uin='+str(uin)+'; skey='+str(skey)+'; pt2gguin='+str(pt2gguin)+'; p_uin='+str(p_uin)+'; pt4_token='+str(pt4_token)+'; p_skey='+str(p_skey)+'; Loading='+str(Loading)+'; qz_screen='+str(qz_screen)+'; pgv_pvid='+str(pgv_pvid)+'; pgv_info=ssid='+str(pgv_info)+'; QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=0'

    def make_url(getCookie,pageSource):
        for i in getCookie:
            if i['name']=='p_skey':
                p_skey = i['value']
                break
        g_tk = make_g_tk(p_skey)
        #print(g_tk)
        
        qzonetoken_r = r'{ try{return "(.*)";} catch'
        pattern2 = re.compile(qzonetoken_r)
        matcher2 = re.search(pattern2,pageSource)
        qzonetoken = matcher2.group(1)
        #print(qzonetoken)

        url='https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6?g_tk='+str(g_tk)+'&qzonetoken='+str(qzonetoken)
        return url

    def make_request(qq_num,qq_psw,sendContent):
        getCookie,pageSource = get_cookie(qq_num,qq_psw)
        
        data = bytes(urllib.parse.urlencode(
            {
                "code_version":"1",
                "con":sendContent,
                "feedversion":"1",
                "format":"fs",
                "hostuin":qq_num,
                "paramstr":"1",
                "pic_template":"",
                "qzreferrer":"https://user.qzone.qq.com/"+qq_num,
                "richtype":"",
                "richval":"",
                "special_url":"",
                "subrichtype":"",
                "syn_tweet_verson":"1",
                "to_sign":"0",
                "ugc_right":"1",
                "ver":"1",
                "who":"1"
            }
        ), encoding='utf8')  
        UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'    

        request =urllib.request.Request(
            make_url(getCookie,pageSource),
            data=data,
            headers={
                'Cookie':make_cookie(getCookie),
                'User-Agent': UA},
            method='POST'
        ) 
        response = urllib.request.urlopen(request)
        content = response.read()#当该语句读取的返回值是bytes类型时，要将其转换成utf-8才能正常显示在python程序中
        print(content.decode('utf-8'))#需要进行类型转换才能正常显示在python中
        return response.status