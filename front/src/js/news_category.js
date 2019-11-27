function NewCategory(){

};
NewCategory.prototype.run = function () {
    var add_btn = $("#add-btn");
    add_btn.click(function(){
        xfzalert.alertOneInput({
            'title':"添加新闻分类",
            'placeholder':"请输入新闻分类",
            "confirmCallback":function(inputValue){
                $.ajax({
                    'url':"/cms/add_news_category/",
                    'data':{
                        'name':inputValue
                    },
                    'type':'POST',
                    'dataType':'json',
                    success: function (result) { 
                        if(result['code'] === 200){
                            console.log(result);
                            window.location.reload();
                        }
                    }
                });
            }
        })
    });
}

$(function(){
    var newCategory  = new NewCategory();
    newCategory.run();
});