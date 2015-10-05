# -*- coding: gb2312 -*-
# vi:ts=4:et
	
"""
目前程序能从下列网站抓取代理列表

http://www.cybersyndrome.net/
http://www.pass-e.com/
http://www.cnproxy.com/
http://www.proxylists.net/
http://www.my-proxy.com/
http://www.samair.ru/proxy/
http://proxy4free.com/
http://proxylist.sakura.ne.jp/
http://www.ipfree.cn/
http://www.publicproxyservers.com/
http://www.digitalcybersoft.com/
http://www.checkedproxylists.com/

问:怎样才能添加自己的新网站，并自动让程序去抓取?
答:

请注意源代码中以下函数的定义.从函数名的最后一个数字从1开始递增，目前已经到了13    

def build_list_urls_1(page=5):
def parse_page_2(html=''):

def build_list_urls_2(page=5):
def parse_page_2(html=''):

.......

def build_list_urls_13(page=5):
def parse_page_13(html=''):


你要做的就是添加 build_list_urls_14 和 parse_page_14 这两个函数
比如你要从 www.somedomain.com 抓取 
    /somepath/showlist.asp?page=1
    ...  到
    /somepath/showlist.asp?page=8  假设共8页

那么 build_list_urls_14 就应该这样定义
要定义这个page这个参数的默认值为你要抓取的页面数8，这样才能正确到抓到8个页面
def build_list_urls_14(page=8):   
    ..... 
    return [        #返回的是一个一维数组，数组每个元素都是你要抓取的页面的绝对地址
    	'http://www.somedomain.com/somepath/showlist.asp?page=1',
        'http://www.somedomain.com/somepath/showlist.asp?page=2',
        'http://www.somedomain.com/somepath/showlist.asp?page=3',
        ....
        'http://www.somedomain.com/somepath/showlist.asp?page=8'
    ]

接下来再写一个函数 parse_page_14(html='')用来分析上面那个函数返回的那些页面html的内容
并从html中提取代理地址
注意： 这个函数会循环处理 parse_page_14 中的所有页面，传入的html就是那些页面的html文本

ip:   必须为 xxx.xxx.xxx.xxx 数字ip格式，不能为 www.xxx.com 格式
port: 必须为 2-5位的数字
type: 必须为 数字 2,1,0,-1 中的其中一个。这些数字代表代理服务器的类型
      2:高度匿名代理  1: 普通匿名代理  0:透明代理    -1: 无法确定的代理类型
 #area: 代理所在国家或者地区， 必须转化为 utf8编码格式  

def parse_page_14(html=''):
    ....
	return [
        [ip,port,type,area]         
        [ip,port,type,area]         
        .....                      
        ....                       
        [ip,port,type,area]        
    ]

最后，最重要的一点:修改全局变量 web_site_count的值，让他加递增1  web_site_count=14



问：我已经按照上面的说明成功的添加了一个自定义站点，我要再添加一个，怎么办?
答：既然已经知道怎么添加 build_list_urls_14 和 parse_page_14了

那么就按照同样的办法添加
def build_list_urls_15(page=5):
def parse_page_15(html=''):

这两个函数，并 更新全局变量   web_site_count=15

"""


import urllib,time,random,re,threading,string

web_site_count=13   #要抓取的网站数目
day_keep=2          #删除数据库中保存时间大于day_keep天的 无效代理
indebug=1        

thread_num=100                   # 开 thread_num 个线程检查代理
check_in_one_call=thread_num*10  # 本次程序运行时 最多检查的代理个数


skip_check_in_hour=1    # 在时间 skip_check_in_hour内,不对同一个代理地址再次验证
skip_get_in_hour=8      # 每次采集新代理的最少时间间隔 (小时)

proxy_array=[]          # 这个数组保存将要添加到数据库的代理列表 
update_array=[]         # 这个数组保存将要更新的代理的数据 

db=None                 #数据库全局对象
conn=None
dbfile='proxier.db'     #数据库文件名

target_url="http://www.baidu.com/"   # 验证代理的时候通过代理访问这个地址
target_string="030173"               # 如果返回的html中包含这个字符串，
target_timeout=30                    # 并且响应时间小于 target_timeout 秒 
                                     #那么我们就认为这个代理是有效的 



