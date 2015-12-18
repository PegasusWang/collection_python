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
            alert('最多上传'+this.settings.file_upload_limit+'个')
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

function uploadProgress(file, bytesLoaded,bytesAll) {

    try {
        var percent = Math.ceil((bytesLoaded / bytesAll) * 100);
        var progress = new FileProgress(file,  this.customSettings.upload_target);
        progress.setProgress(percent);
        if (percent === 100) {
        //progress.setStatus("<span style='margin-right:8px;'>"+file.name+"</span><span class='bar_status_text'>上传成功")
            progress.setStatus("")
            progress.toggleCancel(false, this);
        } else {
            var s = this.getStats(),
                a = s.successful_uploads+1,
                b = s.files_queued + a-1,
                str = a+' / '+b,
                cont = SWF_TYPE=='img'?str+'<span style="margin-left:12px;">上传中...</span>':'上传中'
            //progress.setStatus(cont);
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
    var s=JSON.parse(serverData)
    var name=file.name
    if(name.length>20){
        name=name.substr(0,16)+"..."
    }
    $("#img_list").prepend("<li id="+s.key+" class='line'><span class='left'>"+name+"<span class='img_span'><a class='img_del' href='javascript:void(o));'></a></span></span></li>")
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
    return new SWFUpload({
        // Backend Settings
        upload_url:"https://up.qbox.me/",
        flash_url:"https://dn-less.qbox.me/swfupload.swf",
        flash9_url:"https://dn-less.qbox.me/swfupload_fp9.swf",
        post_params: o.post_params,
        // File Upload Settings
        file_size_limit : o.size + " MB",
        file_types : o.type,//
        file_types_description : o.type_des,//"JPG Images",
        file_upload_limit : o.limit,

        // Event Handler Settings - these functions as defined in Handlers.js
        //  The handlers are not part of SWFUpload but are part of my website and control how
        //  my website reacts to the SWFUpload events.
        file_queue_error_handler : fileQueueError,
        file_dialog_complete_handler : fileDialogComplete,
        upload_progress_handler : uploadProgress,
        upload_error_handler : uploadError,
        upload_success_handler : uploadSuccess,
        upload_complete_handler : uploadComplete,
        upload_start_handler : uploadStart,

        // Button Settings
        button_placeholder_id : o.btn,
        button_width: o.btn_width,//126
        button_height: o.btn_height,//44
        button_text : '',
        button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
        button_cursor: SWFUpload.CURSOR.HAND,
        prevent_swf_caching:0,

        // Flash Settings

        custom_settings : {
            upload_target : "divFileProgressContainer",
            file_mark : o.mark
        },
        // Debug Settings
        file_post_name : 'file',
        //debug: false
        debug: true
    });
};
