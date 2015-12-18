if not window.console or not window.console.log
    window.console = {
        log : ->
    }

errtip_poshytip = (elem,body) ->
    return {
        set : (v)->
            @reset()
            alignX = elem.data('errtip-alignx') or "right"
            offsetY = 0
            aligny = 'center'
            if elem.prop('tagName') == 'SELECT'
                offsety = -28
                aligny = 'bottom'
            border_css = elem.css('border')
            if border_css.indexOf('none') >= 0 and elem.attr('type') != 'checkbox' and elem.attr('type') != 'submit' and  elem.parents('ul')[0]
                elem.parents('ul').poshytip({className: 'tip-err',showOn:'none',alignTo:'target',alignY:aligny, offsetY:offsety, keepInViewport:false, alignX:alignX,content: v,offsetX: 10,body:elem[0].parentNode}).poshytip('show').addClass('ERR')
            else
                elem.poshytip({className: 'tip-err',showOn:'none',alignTo:'target',alignY:aligny, offsetY:offsety, keepInViewport:false, alignX:alignX,content: v,offsetX: 10,body:elem[0].parentNode}).poshytip('show').addClass('ERR')
            return @
        reset : ->
            elem.poshytip('destroy').removeClass('ERR')
    }

errtip_explain = (elem) ->
    html = elem.data('default')
    if not html
        html = elem.html()
        elem.data('default',html)
    p = elem.parent('.ui-form-item')
    err_cls = 'ui-form-item-error'
    return {
        set : (content)->
            @reset()
            p.addClass(err_cls)
            p.keydown ->
                elem.html(html)
                p.removeClass(err_cls)
            if content
                elem.html(content).fadeOut().fadeIn()
                return @
        reset : ->
            elem.html(html)
            p.removeClass(err_cls)
            false

    }

$(document).ajaxError (event, request, settings) ->
    status = request.status
    if status and status!=200
        alert("出错 : #{status}\n#{settings.url}")


jQuery.fn.extend(
    #yellow_fade :(t=500) ->
    #    _ = $(@)
    #    _.css({backgroundColor: "#ffffcc"}).animate(
    #        {
    #                backgroundColor: "#ffffff"
    #        }, t,
    #        ->
    #            _.css({backgroundColor:''})
    #    )
    #    return _
    #font_fade : (o='red',t=500)->
    #    _ = $(@)
    #    _.css({color:o}).animate(
    #        {
    #                backgroundColor: "#ffffff"
    #        }, t,
    #        ->
    #            _.css({color:'black'})
    #    )
    #    return _

    ctrl_enter : (callback) ->
        $(this).keydown(
            (event) ->
                event = event.originalEvent
                if event.keyCode == 13 and (event.metaKey or event.ctrlKey)
                    callback?()
                    false
        )

    click_drop : (drop, callback1, callback2) ->
        html = $("html,body")
        $(@).click (e)->
            self = @
            self.blur()

            _ = ->
                drop.hide()
                html.unbind 'click' , _
                callback2 and callback2()
            if drop.is(":hidden")
                drop.show()
                e.stopPropagation()
                html.click(_)
                clicked = true
                callback1 and callback1()
            else
                _()

    #just_number : (d) ->
    #    ni = $(@)
    #    if d==undefined or isNaN d or d<0
    #        d=8
    #    re = eval("/\\d*\\.?\\d{0," + d + "}/")
    #    ni.keyup ->
    #        if isNaN ni.val()
    #            ni.addClass('num_err')
    #            ret = re.exec(ni.val())
    #            if ret
    #                ni.val(ret[0])
    #            else
    #                ni.val(0)
    #            ni.removeClass('num_err')
    #        else
    #            ret = re.exec(ni.val())
    #            if ret and ret[0] != ni.val()
    #                ni.val(ret[0])
    #        return
)