#到处代理数据的文件格式，如果不想导出数据，请让这个变量为空  output_type=''

output_type='xml'                   #以下格式可选,  默认xml
                                    # xml
                                    # htm           
                                    # tab         制表符分隔, 兼容 excel
                                    # csv         逗号分隔,   兼容 excel
                                    # txt         xxx.xxx.xxx.xxx:xx 格式

# 输出文件名 请保证这个数组含有六个元素
output_filename=[                          
            'uncheck',             # 对于未检查的代理,保存到这个文件
            'checkfail',           # 已经检查，但是被标记为无效的代理,保存到这个文件
            'ok_high_anon',        # 高匿代理(且有效)的代理,按speed排序，最块的放前面
            'ok_anonymous',        # 普通匿名(且有效)的代理,按speed排序，最块的放前面
            'ok_transparent',      # 透明代理(且有效)的代理,按speed排序，最块的放前面
            'ok_other'             # 其他未知类型(且有效)的代理,按speed排序
            ]


#输出数据的格式  支持的数据列有  
# _ip_ , _port_ , _type_ , _status_ , _active_ ,
#_time_added_, _time_checked_ ,_time_used_ ,  _speed_, _area_
                                        
output_head_string=''             # 输出文件的头部字符串
output_format=''                  # 文件数据的格式    
output_foot_string=''             # 输出文件的底部字符串



if   output_type=='xml':
    output_head_string="<?xml version='1.0' encoding='gb2312'?><proxylist>\n" 
    output_format="""<item>
            <ip>_ip_</ip>
            <port>_port_</port>
            <speed>_speed_</speed>
            <last_check>_time_checked_</last_check>
            <area>_area_</area>
        </item>
            """
    output_foot_string="</proxylist>"
elif output_type=='htm':
    output_head_string="""<table border=1 width='100%'>
        <tr><td>代理</td><td>最后检查</td><td>速度</td><td>地区</td></tr>
        """
    output_format="""<tr>
    <td>_ip_:_port_</td><td>_time_checked_</td><td>_speed_</td><td>_area_</td>
    </tr>
    """
    output_foot_string="</table>"
else: 
    output_head_string=''
    output_foot_string=''

if output_type=="csv":
    output_format="_ip_, _port_, _type_,  _speed_, _time_checked_,  _area_\n"

if output_type=="tab":
    output_format="_ip_\t_port_\t_speed_\t_time_checked_\t_area_\n"

if output_type=="txt":
    output_format="_ip_:_port_\n"


# 输出文件的函数
def output_file():
    global output_filename,output_head_string,output_foot_string,output_type
    if output_type=='':
        return
    fnum=len(output_filename)
    content=[]
    for i in range(fnum):
        content.append([output_head_string])
    
    conn.execute("select * from `proxier` order by `active`,`type`,`speed` asc")
    rs=conn.fetchall()
    
    for item in rs:
        type,active=item[2],item[4]
        if   active is None:
            content[0].append(formatline(item))   #未检查
        elif active==0:
            content[1].append(formatline(item))   #非法的代理
        elif active==1 and type==2:
            content[2].append(formatline(item))   #高匿   
        elif active==1 and type==1:
            content[3].append(formatline(item))   #普通匿名  
        elif active==1 and type==0:
            content[4].append(formatline(item))   #透明代理             
        elif active==1 and type==-1:
            content[5].append(formatline(item))   #未知类型的代理
        else:
            pass

    for i in range(fnum):
        content[i].append(output_foot_string)
        f=open(output_filename[i]+"."+output_type,'w')
        f.write(string.join(content[i],''))
        f.close()

#格式化输出每条记录
def formatline(item):
    global output_format
    arr=['_ip_','_port_','_type_','_status_','_active_',
        '_time_added_','_time_checked_','_time_used_',
        '_speed_','_area_']
    s=output_format
    for i  in range(len(arr)):
        s=string.replace(s,arr[i],str(formatitem(item[i],i)))
    return s 


#对于数据库中的每个不同字段，要处理一下，中文要编码，日期字段要转化
def formatitem(value,colnum):
    global output_type
    if (colnum==9):
        value=value.encode('cp936')
    elif value is None:
        value=''

    if colnum==5 or colnum==6 or colnum==7:      #time_xxxed
        value=string.atof(value)
        if value<1:
            value=''
        else:
            value=formattime(value)

    if value=='' and output_type=='htm':value='&#160;'
    return value



