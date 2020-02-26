function NewsList() {

}
//监听发布评论的按钮
NewsList.prototype.listenSubmitEvent = function () {
    var self = this;
    var submitBtn = $(".submit_btn");
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr("data-news-id");
        $.post({
            url: '/news/comment/',
            data: {
                news_id: news_id,
                content: content
            },
            success: function (result) {
                if (result['code'] === 200) {
                    var comment = result['data'];
                    var tpl = template("comment-item", { "comment": comment });
                    var ul = $(".comment_list");
                    ul.prepend(tpl);
                    window.messageBox.showSuccess("评论发表成功~");
                    textarea.val("");
                } else {
                    window.messageBox.showError(result['message']);
                }
            }
        });
    })
}

NewsList.prototype.run = function () {
    self = this;
    self.listenSubmitEvent();
}

$(function () {
    var newsList = new NewsList();
    newsList.run();
})