jQuery.extend(
    timestampsort : (li) ->
        if not li
            return
        li.sort(
            (a,b)->
                if not a.time
                    return 1
                if not b.time
                    return -1

                if a.time < b.time
                    return 1
                else if a.time > b.time
                    return -1
        )


    isodate : (timestamp) ->
        if timestamp == 1 or timestamp == '1'
            return '至今'
        return $.isotime(timestamp).slice(0,10)

    escape : (txt) -> $('<div/>').text(txt).html()
    html : ->
        r = []
        _ = (o) -> r.push o
        _.html = -> r.join ''
        _
    uid : ->
         (""+ Math.random()).slice(2)

    postJSON : (url, data, callback) ->
        if jQuery.isFunction data
            callback = data
            data = 0

        data = JSON.stringify(data||{})
        if url.indexOf("callback=?") > 0
            data = {"o":data}
            processData = true
            type = 'GET'
        else
            type = 'POST'
            processData = false
        #_xsrf = $.cookie.get("_xsrf")
        #if typeof data=="string"
        #    data+="&_xsrf="+_xsrf
        #else
        #    data._xsrf = _xsrf
        #console.log url, data, callback
        return jQuery.ajax(
            url: url,
            data: data,
            dataType: "json",
            type: type,
            processData:processData,
            success: _ajax_success(callback)
        )

    # error = Err("password",) error.xxx.set
    #
    localtime : (timestamp) ->
      if not timestamp
          return ''
      date = new Date(timestamp * 1000)
      return date.getFullYear()+"年"+date.getMonth()+"月"+date.getDate()+"日"

    isotime : (timestamp) ->
      if not timestamp
          return ''
      date = new Date(timestamp * 1000)
      _result = [date.getFullYear(), date.getMonth() + 1, date.getDate(),  date.getHours() , date.getMinutes() ]
      result = []
      for i in _result
          if i <= 9
              i = "0"+i
          result.push(i)
      [y,m,d,hour,minute] = result
      now = new Date()
      [y,m,d].join("-") + " " + [hour, minute].join(":")

    timeago : (timestamp) ->
      date = new Date(timestamp * 1000)
      ago = parseInt((new Date().getTime() - date.getTime()) / 1000)
      minute = undefined
      if ago <= 0
        return "刚刚"
      else if ago < 60
        return ago + "秒前"
      else
        minute = parseInt(ago / 60)
        return minute + "分钟前"  if minute < 60
      jQuery.isotime(timestamp).split(" ")[0]

    num_format : (num, length) ->
        num = num - 0
        if num < 0.01
            length = 8
        if length
            num = num.toFixed(length)
        return num - 0

    require : (o, name, index="") ->
        err = {}
        for i in name.split(" ")
            if not o[i]
                err[i+index] = ""
        return err

    errtip : (o, focus=1) ->
        elem = $(o)
        if not elem[0]
            return
        if elem[0].tagName == "FORM"
            elem.find("input:first").focus()
            kv = []
            return {
                reset : () ->
                    for i in kv
                        i.reset()
                    kv = []
                set : (o) ->
                    @.reset()

                    if typeof(o) == "string"
                        alert o
                        return 1
                    focused = 0
                    count = 0
                    for k, v of o
                        count += 1
                        t = elem.find("[name=#{k}]") #:visable
                        if not t[0]
                            alert v
                            continue

                        if not focused and t[0].tagName == "INPUT" and focus
                            t.focus().select()
                            focused = 1
                        explain = t.parents('.ui-form-item').find('.ui-form-explain')
                        if explain.length
                            tiper = errtip_explain(explain)
                        else
                            tiper = errtip_poshytip(t)
                        if t[0].tagName == "INPUT" or t[0].tagName == "SELECT"
                            if not focused and focus
                                t.focus().select()
                                focused = 1
                            if t[0].type == "checkbox"
                                event = "change"
                            else
                                event = "keypress"
                            t.bind("#{event}.errtip", ->
                                tiper.reset()
                                t.unbind('keypress.errtip')
                            )
                        _ = tiper.set(v)
                        if _
                            kv.push _
                    return count
            }
)


$.ajaxSetup({
    beforeSend: (jqXHR, settings) ->
        jqXHR.url = settings.url
})
$._AJAXING = {}
_ajax_success = (callback) ->
    _ = (data, textStatus, jqXHR) ->
        if data and data.err
            err = data.err
            callback?.end?()
            #TODO
            if err.code == 403
                return $$('ANGELCRUNCH/auth/login')
            else if err.html
                return $.dialog("err",{content:error.html})
            else if err.script
                return eval(err.script)

        if callback
            callback(data, textStatus, jqXHR)
    return _

