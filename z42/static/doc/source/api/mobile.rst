==================================================
手机 API (version 2)
==================================================

作者:  tonghs tonghuashuai@gmail.com

简介
======================

改版以后的新接口。

相关说明:

* 无特殊说明，请求方式默认为 POST。
* 带 *  的参数可以不传，不传时取默认值。


注册登录
======================

获取图片验证码
----------------------

`http://mobile.tonghs.me/v2/home/img_verify_code <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/home/img_verify_code&method=get&_=获取图片验证码>`_

method::
    
    GET

params:: 

    无

return:: 

    {
        key: 验证码 key
        img: 验证码图片 base64
    }


发送手机验证码
----------------------


`http://mobile.tonghs.me/v2/home/verify_code <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/home/verify_code&method=post&phone=18601980445&key=sEGLiNb0SciViQmQm0te6g&token=2E4WE&_=发送手机验证码>`_

params:: 

    phone: 手机号码
    key: 图片验证码 key
    token: 图片验证码

return:: 

    {
        message: 返回信息
        success: 是否成功 true/false
        time: 剩余时间
    }


注册
----------------------


`http://mobile.tonghs.me/v2/home/register <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/home/register&method=post&phone=18601980445&key=sEGLiNb0SciViQmQm0te6g&code=289352&name=tonghs&password=tonghs&password_=tonghs&_=注册>`_


params::

    phone: 手机号码
    code: 验证码
    name: 姓名
    password: 密码
    password_: 确认密码
    key: 图片验证码 key

return::

    {
        message: 返回信息 
        success: true/false
    }


登录
----------------------


`http://mobile.tonghs.me/v2/home/login <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/home/login&account=tonghuashuai@126.com&password=angel1234&_=登录>`_


params::

    account: 邮箱或手机号码
    password: 密码

return::

    登录失败时

    {
        message: 返回信息
        success: true/false
    }


    登录成功时

    {
        user: {
            id: 用户ID
            name: 姓名
            avatar_big: 头像
            avatar_small: 小头像
            access_token: 
            summary: 简介
            firmname: 公司名
            title: 职位
            phone: 电话
            qq: 
            weixin: 
            email: 
            defaultpart: 参与身份1: 投资人 2: 领投人
            regionid: 省份ID
            regionname: 省份名
            cityid: 城市ID
            cityname: 城市名
        }
    }

用户
=====================

投资人列表
--------------------

`http://mobile.tonghs.me/v2/user <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user&pagesize=10&pageindex=1&industry=&region=&_=投资人列表>`_

params::

    *pagesize: 每页条数, 默认为 10
    *pageindex: 当前页数, 默认为 1
    uid: 用户 ID
    access_token:
    *industry: 行业（筛选用）
    *region: 区域（筛选用）

return::

    {
        industry: 行业
        regionid: 区域
        total: 总条数
        list: [{
            id: 
            name: 姓名
            firmname: 公司 
            title: 职位
            followercount: 粉丝数
            industry: 行业
            region_name: 地区
            isfollow: 是否关注
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
            avatar: 头像
            meetingtimes: 约谈数
            view_count: 0 查看次数，主站无该数据
        }]
    }


投资人列表搜索
--------------------

`http://mobile.tonghs.me/v2/user_search <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user_search&pagesize=10&pageindex=1&keyword=兰宁羽&_=投资人列表>`_

params::

    *pagesize: 每页条数, 默认为 10
    *pageindex: 当前页数, 默认为 1
    uid: 用户 ID
    access_token:
    keyword: 关键字

return::

    {
        pagesize: 每页条数
        pageindex: 当前页数
        total: 总条数
        list: [{
            id: 
            name: 姓名
            firmname: 公司 
            title: 职位
            followercount: 粉丝数
            industry: 行业
            region_name: 地区
            isfollow: 是否关注
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
            avatar: 头像
            meetingtimes: 约谈数
            view_count: 0 查看次数，主站无该数据
        }]
    }


投资人详情
--------------------

`http://mobile.tonghs.me/v2/user/detail <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/detail&user_id=10839876&_=投资人详情>`_

params::

    uid: 用户 ID
    access_token:
    user_id: 要查看的用户的ID

