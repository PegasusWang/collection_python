fancybox = $.fancybox 
require_loading = (url, callback)->

    timeout = setTimeout(
        -> 
            $.loader.show() 
        250
    )
    
    require(
        [
            url
        ]
        ->
            clearTimeout(timeout)
            $.loader.hide() 
            callback()
    )

url_name_func = (name) ->
    _ = name.split(".",2)
    if _.length == 2
        [url, name] = _
    else
        url = name
        name = ""
    _ = url.split("/")
    t = jQuery
    for i in _[..-2]
        t = (t[i] = t[i] || {})
     
    return [url, name]

func_by_name = (name) ->
    t = jQuery
    for i in name.split("/")
        t = t?[i]
    return t

window.$$ = $$ = (name, params...) ->
    [url, name] = url_name_func(name)
    if name
        name = "/"+name
    action = url+name
    func = func_by_name action
    if func
        func.apply(func, params)
    else
        require_loading(
            url
            ->
                t = func_by_name action
                t.apply(t,params)
        )


$$.on = (event, css,  js) ->
    [url, name] = url_name_func(js)
    _event = event+"."+$.uid()
    _ = $(document)
    _.on(
        _event 
        css
        ->
            _.off(_event)         
            self = @
            require_loading(
                url 
                ->
                    t = func_by_name(name)
                    t.apply(self)
                    _.on(event, css, t)
            )
    )


window.$import = (path)->
    return (funcname, kwds , callback)->
        if $.isFunction(kwds)
            callback = kwds
            kwds = 0
        if callback
            _callback = callback
            callback = (r) ->
                if $.isArray(r)
                    _callback.apply(_callback, r)
                else
                    _callback(r)

        if ( path.indexOf('//'+CONST.HOST) == 0 or (path.charAt(0) == '/' and path.charAt(1)!="/"))
            suffix = ""
        else
            suffix = "?callback=?"

        $.postJSON1(
            "#{path}.#{funcname}#{suffix}"
            kwds
            callback
        )

#$import auth: "https://mysso.sinaapp.com"
#
#$$auth login : {
#    account : "hi"
#    password : "xxx"
#}, (r)->
#    console.log(r)
#
#$$auth login : ["hi","xxx"], (r)->
#    console.log(r)
#
#$$auth login : "hi", (r)->
#    console.log(r) 
