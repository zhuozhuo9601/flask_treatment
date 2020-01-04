/**
 * Created by python on 19-12-31.
 */
// 添加方法
function add() {
    $("#add_form").submit();
}

// 修改方法（编辑）
function update(id, status) {
    if (status == 'model') {
        user_id = id.split('update')[1];
        var name_value = $("#th_name" + user_id.toString()).text();
        var time_value = $("#th_time" + user_id.toString()).text();
        $("#updatename").val(name_value);
        $("#updatetime").val(time_value);
        $("#updateid").val(user_id);
    } else {
        $("#update_form").submit();
    }

    // $.ajax({
    //     // 请求方式
    //     type: "post",
    //     // contentType
    //     contentType: "application/json",
    //     // dataType
    //     dataType: "json",
    //     // url
    //     url: '/user/add',
    //     // 把JS的对象或数组序列化一个json 字符串
    //     data: JSON.stringify(abc),
    //     // result 为请求的返回结果对象
    //     success: function (result) {
    //
    //     }
    // });
}

// 删除方法
function del(id) {
    var del_id = id.split('delete')[1];
    $.ajax({
        // 请求方式
        type: "post",
        // contentType
        contentType: "application/json",
        // dataType
        dataType: "json",
        // url
        url: '/user/delete/',
        // 把JS的对象或数组序列化一个json 字符串
        data: JSON.stringify(del_id),
        // result 为请求的返回结果对象
        success: function (data) {
            if (data.code == '200'){
                alert(data.msg);
            }else{
                alert(data.msg);
            }
        }
    });
}