return::

    {
        user: {
            id: ID
            name: 姓名
            avatar: 头像
            part: 0: 创业者 1: 投资人
            summary: 简介
            style: 投资理念
            business: 擅长领域
            service: 提供服务
            isfollow: 是否关注
            following_count: 关注人数
            following_list:
            [{
                id:
                name: 姓名
                title: 职位
                avatar: 头像
                industry: 行业
                isfollow: 是否关注
                summary: 简介
                part: 身份 0: 创业者 1: 投资人 2: 领投人
            }]
            follower_count: 粉丝人数
            follower_list: 
            [{
                id:
                name: 姓名
                title: 职位
                avatar: 头像
                industry: 行业
                isfollow: 是否关注
                summary: 简介
                part: 身份 0: 创业者 1: 投资人 2: 领投人
            }]
            invested_com: 参与过的项目
            [{
                id: 公司 ID
                name: 项目名
                logo: 公司 logo
                concept: 一句话介绍
                viewercount: 查看次数
                isfans: 是否是粉丝
                creatorid: 创建人id
                industry: 行业
                region: 区域
                shareurl: 微信分享链接
                meetingcount: 约谈次数
                day: 剩余天数
                amount: 融资金额
                fanscount: 粉丝数
                finishamount: 完成融资数
                part: 参与身份1: 投资人 2: 领投人

            }]
            comment_list: 评论列表
            [{
                user_id: 用户ID
                name: 
                avatar: 头像
                title: 职位
                content: 评论内容
                time: 时间（时间戳，目前未取到）
            }]
            bbs_list: bbs 列表
            [{
                title: 标题
                url: 连接
                time: 时间（时间戳）
            }]
        }
    }


提交项目
----------

`http://mobile.tonghs.me/v2/user/submit_com <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/submit_com&com_id=10937375&target_id=10878516&_=提交项目>`_

params::

    uid: 用户ID
    access_token: 
    com_id: 项目ID
    target_id: 要提交给的投资人的ID

return::

   {
       message: 错误信息
       success: true/false
   }


创业者详情
--------------------

`http://mobile.tonghs.me/v2/user/detail <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/detail&user_id=10879982&_=创业者详情>`_

params::

    uid: 用户 ID
    access_token:
    user_id: 要查看的用户的ID

return::

    {
        user: {
            id: ID
            name: 姓名
            avatar: 头像
            summary: 简介
            skill: 技能
            part: 0: 创业者 1: 投资人
            isfollow: 是否关注
            my_com: 参与过的项目
            [{
                id: 项目ID
                name: 
                logo: 
                state: 项目状态
                concept: 项目简介
                viewercount: 查看次数
                isfans: 是否是粉丝
                industry: 行业
                region: 区域
                shareurl: 微信分享链接
                meetingcount: 约谈次数
                day: 剩余天数
                amount: 融资金额
                fanscount: 粉丝数
                finishamount: 完成融资数

            }]
            following_count: 关注人数
            following_list:
            [{
                id:
                name: 姓名
                title: 职位
                avatar: 头像
                industry: 行业
                isfollow: 是否关注
                summary: 简介
                part: 身份 0: 创业者 1: 投资人 2: 领投人
            }]
            follower_count: 粉丝人数
            follower_list: 
            [{
                id:
                name: 姓名
                title: 职位
                avatar: 头像
                industry: 行业
                isfollow: 是否关注
                summary: 简介
                part: 身份 0: 创业者 1: 投资人 2: 领投人
            }]
            career: 工作经历
            [{
                start: 开始时间
                end: 结束时间
                company: 公司名称
                title: 职位
                txt: 介绍
            }]
            edu: 
            [{
                start: 0, 
                major: 专业 
                school: 学校 
                degress: 学位
            }]
        }
    }


项目相关
======================

项目列表
----------------------

`http://mobile.tonghs.me/v2/startup <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup&pagesize=10&pageindex=1&state=0&industryid=&regionid=&type=0&_=项目列表>`_

params::

    client_id: 
    *pagesize: 每页条数, 默认为 10
    *pageindex: 当前页数, 默认为 1
    uid: 用户 ID
    access_token:
    *state: 项目所处状态 全部 0 /上线 1 /预热 2（筛选用）
    *industryid: 行业（筛选用）
    *regionid: 区域（筛选用）
    type: 请求类型
        0: 项目列表
        1: 我收到的项目
        2: 我关注的项目
        3: 我创建的项目

