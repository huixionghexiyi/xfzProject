/**
 * 已经写到front_base中了
 */
//点击登录按钮，弹出对话框
//不使用面向对象的思想设计的逻辑。
// $(function () {
//     $('#btn').click(function () {
//         $(".mask_wrapper").show();
//     });
//     $('#close_btn').click(function () {
//         $(".mask_wrapper").hide();
//     });
//     $('.switch').click(function () {
//         var scrollGroup = $('.scroll_group');
//         var currentLeft = scrollGroup.css("left");
//         currentLeft = parseInt(currentLeft);
//         if (currentLeft < 0) {
//             scrollGroup.animate({ "left": '0px' });
//         } else {
//             scrollGroup.animate({ "left": '-400px' });

//         }
//         // this.animate({ "left": -400 }, 400);
//     })
// })


//使用面向对象的思想设计的逻辑
function Auth() {
    self = this;
    self.mask_wrapper = $(".mask_wrapper");
    self.scrollGroup = $('.scroll_group');
}
//展示登录/注册页面
Auth.prototype.showEvent = function () {
    self = this;
    self.mask_wrapper.show();
};

//隐藏登录/注册页面
Auth.prototype.hideEvent = function () {
    self = this;
    self.mask_wrapper.hide();
};

//监听按钮事件
Auth.prototype.listenEvent = function () {
    self = this;
    var signinBtn = $(".signin");
    var signupBtn = $(".signup");
    var closeBtn = $("#close_btn");
    var switchBtn = $(".switch");
    // 点右上角登录
    signinBtn.click(function () {
        self.showEvent();
        // console.log("login in");
        self.scrollGroup.css({ "left": 0 });
    });
    //点右上角注册
    signupBtn.click(function () {
        self.showEvent();
        // console.log("login out");
        self.scrollGroup.css({ "left": -400 });
    });
    //点击关闭
    closeBtn.click(function () {
        self.hideEvent();
    });
    //点击切换
    switchBtn.click(function () {
        var currentLeft = self.scrollGroup.css("left");
        currentLeft = parseInt(currentLeft);
        if (currentLeft < 0) {
            self.scrollGroup.animate({ "left": '0px' });
        } else {
            self.scrollGroup.animate({ "left": '-400px' });
        }
    });
}
//监听请求
Auth.prototype.listenRequestEvent = function () {
    self = this;
    var signinGroup = $(".signin_group");
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");
    var loginBtn = signinGroup.find(".submit_btn");
    var logoutBtn = $("#logout_btn");
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
    //退出登录
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
    })

}

//run
Auth.prototype.run = function () {
    self = this;
    if (event.keyCode == 13) {
        switchBtn.trigger('click');
    }
    self.listenEvent();
    self.listenRequestEvent();
}
$(function () {
    var auth = new Auth();
    auth.run();
    if (event.keyCode == 13) {
        console.log("enter");
    }

});