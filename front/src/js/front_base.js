/**
 * 用于监听导航中的用户Box
 */
function FrontBase() { }

FrontBase.prototype.run = function () {
    var self = this;
    self.listenAuthBoxHover();
}
/**
 * 如果已经登录，鼠标放到用户名上会弹出box
 */
FrontBase.prototype.listenAuthBoxHover = function () {
    var authBox = $(".auth-box");
    var userMoreBox = $(".user-more-box");
    authBox.hover(function () {
        userMoreBox.show();
    }, function () {
        userMoreBox.hide();
    });
}

/**
 * 用户鉴权验证，即登录/注册
 */
function Auth() {
    var self = this;
    self.scrollGroup = $('.scroll_group');
    self.telephoneInput = $(".signup_group input[name='telephone']");// 注册的电话
    self.sendSmsBtn = $("#sendSmsBtn");//发送短信验证按钮    
}

//展示登录注册弹窗
function showEvent() {
    var mask_wrapper = $(".mask_wrapper");
    mask_wrapper.show();
};

//隐藏登录注册弹窗
function hideEvent() {
    var mask_wrapper = $(".mask_wrapper");
    mask_wrapper.hide();
};

//监听
Auth.prototype.listenEvent = function () {
    var self = this;
    var signinBtn = $(".signin");
    var signupBtn = $(".signup");
    var closeBtn = $(".close_btn");
    var switchBtn = $(".switch");
    var imgCaptcha = $(".img_captcha");
    // 监听右上角登录按钮
    signinBtn.click(function () {
        showEvent();
        var scrollGroup = $('.scroll_group');
        scrollGroup.css({ "left": 0 });
    });
    // 监听右上角注册按钮
    signupBtn.click(function () {
        showEvent();
        var scrollGroup = $('.scroll_group');
        scrollGroup.css({ "left": -400 });
    });
    // 监听鉴权弹窗关闭按钮
    closeBtn.click(function () {
        var mask_wrapper = $(".mask_wrapper");
        mask_wrapper.hide();
    });
    // 监听切换登录注册按钮
    switchBtn.click(function () {
        var scrollGroup = $('.scroll_group');
        var currentLeft = scrollGroup.css("left");

        currentLeft = parseInt(currentLeft);
        if (currentLeft < 0) {
            scrollGroup.animate({ "left": '0px' });
        } else {
            scrollGroup.animate({ "left": '-400px' });
        }
    });
    // 点击图片更换图片验证码
    imgCaptcha.click(function () {
        //src被重写设置的时候会重写访问。不然重复内容的访问不会被执行。
        imgCaptcha.attr("src", "/account/img_captcha/" + "?random=" + Math.random());
    });
}
// 监听请求按钮
Auth.prototype.listenRequestEvent = function () {
    var self = this;
    var signinGroup = $(".signin_group");//登录 
    var signupGroup = $(".signup_group");//注册
    //登录的信息
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");
    //注册的信息
    var logupTelInput = signupGroup.find("input[name='telephone']");
    var usernameInput = signupGroup.find("input[name='username']");
    var logupPwd1Input = signupGroup.find("input[name='pwd1']");
    var logupPwd2Input = signupGroup.find("input[name='pwd2']");
    var imgCaptchaInput = signupGroup.find("input[name='img_captcha']");
    var smsCaptchaInput = signupGroup.find("input[name='sms_captcha']");
    //按钮
    var loginBtn = signinGroup.find(".submit_btn");//登录按钮
    var logupBtn = signupGroup.find(".submit_btn");//注册按钮
    var logoutBtn = $("#logout_btn");//退出登录(没有使用)

    //listen Enter 给body标签绑定一个键盘按钮
    $("body").bind("keyup", function (event) {
        // 按下回车触发登录事件(如果是在注册界面也是出发登录事件)
        if (event.keyCode == "13") {
            // console.log("login");
            loginBtn.click();
        }
    });
    //登录
    loginBtn.click(function () {
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.prop("checked");
        $.post(
            "/account/login/",
            {
                'telephone': telephone,
                'password': password,
                'remember': remember ? 1 : 0
            },
            function (result) {
                // console.log(result);
                if (result['code'] == 200) {
                    hideEvent();
                    window.location.reload();
                } else {
                    //如果不为200 那么返回的值就是
                    var messageObject = result['message']
                    //如果返回的参数是字符串
                    if (typeof messageObject == 'string' || messageObject.constructor == String) {
                        window.messageBox.show(messageObject, "info");
                        //如果返回的参数不是字符串
                    } else {
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message, "error");
                        }
                    }
                }
            }

        );
    });
    //注册
    logupBtn.click(function () {
        var logupTel = logupTelInput.val();
        var username = usernameInput.val();
        var logupPwd1 = logupPwd1Input.val();
        var logupPwd2 = logupPwd2Input.val();
        var imgCaptcha = imgCaptchaInput.val();
        var smsCaptcha = smsCaptchaInput.val();
        console.log(logupPwd2);
        $.ajax({
            url: "/account/register/",
            type: "POST",
            dataType: "json",
            data: {
                telephone: logupTel,
                username: username,
                password1: logupPwd1,
                password2: logupPwd2,
                img_captcha: imgCaptcha,
                sms_captcha: smsCaptcha,
            },
            success: function (result) {
                if (result['code'] == 200) {
                    window.location.reload();
                } else {
                    //如果不为200 那么返回的值就是
                    var messageObject = result['message']
                    //如果返回的参数是字符串
                    if (typeof messageObject == 'string' || messageObject.constructor == String) {
                        window.messageBox.show(messageObject, "info");
                        //如果返回的参数不是字符串
                    } else {
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message, "error");
                        }
                    }
                }
            },
            fail: function () {
                window.messageBox.show("系统错误", "error");
            }
        });
    });
    //退出
    //使用{% url 'xfzauth:logout %}'替代了
    logoutBtn.click(function () {
        $.ajax({
            url: "account/logout",
            type: "GET",
            dataType: "json",
            data: {},
            success: function (result) {
                console.log("logout success");
            }
        })
    });
}
// 短信验证成功事件
Auth.prototype.SmsSuccessEvent = function () {
    var self = this;
    messageBox.showSuccess("短信验证码发送成功");
    // 将发送验证码设置为不可用，并且有倒计时。
    self.sendSmsBtn.addClass("disabled");
    var count = 59;
    self.sendSmsBtn.unbind("click");
    var timer = setInterval(function () {
        self.sendSmsBtn.text(count + 's');
        count -= 1;
        if (count <= 0) {
            clearInterval(timer);
            self.sendSmsBtn.removeClass('disabled');
            self.sendSmsBtn.text("发送验证码");
            self.listenSmsCaptchaEvent();
        }
    }, 1000);
}
// 短信验证失败事件
Auth.prototype.SmsFailEvent = function (fail_info) {
    messageBox.showError(fail_info);
}
// 监听短信验证
Auth.prototype.listenSmsCaptchaEvent = function () {
    var self = this;
    //ajax请求
    self.sendSmsBtn.click(function () {
        //校验手机号是否正确
        var telephoneInput = $(".signup_group input[name='telephone']");
        console.log(telephoneInput.val());
        var telephone = telephoneInput.val();
        if (!telephone) {
            messageBox.showInfo("请输入手机号码");
        } else {
            $.get({
                url: "account/sms_captcha/",
                data: { "telephone": telephone },
                success: function (result) {
                    if (result['code'] == 200) {
                        self.SmsSuccessEvent();
                    } else {
                        self.SmsFailEvent(result['message']);
                    }
                }
            });
        }

    });
}

