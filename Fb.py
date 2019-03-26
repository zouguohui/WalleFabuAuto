import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
import paramiko
import pymysql
import time

from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8888, type=int, help="run server on the given port!")

allData = []


sql_user_insert = ["INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (1, 'wu.jiang@atkj6666.com', 1, 'V2R5Mnh7YI694KPpE5hy0sx-VQgR-dJ7', '$2y$13$mAO6nN/0tTcR.R7bO9XnCOzK9TU62/Ol7WaxPdy1zoNyfMO5bTpqq', NULL, NULL, 'wu.jiang@atkj6666.com', 'default.jpg', 2, 2, '2018-09-14 17:40:46', '2018-09-14 18:55:17', '江吴');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (2, 'zhipeng.liu@atkj6666.com', 1, 'uW-Z3OS2yYoMzsI1iPpQzdHAJ0gbOyBM', '$2y$13$LoU2/0uYcyCCtXKHd7hiEeVujyjVI0/.RnUaA1aqNhV8OIbLjplUC', NULL, NULL, 'zhipeng.liu@atkj6666.com', 'default.jpg', 2, 2, '2018-09-26 16:04:19', '2019-03-15 13:37:58', '刘志鹏');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (3, 'hao.cui@atkj6666.com', 1, '-1iu766sxpKTjhWHIIeZwUN79iBvlquG', '$2y$13$g8Dhbwd5TdUdJ4ukaiQlwO3sCMlQJLsJSYQgOGbhR7MN5pgGpmuX6', NULL, NULL, 'hao.cui@atkj6666.com', 'default.jpg', 1, 0, '2018-09-27 14:38:03', '2018-09-27 14:38:18', '崔浩');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (4, 'yidi.yu@atkj6666.com', 1, 'k6PLozOD47vEtjUgJ7c_fc1FL3dlA0RO', '$2y$13$J5NEyDZKtx8Ugvu5qb1DBuZgEdYHoMJFqi.dWqhia7gmZT/9aIpt.', NULL, NULL, 'yidi.yu@atkj6666.com', 'default.jpg', 1, 1, '2018-09-27 14:38:14', '2018-09-27 14:38:26', '余乙迪');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (5, 'yanlan.wang@atkj6666.com', 1, 'lX5ClxeaZH9kATPJ4uyDnfnRFuxmJs3E', '$2y$13$prmupIXf5EnDjmU.lIAATu65e51t8DN/JsZY4lcQp2148ut.OQoea', NULL, NULL, 'yanlan.wang@atkj6666.com', 'default.jpg', 1, 1, '2018-09-27 14:38:34', '2019-03-13 18:20:07', '王艳兰');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (6, 'yong.xiao@atkj6666.com', 1, 'J9-rJULJSQZm5WXcak8uTr4_IegE_qtL', '$2y$13$SMq9.hKhAEpf/GMtBgGq5uaF1iGYj0bRw1moDXaCrNNG4NKyh.5OK', NULL, NULL, 'yong.xiao@atkj6666.com', 'default.jpg', 1, 1, '2018-09-27 14:39:11', '2018-09-27 14:43:44', '肖勇');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (7, 'jinrong.li@atkj6666.com', 1, 'lMcF88LaRgFwpdgTIRBx0pObUh9JaLzj', '$2y$13$Ft3sUfZtSLakwXofuMw9ieqTULui20PX/7dUSI1iLvqcsYYArcc.C', NULL, NULL, 'jinrong.li@atkj6666.com', 'default.jpg', 1, 0, '2018-09-27 14:56:46', '2018-09-27 14:57:02', '李锦荣');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (8, 'xiaoyuan.lu@atkj6666.com', 1, 'IANYVwXmSPdXCgjigL8WN3ryc4SkX3L1', '$2y$13$QE4nLcJrAnLAZMU6CCkY3eTg51YaxkY0NgjCdYyqkIfPaqfSKL7bS', NULL, NULL, 'xiaoyuan.lu@atkj6666.com', 'default.jpg', 1, 0, '2018-09-27 15:01:04', '2018-09-27 15:01:33', '卢晓媛');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (9, 'yi.chi@atkj6666.com', 1, 'uzZueVlvLYccFrOZw0PGx7-W8NpFibei', '$2y$13$OFyx9uCPQeJAY9b05BReGuz62Iuxxr64ogrZo2Rbz0Jis5lcAGyi.', NULL, NULL, 'yi.chi@atkj6666.com', 'default.jpg', 1, 1, '2018-09-27 15:07:31', '2018-09-27 15:07:38', '池熠');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (10, 'pan.wang@atkj6666.com', 1, 'itZc-QkcAmy6dAm5pohtO8Cskxuo3voh', '$2y$13$U7GUOwg.dh7XvncZlJ6VXuK6LdBTsme0IrHXrEZjmx7l04neiNbPO', NULL, NULL, 'pan.wang@atkj6666.com', 'default.jpg', 1, 1, '2018-09-27 17:13:42', '2018-09-27 17:14:10', '王蟠');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (11, 'zhonghui.fan@atkj6666.com', 1, 'jOw2bu4KqRLzVewqRpUXHHfkPpM4kz44', '$2y$13$a099.j9MBttyQboyCv.O6Onb78BAk2S1Erd.Yy9kLEJRJ/i13k81m', '', NULL, 'zhonghui.fan@atkj6666.com', 'default.jpg', 1, 1, '2018-09-27 17:14:27', '2018-09-27 17:16:06', '范忠辉');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (12, 'liang.jiang@atkj6666.com', 1, '1umTOPLptYZf8_v1BNOjy07Z0Tq5EHKA', '$2y$13$8jVyIkDAfWSoAte1C84DpO5vMso0xZSxYZ98ww1khPoaDaoEkTSn2', NULL, NULL, 'liang.jiang@atkj6666.com', 'default.jpg', 1, 2, '2018-09-30 17:17:45', '2019-02-13 10:30:38', '蒋亮');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (13, 'li.chen@atkj6666.com', 1, 'E41e5Z1j4Fkph4jPHmCydx83k0qs_doj', '$2y$13$hwdDy./goyMdzDD6B5NlJ.KmQG7QzmZag3Nk61ihTxxvMTCxzCjJq', NULL, NULL, 'li.chen@atkj6666.com', 'default.jpg', 1, 2, '2018-10-08 09:44:49', '2018-10-26 15:20:25', '陈利');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (14, 'zhenjie.cui@atkj6666.com', 1, 'g4iqRka8r-z0Xm_e5GJDiR5JLRJnDZSE', '$2y$13$IF5INH.lGVOLypizdUf/MeEcqJM/m68QPmS5.dKyP9UiZkhdK1uh6', NULL, NULL, 'zhenjie.cui@atkj6666.com', 'default.jpg', 1, 2, '2018-10-20 10:47:27', '2019-03-06 09:54:10', '崔振杰');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (15, '13602667394@163.com', 1, '33rEun6ivxChdfI1SHrLb8TbyWRo22aC', '$2y$13$gZyJbVrpRqb67N3lmNulGOZCliLU0ReeQhNT3m2UUhTqYeG3uLpeW', NULL, NULL, '13602667394@163.com', 'default.jpg', 1, 0, '2018-10-31 15:55:57', '2018-10-31 15:56:41', 'zengzifeng');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (16, 'rouergun@126.com', 1, 'lAbhTKg5Z-m9XOlYX1KZLqVLOaZyEbis', '$2y$13$POor.RUYjiZccH6QakWexueZ/dgXENMBOkIfntHZCjjwG5xQGu0Nu', NULL, NULL, 'rouergun@126.com', 'default.jpg', 1, 0, '2018-10-31 16:00:44', '2018-10-31 16:04:19', 'rider');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (17, 'feiwu.li@atkj6666.com', 1, 'TJpsyegrDd8UyyS1XDCjpgte5Y6he7YQ', '$2y$13$QPc5ddeTWn72V7s6lVQmD.abLijmKKciD9MNKCqpmttW3/.e4o/ai', NULL, NULL, 'feiwu.li@atkj6666.com', 'default.jpg', 2, 0, '2018-11-12 11:25:28', '2018-11-12 11:27:48', '李飞武');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (18, 'ao.liu@atkj6666.com', 1, 'UsMfy-dWK0aKXhZlaA8ScfuDcfBogaoC', '$2y$13$3yxLtZ1yKGW7TW3UkDtufObn6UCzSHI20NdpJbjgvWnt5bYnSdIIG', NULL, NULL, 'ao.liu@atkj6666.com', 'default.jpg', 1, 1, '2018-12-06 16:48:37', '2018-12-06 16:49:52', '刘傲');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (19, 'xinpu.zhu@atkj6666.com', 1, '8oOAahjmwu0Zrx2AmW_09LLfUufuytpW', '$2y$13$EFFfpYX8mMYJLCPWRCkVYOMUP6Gi9nlyhtGdyxQZUeLQwZ8B/jNya', NULL, NULL, 'xinpu.zhu@atkj6666.com', 'default.jpg', 1, 1, '2018-12-06 16:52:15', '2018-12-08 16:37:21', '朱新普');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (20, 'xingmeng.zhang@atkj6666.com', 1, '-dgYNMCfzfBw9j9GViJi3QLcvF7EEK3c', '$2y$13$ACAo0iYczL.G.aFC5vNAIuXn0avSf4qX4ZUJkN/1GrwS1eK8Ppg/6', NULL, NULL, 'xingmeng.zhang@atkj6666.com', 'default.jpg', 1, 1, '2018-12-06 16:55:10', '2018-12-06 16:57:06', '张醒梦');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (21, 'guohui.zou@atkj6666.com', 1, 'P08u-DKs6GmBEf5vDU743G9sNOPycZ4l', '$2y$13$7XWSy4YN3SjVAizsgfwvEObMUWKXPNnnt2jafa6n6i.KbCjhBXvMu', NULL, NULL, 'guohui.zou@atkj6666.com', 'default.jpg', 2, 2, '2018-12-25 15:24:26', '2018-12-25 15:30:01', '邹国辉');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (23, 'changhu.li@atkj6666.com', 1, 'vO4WxG394iXjD12ujtvm8i0cr8wFQWKx', '$2y$13$dvp/uyytAa9Iie3NBtqQcOX.5jvqDl1Y7OCN29EQQw6QJ8m6YGjHK', NULL, NULL, 'changhu.li@atkj6666.com', 'default.jpg', 1, 1, '2019-01-09 15:04:40', '2019-01-09 15:05:12', 'lichanghu');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (24, 'weibo@atkj6666.com', 1, 'frXrUcQgNW1vSL-xw-GZ7hh-PsjNK6nl', '$2y$13$0KpvgWSYKmdTUv2yBqyEHumPK7gSW8fFy2A.IDrxcY.F6pxKGUUK.', NULL, NULL, 'weibo@atkj6666.com', 'default.jpg', 1, 1, '2019-01-15 10:31:29', '2019-01-23 10:58:04', 'weibo');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (25, 'xu.chen@atkj6666.com', 1, 'RD0YxzIUDUVT043gZt1QG3fbnFlXHG_r', '$2y$13$i5TYgwFfQ.WMzFle2Boh1OpO7/qWWnlQeQYlhHQ1f9YmjxMuq3ZYy', NULL, NULL, 'xu.chen@atkj6666.com', 'default.jpg', 1, 1, '2019-01-16 09:52:08', '2019-01-16 10:32:58', '陈旭');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (26, 'siqi.lu@atkj6666.com', 1, 'glf9m_RCDjD7j_m1xbuL3OGSu3YE62WC', '$2y$13$2h62j1FohuHzALhsakJOuuaw0ARj5D1qBY/4ByP1UPXz0tz2PJ8d2', NULL, '', 'siqi.lu@atkj6666.com', 'default.jpg', 1, 1, '2019-01-17 14:58:53', '2019-01-17 14:58:53', 'siqi.lu');",
"INSERT INTO `user`(`id`, `username`, `is_email_verified`, `auth_key`, `password_hash`, `password_reset_token`, `email_confirmation_token`, `email`, `avatar`, `role`, `status`, `created_at`, `updated_at`, `realname`) VALUES (27, 'jintao.guo@atkj6666.com', 1, 's8O-eh-qXXSoeYiCpShx5seyrpb0eLsI', '$2y$13$D6Kot4kQA/HTAMsTzrI5B.MDB83BviU4v05qSId/08Lp4l7ji6Jv6', NULL, NULL, 'jintao.guo@atkj6666.com', 'default.jpg', 2, 2, '2019-03-14 16:49:58', '2019-03-14 16:52:44', 'guojintao');"]


