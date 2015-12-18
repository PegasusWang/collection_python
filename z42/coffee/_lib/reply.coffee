$$reply = $import "/rpc/reply"

_reply_pusher = (old_li, new_li, user_dict) ->
    for i in new_li
        [id, user_id, time, txt, rid, rmer, can_rm] = i
        last = old_li[old_li.length-1]
        if last and rid == last[0].id
            t = last
        else
            t = []
            old_li.push t
        [name, ico] = user_dict[user_id]
        t.push {id, time, user:{id:user_id, ico, name}, txt, can_rm, rmer}
    return old_li

avalon.ui.reply  = (element, data, vmodels) ->
    opt = data.replyOptions
    po_id = opt.id
    view = "reply"+po_id
    height = devicePixelRatio*56
    model = avalon.define(view, (v) ->
        v.$init = ->
            avalon.nextTick(
                () ->
                    element.innerHTML = """
<div ms_view="#{view}">
    <div class="reply-list" ms_class="loading:!live"><div ms_repeat_i="reply_list"><div class="L1">
<div class="content" ms_repeat="i">
    <a ms_if="!el.user.ico" href="javascript:void(0)" class="owner" ms_attr_rel="{{el.user.id}}"></a>
    <a ms_if="el.user.ico" ms_css_background_image="url(#{CONST.SSO.QINIU}/{{el.user.ico}}?imageView2/5/w/#{height}/h/#{height})" href="javascript:void(0)" class="owner" ms_attr_rel="{{el.user.id}}"></a>
    <span ms_click="rm(el)" class="reply_rm" ms_if="el.can_rm&&!el.rmer">+</span>

    <a ms_if="$first" href="javascript:void(0)" class="reply_a" ms_click="reply_show(el,i)">{{$outer.$index+1}}</a>
    <a ms_if="!$first" href="javascript:void(0)" class="reply_ico" ms_click="reply_show(el,i)"></a>
    <div class="box">
    <div class="time"><a href="javascript:void(0)">{{el.user.name}}</a><span>{{$.isotime(el.time)}}</span></div>
    <pre class="L1pre" ms_if="!el.rmer">{{el.txt}}</pre>
    <pre class="L1pre c9" ms_if="el.rmer">内容被 <a href="javascript:void(0);" class="ssoTip" rel="{{el.rmer[0]}}">{{el.rmer[1]}}</a> 删除</pre>
    </div>
</div>
<form ms_if="i[0].id==replying"  class="reply L1reply" ms_submit="submit(i)">
    <div class="textarea-box c">
        <textarea ms_duplex="reply" ms_class="reply{{i[0].id}}"></textarea>
        <button type="submit" class="button">回复</button>
        <span class="key">CTRL+ENTER 快速发布</span>
    </div>
</form>
    </div></div></div>
    <div class="reply0 reply">
        <form class="textarea-box c" ms_submit="submit(0)">
            <textarea ms_duplex="reply0" id="reply0_#{po_id}"></textarea>
            <button type="submit" class="button">发表评论</button>
            <span class="key">CTRL+ENTER 快速发布</span>
        </form>
    </div>
</div>
"""
                    avalon.scan(element, [model].concat(vmodels))
            )
# <!--                            
#                             <div ms_repeat_l3="el[1]" class="L3">
#                                 <div class="content">
#                                     <span class="reply_rm">+</span><a href="javascript:void(0)"><img ms_src="{{l3[0].user.ico}}"></a>
#                                     <pre class="L3pre"><a href="">{{l3[0].user.name}}：</a>{{l3[0].txt}}</pre>
#                                     <div class="time">
#                                         <span>{{$.isotime(l3[0].time)}}</span>
#                                     </div>
#                                 </div>
#                             </div>
# -->

        v.id = po_id
        v.reply_list = []
        v.replying = 0
        replying_by = 0
        v.reply = ''
        v.reply0 = ''
        v.live = 0

        v.rm = (el) ->
            $$reply "rm", el.id, (name)->
                el.rmer = [
                    $.current_user_id,
                    name
                ]


        v.submit = (el) ->
            if $.login()
                if el
                    _ = ""
                    replying_by = 0
                    v.replying = 0
                else
                    _ = 0
                name = 'reply'+_
                txt = v[name]
                if txt
                    txt = txt.trimRight()
                if txt
                    v[name] = ''
                    if el
                        t = el
                    else
                        t = []
                    $$reply "new", [po_id, el and el[el.length-1].id or 0 , txt], (name,ico,reply_id)->
                        t.push {
                            id:reply_id,
                            time:(new Date()).getTime()/1000,
                            txt,
                            user:{ico,id:$.current_user_id,name},
                            can_rm:1,
                            rmer:0
                        }
                        if not el
                            v.reply_list.push t
            return false

        setTimeout(
            ->
                reply0txt = $("#reply0_#{po_id}")

                reply0txt.autosize()

                reply0txt.ctrl_enter ->
                    v.submit()
                
                reply0txt.focus ->
                    $.login()


                $$reply "by_po_id", po_id, (user_dict, reply_list)->
                    model.live = 1
                    model.reply_list = _reply_pusher [], reply_list, user_dict
            300
        )

        v.reply_show = (el, li) ->
            if $.login()
                id = li[0].id
                if v.replying == id and replying_by == el.id
                    v.replying = 0
                    replying_by = 0
                else
                    replying_by = el.id
                    v.replying= id
                    avalon.nextTick(
                        ->
                            txt = $("#slide .reply#{id}").ctrl_enter ->
                                v.submit(li)
                            txt.focus().select().autosize()
                    )
    )

    return model



