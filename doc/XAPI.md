# 现有XAPI接口

## basic_tool 基础工具接口

 ❏ | Name          | Method | Address
---|---------------|--------|---------
 √ | 词库          | GET    | [https://xapi.seuxw.cn:8895/basicTool/lexiconD?key=](https://xapi.seuxw.cn:8895/basicTool/lexiconD?key=)

## stu 学生相关接口

### stu_info 学生信息接口

 ❏ | Name          | Method | Address
---|---------------|--------|---------
 √ | 课表查询       | GET    | [https://xapi.seuxw.cn:8895/stu/stuInfo/courseTableAllL?cardno=](https://xapi.seuxw.cn:8895/stu/stuInfo/courseTableAllL?cardno=)
 √ | 跑操查询       | GET    | [https://xapi.seuxw.cn:8895/stu/stuInfo/paocaoD?cardno=](https://xapi.seuxw.cn:8895/stu/stuInfo/paocaoD?cardno=)

## translate 转换接口

 ❏ | Name         | Method | Address
---|--------------|--------|--------
 √ | 一卡通转QQ    | GET    | [https://xapi.seuxw.cn:8895/translate/cardnoToQqD?cardno=](https://xapi.seuxw.cn:8895/translate/cardnoToQqD?cardno=)
 √ | 一卡通转学号  | GET    | [https://xapi.seuxw.cn:8895/translate/cardnoToStuidD?cardno=](https://xapi.seuxw.cn:8895/translate/cardnoToStuidD?cardno=)
 √ | QQ转一卡通    | GET    | [https://xapi.seuxw.cn:8895/translate/qqToCardnoD?qq=](https://xapi.seuxw.cn:8895/translate/qqToCardnoD?qq=)
 √ | 学号转一卡通  | GET    | [https://xapi.seuxw.cn:8895/translate/stuidToCardnoD?stuid=](https://xapi.seuxw.cn:8895/translate/stuidToCardnoD?stuid=)
 √ | QQ转身份信息  | GET    | [https://xapi.seuxw.cn:8895/translate/qqToInfoD?qq=](https://xapi.seuxw.cn:8895/translate/qqToInfoD?qq=)
 √ | 姓名转身份信息 | GET    | [https://xapi.seuxw.cn:8895/translate/nameToInfoL?name=&page=&pagesize=](https://xapi.seuxw.cn:8895/translate/nameToInfoL?name=&page=&pagesize=)

## user 用户相关接口

### signin 签到接口

 ❏ | Name          | Method | Address
---|---------------|--------|---------
 √ | 用户签到       | POST   | [https://xapi.seuxw.cn:8895/user/signin/signinD?qq=](https://xapi.seuxw.cn:8895/user/signin/signinD?qq=)
 √ | 查询签到分数   | GET    | [https://xapi.seuxw.cn:8895/user/signin/signinScoreD?qq=](https://xapi.seuxw.cn:8895/user/signin/signinScoreD?qq=)

### user_info 用户信息接口

 ❏ | Name          | Method | Address
---|---------------|--------|---------
 √ | 查询用户昵称   | GET    | [https://xapi.seuxw.cn:8895/user/userInfo/nicknameD?qq=](https://xapi.seuxw.cn:8895/user/userInfo/nicknameD?qq=)
 √ | 修改用户昵称   | POST   | [https://xapi.seuxw.cn:8895/user/userInfo/alterNicknameD?qq=&nickname=](https://xapi.seuxw.cn:8895/user/userInfo/alterNicknameD?qq=&nickname=)
 √ | 用户注册       | POST   | [https://xapi.seuxw.cn:8895/user/userInfo/registD?qq=&nickname=](https://xapi.seuxw.cn:8895/user/userInfo/registD?qq=&nickname=)

## 物品丢失状态接口 basic_tool

 ❏ | Name          | Method | Address
---|---------------|--------|---------
 X | 一卡通丢失状态 | GET    | [https://xapi.seuxw.cn:8895/cardStatus/{cardNo}](https://xapi.seuxw.cn:8895/cardStatus/{cardNo})

## 发送接口

 ❏ | Name          | Method | Address
---|---------------|--------|---------
 X | QQ空间说说发送 | POST   | [https://xapi.seuxw.cn:8895/zoneSend/](https://xapi.seuxw.cn:8895/zoneSend/)
 X | QQ邮箱发送     | POST   | [https://xapi.seuxw.cn:8895/mailSend/](https://xapi.seuxw.cn:8895/mailSend/)
