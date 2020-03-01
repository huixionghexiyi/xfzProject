function Staff() { }

Staff.prototype.removeStaff = function () {
    var removeBtn = $("#removeBtn");
    var pk = removeBtn.attr("data-staff-id");
    removeBtn.click(function(){
        console.log(pk);
    });
    // removeBtn.click(function () {
    //     var curBtn = $(this);
    //     xfzalert.alterConfirm({
    //         text: "确认删除改员工吗？删除后不可恢复",
    //         confirmText: "删除",
    //         confirmCallback:function(){
                
    //         }
    //     })
    //     $.post({
    //         url: '/cms/removeStaff/',
    //         data: {
    //             pk: pk
    //         },
    //         dataType: 'json',
    //         success: function (result) {
    //             if (result['code'] === 200) {
    //                 window.location.reload();
    //             } else {
    //                 xfzalert.alertError(result['message']);
    //             }
    //         }
    //     })
    // });
}

Staff.prototype.run = function () {
    var self = this;
    self.removeStaff();
}

$(function () {
    var staff = new Staff();
    staff.run();
});