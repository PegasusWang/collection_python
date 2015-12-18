$import = (config)->
    for name, path of config
        window["$$#{name}"] = (args , callback)->
            for funcname, kwds of args
                if $.isFunction(kwds)
                    callback = kwds
                    kwds = {}
                $.getJSON1(
                    "#{path}/#{name}.#{funcname}?callback=?",
                    {
                        o:JSON.stringify(kwds)
                    }
                    callback
                )
                break

#$import auth: "https://mysso.sinaapp.com"
#
#$$auth login : {
#    account : "hi"
#    password : "xxx"
#}, (r)->
#    console.log(r)
