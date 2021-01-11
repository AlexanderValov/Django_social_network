(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        // 127.0.0.1:8000 ? ngrok ---.ngrok.io
        document.body.appendChild(document.createElement('script')).src='http://127.0.0.1/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();