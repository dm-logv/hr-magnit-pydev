(function comment(window) {
    function verifyFilling(node) {
        var node = node.target || node;
        if (node.value.trim().length > 0) {
            node.classList.remove('verify-fail');
            node.classList.add('verify-pass');
        } else {
            node.classList.remove('verify-pass');
            node.classList.add('verify-fail');
        }
    }

    function verifyPatternMatching(node) {
        var node = node.target || node;
        var re = new RegExp(node.getAttribute('pattern') || '\S+');
        if (re.test(node.value) || node.value.trim().length == 0) {
            node.classList.remove('verify-fail');
            node.classList.add('verify-pass');
        } else {
            node.classList.remove('verify-pass');
            node.classList.add('verify-fail');
        }
    }

    function getFormNodes(root){
        var collections = ['input', 'select', 'textarea'].map(
            function(tag) {
                return root.getElementsByTagName(tag);
            });
        return collections
            .map(function (collect) {
                return Array.prototype.slice.call(collect);
            })
            .reduce(function (a, b) {
                return a.concat(b)
            });
    }

    function getNodesToVerifyFilling(root) {
        return getFormNodes(root).filter(function(node) { return node.hasAttribute('required'); });
    }

    function getNodesToMatchPattern(root) {
        return getFormNodes(root).filter(function(node) {
            return (node.getAttribute('pattern') || '').trim().length > 0;
        });
    }

    function loadCitiesList(e){
        var id = e.target.value || 0;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/comment/getCities/' + id.toString(), true);
        xhr.onload = function(e) {
            if (e.target.status == 200 && e.target.readyState == 4) {
                document.getElementsByClassName('comment-form__city')[0]
                    .getElementsByTagName('select')[0]
                    .innerHTML = e.target.response;
            }
        };
        xhr.send();
    }

    function submit(root, e) {
        e.preventDefault();

        getNodesToVerifyFilling(root).forEach(verifyFilling);
        getNodesToMatchPattern(root).forEach(verifyPatternMatching);
        var nodes = getFormNodes(root);
        if (nodes.filter(function(node){
                return !node.classList.contains('verify-fail');
            }).length == nodes.length) {
            var json = serialize(nodes);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/comment/addComment/', true);
            xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
            xhr.onload = postHandler.bind(null, true);
            xhr.send(json);
        }

        return false;
    }

    function serialize(nodesArray){
        var json = {};
        Array.prototype.forEach.call(nodesArray, function(node){
            json[node.name] = node.value;
        });
        return JSON.stringify(json);
    }

    document.addEventListener('DOMContentLoaded', function(e){
        var root = document.getElementsByClassName('comment-form')[0];

        getNodesToVerifyFilling(root).forEach(function(node){
            node.addEventListener('change', verifyFilling);
        });
        getNodesToVerifyFilling(root).forEach(function(node){
            node.addEventListener('blur', verifyFilling);
        });
        getNodesToMatchPattern(root).forEach(function(node){
            node.addEventListener('change', verifyPatternMatching);
        });
        getNodesToMatchPattern(root).forEach(function(node){
            node.addEventListener('blur', verifyPatternMatching);
        });

        root.onsubmit = submit.bind(null,root);

        // Load cities list
        root.getElementsByClassName('comment-form__region')[0]
            .getElementsByTagName('select')[0]
            .addEventListener('change', loadCitiesList);
    });
})(window);


