function indexes(collection) {
    return [].slice.apply(collection).map(function(el){return el.id});
}
function update(slug) {
    var el = document.getElementById(slug.id);
    if (el) { el.outerHTML = slug.html; }
}
function load() {
    JSON.parse(xhr.response).forEach(update);
}
function query() {
    if (firstLoad) { firstLoad = false; return }
    xhr = new XMLHttpRequest();
    xhr.open("GET", "{% url 'topics-ajax' %}?ids="+ids);
    xhr.send();
    xhr.onload = load;
}
var topics = document.getElementsByClassName("topic");
var ids = indexes(topics);
var firstLoad = true;
window.onpageshow = query;
