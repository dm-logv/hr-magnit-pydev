(function view(vindow) {
    function removeComment(url, e) {
        e.preventDefault();

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.onload = postHandler.bind(null, true);
        xhr.send();

        return false;
    }

    document.addEventListener('DOMContentLoaded', function () {
        var anchors = Array.prototype.slice.call(
            document.getElementsByClassName('view')[0]
                .getElementsByTagName('a'))
            .filter(function(node){
                return node.getAttribute('data-action') == 'true'
            });
        anchors.forEach(function(node) {
            node.addEventListener('click', removeComment.bind(null, node.href))
        });
    });
})(window);