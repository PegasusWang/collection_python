var SWF_PIC_NUM = 0,
    TIMEOUT,
    SWF_TYPE = ''

function fileQueueError(file, errorCode, message) {
    try {
        var errorName = "";
        if (errorCode === SWFUpload.errorCode_QUEUE_LIMIT_EXCEEDED) {
            errorName = "You have attempted to queue too many files.";
        }

        if (errorName !== "") {
            alert(errorName);
            return;
        }

        switch (errorCode) {
        case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
            break;
        case SWFUpload.QUEUE_ERROR.FILE_EXCEEDS_SIZE_LIMIT:
            break;
        case SWFUpload.QUEUE_ERROR.QUEUE_LIMIT_EXCEEDED:
            alert('一次最多上传'+this.settings.file_upload_limit+'个')
            break;
        case SWFUpload.QUEUE_ERROR.ZERO_BYTE_FILE:
        case SWFUpload.QUEUE_ERROR.INVALID_FILETYPE:
        default:
            alert(message);
            break;
        }
    } catch (ex) {
        this.debug(ex);
    }

}

function fileDialogComplete(numFilesSelected, numFilesQueued) {
    try {
        if (numFilesQueued > 0) {
            this.startUpload();

        }
    } catch (ex) {
        this.debug(ex);
    }
}

function uploadProgress(file, bytesLoaded) {

    try {
        var percent = Math.ceil((bytesLoaded / file.size) * 100);
        var progress = new FileProgress(file,  this.customSettings.upload_target);
        progress.setProgress(percent);
        if (percent === 100) {
            if(SWF_TYPE=='blog'){
                progress.setStatus("创建缩略图...")
            }else if($.inArray(SWF_TYPE,['mp3', 'img', 'show'])){
                progress.setStatus("<span style='margin-right:8px;'>"+file.name+"</span><span class='bar_status_text'>上传成功")
            }
            progress.toggleCancel(false, this);
        } else {
            if(SWF_TYPE=='mp3'){
                $('.upload_hint').remove()
                $('.upload_title').css('z-index',4)
            }else if(SWF_TYPE=='img'){
                $('.upload_hint').remove()
            }
            var s = this.getStats(),
                a = s.successful_uploads+1,
                b = s.files_queued + a-1,
                str = a+' / '+b,
                cont = SWF_TYPE=='img'?str+'<span style="margin-left:12px;">上传中...</span>':'上传中'
            progress.setStatus(cont);
            progress.toggleCancel(true, this);
        }
    } catch (ex) {
        this.debug(ex);
    }
}

function uploadStart(file){
    SWF_TYPE = this.customSettings.file_mark
    $('#upload_guide').hide()

}

