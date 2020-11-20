

function playSound( sound )
{
    playResource( sound, 'swan/audio' );
}

function playVideo( video )
{
    playResource( video, 'swan/video' );
}

function playResource( resource, urlPath )
{
    var data = { "res": resource };
    $.ajax({
        method: "POST",
        contentType: "application/json; charset=UTF-8",
        url: urlPath,
        data: JSON.stringify(data),
        dataType : "json"
    }).
    done(function( json )  {
        alert( json );
    }).
    fail(function(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        alert("Sorry. Server unavailable. ");
    });
}