Auth.prototype.listenLoginEvent = function () {
}

//run
Auth.prototype.run = function () {
    var self = this;
    self.listenEvent();
    self.listenRequestEvent();
    self.listenSmsCaptchaEvent();
}

/**
 * 页面加载时，加载两个js对象
 */
$(function () {
    var auth = new Auth();
    var frontBase = new FrontBase();
    auth.run();
    frontBase.run();
});


$(function () {
    //如果加载了这个对象template
    
    if (template) {
        //这个方法加载，就是使用art template动态的插入数据.过滤器
        template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);//创建一个Date对象
            var datets = date.getTime();//将秒化为时间
            var nowts = (new Date()).getTime();//获取当前时间
            var timestamp = (nowts - datets) / 1000;//得到相差的时间秒数
            // 判断相差多少秒
            if (timestamp < 60) {
                return '刚刚';
            } else if (timestamp >= 60 && timestamp < 60 * 60) {
                minutes = parseInt(timestamp / 60);
                return minutes + "分钟前";
            } else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
                hours = parseInt(timestamp / 60 / 60);
                return hours + "小时前";
            } else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
                days = parseInt(timestamp / 60 / 60 / 24);
                return days + "天前";
            } else {
                var year = date.getFullYear();
                var month = date.getMonth() + 1;//js中用0 表示第一个月，所以要+1 
                var day = date.getDate();
                var hour = date.getHours();
                var minutes = date.getMinutes();
                return year + "/" + month + "/" + day + " " + hour + ":" + minutes;
            }
        }
    }
});