function uploadSuccess(file, serverData) {
    try {
//        alert(this.customSettings.file_mark)
          var progress = new FileProgress(file,  this.customSettings.upload_target),
            s = JSON.parse(serverData),
            me = this

        if(SWF_TYPE == 'blog'){
            SWF_PIC_NUM++
            var cont_input = $('.cont_input'),
                temp_scroll = cont_input.scrollTop()
            $('#thumbnails').prepend('<div class="thumb_wrap"><img class="thumb" src="http://'+UPYUN[1]+'/'+s.url+'!1"/><div class="rm_pic_wrap"><a class="rm_pic_a" href="javascript:void(0)" rel="'+ SWF_PIC_NUM+'"></a><span class="rm_pic_name">图:'+SWF_PIC_NUM+'</span></div><input type="hidden" name="img" value="'+SWF_PIC_NUM+':'+s['image-width']+':'+s['image-height']+':'+s.url.substr(1)+'"></div>')
            cont_input.insert_caret(' 图:'+SWF_PIC_NUM + " ")
            progress.setStatus("<span style='margin-right:8px;'>图 : "+SWF_PIC_NUM+"</span>上传成功");
            cont_input.scrollTop(temp_scroll)
        } else if(SWF_TYPE == 'img'){
            $('.btn_wrap').show()
            SWF_PIC_NUM++
            $('.img_wrap').prepend('<div class="img_block"><div class="thumb_wrap"><img class="thumb" src="http://'+UPYUN[1]+s.url+'!1" width="125" height="125" /><div class="rm_pic_wrap"><a class="rm_pic_a" href="javascript:void(0)" rel="'+ SWF_PIC_NUM+'"></a><span class="rm_pic_name">图 : '+SWF_PIC_NUM+'</span></div></div><textarea class="img_txt" placeholder="旁白 ..." name="name"></textarea><input type="hidden" name="size" value="'+s['image-width']+','+s['image-height']+'" /><input type="hidden" name="url" value="'+s.url.substr(1)+'" /></div>')
         } else if(SWF_TYPE == 'mp3'){
            $('.progressCancel').addClass('rm_mp3_a')
            $('.upload_btn').css('background-color','#eee').after('<input type="hidden" name="url" id="mp3_url" value="'+s.url.substr(1)+'" />')
            $('.rm_mp3_a').click(function(){
                 if( confirm("确定要删除?")){
                    $('#mp3_url').remove()
                    $('.bar_status_text').text('已删除')
                    $('.upload_btn').css('background-color','#f9f9f9')
                    me.setStats({successful_uploads:0})
                    $('.upload_title').css('z-index',1)
                    $(this).css('visibility','hidden').unbind('click').removeClass('.rm_mp3_a')
                 }
             })
         } else if(SWF_TYPE == 'show'){
            SWF_PIC_NUM++
            _img_width = Math.ceil((520/s['image-height'])*s['image-width'])
            $.postJSON('/j/hi/photo/new',{
                'url': [s.url.substr(1),s['image-width'],s['image-height']].join(':')
            }, function(r){
                if(r.id){
                    $('#add_pic_block').before($('<div class="show_main_block next_block show_pic_block" style="width:'+_img_width+'px;line-height:0;"><img src="http://'+UPYUN[1]+s.url+'!1" width='+_img_width+' height="520" /><a rel="'+r.id+'" class="hi_pic_rm" href="javascript:void(0)"></a><input type="hidden" class="upload_img_input" value="'+r.id+'" /></div>'))
                    left_right({img_deal:1})
                    $('.hi_show_block').css('padding-left',screen_width())
                }
            })
         }
    } catch (ex) {
        this.debug(ex);
    }
}

function uploadComplete(file) {
    try {

        /*  I want the next upload to continue automatically so I'll call startUpload here */
        if (this.getStats().files_queued > 0) {
            this.startUpload();
        } else {
            var progress = new FileProgress(file,  this.customSettings.upload_target);
            progress.setComplete();
            var show = SWF_TYPE=='mp3'?true:false
            progress.toggleCancel(show);
        }

    } catch (ex) {
        this.debug(ex);
    }
}

function uploadError(file, errorCode, message) {
    var progress;
    try {
        switch (errorCode) {
        case SWFUpload.UPLOAD_ERROR.FILE_CANCELLED:
            try {
                progress = new FileProgress(file,  this.customSettings.upload_target);
                progress.setCancelled();
                progress.setStatus("上传取消");
                progress.toggleCancel(false);
            }
            catch (ex1) {
                this.debug(ex1);
            }
            break;
        case SWFUpload.UPLOAD_ERROR.UPLOAD_STOPPED:
            try {
                progress = new FileProgress(file,  this.customSettings.upload_target);
                progress.setCancelled();
                progress.setStatus("Stopped");
                progress.toggleCancel(true);
            }
            catch (ex2) {
                this.debug(ex2);
            }
        case SWFUpload.UPLOAD_ERROR.UPLOAD_LIMIT_EXCEEDED:
            break;
        default:
            alert(message);
            break;
        }
    } catch (ex3) {
        this.debug(ex3);
    }
}

function fadeIn(element, opacity) {
    var reduceOpacityBy = 5;
    var rate = 30;  // 15 fps


    if (opacity < 100) {
        opacity += reduceOpacityBy;
        if (opacity > 100) {
            opacity = 100;
        }

        if (element.filters) {
            try {
                element.filters.item("DXImageTransform.Microsoft.Alpha").opacity = opacity;
            } catch (e) {
                // If it is not set initially, the browser will throw an error.  This will set it if it is not set yet.
                element.style.filter = 'progid:DXImageTransform.Microsoft.Alpha(opacity=' + opacity + ')';
            }
        } else {
            element.style.opacity = opacity / 100;
        }
    }

    if (opacity < 100) {
        setTimeout(function () {
            fadeIn(element, opacity);
        }, rate);
    }
}



/* ******************************************
 *  FileProgress Object
 *  Control object for displaying file info
 * ****************************************** */