return::

    {
        pageindex: 当前页数, 默认为 1
        industryid: 行业
        total: 总条数
        regionid: 区域
        list: [{
            viewercount: 查看次数
            concept: 一句话介绍
            viewapply: 是否申请查看 1/0
            name: 项目名
            coinveststatus: 合投状态
                10: '申请未通过',
                20: '创建中',
                21: '未申请合投',
                30: '申请合投中',
                40: '合投预热',
                50: '合投待上线',
                60: '合投上线',
                70: '确认投资人名单',
                80: '融资完成',
                90: '融资失败',
            isfans: 是否是粉丝 
            industry: 行业
            region: 区域
            member_count: 成员数
            shareurl: 微信分享链接
            meetingcount: 约谈次数
            day: 剩余天数
            creatorname: 创建者姓名
            amount: 融资金额
            canview: 是否可以查看
            creatorid: 创建者 ID
            financingid: 融资 ID （目前没用）
            creatorphone: 创建者手机
            logo: 公司 logo
            id: 公司 ID
            fanscount: 粉丝数
            finishamount: 完成融资数 
        }]
    }

项目列表搜索
----------------------

`http://mobile.tonghs.me/v2/startup_search <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup_search&pagesize=10&pageindex=1&keyword=云视野&_=项目列表>`_

params::

    client_id: 
    *pagesize: 每页条数, 默认为 10
    *pageindex: 当前页数, 默认为 1
    uid: 用户 ID
    access_token:
    *keyword: 关键字

return::

    {
        pagesize: 每页条数
        pageindex: 当前页数
        total: 总条数
        list: [{
            viewercount: 查看次数
            concept: 一句话介绍
            viewapply: 是否申请查看 1/0
            name: 项目名
            coinveststatus: 合投状态
                10: '申请未通过',
                20: '创建中',
                21: '未申请合投',
                30: '申请合投中',
                40: '合投预热',
                50: '合投待上线',
                60: '合投上线',
                70: '确认投资人名单',
                80: '融资完成',
                90: '融资失败',
            isfans: 是否是粉丝 
            industry: 行业
            region: 区域
            member_count: 成员数
            shareurl: 微信分享链接
            meetingcount: 约谈次数
            day: 剩余天数
            creatorname: 创建者姓名
            amount: 融资金额
            canview: 是否可以查看
            creatorid: 创建者 ID
            financingid: 融资 ID （目前没用）
            creatorphone: 创建者手机
            logo: 公司 logo
            id: 公司 ID
            fanscount: 粉丝数
            finishamount: 完成融资数 
        }]
    }

项目详情页
----------------------

`http://mobile.tonghs.me/v2/startup/detail <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/detail&com_id=12813761&_=项目详情页>`_

params::

    uid: 用户 ID
    access_token:
    com_id: 要查看的项目ID

return::

    {
        id: 项目ID
        name: "运策网"
        url: 官方网站
        creatorid: 创始人ID
        logo: 
        summary: 简介

        demourl: 试用地址
        android: android 下载地址
        demouser: 试用用户
        demopwd: 试用密码
        weibo: 微博
        weixin: 微信 
        ios: iOS 下载地址

        growthdata: 成长数据
        [{
            occurtime: 时间
            name: 数据名称
            quantity: 数量
        }]

        tutor: 导师
        [{
            id:
            name: 姓名
            title: 职位
            avatar: 头像
            industry: 行业
            isfollow: 是否关注
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
        }]

        milestone: 大事记
        [{
            content: 内容
            occurdate: 时间
        }]

        news: 新闻
        [{
            title: 标题
            content: 内容
            url: 连接
            from: 来源
            occurdate: 时间
        }]


        pics: 图片信息列表
        [{
            small: 小图片(320px)
            big: 大图片(640px)
        }]

        incubator: 孵化器
        [{
            id: 
            name: 
            avatar: 头像
            summary: 简介
            region: 区域
            start_date: 开始时间
            end_date: 结束时间
        }]

        team: 团队
        [{
            id:
            name: 姓名
            title: 职位
            avatar: 头像
            industry: 行业
            isfollow: 是否关注
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
        }]
    }

项目融资信息
---------------

`http://mobile.tonghs.me/v2/startup/finance <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/finance&com_id=12813761&_=项目融资信息>`_

params::

    uid: 用户 ID
    access_token:
    com_id: 项目ID

