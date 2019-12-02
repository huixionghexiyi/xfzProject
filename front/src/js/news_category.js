function NewCategory() {

};
NewCategory.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDelCategoryEvent();
}
NewCategory.prototype.listenAddCategoryEvent = function () {
    var add_btn = $("#add-btn");
    add_btn.click(function () {
        xfzalert.alertOneInput({
            'title': "添加新闻分类",
            'placeholder': "请输入新闻分类",
            "confirmCallback": function (inputValue) {
                $.ajax({
                    'url': "/cms/add_news_category/",
                    'data': {
                        'name': inputValue
                    },
                    'type': 'POST',
                    'dataType': 'json',
                    success: function (result) {
                        if (result['code'] === 200) {
                            console.log(result);
                            window.location.reload();
                        } else {
                            // xfzalert.close();
                            xfzalert.alertError(result['message']);
                        }
                    }
                });
            }
        })
    });
}
NewCategory.prototype.listenEditCategoryEvent = function () {
    var editBtn = $('.edit_btn');
    editBtn.click(function () {
        var curBtn = $(this);
        var tr = curBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        xfzalert.alertOneInput({
            'title': '请编辑',
            'placeholder': '请输入新分类名称',
            'value': name,
            'confirmCallback': function (inputValue) {
                $.post({
                    'url': '/cms/edit_news_category/',
                    'data': {
                        'pk': pk,
                        'name': inputValue,
                    },
                    'type': 'post',
                    dataType: 'json',
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload();
                        } else {
                            var messageObject = result['message']
                            //如果返回的是字符串
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
                })
            }
        });
    });
}

NewCategory.prototype.listenDelCategoryEvent = function () {
    var self = this;
    var delBtn = $('.del_btn');
    delBtn.click(function () {
        var curBtn = $(this);
        var tr = curBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            title: '确定删除吗？',
            confirmText: '删除',
            confirmCallback: function () {
                $.post({
                    url: '/cms/del_news_category/',
                    data: {
                        pk: pk
                    },
                    dataType: 'json',
                    type: 'post',
                    success: function (result) {
                        if (result['code'] === 200) {
                            window.location.reload();
                        } else {
                            xfzalert.alertError(result['message']);
                        }
                    }
                })
            }
        })
    });
};

$(function () {
    var newCategory = new NewCategory();
    newCategory.run();
});