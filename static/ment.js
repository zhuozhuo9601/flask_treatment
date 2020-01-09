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
        var user_id = id.split('update')[1];
        var name_value = $("#th_name" + user_id.toString()).text();
        var subject_value = $("#th_subject" + user_id.toString()).text();
        var school_value = $("#th_school" + user_id.toString()).text();
        $("#updatename").val(name_value);
        $("#update_sub").val(subject_value);
        $("#update_sch").val(school_value);
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
    var sub_list = $("#th_subject" + del_id +" span").text();
    var subject_list = sub_list.split('--');
    var sch_list = $("#th_school"+del_id).text();
    var delete_dict = {
        "del_id":del_id,
        "school_list":sch_list,
        "subject":subject_list
    };
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
        data: JSON.stringify(delete_dict),
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

// 点击添加按钮返回下拉框数据
function add_select(id, status) {
    if (status == 'update'){
        var user_id = id.split('update')[1];
        $("#updateid").val(user_id);
    }
    $.ajax({
        // 请求方式
        type: "post",
        // contentType
        contentType: "application/json",
        // dataType
        dataType: "json",
        // url
        url: '/user/add_select/',
        // 把JS的对象或数组序列化一个json 字符串
        data: '',
        // result 为请求的返回结果对象
        success: function (data) {
            for (i=0;i<data.length;i++){
                if (data[i].id == 'school'){
                    if (status == 'add'){
                        $("#select_sch").append("<option value='"+ data[i].school_id +"'>"+data[i].sch_name+"</option>");
                    }else{
                        $("#update_sch").append("<option value='"+ data[i].school_id +"'>"+data[i].sch_name+"</option>");
                    }

                }else{
                    if (status == 'add'){
                        $("#select_sub").append("<option value='"+ data[i].subject_id +"'>"+data[i].sub_name+"</option>");
                    }else{
                        $("#update_sub").append("<option value='"+ data[i].subject_id +"'>"+data[i].sub_name+"</option>");
                    }

                }
            }

        }
    });
}