return::

    {
        stock_sale: 出让股权比例
        min_quota: 最小融资额度
        hope_amounta: 预计融资
        price: 融资前估值
        finace_history: 过往融资
        txt: 除资金以外的其他需求
        [{
            time: 时间（时间戳）
            content: 内容？（带确定，目前该字段内容为融资金额）
        }]
        vc_list: 本轮投资意向列表
        [{
            id:
            name: 姓名
            title: 职位
            avatar: 头像
            industry: 行业
            isfollow: 是否关注
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
        }]
        pre_vc_list: 上一轮投资意向列表
        [{
            id:
            name: 姓名
            title: 职位
            avatar: 头像
            industry: 行业
            isfollow: 是否关注
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
        }]
        purpose: 资金用途
        qa_list: 提问列表
        [{
            q: 提问内容
            q_time: 提问时间（时间戳）
            a: 回答
            a_time: 回答时间（时间戳）
            user_id: 提问用户
            name: 提问用户名
            title: 提问用户职位
        }]
    }

我收到的项目/我关注的项目/我创建的项目
----------------------------------------------

`http://mobile.tonghs.me/v2/startup/my <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/my&pagesize=0&pageindex=1&state=0&type=0&_=我收到的项目/我关注的项目/我创建的项目>`_

params::
    
    *pagesize: 每页条数, 默认为 10
    *pageindex: 当前页数, 默认为 1
    uid: 用户 ID
    access_token:
    *state: 项目所处状态 全部 0 /上线 1 /预热 2（筛选用）
    type: 请求类型
        0: 我收到的项目
        1: 我关注的项目
        2: 我创建的项目

return::

    {
        pageindex: 当前页
        total: 总条数
        list:
        [{
            id: 公司ID
            name: 项目名
            logo: 公司logo
            concept: 项目简介
            member_count: 成员数
            industry: 行业
            region: 地区
            stage: 所处阶段
            fanscount: 粉丝数
            viewcount: 查看数
            meetingcount: 约谈数
        }]
    } 


申请查看项目
----------------------

`http://mobile.tonghs.me/v2/startup/view_apply <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/view_apply&com_id=12813761&_=申请查看公司>`_

params::

    uid: 用户ID
    access_token:
    com_id: 要查看的公司ID

return::

    {
        message: 提示信息
        success: true/false
    }


发送投资意向
------------

`http://mobile.tonghs.me/v2/startup/vc <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/vc&com_id=12813761&amount=40&phone=18601980445&weixin=test&service=办公场所&angel_name=tonghs&_=发送投资意向>`_

params::

    uid: 用户ID 
    access_token: 
    com_id: 项目
    amount: 投资金额
    phone: 电话
    weixin: 微信
    service: 提供的服务
    *angel_name: 投资人姓名 

retrun::

    {
        message: 返回信息
        success: true/false
    }


项目新闻列表
-------------

`http://mobile.tonghs.me/v2/startup/news <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/news&method=get&com_id=10925092&pageindex=1&pagesize=10&_=项目新闻列表>`_

params::

    uid: 用户ID
    access_token: 
    com_id: 项目ID
    *pageindex: 当前页
    *pagesize: 每页条数

return::

    {
        list:
        {
            title: 标题
            content: 内容
            url: 
            from: 来源
            occurdate: 日期（时间戳）
        }
    }


约谈
-----

`http://mobile.tonghs.me/v2/startup/meeting <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/meeting&com_id=10925092&content=约谈约吗&_=约谈>`_

params::
    
    uid: 用户ID
    access_token: 
    com_id: 项目ID
    content: 内容

return::

    {
        message: 提示信息
        success: true/false
    }

分享项目
---------

`http://mobile.tonghs.me/v2/startup/share <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/share&com_id=12813761&user_list=10878516,10878516&content=test&_=%E5%88%86%E4%BA%AB%E9%A1%B9%E7%9B%AE>`_

params::
    
    uid: 用户ID
    access_token: 
    com_id: 项目ID
    user_list: 用户ID 列表，字符串，ID以逗号分隔，如：'10878516,10878515'
    content: 内容

return::

    {
        message: 提示信息
        success: true/false
    }


关注和粉丝
=====================

关注人或项目
--------------------

`http://mobile.tonghs.me/v2/follow <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/follow&id=10925092&_=关注人或项目>`_

params::

    id: 要关注的人或项目的ID
    uid: 登录人ID
    access_token:

return::

    {
        message: 提示信息
        success: true/false
    }