def check_one_proxy(ip,port):
    global update_array
    global check_in_one_call
    global target_url,target_string,target_timeout
    
    url=target_url
    checkstr=target_string
    timeout=target_timeout
    ip=string.strip(ip)
    proxy=ip+':'+str(port)
	proxies = {'http': 'http://'+proxy+'/'}
	opener = urllib.FancyURLopener(proxies)
	opener.addheaders = [
        ('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
        ]
	t1=time.time()

	if (url.find("?")==-1):
		url=url+'?rnd='+str(random.random())
	else:
		url=url+'&rnd='+str(random.random())

	try:
		f = opener.open(url)
		s= f.read()		
		pos=s.find(checkstr)
	except:
		pos=-1
		pass
	t2=time.time()	
	timeused=t2-t1
	if (timeused<timeout and pos>0):
        active=1
    else:
        active=0    
    update_array.append([ip,port,active,timeused])
    print len(update_array),' of ',check_in_one_call," ",ip,':',port,'--',int(timeused)    


def get_html(url=''):
	opener = urllib.FancyURLopener({})      #不使用代理
	#www.my-proxy.com 需要下面这个Cookie才能正常抓取
	opener.addheaders = [
            ('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'),
            ('Cookie','permission=1')
            ]
	t=time.time()
	if (url.find("?")==-1):
		url=url+'?rnd='+str(random.random())
	else:
		url=url+'&rnd='+str(random.random())
	try:
		f = opener.open(url)
		return f.read()		
	except:
		return ''	


    

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################


def build_list_urls_1(page=5):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://proxy4free.com/page%(num)01d.html'%{'num':i})		
	return ret

def parse_page_1(html=''):
	matches=re.findall(r'''
            <td>([\d\.]+)<\/td>[\s\n\r]*   #ip
            <td>([\d]+)<\/td>[\s\n\r]*     #port
            <td>([^\<]*)<\/td>[\s\n\r]*    #type 
            <td>([^\<]*)<\/td>             #area 
            ''',html,re.VERBOSE)
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]
		area=match[3]
		if (type=='anonymous'):
			type=1
		elif (type=='high anonymity'):
			type=2
		elif (type=='transparent'):
			type=0
		else:
			type=-1
		ret.append([ip,port,type,area])
        if indebug:print '1',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_2(page=1):
	return ['http://www.digitalcybersoft.com/ProxyList/fresh-proxy-list.shtml']

def parse_page_2(html=''):
	matches=re.findall(r'''
        ((?:[\d]{1,3}\.){3}[\d]{1,3})\:([\d]+)      #ip:port
        \s+(Anonymous|Elite Proxy)[+\s]+            #type
        (.+)\r?\n                                   #area
        ''',html,re.VERBOSE)
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]
		area=match[3]
		if (type=='Anonymous'):
			type=1
		else:
			type=2
		ret.append([ip,port,type,area])
        if indebug:print '2',ip,port,type,area
	return ret


################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_3(page=15):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.samair.ru/proxy/proxy-%(num)02d.htm'%{'num':i})		
	return ret

def parse_page_3(html=''):
	matches=re.findall(r'''
        <tr><td><span\sclass\="\w+">(\d{1,3})<\/span>\. #ip(part1)
        <span\sclass\="\w+">                            
        (\d{1,3})<\/span>                               #ip(part2)
        (\.\d{1,3}\.\d{1,3})                            #ip(part3,part4)

        \:\r?\n(\d{2,5})<\/td>                          #port
        <td>([^<]+)</td>                                #type
        <td>[^<]+<\/td>                                
        <td>([^<]+)<\/td>                               #area
        <\/tr>''',html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]+"."+match[1]+match[2]
		port=match[3]
		type=match[4]
		area=match[5]
		if (type=='anonymous proxy server'):
			type=1
		elif (type=='high-anonymous proxy server'):
			type=2
		elif (type=='transparent proxy'):
			type=0
		else:
			type=-1
		ret.append([ip,port,type,area])
        if indebug:print '3',ip,port,type,area
	return ret



################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################


