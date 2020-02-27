function News() {
};
//上传到本地
News.prototype.listenUploadImgEvent = function () {
    var uploadBtn = $("#thumbnail-btn");
    var thumbnailUrl = $('#thumbnail-form');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        $.post({
            url: '/cms/upload_file/',
            data: formData,
            processData: false, //这是告诉jquery不要再处理了
            contentType: false, //告诉jquery不要添加内容，就以二进制形式传递
            success: function (result) { 
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    thumbnailUrl.val(url);
                }
            }
        })
    });
}

//上传到七牛云
News.prototype.listenQiniuUploadImgEvent = function () {
    self = this;
    var uploadBtn = $('#thumbnail-btn');
    var thumbnailUrl = $('#thumbnail-form');

    uploadBtn.change(function () {
        //获取七牛的Token,只需要获取到正确可用的token值，就能从前端你直接传递图片到七牛云。而不需要通过后端服务器
        $.get({
            url: '/cms/qn_token/',
            dataType: "json",
            success: function (result) {
                if (result['code'] === 200) {
                    var file = uploadBtn[0].files[0];
                    console.log(result['data']['token']);
                    var token = result['data']['token'];
                    var key = (new Date()).getTime() + '.' + file.name.split('.').pop();
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpg', 'image/gif', 'image/jpeg'],
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 5,
                        regions: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    //用于获取返回值
                    var listenQiniuObserver = {
                        next: function (response) {
                            var total = response.total;
                            var percent = total.percent;
                            var percentText = percent.toFixed(0) + "%";
                            var progressBar = $('#progress-bar');
                            progressBar.css({ "width": percent + "%" });
                            progressBar.text(percentText);
                            console.log(percent);
                        },
                        error: function (response) {
                            console.log(response.message);
                        },
                        complete: function (response) {
                            console.log(response);
                        }
                    }
                    var subscription = observable.subscribe(listenQiniuObserver);
                } else {
                    alert("bad");
                }
            }
        })

    })
}

//监听创建/修改新闻事件
News.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submitBtn");
    submitBtn.click(function (event) {
        event.preventDefault();//阻止默认的提交事件
        var btn = $(this);
        var pk = btn.attr('data-news-id');
        url = '';
        if (pk) {
            url = '/cms/edit_news/';
        } else {
            url = '/cms/write_news/';
        }
        var title = $("#title-form").val();
        var category = $("#category-form").val();
        var desc = $("#desc-form").val();
        var thumbnail = $("#thumbnail-form").val();
        var content = window.editor.getValue();
        $.post({
            url: url,
            data: {
                title: title,
                category: category,
                desc: desc,
                thumbnail: thumbnail,
                content: content,
                pk: pk
            },
            success: function (result) {
                if (result['code'] === 200) {
                    if (pk) {
                        xfzalert.alertSuccess('新闻修改成功', function () {
                            window.location.reload();
                        });
                    } else {
                        xfzalert.alertSuccess('新闻发布成功', function () {
                            window.location.reload();
                        });
                    }
                } else {
                    var messageObject = result['message'];
                    if (typeof messageObject == 'string' || messageObject.constructor == String) {
                        xfzalert.alertError(result['message']);
                    } else {
                        for (var key in messageObject) {
                            var message = messageObject[key];
                            var message = message[0];
                            xfzalert.alertError(message);
                        }
                    }
                }
            }
        });
    });
}


// 初始化富文本编辑器
News.prototype.initSimditor = function () {
    window.editor = new Simditor({
        textarea: $('#content-form'),
        placeholder: "在此编辑你的文章",
        upload: {
            url: '/cms/upload_content_img/',
            fileKey: 'upload_file',
            leaveConfirm: '图片正在上传，确定离开吗？',
            params: null
        }
    });
}



//启动监听
News.prototype.run = function () {
    var self = this;
    self.listenUploadImgEvent();
    // self.listenQiniuUploadImgEvent();
    self.initSimditor();
    self.listenSubmitEvent();
    // self.listenRemoveEvent();

}
$(function () {
    var news = new News();
    news.run();
});