取消关注人或项目
--------------------

`http://mobile.tonghs.me/v2/unfollow <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/unfollow&id=10925092&_=取消关注人或项目>`_

params::

    id: 要关注的人或项目的ID
    uid: 登录人ID
    access_token:

return::

    {
        message: 提示信息
        success: true/false
    }

关注的人
--------------------

`http://mobile.tonghs.me/v2/user/focused <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/focused&method=post&type=0&id=10878516&pageindex=1&pagesize=10&_=关注的人>`_


params::

    uid: 用户ID
    *id: 要查询的用户或公司的ID，如果不传，则默认用为当前登录人ID
    access_token:
    *pageindex: 页数
    *pagesize: 每页显示条数
    *type: 请求列表类型 0: 全部 1: 创业者 2: 投资人

return::

    {
        list:
        [{
            id: 用户ID 
            name: 姓名
            title: 职位
            company: 公司
            industry: 行业
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
            avatar: 头像
            active_time: 活跃时间（时间戳） 
        }]
    }


粉丝
--------------------

`http://mobile.tonghs.me/v2/user/follower <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/follower&method=post&type=0&id=10878516&pageindex=1&pagesize=10&_=粉丝>`_


params::

    uid: 用户ID
    *id: 要查询的用户或公司的ID，如果不传，则默认用为当前登录人ID
    access_token:
    *pageindex: 页数
    *pagesize: 每页显示条数
    *type: 请求列表类型 0: 全部 1: 创业者 2: 投资人

return::

    {
        list:
        [{
            id: 用户ID 
            name: 姓名
            title: 职位
            company: 公司
            industry: 行业
            summary: 简介
            part: 身份 0: 创业者 1: 投资人 2: 领投人
            avatar: 头像
            active_time: 活跃时间（时间戳） 
        }]
    }


个人设置
==========

修改姓名
--------

`http://mobile.tonghs.me/v2/settings/profile/save_name <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_name&name=tonghs&_=修改姓名>`_


params::
    
    uid: 用户ID
    access_token:
    name: 用户姓名

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改公司
--------

`http://mobile.tonghs.me/v2/settings/profile/save_com <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_com&com=angelcrunch&_=修改公司>`_

params::
    
    uid: 用户ID
    access_token:
    com: 公司名称

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改职位
--------

`http://mobile.tonghs.me/v2/settings/profile/save_title <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_title&title=web developer&_=修改职位>`_

params::
    
    uid: 用户ID
    access_token:
    title: 职位

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改电话
--------

`http://mobile.tonghs.me/v2/settings/profile/save_phone <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_phone&phone=18601980445&_=修改电话>`_

params::
    
    uid: 用户ID
    access_token:
    phone: 电话

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改QQ
--------

`http://mobile.tonghs.me/v2/settings/profile/save_qq <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_qq&qq=522183104&_=修改QQ>`_

params::
    
    uid: 用户ID
    access_token:
    qq: QQ

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改微信
--------

`http://mobile.tonghs.me/v2/settings/profile/save_weixin <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_weixin&weixin=weixin&_=修改微信>`_

params::
    
    uid: 用户ID
    access_token:
    weixin: 微信

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改简介
--------

`http://mobile.tonghs.me/v2/settings/profile/save_summary <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_summary&summary=summary&_=修改简介>`_

params::
    
    uid: 用户ID
    access_token:
    summary: 简介

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改地区
--------

`http://mobile.tonghs.me/v2/settings/profile/save_region <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/save_region&region=4295032832&_=修改地区>`_

params::
    
    uid: 用户ID
    access_token:
    region: 区域ID

return::
    
    {
        message: 返回信息 
        success: true/false
    }


修改头像
--------

http://mobile.tonghs.me/v2/settings/profile/save_avatar

params::
    
    uid: 用户ID
    access_token:
    avatar: 头像文件

return::
    
    {
        message: 返回信息 
        success: true/false
        avatar: 返回头像 url 值
    }


其他
=====================

获取区域列表
--------------------

`http://mobile.tonghs.me/v2/settings/profile/getregionlist <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/profile/getregionlist&method=get&_=获取区域列表>`_

method::
    
    GET

params::
    
    无

return::
    
    {
        list:
        [{
            parentid: 父级ID
            ancestornames: 父级名称
            id: 区域ID
            name: 区域名称
        }]
    }

