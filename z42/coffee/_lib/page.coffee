formatstr = (href, template, page, txt) ->
  href = href.replace("$page", page)
  template = template.replace('%s', href)
  template = template.replace('%s', txt)
  return template

$.page = (href, count, limit, now, template = "<a href=\"%s\">%s</a>") ->
  if not count
    return ''
  now = parseInt(now)
  now = 1  if now <= 0
  end = Math.floor((count + limit - 1) / limit)
  now = end  if now > end
  scope = 2
  total = Math.floor((count + limit - 1) / limit)
  if total > 1
    merge_begin = false
    merge_end = false
    omit_len = scope + 3
    if total <= (scope + omit_len + 1)
      begin = 1
      end = total
    else
      if now > omit_len
        merge_begin = true
        begin = now - scope
      else
        begin = 1
      if (total - now) >= omit_len
        merge_end = true
        end = now + scope
      else
        end = total
      if (end - begin) < (scope * 2)
        if now <= omit_len
          end = Math.min(begin + scope * 2, total)
        else
          begin = Math.max(end - scope * 2, 1)
        unless begin > omit_len
          merge_begin = false
          begin = 1
        unless (total - end) >= omit_len
          merge_end = false
          end = total
  links = []
  if now > 1
    pageLink = formatstr(href, template, now - 1, "上一页")
    links.push pageLink
  else
    links.push "<span class=\"plt\">上一页</span>"
  if merge_begin
    pageLink = formatstr(href, template, 1, 1)
    pageLink += "..."
    links.push pageLink
    show_begin_mid = false
    show_begin_mid = Math.floor(begin / 2)  if begin > 8
    if show_begin_mid
      pageLink = formatstr(href, template, show_begin_mid, show_begin_mid)
      pageLink += "..."
      links.push pageLink
  i = begin
  while i < now
    pageLink = formatstr(href, template, i, i)
    links.push pageLink
    i++
  spanNow = "<span class=\"now\">%s</span>"
  spanNow = spanNow.replace(/%s/, now)
  links.push spanNow
  i = now + 1
  while i < end + 1
    pageLink = formatstr(href, template, i, i)
    links.push pageLink
    i++
  links.push "..."  if merge_end
  if now < total
    pageLink = formatstr(href, template, now + 1, "下一页")
    links.push pageLink
  else
    links.push "<span class=\"pgt\">下一页</span>"
  htm = ""
  i = 0
  while i < links.length
      htm += links[i]
      i++

  return htm

$.fn.page = (url,  callback , route, prefix="")->
    _ = (page)->
        if $.isFunction(url)
            _url = url()
        else
            _url = url

        url_page = prefix+":"+page

        if _url.indexOf("?") == -1
            _url = _url+url_page
        else
            arr = _url.split('?')
            _url = "#{arr[0]}#{url_page}?#{arr[1]}"
        if not location.hash
            location.hash = url_page
            return
        $.getJSON1(
            _url
            (r) ->
                page = page - 0
                total = r.pop()
                limit = r.pop()
                o = {
                    page:page
                    limit:limit
                    total:total
                    li:r
                }
                callback(o)
                $.scrollTop(0)
                self.html $.page("##{prefix}:$page",total, limit, page)
             true
        )
    self = $ @
    if route
        pager = (_prefix, page)->
            prefix = _prefix
            _(page)
        _route = route(pager)
    else
        _route = {
            ":(\\d+)" : _
        }

    Router(_route).init()

    if not location.hash
        _ 1