function FileProgress(file, targetID) {
    this.file_id = file.id
    this.fileProgressID = "divFileProgress";

    this.fileProgressWrapper = document.getElementById(this.fileProgressID);
    clearTimeout(TIMEOUT)
    $('#divFileProgressContainer').show()
    if (!this.fileProgressWrapper) {
        this.fileProgressWrapper = document.createElement("div");
        this.fileProgressWrapper.className = "progressWrapper";
        this.fileProgressWrapper.id = this.fileProgressID;

        this.fileProgressElement = document.createElement("div");
        this.fileProgressElement.className = "progressContainer";

        var progressCancel = document.createElement("a");
        progressCancel.className = "progressCancel";
        progressCancel.href = "#";
        progressCancel.style.visibility = "hidden";
        progressCancel.appendChild(document.createTextNode(" "));

        var progressText = document.createElement("div");
        progressText.className = "progressName";
        progressText.appendChild(document.createTextNode(file.name));

        var progressBar = document.createElement("div");
        progressBar.className = "progressBarInProgress";

        var progressStatus = document.createElement("div");
        progressStatus.className = "progressBarStatus";
        progressStatus.innerHTML = "&nbsp;";

        this.fileProgressElement.appendChild(progressCancel);
        this.fileProgressElement.appendChild(progressText);
        this.fileProgressElement.appendChild(progressStatus);
        this.fileProgressElement.appendChild(progressBar);

        this.fileProgressWrapper.appendChild(this.fileProgressElement);

        document.getElementById(targetID).appendChild(this.fileProgressWrapper);
        fadeIn(this.fileProgressWrapper, 0);

    } else {
        this.fileProgressElement = this.fileProgressWrapper.firstChild;
        this.fileProgressElement.childNodes[1].firstChild.nodeValue = file.name;
    }

    this.height = this.fileProgressWrapper.offsetHeight;

}


FileProgress.prototype.setProgress = function (percentage) {
    this.fileProgressElement.className = "progressContainer green";
    this.fileProgressElement.childNodes[3].className = "progressBarInProgress";
    this.fileProgressElement.childNodes[3].style.width = percentage + "%";
};
FileProgress.prototype.setComplete = function () {
    this.fileProgressElement.className = "progressContainer blue";
    this.fileProgressElement.childNodes[3].className = "progressBarComplete";
    this.fileProgressElement.childNodes[3].style.width = "";
    if(SWF_TYPE=='blog'){
        TIMEOUT = setTimeout(function(){$('#divFileProgressContainer').hide()},6000)
    }
    if(SWF_TYPE=='show'){
        $('#divFileProgressContainer').hide()
        $('#upload_guide').show()
    }
};
FileProgress.prototype.setError = function () {
    this.fileProgressElement.className = "progressContainer red";
    this.fileProgressElement.childNodes[3].className = "progressBarError";
    this.fileProgressElement.childNodes[3].style.width = "";

};
FileProgress.prototype.setCancelled = function () {
    this.fileProgressElement.className = "progressContainer";
    this.fileProgressElement.childNodes[3].className = "progressBarError";
    this.fileProgressElement.childNodes[3].style.width = "";
    $('.upload_title').css('z-index',1)
};
FileProgress.prototype.setStatus = function (status) {
    this.fileProgressElement.childNodes[2].innerHTML = status;
};

FileProgress.prototype.toggleCancel = function (show, swfuploadInstance) {
    this.fileProgressElement.childNodes[0].style.visibility = show ? "visible" : "hidden";
    if (swfuploadInstance) {
        var fileID = this.file_id;
        this.fileProgressElement.childNodes[0].onclick = function () {
            swfuploadInstance.cancelUpload(fileID);
            return false;
        };
    }
};

function swfupload(o) {
    if(window.IMG_DATA){
        var D = IMG_DATA
        for(var i=0;i<D.length;i++){
            var d = D[i],
                num = d[0],
                url = d[1],
                _ = d[2].split(',')
                width = _[0],
                height = _[1]
            $('#thumbnails').prepend('<div class="thumb_wrap"><img class="thumb" src="http://'+UPYUN[1]+'/'+url+'!1"/><div class="rm_pic_wrap"><a class="rm_pic_a" href="javascript:void(0)" rel="'+ num +'"></a><span class="rm_pic_name">图:'+ num +'</span></div><input type="hidden" name="img" value="'+ num +':'+width+':'+height+':'+url+'"></div>')
        }
        SWF_PIC_NUM = D[D.length-1][0]-0
    }
};
