#coding:utf-8

PAGE_LIMIT = 42

PAGE_NO_TEMPLATE = """<a href="%s">%s</a>"""

def limit_offset(n, limit):
    if n:
        try:
            n = int(n)
        except ValueError:
            n = 1
    else:
        n = 1

    offset = 0
    if n <= 0:
        offset = -n
        n = (-n+limit)//limit
        list_limit = max(n*limit - offset, 1)
    else:
        offset = (n-1)*limit
        list_limit = limit
    return n, list_limit, offset

def page_limit_offset(href, count, n, limit=PAGE_LIMIT):
    now, list_limit, offset = limit_offset(n, limit)
    page_common = str(_Page(
        href, count, now, limit
    ))
    page_simple = page_prev_next(href, count, n, limit)
    page = Page(page_common)
    page.make_page(page_simple)
    return page, list_limit, offset

def page_prev_next(href, count, n, limit, class_name=['pre_po', 'next_po'], void_class_name='void_po', prev_next=('&lt;', '&gt;')):
    '''
    用于只需要上一页，下一页的情况
    '''
    now, list_limit, offset = limit_offset(n, limit)
    tmp = '<a class="%s" href="%s">%s</a>'
    style = 'style="color:#ccc;"'
    tmp_void = '<span class="%s">%s</span>'
    total = count/limit
    if count%limit != 0:
        total += 1
    prev = tmp%(class_name[0], href%(now-1), prev_next[0])
    next = tmp%(class_name[1], href%(now+1), prev_next[1])
    if now <= 1:
        prev = tmp_void%(void_class_name, prev_next[0])
    if now >= total:
        next = tmp_void%(void_class_name, prev_next[1])
    return prev, next


class Page(str):
    def __init__(self, arg):
        super(Page, self).__init__()
        self._prev = self._next = ''

    def make_page(self, arg):
        self._prev, self._next = arg

    @property
    def prev(self):
        return self._prev

    @property
    def next(self):
        return self._next


class _Page(object):
    limit = PAGE_LIMIT
    def __init__(self, href, count, now, limit=PAGE_LIMIT, template='<div class="page">%s</div>'):
        now = int(now)
        if now <= 0:
            now = 1

        end = (count+limit-1)//limit
        if now > end:
            now = end

        self.now = now

        self.total = (count+limit-1)//limit
        self.href = href
        self.template = template
        self.limit = limit

    def __str__(self):
        href = self.href
        total = self.total
        now = self.now

        scope = 2

        if total > 1:
            merge_begin = None
            merge_end = None
            omit_len = scope+3

            if total <= (scope+omit_len+1):
                begin = 1
                end = total
            else:
                if now > omit_len:
                    merge_begin = True
                    begin = now-scope
                else:
                    begin = 1

                if total - now >= omit_len:
                    merge_end = True
                    end = now+scope
                else:
                    end = total

                if end - begin < scope*2:
                    if now <= omit_len:
                        end = min(begin + scope*2, total)
                    else:
                        begin = max(end - scope*2, 1)

                    if begin > omit_len:
                        merge_begin = True
                    else:
                        merge_begin = False
                        begin = 1

                    if total - end >= omit_len:
                        merge_end = True
                    else:
                        merge_end = False
                        end = total
            links = []
            if now > 1:
                links.append(
                    PAGE_NO_TEMPLATE%(href%(now-1), '&lt;')
                )
            else:
                links.append('<span class="plt">&lt;</span>')

            if merge_begin:
                links.append(
                    PAGE_NO_TEMPLATE%(href%1, 1)+' ... '
                )

                show_begin_mid = False

                if begin > 8:
                    show_begin_mid = begin//2

                if show_begin_mid:
                    links.append(
                        PAGE_NO_TEMPLATE%(href%show_begin_mid, show_begin_mid) + '...'
                    )

            for i in xrange(begin, now):
                links.append(
                    PAGE_NO_TEMPLATE%(href%i, i)
                )

            links.append("""<span class="now">%s</span>"""%now)

            for i in xrange(now+1, end+1):
                links.append(
                    PAGE_NO_TEMPLATE%(href%i, i)
                )


            if merge_end:
                #          show_end_mid = False

                #          if total - end > 8:
                #              show_end_mid = (total+end+1)//2

                #          if show_end_mid:
                #              links.append(
                #                  "..." + PAGE_NO_TEMPLATE%(href%show_end_mid, show_end_mid)
                #              )

                links.append(
                    ' ... ' #+ PAGE_NO_TEMPLATE%(href%total, total)
                )

            if now < total:
                links.append(
                    PAGE_NO_TEMPLATE%(href%(now+1), '&gt;')
                )
            else:
                links.append(
                    """<span class="pgt">&gt;</span>"""
                )
            htm = ''.join(links)
            return self.template%htm
        return ''

if __name__ == '__main__':
    pass