def build_list_urls_4(page=3):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.pass-e.com/proxy/index.php?page=%(n)01d'%{'n':i})		
	return ret

def parse_page_4(html=''):
	matches=re.findall(r"""
        list
        \('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'        #ip
        \,'(\d{2,5})'                                   #port
        \,'(\d)'                                        #type
        \,'([^']+)'\)                                   #area
        \;\r?\n""",html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]
		area=match[3]
		if (type=='1'):      #type的判断可以查看抓回来的网页的javascript部分
			type=1
		elif (type=='3'):
			type=2
		elif (type=='2'):
			type=0
		else:
			type=-1
        if indebug:print '4',ip,port,type,area            
        area=unicode(area, 'cp936') 
        area=area.encode('utf8')             
		ret.append([ip,port,type,area])
	return ret


################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_5(page=12):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.ipfree.cn/index2.asp?page=%(num)01d'%{'num':i})		
	return ret

def parse_page_5(html=''):
	matches=re.findall(r"<font color=black>([^<]*)</font>",html)	
	ret=[]
	for index, match in enumerate(matches):
		if (index%3==0):
			ip=matches[index+1]
			port=matches[index+2]
			type=-1      #该网站未提供代理服务器类型
            if indebug:print '5',ip,port,type,match 
            area=unicode(match, 'cp936') 
            area=area.encode('utf8') 
			ret.append([ip,port,type,area])			
		else:
			continue
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_6(page=3):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.cnproxy.com/proxy%(num)01d.html'%{'num':i})		
	return ret

def parse_page_6(html=''):
	matches=re.findall(r'''<tr>
        <td>([^&]+)                     #ip
        &#8204&#8205
        \:([^<]+)                       #port
        </td>
        <td>HTTP</td>
        <td>[^<]+</td>
        <td>([^<]+)</td>                #area
        </tr>''',html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=-1          #该网站未提供代理服务器类型
		area=match[2]
        if indebug:print '6',ip,port,type,area
        area=unicode(area, 'cp936') 
        area=area.encode('utf8') 
		ret.append([ip,port,type,area])

	return ret



################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################




def build_list_urls_7(page=1):
	return ['http://www.proxylists.net/http_highanon.txt']

def parse_page_7(html=''):
    matches=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})',html)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=2         
		area='--'
		ret.append([ip,port,type,area])
        if indebug:print '7',ip,port,type,area
	return ret



################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################





def build_list_urls_8(page=1):
	return ['http://www.proxylists.net/http.txt']

def parse_page_8(html=''):
    matches=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})',html)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=-1         
		area='--'
		ret.append([ip,port,type,area])
        if indebug:print '8',ip,port,type,area
	return ret



################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_9(page=6):
	page=page+1
	ret=[]
	for i in range(0,page):
		ret.append('http://proxylist.sakura.ne.jp/index.htm?pages=%(n)01d'%{'n':i})		
	return ret

def parse_page_9(html=''):
    matches=re.findall(r'''
        (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})        #ip
        \:(\d{2,5})                                 #port
        <\/TD>[\s\r\n]*
        <TD>([^<]+)</TD>                            #area
        [\s\r\n]*
        <TD>([^<]+)</TD>                            #type
    ''',html,re.VERBOSE)	
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[3]         
		area=match[2]
        if (type=='Anonymous'):
            type=1
        else:
            type=-1
		ret.append([ip,port,type,area])
        if indebug:print '9',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################


def build_list_urls_10(page=5):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.publicproxyservers.com/page%(n)01d.html'%{'n':i})		
	return ret

def parse_page_10(html=''):
    matches=re.findall(r'''
        (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})    #ip
        <\/td>[\s\r\n]*
        <td[^>]+>(\d{2,5})<\/td>                #port
        [\s\r\n]*
        <td>([^<]+)<\/td>                       #type
        [\s\r\n]*
        <td>([^<]+)<\/td>                       #area
        ''',html,re.VERBOSE)
	ret=[]
	for match in matches:
		ip=match[0]
		port=match[1]
		type=match[2]         
		area=match[3]
        if (type=='high anonymity'):
            type=2
        elif (type=='anonymous'):
            type=1
        elif (type=='transparent'):
            type=0
        else:
            type=-1
		ret.append([ip,port,type,area])
        if indebug:print '10',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################