示例::

    {
        list:
        [{
            parentid: "1"
            ancestornames: ""
            id: "1"
            name: "中国"
        }
        {
            parentid: "1"
            ancestornames: "中国"
            id: "4295032832"
            name: "北京"
        }
        {
            parentid: "4295032832"
            ancestornames: "北京"
            id: "4295033088"
            name: "东城区"
        }]
    }

说明:

可通过以下方法判断国家、省（直辖市）和城市（区）:

* 当id 的长度小于 10 时是国家
* 当parentid 长度小于 10 时是省（直辖市）
* 当parentid 长度等于 10 时是市（地区）

提问
-----------------

`http://mobile.tonghs.me/v2/startup/q <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/q&com_id=12813761&content=提问内容&_=提问>`_

param::
    
    uid: 当前登录人ID
    access_token:
    com_id: 公司ID
    content: 提问内容

return::

    {
        success: true/false
        message: 
    }


回答
------------

`http://mobile.tonghs.me/v2/startup/a <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/startup/a&q_id=546eb3ccb0d8b616cbbb8127&content=回答内容&_=回答>`_

param::
    
    uid: 当前登录人ID
    access_token:
    q_id: 问题ID
    content: 回答内容

return::

    {
        success: true/false
        message: 
    }


是否收到新项目
---------------

`http://mobile.tonghs.me/v2/user/receive_com_count <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/receive_com_count&method=get&count=17&id=10878516&pageindex=1&pagesize=10&_=是否收到新项目>`_

param::

    uid: 当前登录人ID
    access_token:
    count: 本地保存的接受项目个数

return::

    {
        success: true/false 是否接收到新项目
        message: 
        count: 新更新的项目数
    }


是否有新粉丝
------------

`http://mobile.tonghs.me/v2/user/follow_count <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/user/follow_count&method=get&count=17&id=10878516&pageindex=1&pagesize=10&_=是否有新粉丝>`_

param::

    uid: 当前登录人ID
    access_token:
    count: 本地保存的粉丝数

return::

    {
        success: true/false 是否有新粉丝
        message: 
        count: 新更新的粉丝数
    }


系统通知
--------

`http://mobile.tonghs.me/v2/settings/notice <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/v2/settings/notice&method=get&_=系统通知>`_

旧版: `http://mobile.tonghs.me/settings/notice <http://mobile.tonghs.me/?url=http://mobile.tonghs.me/settings/notice&method=get&_=系统通知>`_

param::

    uid: 当前登录人ID
    access_token:

return::
    
    {
        list: [{
            id: 通知ID
            cid: 通知类型 详细类型见说明
            create_time: 通知时间
            txt: 详细数据类型见说明 
        }]
    }


说明：

通知类型::

    提交项目: 3
    分享项目: 4
    项目进入预热: 5 
    项目审核失败 : 6
    发送投资意向: 7
    合投上线: 8
    融资成功: 9
    融资失败: 10
    投资人审核通过: 11
    投资人审核失败: 12
    管理员分享项目: 13（新版未上，目前没有）

不同类型的返回值如下：

提交项目::

    user_id: 提交人ID
    user_name: 提交人姓名
    user_ico: 提交人ico

    com_id: 项目ID
    com_name: 项目名
    com_ico: 项目logo

分享项目::

    user_id: 提交人ID
    user_name: 提交人姓名
    user_ico: 提交人ico

    com_id: 项目ID
    com_name: 项目名
    com_ico: 项目logo

    reson: 分享理由

项目进入预热/合投上线/融资成功/融资失败::

    com_id: 项目ID
    com_name: 项目名
    com_ico: 项目logo

项目审核失败::

    com_id: 项目ID
    com_name: 项目名
    com_ico: 项目logo

    reason: 失败原因

发送投资意向::

    user_id: 提交人ID
    user_name: 提交人姓名
    user_ico: 提交人ico

    com_id: 项目ID
    com_name: 项目名
    com_ico: 项目logo

    amount: 发送金额


投资人申请通过::

    {}

投资人申请未通过::

    reason: 未通过原因

    
管理员分享项目::

    com_id: 项目ID
    com_name: 项目名
    com_ico: 项目logo

    reason: 分享理由
    team: 团队成员介绍 
    summary: 公司简介

另外::

   成功图片：http://dn-ac88.qbox.me/default_cheer.png 
   成功图片：http://dn-ac88.qbox.me/default_sorry.png 
