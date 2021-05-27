$(document).ready( function() {
    
    // evento al seleccionar un author
    $('#author').change( function () {
        console.log('change')
        var optionSelected = $("option:selected", this);
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        console.log(optionSelected)
        console.log(valueSelected)

        $('#name').val($("#author option:selected" ).text())

    });

});

function deleteMessage(id) {
    console.log('click mensaje: ' + id)
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log(csrf)
    $.ajax({
        method : "GET",
        url : "/wall/delete_msg_ajax/"+id,
        dataType : "JSON",
        data : {
            csrfmiddlewaretoken: csrf
        }
    })
    .done (function(response){
        console.log(response)
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
            //$('#messages').html(JSON.stringify(response["errors"]));
        }
    })
}

function deleteComment(id) {
    console.log('click comentario: ' + id)
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log(csrf)
    $.ajax({
        method : "GET",
        url : "/wall/delete_comment_ajax/"+id,
        dataType : "JSON",
        data : {
            csrfmiddlewaretoken: csrf
        }
    })
    .done (function(response){
        console.log(response)
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
            //$('#messages').html(JSON.stringify(response["errors"]));
        }
    })

}

function addMessage(){
    var data = $("#formMessage").serialize()
    $.ajax({
        method : "POST",
        url : "/wall/add_message_ajax",
        data : data,
        dataType : "JSON"
    })
    .done (function(response){
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
        } else {
            console.log("no hay mensajes")
        }

    })
}

function addComment(formComment){
    var data = $("#"+formComment).serialize()
    $.ajax({
        method : "POST",
        url : "/wall/add_comment_ajax",
        data : data,
        dataType : "JSON"
    })
    .done (function(response){
        var size = Object.keys(response["alert"]).length
        if ( size > 0 ) {
            alert(response["alert"])
        } else {
            console.log("no hay mensajes")
        }

    })
    location.reload();
}
