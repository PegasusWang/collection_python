BUSINESS = {"l1":["电子商务", "移动互联网", "游戏", "旅游", "教育", "金融", "社交", "硬件", "能源", "医疗", "餐饮", "企业", "平台", "汽车", "数据"," 娱乐"]}

$.fn.extend({
    business_tag : (options) ->
        self = @
        @.tagit(options).tagit('instance').tagInput.parents('ul').click (e)->
            if e.target == this or e.target.className.indexOf('ui-autocomplete-input') >= 0
                dialog = $.dialog(
                    "dialog_place",
                    """
    <div class="multi-layer" ms_view="multi_layer">
        <div class="first-layer fn-clear c">
            <span ms_repeat="first_layer" class="fixed" ms_click="click1($index, el)" ms_class="checked:checked1==$index">{{el}}</span>
        </div>
        <!--
        <div class="second-layer perfect-scroll">
            <ul class="float-left">
                <li ms_click="click2($index, el)"ms_repeat="second_layer"><span class="fixed">{{el}}</span></li>
            </ul>
        </div>
        -->
        <div class="direct-search fn-clear c">
            <input placeholder="" id="direct-search">
            <div id="bottom">
                <div class="dialog-palce-tip" id="dialog-palce-tip">最多填写5个</div>
                <a href="javascript:void(0);" id="remove-all">清空</a>
                <button class="ui-button-mblue ui-button"ms_click="submit">确定</button>
            </div>
        </div>
    </div>
                    """,
                    {
                        width:632
                        title : "选择或输入关注的领域"
                        create: ->
                            that = $("#direct-search").tagit({
                                tagLimit: 5
                                onTagLimitExceeded: ->
                                    $('#dialog-palce-tip').fadeIn().fadeOut().fadeIn().fadeOut().fadeIn()

                            })
                            for i in self.tagit('assignedTags')
                                that.tagit('createTag', i)
                            $('#remove-all').click ->
                                $("#direct-search").tagit("removeAll")
                            width = 500
                            height = 300
            #                $(".perfect-scroll").width(width).height(height)
            #                $('.perfect-scroll').perfectScrollbar('update')
            #                $('.perfect-scroll').perfectScrollbar()
                            def_view(
                                'multi_layer'
                                (v) ->
                                    v.o = ""
                                    v.first_layer = BUSINESS.l1
                                    # v.second_layer = BUSINESS.l2[0]
                                    v.checked1 = 0
                                    v.checked2 = 0
                                    v.click1 = (index, el)->
                                        v.checked1 = index
                                        that.tagit('createTag', el)
    #                                    v.second_layer = BUSINESS.l2[index]
    #                                    if not v.second_layer.length
    #                                        that.tagit('createTag', el)
    #                                v.click2 = (index, el)->
    #                                    v.checked2 = index
    #                                    that.tagit('createTag', el)
                                    v.submit = (el)->
                                        # 1 empty 2 for and createTag 3 close
                                        self.tagit('removeAll')
                                        for i in that.tagit('assignedTags')
                                            self.tagit('createTag', i)
                                        dialog.dialog('close')
                            )
                    }
                )
            this
})
