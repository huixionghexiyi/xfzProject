/**
 * 这是CMS中的新闻列表，后台管理
 */
function NewsList() {

}

//删除新闻
NewsList.prototype.listenRemoveEvent = function () {
    var removeBtn = $(".remove-btn");
    removeBtn.click(function () {
        var curBtn = $(this);
        xfzalert.alertConfirm({
            'text': "确认删除该新闻吗？删除后不可恢复。",
            'confirmText': '删除',
            confirmCallback: function () {
                var news_id = curBtn.attr("data-news-id");
                $.post({
                    url: '/cms/remove_news/',
                    data: {
                        pk: news_id
                    },
                    dataType: 'json',
                    success: function (result) {
                        if (result['code'] === 200) {
                            window.location.href="/cms/news_list/";
                        } else {
                            xfzalert.alertError(result['message']);
                        }
                    }
                });
            }
        });
    });
}

/**
 * adminLET已经给我们集成了。
 */
NewsList.prototype.listenDatePickerEvent = function () {
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var option = {
        showButtonPanel: true,//是否展示按钮
        format: 'yyyy/mm/dd',//时间格式
        language: 'zh-CN',//语言
        endDate: todayStr,//今日作为截止日期
        todayHighlight:true,//高亮今日
        todayBtn: 'linked',//选中今天
        clearBtn: true,//情况按钮
        autoclose: true,//选择后自动关闭
    }
    startPicker.datepicker(option);
    endPicker.datepicker(option);

}

NewsList.prototype.run = function () {
    self = this;
    self.listenRemoveEvent();
    self.listenDatePickerEvent();
}

$(function () {
    newsList = new NewsList();
    newsList.run();
});