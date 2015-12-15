/**
 * Created by fangpeng on 12/4/15.
 */

$(function(){
    // 选择时间
    $("#ctime")
        .datetimepicker({
            format: 'yyyy-mm-dd hh:ii',
            autoclose: true,
            startDate: new Date(),
            minuteStep: 10
        })
        .on('outOfRange', function(ev){
            alert('时间不能小于今天');
        });
});

