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
    var closeBtn = $("#close_btn");
    var switchBtn = $(".switch");
    signinBtn.click(function () {
        self.showEvent();
        self.scrollGroup.css("left:0");
    });
    signupBtn.click(function () {
        self.showEvent();
        self.scrollGroup.css("left:-400");

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
}
Auth.prototype.listenRequestEvent = function () {
    self = this;
    var signinGroup = $(".signin_group");
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");
    var submitBtn = signinGroup.find(".submit_btn");

    submitBtn.click(function () {
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
                console.log("========");
                console.log(result);
                console.log("========");
            }

        );
    });

}
//运行
Auth.prototype.run = function () {
    self = this;
    self.listenEvent();
    self.listenRequestEvent();
}
$(function () {
    var auth = new Auth();
    auth.run();
});