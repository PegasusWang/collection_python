# coding:utf-8


def cnenlen(s):
    if type(s) is str:
        s = s.decode('utf-8', 'ignore')
    return len(s.encode('gb18030', 'ignore')) // 2


def cnencut(s, length):
    ts = type(s)
    if ts is str:
        s = s.decode('utf-8', 'ignore')
    s = s.encode('gb18030', 'ignore')[:length * 2].decode('gb18030', 'ignore')
    if ts is str:
        s = s.encode('utf-8', 'ignore')
    return s


def cnenoverflow(s, length):
    txt = cnencut(s, length)
    if txt != s:
        #txt = '%s ...' % txt.rstrip()
        txt = '%s … …' % txt.rstrip()
        has_more = True
    else:
        has_more = False
    return txt, has_more


def txt_rstrip(txt):
    if type(txt) is unicode:
        txt = txt.encode('utf-8', 'ignore')
    return '\n'.join(
        map(
            str.rstrip,
            txt.replace('\r\n', '\n')
               .replace('\r', '\n').rstrip('\n ')
               .split('\n')
        )
    )


def make_tag_list(tag_txt):
    _tag_list = txt_rstrip(tag_txt).split('\n')
    result = []
    for i in _tag_list:
        tag = i.strip()
        if not tag:
            continue
        if tag not in result:
            result.append(tag)
    return result

if __name__ == '__main__':
    pass
