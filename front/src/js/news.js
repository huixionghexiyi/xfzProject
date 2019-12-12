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

News.prototype.listenQiniuUploadImgEvent = function () {
    self = this;
    var uploadBtn = $('#thumbnail-btn');
    var thumbnailUrl = $('#thumbnail-form');
    uploadBtn.change(function () {
        $.get({
            url: '/cms/qn_token/',
            dataType: "json",
            success: function (result) {
                if (result['code'] === 200) {
                    var file = uploadBtn[0].files[0];
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

                }
            }
        })

    })
}

News.listenQiniuObserver = {
    next: function (response) {
        var total = response.total;
        var percent = total.percent;
        console.log(percent);
    },
    error: function (response) {
        console.log(response.message);
    },
    complete: function (response) {
        console.log(response);
    }
}
//上传到七牛云
News.prototype.run = function () {
    var self = this;
    // self.listenUploadImgEvent();
    self.listenQiniuUploadImgEvent();
}
$(function () {
    var news = new News();
    news.run();
});