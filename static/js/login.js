$(function () {
    var error_name = false;
    var error_password = false;

    $('#username').blur(function () {
        check_user_name()
    });

    $('#username').focus(function () {
		$('#username_error').hide();
    });

    $('#pwd').blur(function () {
        check_pwd()
    });

    function check_user_name() {
    var len = $('#username').val().length;
		if(len<5||len>20)
		{
			$('#username').next().html('请输入5-20个字符的用户名');
			$('#username').next().show();
			$('#username_error').hide();
			error_name = true;
		}
		else
		{
			$('#username').next().hide();
			$('#username_error').show();
			error_name = false;
		}
    }

    function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位');
			$('#pwd').next().show();
			$('#password_error').hide();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			$('#password_error').show();
			error_password = false;
		}
	}

	$('form').submit(function() {
		check_user_name();
		check_pwd();

		if(error_name == false && error_password == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});
});