jQuery.getJSON = ( url , data , callback , cache=0) ->
    if jQuery.isFunction data
        cache = callback
        callback = data
        data = 0
    return jQuery.ajax(
        url: url,
        cache: cache or false,
        data: data or {},
        dataType: "json",
        type: "GET",
        success: _ajax_success(callback)
    )

jQuery.getUser = ->
    user_id = $.cookie.get("S")
    if user_id
        return user_id
    return 0

$.whenScroll = (pos_get, more_than, less_than) ->
    body = $ window
    top = body.scrollTop()
    pos = 0

    resize = ->
        setTimeout(
            ->
                pos = pos_get()
                _top = body.scrollTop()
                if  _top > pos
                    more_than()
                else if  _top < pos
                    less_than()

            10
        )
    when_change = ->
        _top = body.scrollTop()
        if  top <= pos and _top > pos
            more_than()
        else if top >= pos and _top < pos
            less_than()

        top = _top

    body.resize(resize).scroll when_change
    resize()


$.loader = {
    show:->
        if not this._timer
            this._timer = setTimeout(
                ->
                    if not $("#spin")[0]
                        $("body").append('<div id="spin"></div>')
                        try
                            delete this._timer
                        catch e
                            #IE8 fix
                            this.removeAttribute _timer if this.removeAttribute
                300
            )
    hide:->
        clearTimeout(this._timer)
        try
            delete this._timer
        catch e
            #IE8 fix
            this.removeAttribute _timer if this.removeAttribute
        $("#spin").remove()

}
ajaxing = ( func) ->
    return (url, data, callback, cache=false) ->
        if $._AJAXING[url]
            return
        $._AJAXING[url] = 1
        if jQuery.isFunction data
            cache = callback
            callback = data
            data = 0
        #fancybox = $.fancybox
        $.loader.show()
        _callback = (data, textStatus, jqXHR) ->
            if callback
                callback(data, textStatus, jqXHR)
            end()
        _callback.end = end = ->
            $.loader.hide()
            delete $._AJAXING[url]
        func(
            url, data, _callback, cache
        ).fail(end)

$.postJSON1 = ajaxing($.postJSON)
$.getJSON1 = ajaxing($.getJSON)
$.get1 = ajaxing($.get)
$.post1 = ajaxing($.post)
#$.postJSON1(" http://sso.istarsea.me/auth.ob_new_by_mail?callback=jQuery11110669746409368233_1413519962329&o=%7B%22app_id%22%3A9812522%2C%22code%22%3A%222J2tNuziU3qMdgeF9JMIXzt3h66M4lQeGAuVFfa-z2GBpG1haWyoenNAZy5jb20%22%2C%22mail%22%3A%22zs%40g.com%22%2C%22name%22%3A%22%22%2C%22password%22%3A%22%22%2C%22url%22%3A%22http%3A%2F%2Fistarsea.me%2Frpc%2Fauth%2Flogin%22%7D&_=141351996233").fail(function(){alert(1)})


$.get_current_user = ->
    s = $.cookie.get("S")
    if s
        $.current_user_id = s.split(".")[0] - 0
        $.current_user = {
            id : $.current_user_id
            url : "//#{$.current_user_id}.#{CONST.HOST}"
        }
$.get_current_user()



$.dialog = (id, html, option) ->
    if $("#"+id)[0]
        return
    elem = $ html
    elem.attr 'id' , id
    if 'modal' not in option
        option.modal = true
    if 'resizable' not in option
        option.resizable = false
    elem.dialog(option)

doc = $ document
$.scrollTop = (top=0)->
    $("html,body").animate(scrollTop:top)


RE_CNCHAR = /[^\x00-\x80]/g

_cnenlen = (str) ->
    if typeof str == "undefined"
        return 0

    aMatch = str.match RE_CNCHAR

    str.length + if !aMatch then 0 else aMatch.length

$.cnenlen = (str) ->
    Math.ceil(_cnenlen($.trim(str)) / 2)


$.login = ->
    if $.current_user_id
        return 1
    else
        $$('ANGELCRUNCH/auth/login')
        return false

$.login_dialog = (id, html, option) ->
    if $.login()
        $.dialog(id, html, option)