def build_list_urls_11(page=10):
	page=page+1
	ret=[]
	for i in range(1,page):
		ret.append('http://www.my-proxy.com/list/proxy.php?list=%(n)01d'%{'n':i})

    ret.append('http://www.my-proxy.com/list/proxy.php?list=s1')	
    ret.append('http://www.my-proxy.com/list/proxy.php?list=s2')	
    ret.append('http://www.my-proxy.com/list/proxy.php?list=s3')	    
	return ret

def parse_page_11(html=''):
    matches=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(\d{2,5})',html)	
	ret=[]    

    if (html.find('(Level 1)')>0):
        type=2
    elif (html.find('(Level 2)')>0):
        type=1
    elif (html.find('(Level 3)')>0):
        type=0
    else:
        type=-1

	for match in matches:
		ip=match[0]
		port=match[1]
		area='--'        
		ret.append([ip,port,type,area])
        if indebug:print '11',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################




def build_list_urls_12(page=4):
	ret=[]
    ret.append('http://www.cybersyndrome.net/plr4.html')
    ret.append('http://www.cybersyndrome.net/pla4.html')
    ret.append('http://www.cybersyndrome.net/pld4.html')
    ret.append('http://www.cybersyndrome.net/pls4.html')
	return ret

def parse_page_12(html=''):
    matches=re.findall(r'''
        onMouseOver\=
        "s\(\'(\w\w)\'\)"                           #area
        \sonMouseOut\="d\(\)"\s?c?l?a?s?s?\=?"?
        (\w?)                                       #type    
        "?>
        (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})        #ip
        \:(\d{2,5})                                 #port
        ''',html,re.VERBOSE)	
	ret=[]    
	for match in matches:
		ip=match[2]
		port=match[3]
		area=match[0]
        type=match[1]
        if (type=='A'):
            type=2
        elif (type=='B'):
            type=1
        else:
            type=0
		ret.append([ip,port,type,area])
        if indebug:print '12',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################



def build_list_urls_13(page=3):
    url='http://www.checkedproxylists.com/'
    html=get_html(url)    
    matchs=re.findall(r"""
        href\='([^']+)'>(?:high_anonymous|anonymous|transparent)
        \sproxy\slist<\/a>""",html,re.VERBOSE)    
	return map(lambda x: url+x, matchs)

def parse_page_13(html=''):
    html_matches=re.findall(r"eval\(unescape\('([^']+)'\)",html)	
    if (len(html_matches)>0):
        conent=urllib.unquote(html_matches[0])
    matches=re.findall(r"""<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<\/td>
            <td>(\d{2,5})<\/td><\/tr>""",conent,re.VERBOSE)        
    ret=[]
    if   (html.find('<title>Checked Proxy Lists - proxylist_high_anonymous_')>0):
        type=2
    elif (html.find('<title>Checked Proxy Lists - proxylist_anonymous_')>0):                     
        type=1
    elif (html.find('<title>Checked Proxy Lists - proxylist_transparent_')>0):
        type=0
    else:
        type=-1

	for match in matches:
		ip=match[0]
		port=match[1]
		area='--'
    	ret.append([ip,port,type,area])
        if indebug:print '13',ip,port,type,area
	return ret

################################################################################
#
##        by Go_Rush(阿舜) from http://ashun.cnblogs.com/
#
################################################################################




#线程类

class TEST(threading.Thread):
    def __init__(self,action,index=None,checklist=None):
        threading.Thread.__init__(self)
        self.index =index
        self.action=action
        self.checklist=checklist

    def run(self):
        if (self.action=='getproxy'):
            get_proxy_one_website(self.index)
        else:
            check_proxy(self.index,self.checklist)


def check_proxy(index,checklist=[]):
    for item in checklist:
        check_one_proxy(item[0],item[1])


