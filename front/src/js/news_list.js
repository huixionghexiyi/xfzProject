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
                            window.location.reload();
                        } else {
                            xfzalert.alertError(result['message']);
                        }
                    }
                });
            }
        });
    });
}

//日期选择
NewsList.prototype.listenDatePickerEvent = function () {
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var option = {
        showButtonPanel: true,
        format: 'yyyy/mm/dd',
        language: 'zh-CN',
        endDate: todayStr,
        todayHighlight:true,
        todayBtn: 'linked',
        clearBtn: true,
        autoclose: true,
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