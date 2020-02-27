function Courses() {

};

Courses.prototype.initSimditor = function () {
    window.editor = new Simditor({
        textarea: $('#desc-input'),
        placeholder: "在此编辑你的简介",
        upload: {
            url: '/cms/upload_content_img/',
            fileKey: 'upload_file',
            leaveConfirm: '图片正在上传，确定离开吗？',
            params: null
        }
    });
};

Courses.prototype.listenSubmitBtn = function () {
    var submitBtn = $("#submitBtn");
    submitBtn.click(function (event) {
        event.preventDefault();//阻止自动提交事件
        var title = $("#title-input").val();
        var category_id = $("#category-input").val();
        var teacher_id = $("#teacher-input").val();
        var video_url = $("#video-addr-input").val();
        var cover_url = $("#cover-input").val();
        var price = $("#price-input").val();
        var duration = $("#duration-input").val();
        var profile = window.editor.getValue();
        console.log("=== submit");
        $.post({
            url: '/cms/pub_courses/',
            data: {
                title: title,
                teacher_id: teacher_id,
                category_id: category_id,
                video_url: video_url,
                price: price,
                duration: duration,
                cover_url: cover_url,
                profile: profile,
            },
            success: function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess('课程添加成功', function () {
                        // window.location.reload();
                    });
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
Courses.prototype.run = function () {
    var self = this;
    self.initSimditor();
    self.listenSubmitBtn();

}
$(function () {
    var courses = new Courses();
    courses.run();
});