def patch_check_proxy(threadCount,action=''):
    global check_in_one_call,skip_check_in_hour,conn
    threads=[]
    if   (action=='checknew'):        #检查所有新加入，并且从未被检查过的
        orderby=' `time_added` desc '
        strwhere=' `active` is null '
    elif (action=='checkok'):         #再次检查 以前已经验证成功的 代理
        orderby=' `time_checked` asc '
        strwhere=' `active`=1 '
    elif (action=='checkfail'):       #再次检查以前验证失败的代理
        orderby=' `time_checked` asc '
        strwhere=' `active`=0 '           
    else:                            #检查所有的 
        orderby=' `time_checked` asc '
        strwhere=' 1=1 '           
    sql="""
           select `ip`,`port` FROM `proxier` where
                 `time_checked` < (unix_timestamp()-%(skip_time)01s) 
                 and %(strwhere)01s 
            	 order by %(order)01s 
            	 limit %(num)01d
        """%{     'num':check_in_one_call,
             'strwhere':strwhere,
                'order':orderby,
            'skip_time':skip_check_in_hour*3600}
    conn.execute(sql)
    rows = conn.fetchall()   

    check_in_one_call=len(rows)
    
    #计算每个线程将要检查的代理个数
    if len(rows)>=threadCount:
        num_in_one_thread=len(rows)/threadCount   
    else:
        num_in_one_thread=1

    threadCount=threadCount+1
    print "现在开始验证以下代理服务器....."
    for index in range(1,threadCount):        
     #分配每个线程要检查的checklist,并把那些剩余任务留给最后一个线程               
        checklist=rows[(index-1)*num_in_one_thread:index*num_in_one_thread]     
        if (index+1==threadCount):              
            checklist=rows[(index-1)*num_in_one_thread:]

        t=TEST(action,index,checklist)
        t.setDaemon(True)
        t.start()
        threads.append((t))
    for thread in threads:
        thread.join(60)        
    update_proxies()            #把所有的检查结果更新到数据库
    

