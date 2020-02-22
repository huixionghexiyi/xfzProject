function Banners() {

}

/**
 * 加载轮播图的数据
 */
Banners.prototype.loadData = function () {
    self = this;
    $.get({
        url: '/cms/banner_list/',
        success: function (result) {
            if (result['code'] === 200) {
                var banners = result['data'];
                for (var i = 0; i < banners.length; i++) {
                    self.createBannerItem(banners[i]);
                }
            }
        }
    })

}
/**
 * 调用createBanner创建一个新的banner
 */
Banners.prototype.listenAddBanner = function () {
    self = this;
    var addBtn = $("#add-banner-btn");
    addBtn.click(function () {
        var bannerListGroup = $(".banner-list-group");
        var length = bannerListGroup.children().length;
        if (length >= 6) {
            window.messageBox.showInfo("最多添加6个");
            return;
        }
        self.createBannerItem();
    });
}

/**
 * 创建一个bannerItem
 */
Banners.prototype.createBannerItem = function (banner) {// 一开始加载的时候,如果有一个调用一次这个方法，并传日参数banner
    // 其中banner是后端传递的数据
    var tpl = template("banner-item", { "banner": banner });
    var bannerListGroup = $(".banner-list-group");
    var bannerItem = null;
    if (banner) {
        //如果bannerItem存在,即自动加载的bannerItem
        bannerListGroup.append(tpl);
        //获取当前添加的banner,羡慕要给他绑定事件:save、addImage、remove
        bannerItem = bannerListGroup.find(".banner-item:last");
    } else {
        //如果不存在,即点击创建按钮创建的bannerItem
        bannerListGroup.prepend(tpl);
        //下面给他绑定事件：
        bannerItem = bannerListGroup.find(".banner-item:first");
    }
    //绑定事件:保存图片、saveBanner、删除
    self.addImageSelectEvent(bannerItem);
    self.removeBannerEvent(bannerItem);
    self.saveBannerEvent(bannerItem);
}

/**
 * 点击图片更换轮播图
 */
Banners.prototype.addImageSelectEvent = function (bannerItem) {
    //先拿到image标签
    //通过bannerItem找到 .image-input
    var image = bannerItem.find(".thumbnail");
    var imageInput = bannerItem.find('.image-input');
    // 点击图片的时候,就触发一个input的点击事件
    image.click(function () {
        imageInput.click();
    });
    // 当input按钮选中 文件的时候触发
    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file", file);
        $.post({
            url: '/cms/upload_file/',
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['code'] === 200) {
                    //返回一个url
                    var url = result['data']['url'];
                    // 修改图片的url
                    image.attr('src', url);
                }
            }
        })
    });
}

/**
 * 保存事件
 */
Banners.prototype.saveBannerEvent = function (bannerItem) {
    var saveBtn = bannerItem.find(".save-btn");
    // 三个变量
    saveBtn.click(function () {
        var image_url = bannerItem.find(".thumbnail");
        var priority = bannerItem.find("input[name='priority']");
        var link_to = bannerItem.find("input[name='link_to']");
        var bannerId = bannerItem.attr('data-banner-id');
        var bannerSpan = bannerItem.find('#priority-span');
        var url = '';
        if (bannerId) {
            console.log(bannerId);
            url = '/cms/edit_banner/'
        } else {
            url = '/cms/save_banner/'
        }
        $.post({
            url: url,
            data: {
                banner_id: bannerId,
                image_url: image_url.attr("src"),
                priority: priority.val(),
                link_to: link_to.val(),
            },
            success: function (result) {
                if (result['code'] === 200) {
                    console.log(result);
                    if (bannerId) {
                        messageBox.showSuccess("轮播图修改成功");
                    } else {
                        bannerId = result['data']['banner_id'];
                        messageBox.showSuccess("轮播图添加成功");
                        bannerItem.attr('data-banner-id', bannerId);
                    }
                    //修改banner左上角的显示
                    bannerSpan.text("优先级:" + priority.val());

                } else {
                    console.log(result);
                }
            }
        });
    });
}

/**
 * 删除事件
 */
Banners.prototype.removeBannerEvent = function (bannerItem) {
    //从当前的bannerItem中找到关闭的按钮
    var closeBtn = bannerItem.find('.close-btn');
    closeBtn.click(function () {
        var bannerId = bannerItem.attr("data-banner-id");
        if (bannerId) {
            xfzalert.alertConfirm({
                'title': "确定删除轮播图？",
                'confirmCallback': function () {
                    console.log("确定删除");
                    $.post({
                        url: '/cms/remove_banner/',
                        data: {
                            banner_id: bannerId
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                messageBox.showSuccess('删除成功');
                                bannerItem.remove();
                            } else {
                                console.log("fail");
                            }
                        }
                    })
                }
            });
        } else {
            bannerItem.remove();
        }
    });
}

Banners.prototype.run = function () {
    self = this;
    self.listenAddBanner();
}

$(function () {
    var banners = new Banners();
    banners.run();
    banners.loadData();
});