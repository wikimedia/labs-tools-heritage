<!DOCTYPE html>
<html><head>
    <title></title>
    <style>
        #photos-wlm {
            margin: 0;
            padding: 0;
        }

        #photos-wlm li {
            list-style-type: none;
        }

        #photos-wlm a {
            float: left;
            width: 150px;
            height: 150px;
            margin: 10px;
            background-repeat: no-repeat;
            background-position: center center;
        }
    </style>
<body>

<div id="photos-wlm">
</div>

<script>
    var photosDiv = document.getElementById('photos-wlm');
    var photos;

    function jscallback(data) {
        for (var i = 0, l = data.length; i < l; i++) {
            var photo = data[i],
                thumb = (photo.image + "/150px-.jpg").replace("commons/", "commons/thumb/");

            var li = document.createElement( 'li' );
            var a = document.createElement( 'a' );
            a.href = photo.url;
            a.target = '_top';
            a.title = 'By: ' + photo.uploader;
            a.style.backgroundImage = 'url("' + thumb + '")';
            li.appendChild(a);

            photos.appendChild(li);
        }
    }

    function loadPhotos() {
        var s = document.createElement('script');
        s.id = 'achterkamer';
        s.src = 'http://toolserver.org/~erfgoed/tools/wlmlast.php?callback=jscallback<?php if (isset($_GET['country'])) { echo '&country=' . htmlspecialchars(urlencode($_GET['country'])); } if (isset($_GET['number'])) { echo '&number=' . htmlspecialchars(urlencode($_GET['number'])); } ?>';
        document.getElementsByTagName("head")[0].appendChild(s);
    }
    if (photosDiv) {
        photos = document.createElement('ul');
        photosDiv.appendChild(photos);
        loadPhotos();
    }
</script>

</body></html>
