jQuery.extend({
    cookie : {
        set:function(dict, option){
            option = option || {};
            var expires = option.expires || 365,
                path = option.path||'/',
                domain = option.domain,
                date = new Date();

            if(!domain){
                domain="."+CONST.HOST;
            }
            date.setTime(date.getTime()+(expires*24*60*60*1000));
            expires = "; expires="+date.toGMTString();
            for (var i in dict){
                document.cookie = i+"="+dict[i]+expires+"; path="+path+"; domain="+domain;
            }
        },
        get:function(name) {
            var e = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(e) == 0) {
                    return c.substring(e.length,c.length).replace(/\"/g,'');
                }
            }
            return null;
        }
    }
});
//设置根HOST (根据TLD)
(function(){
    CONST = window.CONST||{};
    var host_list = location.hostname.split('.'), key = "_COOKIE_", cookie=jQuery.cookie, o={}, host;
    o[key] = 0;
    for(var i=2;i<=host_list.length;++i){
        host = host_list.slice(-i).join(".")
        cookie.set(o , {domain:host,expires:0.01})
        if(cookie.get(key)=='0'){
            CONST.HOST = host; 
            break;
        }
    }
    cookie.set(o,{expires:-1, domain:host})
})();