class PostHandler(RequestHandler):
    def get(self):
        self.render("post.html")


class IndexHandler(RequestHandler):

    def ssh(self, name):
        i = 0
        con = pymysql.connect(host="10.8.29.34", user="root", password="N4opS4{2nQclb{SL7[Lx", charset="utf8")
        cur = con.cursor()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="10.8.29.34", port=22, username="root", password="znvoS>ZF1u8I0F0e{vE1")
        cp = "cp -r /data/web/share /data/web/%s" % name
        sed = "sed -i 's/share/%s/g' /data/web/%s/config/local.php" % (name, name)
        cp_config = "cp /etc/nginx/conf.d/share.conf /etc/nginx/conf.d/%s.conf" % name
        sed_config = "sed -i 's/share/%s/g' /etc/nginx/conf.d/%s.conf" % (name, name)
        setup = "/var/www/html/deploy/%s/yii walle/setup --interactive 0" % name
        ssh.exec_command(cp)
        time.sleep(1)
        ssh.exec_command(sed)
        time.sleep(1)
        ssh.exec_command(cp_config)
        time.sleep(1)
        ssh.exec_command(sed_config)
        cur.execute("create database %s character set utf8;" % name)
        cur.execute("use %s;" % name)
        time.sleep(1)
        ssh.exec_command(setup)
        time.sleep(1)
        cur.execute("TRUNCATE TABLE user;")
        while i < len(sql_user_insert):
            cur.execute(sql_user_insert[i])
            con.commit()
            i += 1

    def post(self, *args, **kwargs):
        infoDict = {}
        name = self.get_argument("name")
        infoDict['name'] = name
        print(infoDict)
        allData.append(infoDict)
        print(allData)
        self.redirect('/index')

    def get(self):
        e = "部署成功！"
        if len(allData) == 1:
            name = allData[0]['name']
            try:
                self.ssh(name)
            except Exception as e:
                e = e
        else:
            allData.pop(0)
            name = allData[0]['name']
            try:
                self.ssh(name)
            except Exception as e:
                e = e
        self.render("index.html", name=name, e=e)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        [
            (r'/post', PostHandler),
            (r'/index', IndexHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
