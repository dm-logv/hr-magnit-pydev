function Tip(reloadAfter){
    var tip = document.getElementsByClassName('info-tip')[0];
    return {
        fail: function(text){
            tip.classList.remove('success');
            tip.classList.add('fail');
            commons(text);
        },
        success: function(text){
            tip.classList.remove('fail');
            tip.classList.add('success');
            commons(text);
        }
    }
    function commons(text){
        tip.innerHTML = text;
        tip.style.top = '2em';
        setInterval(function(e){
            tip.style.top = '-1000px';
            if(reloadAfter){
                location.reload();
            }
        }, 3000);
    }
}

function postHandler(reload, e) {
    var response = e.target.responseText;
    var obj = JSON.parse(response);
    Tip(reload)[obj['type']](obj['text']);
}