def get_proxy_one_website(index):
    global proxy_array
    func='build_list_urls_'+str(index)
    parse_func=eval('parse_page_'+str(index))
    urls=eval(func+'()')
    for url in urls:
        html=get_html(url)
        print url
        proxylist=parse_func(html)
        for proxy in proxylist:
            ip=string.strip(proxy[0])
            port=string.strip(proxy[1])
            if (re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$").search(ip)):
                type=str(proxy[2])
                area=string.strip(proxy[3])
                proxy_array.append([ip,port,type,area])


def get_all_proxies():
    global web_site_count,conn,skip_get_in_hour

    #检查最近添加代理是什么时候，避免短时间内多次抓取
    rs=conn.execute("select max(`time_added`) from `proxier` limit 1")
    last_add=rs.fetchone()[0]
    if (last_add and my_unix_timestamp()-last_add<skip_get_in_hour*3600):   
        print """
 放弃抓取代理列表!
 因为最近一次抓取代理的时间是: %(t)1s
 这个时间距离现在的时间小于抓取代理的最小时间间隔: %(n)1d 小时
 如果一定要现在抓取代理，请修改全局变量: skip_get_in_hour 的值
            """%{'t':formattime(last_add),'n':skip_get_in_hour}
        return
    
    print "现在开始从以下"+str(web_site_count)+"个网站抓取代理列表...."
    threads=[]
    count=web_site_count+1
    for index in range(1,count):
        t=TEST('getproxy',index)
        t.setDaemon(True)
        t.start()
        threads.append((t))
    for thread in threads:
        thread.join(60)         
    add_proxies_to_db()

def add_proxies_to_db():
    global proxy_array
    count=len(proxy_array)
    for i in range(count):
        item=proxy_array[i]
        sql="""insert into `proxier` (`ip`,`port`,`type`,`time_added`,`area`) values
        ('"""+item[0]+"',"+item[1]+","+item[2]+",unix_timestamp(),'"+clean_string(item[3])+"')"        
        try:
            conn.execute(sql)
            print "%(num)2.1f\%\t"%{'num':100*(i+1)/count},item[0],":",item[1]
        except:
            pass 


def update_proxies():
    global update_array
    for item in update_array:
        sql='''
             update `proxier` set `time_checked`=unix_timestamp(), 
                `active`=%(active)01d, 
                 `speed`=%(speed)02.3f                 
                 where `ip`='%(ip)01s' and `port`=%(port)01d                            
            '''%{'active':item[2],'speed':item[3],'ip':item[0],'port':item[1]}
        try:
            conn.execute(sql)    
        except:
            pass 

#sqlite 不支持 unix_timestamp这个函数,所以我们要自己实现
def my_unix_timestamp():
    return int(time.time())

def clean_string(s):
    tmp=re.sub(r"['\,\s\\\/]", ' ', s)
    return re.sub(r"\s+", ' ', tmp)

def formattime(t):
    return time.strftime('%c',time.gmtime(t+8*3600))


def open_database():
    global db,conn,day_keep,dbfile    
    
    try:
        from pysqlite2 import dbapi2 as sqlite
    except:
        print """
        本程序使用 sqlite 做数据库来保存数据，运行本程序需要 pysqlite的支持
        python 访问 sqlite 需要到下面地址下载这个模块 pysqlite,  272kb
        http://initd.org/tracker/pysqlite/wiki/pysqlite#Downloads
        下载(Windows binaries for Python 2.x)
        """
        raise SystemExit

    try:
        db = sqlite.connect(dbfile,isolation_level=None)    
        db.create_function("unix_timestamp", 0, my_unix_timestamp)  
        conn  = db.cursor()
    except:
        print "操作sqlite数据库失败，请确保脚本所在目录具有写权限"
        raise SystemExit

    sql="""
       /* ip:     只要纯ip地址(xxx.xxx.xxx.xxx)的代理 */
       /* type:   代理类型 2:高匿 1:普匿 0:透明 -1: 未知 */
       /* status: 这个字段本程序还没有用到，留在这里作以后扩展*/ 
       /* active: 代理是否可用  1:可用  0:不可用  */ 
       /* speed:  请求相应时间，speed越小说明速度越快 */ 

        CREATE TABLE IF NOT EXISTS  `proxier` (
          `ip` varchar(15) NOT NULL default '',    
          `port` int(6)  NOT NULL default '0',
          `type` int(11) NOT NULL default '-1',    
          `status` int(11) default '0',            
          `active` int(11) default NULL,           
          `time_added` int(11)  NOT NULL default '0',  
          `time_checked` int(11) default '0',      
          `time_used` int(11)  default '0',            
          `speed` float default NULL,             
          `area` varchar(120) default '--',      /*  代理服务器所在位置 */
          PRIMARY KEY (`ip`) 
        );
        /*
        CREATE INDEX IF NOT EXISTS `type`        ON proxier(`type`);
        CREATE INDEX IF NOT EXISTS `time_used`   ON proxier(`time_used`);
        CREATE INDEX IF NOT EXISTS `speed`       ON proxier(`speed`);
        CREATE INDEX IF NOT EXISTS `active`      ON proxier(`active`);
        */
        PRAGMA encoding = "utf-8";      /* 数据库用 utf-8编码保存 */
    """
    conn.executescript(sql)
    conn.execute("""DELETE FROM `proxier`
                        where `time_added`< (unix_timestamp()-?) 
                        and `active`=0""",(day_keep*86400,))      

    conn.execute("select count(`ip`) from `proxier`")
    m1=conn.fetchone()[0]
    if m1 is None:return

    conn.execute("""select count(`time_checked`) 
                        from `proxier` where `time_checked`>0""")
    m2=conn.fetchone()[0]
    
    if m2==0:
        m3,m4,m5=0,"尚未检查","尚未检查"
    else:
        conn.execute("select count(`active`) from `proxier` where `active`=1")
        m3=conn.fetchone()[0]
        conn.execute("""select max(`time_checked`), min(`time_checked`) 
                             from `proxier` where `time_checked`>0 limit 1""")
        rs=conn.fetchone()
        m4,m5=rs[0],rs[1]
        m4=formattime(m4)
        m5=formattime(m5)
    print """
    共%(m1)1d条代理，其中%(m2)1d个代理被验证过，%(m3)1d个代理验证有效。
            最近一次检查时间是：%(m4)1s
            最远一次检查时间是: %(m5)1s
    提示：对于检查时间超过24小时的代理，应该重新检查其有效性
    """%{'m1':m1,'m2':m2,'m3':m3,'m4':m4,'m5':m5}



def close_database():
    global db,conn
    conn.close()
    db.close()
    conn=None
    db=None

if __name__ == '__main__':
    open_database()
    get_all_proxies()
    patch_check_proxy(thread_num)
    output_file() 
    close_database()
    print "所有工作已经完成"
