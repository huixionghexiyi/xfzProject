function News() {

};

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

News.prototype.run = function () {
    var self = this;
    self.listenUploadImgEvent();
}
$(function () {
    var news = new News();
    news.run();
});