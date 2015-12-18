
uploadComplete = (file)->
    if this.getStats().files_queued > 0
        this.startUpload()

$.fn.extend(
    uploader: (option) ->
        self = this
        if not self[0]
            return
        id = self[0].id
        if self[0].uploader
            return
        
        require(['_lib/swfupload'], () ->
            ## TODO uploader.stop
            self[0].uploader = new SWFUpload({
                upload_url: 'http://upload.qiniu.com/',
                post_params: {},#{"policy": UPYUN[2], "signature": UPYUN[3]},

                file_types_description : "文件",

                upload_complete_handler : uploadComplete,
                upload_progress_handler : option.uploading,
                upload_success_handler : option.uploaded,
#file_queue_error_handler : fileQueueError,
#            upload_start_handler : uploadStart,
#                file_dialog_complete_handler : fileDialogComplete,
#                upload_error_handler : uploadError,
#button_text:self.html()

                button_placeholder_id :id,
                button_width: self.width(),
                button_height: self.height(),
                button_text : '点此上传',
                button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
                button_cursor: SWFUpload.CURSOR.HAND,
                prevent_swf_caching:0,

                flash_url : "http://dn-dfdg.qbox.me/swfupload0.swf",

                debug: false
        })
    )
)
    #
    #    try {
    #        var percent = Math.ceil((bytesLoaded / file.size) * 100);
    #        var progress = new FileProgress(file,  this.customSettings.upload_target);
    #        progress.setProgress(percent);
    #        if (percent === 100) {
    #            if(SWF_TYPE=='blog'){
    #                progress.setStatus("创建缩略图...")
    #            }else if($.inArray(SWF_TYPE,['mp3', 'img', 'show'])){
    #                progress.setStatus("<span style='margin-right:8px;'>"+file.name+"</span><span class='bar_status_text'>上传成功")
    #            }
    #            progress.toggleCancel(false, this);
    #        } else {
    #            if(SWF_TYPE=='mp3'){
    #                $('.upload_hint').remove()
    #                $('.upload_title').css('z-index',4)
    #            }else if(SWF_TYPE=='img'){
    #                $('.upload_hint').remove()
    #            }
    #            var s = this.getStats(),
    #                a = s.successful_uploads+1,
    #                b = s.files_queued + a-1,
    #                str = a+' / '+b,
    #                cont = SWF_TYPE=='img'?str+'<span style="margin-left:12px;">上传中...</span>':'上传中'
    #            progress.setStatus(cont);
    #            progress.toggleCancel(true, this);
    #        }
    #    } catch (ex) {
    #        this.debug(ex);
    #    }

#function uploadSuccess(file, serverData) {
#    try {
#//        alert(this.customSettings.file_mark)
#          var progress = new FileProgress(file,  this.customSettings.upload_target),
#            s = JSON.parse(serverData),
#            me = this
#
#        if(SWF_TYPE == 'blog'){
#            SWF_PIC_NUM++
#            var cont_input = $('.cont_input'),
#                temp_scroll = cont_input.scrollTop()
#            $('#thumbnails').prepend('<div class="thumb_wrap"><img class="thumb" src="http://'+UPYUN[1]+'/'+s.url+'!1"/><div class="rm_pic_wrap"><a class="rm_pic_a" href="javascript:void(0)" rel="'+ SWF_PIC_NUM+'"></a><span class="rm_pic_name">图:'+SWF_PIC_NUM+'</span></div><input type="hidden" name="img" value="'+SWF_PIC_NUM+':'+s['image-width']+':'+s['image-height']+':'+s.url.substr(1)+'"></div>')
#            cont_input.insert_caret(' 图:'+SWF_PIC_NUM + " ")
#            progress.setStatus("<span style='margin-right:8px;'>图 : "+SWF_PIC_NUM+"</span>上传成功");
#            cont_input.scrollTop(temp_scroll)
#        } else if(SWF_TYPE == 'img'){
#            $('.btn_wrap').show()
#            SWF_PIC_NUM++
#            $('.img_wrap').prepend('<div class="img_block"><div class="thumb_wrap"><img class="thumb" src="http://'+UPYUN[1]+s.url+'!1" width="125" height="125" /><div class="rm_pic_wrap"><a class="rm_pic_a" href="javascript:void(0)" rel="'+ SWF_PIC_NUM+'"></a><span class="rm_pic_name">图 : '+SWF_PIC_NUM+'</span></div></div><textarea class="img_txt" placeholder="旁白 ..." name="name"></textarea><input type="hidden" name="size" value="'+s['image-width']+','+s['image-height']+'" /><input type="hidden" name="url" value="'+s.url.substr(1)+'" /></div>')
#         } else if(SWF_TYPE == 'mp3'){
#            $('.progressCancel').addClass('rm_mp3_a')
#            $('.upload_btn').css('background-color','#eee').after('<input type="hidden" name="url" id="mp3_url" value="'+s.url.substr(1)+'" />')
#            $('.rm_mp3_a').click(function(){
#                 if( confirm("确定要删除?")){
#                    $('#mp3_url').remove()
#                    $('.bar_status_text').text('已删除')
#                    $('.upload_btn').css('background-color','#f9f9f9')
#                    me.setStats({successful_uploads:0})
#                    $('.upload_title').css('z-index',1)
#                    $(this).css('visibility','hidden').unbind('click').removeClass('.rm_mp3_a')
#                 }
#             })
#         } else if(SWF_TYPE == 'show'){
#            SWF_PIC_NUM++
#            _img_width = Math.ceil((520/s['image-height'])*s['image-width'])
#            $.postJSON('/j/hi/photo/new',{
#                'url': [s.url.substr(1),s['image-width'],s['image-height']].join(':')
#            }, function(r){
#                if(r.id){
#                    $('#add_pic_block').before($('<div class="show_main_block next_block show_pic_block" style="width:'+_img_width+'px;line-height:0;"><img src="http://'+UPYUN[1]+s.url+'!1" width='+_img_width+' height="520" /><a rel="'+r.id+'" class="hi_pic_rm" href="javascript:void(0)"></a><input type="hidden" class="upload_img_input" value="'+r.id+'" /></div>'))
#                    left_right({img_deal:1})
#                    $('.hi_show_block').css('padding-left',screen_width())
#                }
#            })
#         }
#    } catch (ex) {
#        this.debug(ex);
#    }
#}
