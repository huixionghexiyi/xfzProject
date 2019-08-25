//点击登录按钮，弹出对话框

$(function () {
    $('#btn').click(function () {
        $(".mask_wrapper").show();
    });
    $('#close_btn').click(function () {
        $(".mask_wrapper").hide();
    });
    $('.switch').click(function () {
        var scrollGroup = $('.scroll_group');
        var currentLeft = scrollGroup.css("left");
        currentLeft = parseInt(currentLeft);
        if(currentLeft < 0){
            scrollGroup.animate({"left":'0px'});
        }else{
            scrollGroup.animate({"left":'-400px'});
            
        }
        // this.animate({ "left": -400 }, 400);
    })
})

