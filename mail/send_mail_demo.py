#!/usr/bin/env python
# -*- coding:utf-8 -*-


from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MailConfig

"""
注意需要邮箱pop3开启，设置独立密码，下边的password也是独立密码，
非登录密码
"""

send_to_mail_list = ['291374108@qq.com']
html = """
<tbody><tr>
                <td class="border" style="padding: 0;vertical-align: top;font-size: 1px;line-height: 1px;background-color: #dadada;width: 1px">​</td>
                <td style="padding: 0;vertical-align: top">
                  <table class="one-col" style="border-collapse: collapse;border-spacing: 0;Margin-left: auto;Margin-right: auto;width: 600px;background-color: #ffffff;table-layout: fixed" emb-background-style="">
                    <tbody><tr>
                      <td class="column" style="padding: 0;vertical-align: top;text-align: left">

              <div class="image" style="font-size: 12px;mso-line-height-rule: at-least;font-style: normal;font-weight: 400;Margin-bottom: 0;Margin-top: 0;font-family: sans-serif;color: #60666d" align="center">
                <img style="border: 0;-ms-interpolation-mode: bicubic;display:
                block;max-width: 600px"
                src="http://7ktuty.com1.z0.glb.clouddn.com/tupian_today.jpg" alt="" width="600" height="425">
              </div>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <p style="font-style: normal;font-weight: 400;Margin-bottom:
              0;Margin-top: 24px;font-size: 15px;line-height: 24px;font-family:
              sans-serif;color: #60666d"><strong style="font-weight: bold">Hi
              ,</strong></p><p style="font-style: normal;font-weight:
              400;Margin-bottom: 24px;Margin-top: 24px;font-size:
              15px;line-height: 24px;font-family: sans-serif;color: #60666d">
          尊敬的用户，我们正在做一个图片网站，有妹子图，鲜肉图，萌物图等等，我们希望提升用户的浏览体验，如果您有兴趣，可以访问我们的网站“今日图片”。欢迎提出您的建议.&nbsp;</p>

                              </td>
                            </tr>
                          </tbody></table>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <div class="divider" style="Margin-bottom: 24px;Margin-top: 0">
                <div class="border" style="font-size: 1px;line-height: 1px;background-color: #dadada">&nbsp;</div>
              </div>

                              </td>
                            </tr>
                          </tbody></table>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <div class="btn" style="Margin-bottom: 24px;Margin-top: 0;text-align: center">
                <!--[if !mso]--><a style="border-radius: 3px;display:
                    inline-block;font-size: 14px;font-weight: 700;line-height:
                    24px;padding: 13px 35px 12px 35px;text-align:
                center;text-decoration: none !important;transition: opacity 0.2s
                ease-in;color: #fff;font-family: sans-serif;background-color:
            #00afd1" href="http://jinritu.com" target="_blank">访问"今日图片"</a><!--[endif]-->
              <!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" href="http://google.com" style="width:258px" arcsize="7%" fillcolor="#00AFD1" stroke="f"><v:textbox style="mso-fit-shape-to-text:t" inset="0px,12px,0px,11px"><center style="font-size:14px;line-height:24px;color:#FFFFFF;font-family:sans-serif;font-weight:700;mso-line-height-rule:exactly;mso-text-raise:4px">How was your recent order?</center></v:textbox></v:roundrect><![endif]--></div>

                              </td>
                            </tr>
                          </tbody></table>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <div class="divider" style="Margin-bottom: 24px;Margin-top: 0">
                <div class="border" style="font-size: 1px;line-height: 1px;background-color: #dadada">&nbsp;</div>
              </div>

                              </td>
                            </tr>
                          </tbody></table>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <div style="height:5px">&nbsp;</div>

                              </td>
                            </tr>
                          </tbody></table>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <p style="font-style: normal;font-weight: 400;Margin-bottom:
              24px;Margin-top: 0;font-size: 15px;line-height: 24px;font-family:
              sans-serif;color: #60666d">感谢您的支持,<br>
<strong style="font-weight: bold">今日图片。</strong></p>

                              </td>
                            </tr>
                          </tbody></table>

                          <table class="contents" style="border-collapse: collapse;border-spacing: 0;table-layout: fixed;width: 100%">
                            <tbody><tr>
                              <td class="padded" style="padding: 0;vertical-align: top;padding-left: 32px;padding-right: 32px;word-break: break-word;word-wrap: break-word">

              <div style="height:5px">&nbsp;</div>

                              </td>
                            </tr>
                          </tbody></table>

                        <div class="column-bottom" style="font-size: 32px;line-height: 32px;transition-timing-function: cubic-bezier(0, 0, 0.2, 1);transition-duration: 150ms;transition-property: all">&nbsp;</div>
                      </td>
                    </tr>
                  </tbody></table>
                </td>
                <td class="border" style="padding: 0;vertical-align: top;font-size: 1px;line-height: 1px;background-color: #dadada;width: 1px">​</td>
              </tr>
            </tbody>

"""


mailInfo = {
    "from": MailConfig.USERNAME,
    "to": ', '.join(send_to_mail_list),
    "hostname": MailConfig.HOSTNAME,
    "username": MailConfig.USERNAME,
    "password": MailConfig.PASSWORD,    # 邮箱独立密码，非登录密码
    "mailsubject": "我是标题",
    #"mailtext": "使用python脚本发的测试邮件。http://jinritu.com",
    "mailtext": html,
    "mailencoding": "utf-8",
    #"mailtype": "plain",
    "mailtype": "html",
}


def send_mail():
    smtp = SMTP_SSL(mailInfo["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mailInfo["hostname"])
    smtp.login(mailInfo["username"], mailInfo["password"])

    msg = MIMEText(mailInfo["mailtext"], mailInfo["mailtype"],
                   mailInfo["mailencoding"])
    msg["Subject"] = Header(mailInfo["mailsubject"], mailInfo["mailencoding"])
    msg["from"] = mailInfo["from"]
    msg["to"] = mailInfo["to"]
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())

    smtp.quit()

if __name__ == '__main__':
    send_mail()
