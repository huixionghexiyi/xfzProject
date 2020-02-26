/**
 * 轮播的横幅对象
 */
function Banner() {
    this.bannerWidth = 795;
    this.bannerGroup = $("#banner_gruop");//获取标签
    this.bannerUl = $("#banner_ul");
    //当这个对象被创建的时候就会执行该方法
    this.index = 1;//定义全局的变量,控制轮播图
    //获取左右两个箭头
    this.leftArrow = $("#left_arrow");
    this.rightArrow = $("#right_arrow");
    //获取bannerUl中的li的数量
    this.liList = this.bannerUl.children("li");
    //获取page_control
    this.pageControl = $("#page_control");
    //获取li的数量
    this.bannerCount = this.liList.length;
}

/**
 * 初始化initBanner
 */
Banner.prototype.initBanner = function () {
    var self = this;
    //获取第一个banner和最后一个用于实现无限循环轮播
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone();
    this.bannerUl.append(firstBanner);//第一张加到最后面
    this.bannerUl.prepend(lastBanner);//最后一张加到最前面
    this.bannerUl.css({ "width": (self.bannerCount + 2) * self.bannerWidth, "left": -self.bannerWidth });
}
/**
 * 初始化小圆点，pageContorl
 */
Banner.prototype.initPageControl = function () {
    var self = this;
    var pageControl = $(".page_control");
    for (var i = 0; i < self.bannerCount; i++) {
        //$("li")获取所有li元素，$("<li></li>")创建一个li标签
        var circle = $("<li></li>");
        //添加到pageControl中
        pageControl.append(circle);
        if (i === 0) {
            circle.addClass("active");
        }
    }
    //10是每个圆的大小，16是一个圆两边的间距。
    pageControl.css({ "width": self.bannerCount * (16 + 10) });
}

/**
 * 箭头的隐藏和显示
 */
Banner.prototype.toggleArrow = function (isShow) {
    if (isShow) {
        this.leftArrow.show();
        this.rightArrow.show();
    } else {
        this.leftArrow.hide();
        this.rightArrow.hide();
    }
}
/**
 * 滑动到下一个横幅
 */
Banner.prototype.animate = function () {
    var self = this;
    //设置滑动的方向和花费的时间。
    this.bannerUl.stop().animate({ "left": -self.bannerWidth * self.index }, 500);
    //设置pageControl
    var index = self.index;
    if (index === 0) {
        index = self.bannerCount - 1;
    } else if (index === self.bannerCount + 1) {
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pageControl.children('li').eq(index).addClass("active").siblings().removeClass("active");
};

/**
 * 执行定时器方法循环轮播
 */
Banner.prototype.loop = function () {
    var self = this;
    //定时器,Banner对象的timer指向该定时器
    self.timer = setInterval(function () {
        //由于bannerCount的值并没有改变，所以+1
        if (self.index >= self.bannerCount + 1) {
            //如果是倒数第二张，强制跳转，并没有特效，这样用户就看不出来，
            self.bannerUl.css({ "left": -self.bannerWidth });
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
        //通过self.index查询找到是第几个，再修改class的名称以达到修改颜色的功能。修改为无线循环后，该功能就放到self.animate()中了
        // self.pageControl.children("li").eq(self.index).addClass("active").siblings().removeClass("active")
    }, 2000);
};

/**
 * 监听pageControl点击事件
 */

Banner.prototype.listenPageCotrol = function () {
    var self = this;
    //each是遍历所有节点，会传递index序号和该节点对象到function中。
    self.pageControl.children("li").each(function (index, obj) {
        $(obj).click(function () {
            //修改Banner中的index为当前index
            self.index = index;
            //再调用animate方法跳转到对应页面就可以了
            self.animate();
            //修改小圆点颜色,并将其兄弟元素设置为透明。因为再css中，设置了active为白色。
            $(obj).addClass("active").siblings().removeClass("active");

        });
    })

}


/**
 * 监听鼠标的移入/移出
 */
Banner.prototype.listenBannerHover = function () {
    //将self指向当前的Banner对象
    var self = this;
    self.bannerGroup.hover(
        //传入两个函数
        function () {
            //鼠标移到banner上时执行
            //关闭定时器cleraInterval，js内置方法
            clearInterval(self.timer);
            self.toggleArrow(true);
        },
        function () {
            //鼠标移走时执行
            self.loop();//
            self.toggleArrow(false);

        });
}
/**
 * 监听箭头的点击
 */
Banner.prototype.listenArrowClick = function () {
    var self = this;
    //监听左边
    self.leftArrow.click(function () {
        if (self.index === 0) {
            self.bannerUl.css({ "left": -self.bannerWidth * self.bannerCount });
            self.index = self.bannerCount - 1;
        } else {
            self.index--;
        }
        self.animate();
    });
    //监听右边
    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({ "left": -self.bannerWidth });
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    });
};

/**
 * Banner执行run方法，相当于启动所有和Banner相关的功能，这里只有一个轮播功能。
 */
Banner.prototype.run = function () {

    //执行轮播图
    this.loop();
    //执行箭头点击监听事件
    this.listenArrowClick();
    //执行监听鼠标放到banner上的事件
    this.listenBannerHover();
    // 初始化pageControl，小点点
    this.initPageControl();
    //初始化横幅
    this.initBanner();
    this.listenPageCotrol();

}
// 【加载更多】的对象
function Index() {
    var self = this;
    self.page = 2; //第一页已经自动加载了，所以从第二页开始
    self.category_id = 0;

}
Index.prototype.listenMoreNewsEvent = function () {
    var self = this;
    moreNewsBtn = $("#load-more-btn");
    moreNewsBtn.click(function () {
        $.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                category_id: self.category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data'];
                    if (newses.length > 0) {
                        var tpl = template("news-item", { "newses": newses });
                        var ul = $(".list_inner_group");
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        moreNewsBtn.hide();
                    }
                }
            }
        });
    })
}

Index.prototype.listenCategorySwitchEnvet = function () {
    var self = this;
    var tabGroup = $(".list_tab");
    var listGroup = $(".list_inner_group");
    moreNewsBtn = $("#load-more-btn");
    tabGroup.children().click(function () {
        var li = $(this);
        var category_id = li.attr("date-category");
        $.get({
            url: '/news/list/',
            data: {
                category_id: category_id
            },
            dataType: 'json',
            success: function (result) {
                if (result['code'] === 200) {
                    // console.log(result['data']);
                    var newses = result['data'];
                    var tpl = template("news-item", { "newses": newses });
                    listGroup.empty();
                    listGroup.append(tpl);
                    li.addClass('active').siblings().removeClass('active');
                    self.category_id = category_id;
                    self.page = 2;
                    moreNewsBtn.show();

                }
            }

        })
    })
}
Index.prototype.run = function () {
    self = this;
    self.listenMoreNewsEvent();
    self.listenCategorySwitchEnvet();
}
/**
 * 页面加载完毕执行的方法
 */

$(function () {
    var banner = new Banner();
    var index = new Index();
    index.run();
    banner.run();
});