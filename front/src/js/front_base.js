/**
 * 用于监听导航中的用户Box
 */
function FrontBase() { }

FrontBase.prototype.run = function () {
    var self = this;
    self.listenAuthBoxHaver();
}

FrontBase.prototype.listenAuthBoxHaver = function () {
    var authBox = $(".auth-box");
    var userMoreBox = $(".user-more-box");
    authBox.hover(function () {
        userMoreBox.show();
    }, function () {
        userMoreBox.hide();
    });
}

/**
 * 用来监听登录
 * 使用面向对象的思想设计的逻辑
 */
function Auth() {
    self = this;
    self.mask_wrapper = $(".mask_wrapper");
    self.scrollGroup = $('.scroll_group');
    self.telephoneInput = $(".signup_group input[name='telephone']");
    self.sendSmsBtn = $("#sendSmsBtn");
}
//展示
Auth.prototype.showEvent = function () {
    self = this;
    self.mask_wrapper.show();
};

//隐藏
Auth.prototype.hideEvent = function () {
    self = this;
    self.mask_wrapper.hide();
};

//监听
Auth.prototype.listenEvent = function () {
    self = this;
    var signinBtn = $(".signin");
    var signupBtn = $(".signup");
    var closeBtn = $(".close_btn");
    var switchBtn = $(".switch");
    var imgCaptcha = $(".img_captcha");
    signinBtn.click(function () {
        self.showEvent();
        // console.log("login in");
        self.scrollGroup.css({ "left": 0 });
    });
    signupBtn.click(function () {
        self.showEvent();
        // console.log("login out");
        self.scrollGroup.css({ "left": -400 });
    });
    closeBtn.click(function () {
        self.hideEvent();
    });
    switchBtn.click(function () {
        var currentLeft = self.scrollGroup.css("left");
        currentLeft = parseInt(currentLeft);
        if (currentLeft < 0) {
            self.scrollGroup.animate({ "left": '0px' });
        } else {
            self.scrollGroup.animate({ "left": '-400px' });
        }
    });
    imgCaptcha.click(function () {
        //src被重写设置的时候会重写访问。不然重复内容的访问不会被执行。
        imgCaptcha.attr("src", "/account/img_captcha/" + "?random=" + Math.random());
    });

}

Auth.prototype.listenRequestEvent = function () {
    self = this;
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
    var smsCaptchaInput = signupGroup.find("input[id='smSCaptcha']");
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
                    self.hideEvent();
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
        var logupTel =   logupTelInput.val();
        var username =   usernameInput.val();
        var logupPwd1 =  logupPwd1Input.val();
        var logupPwd2 =  logupPwd2Input.val();
        var imgCaptcha = imgCaptchaInput.val();
        var smsCaptcha = smsCaptchaInput.val();
        console.log(logupPwd2);
        $.ajax({
            url:"/account/register/",
            type: "POST",
            dataType: "json",
            data:{
                telephone:logupTel,
                username:username, 
                password1:logupPwd1,
                password2:logupPwd2,
                img_captcha:imgCaptcha,
                sms_captcha:smsCaptcha,
            },
            success: function (result) {
                if(result['code'] ==200){
                    window.location.reload();
                }else{
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
            fail:function(){
                window.messageBox.show("系统错误","error");
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
Auth.prototype.SmsSuccessEvent = function () {
    self = this;
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
Auth.prototype.SmsFailEvent = function (fail_info) {
    messageBox.showError(fail_info);
}
Auth.prototype.listenSmsCaptchaEvent = function () {
    self = this;
    //ajax请求
    self.sendSmsBtn.click(function () {
        //校验手机号是否正确
        var telephone = self.telephoneInput.val();
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

Auth.prototype.listenLoginEvent = function(){
    
}
//run
Auth.prototype.run = function () {
    self = this;
    self.listenEvent();
    self.listenRequestEvent();
    self.listenSmsCaptchaEvent();
}

/**
 * 页面加载时，加载两个js对象
 */
$(function () {
    var frontBase = new FrontBase();
    var auth = new Auth();
    frontBase.run();
    auth.run();
});