$(document).ready(function(){

	$("button#returnButton").click(function(){
		window.location.history.go(-1);
	});

    SyntaxHighlighter.config.clipboardSwf = '/static/js/syntaxhighlighter/scripts/clipboard.swf';
    SyntaxHighlighter.all();

    $('#wmd-input').before('<div id="wmd-button-bar" class="wmd-button-bar"></div>');
    $('#wmd-input').after('<div id="wmd-preview" class="wmd-preview ke-content" style="display:none;"></div>');
    var converter = Markdown.getSanitizingConverter();
    var wmd = new Markdown.Editor(converter,null);
    wmd.hooks.set('insertImageDialog', doInsertImage);
    wmd.run();
    $('#wmd-redo-button').after('<li title="预览" class="wmd-spacer" style="left: 590px; width:20px;background:none;cursor:pointer;" id="preview-tab-button"><i class="icon-eye-open"></i></li>');
    $('#edit-tab-button,#preview-tab-button').click(function(){
        var thiz  = $(this);
        thiz.toggleClass('selected');
        $('#wmd-preview').find("pre").each(function(){
            var re = /-- lang: (.*?) --/;
            var r = re.exec($(this).html());
            $(this).addClass("brush: " + r[1] + "; toolbar: true; auto-links: false; ");
        });
        $('#wmd-input').toggle();
        $('#wmd-preview').toggle();
    });
});

function editUser(id, url) {
    if(id) {
        $.ajax( {
            url: url,
            data: {id: id},
            type: "GET",
            dataType: "html",
            cache: false,
            success: function(data){
                $.box({
                    title: "修改用户",
                    html: data,
                    ok: "确认修改",
                    cancel: "取消",
                    height: "250px",
                    okfn: function(){
                        var checkIds = ["inputUsername", "inputNick", "inputEmail"];
                        for(var i = 0; i < checkIds.length; i++){
                            checkInput(checkIds[i]);
                        }
                        if($("#inputPassword").val() != $("#inputPassword2").val()){
                            alert("两次密码不一致");
                            return false;
                        }
                        if($("#addUserForm").find(".alert-error").length == 0){
                            $("#addUserForm").submit();
                        }
                    }
                });
            }
        });
    }
}

function checkInput(idName){
    var $this =  $("#" + idName);
    if(!$.trim($this.val())){
        $this.next(".alert").remove();
        $this.after(" <span class='alert alert-error'>不能为空</span>");
    } else {
        $this.next(".alert").remove();
        $this.after(" <span class='alert alert-success'>OK</span>");
    }
}

// 整除
function div(a, b) {
    var n1 = Math.round(a); //四舍五入
    var n2 = Math.round(b); //四舍五入
    var rslt = n1 / n2; //除
    if (rslt >= 0) {
        rslt = Math.floor(rslt); //返回小于等于原rslt的最大整数。
    }
    else {
        rslt = Math.ceil(rslt); //返回大于等于原rslt的最小整数。
    }
    return rslt;
}
