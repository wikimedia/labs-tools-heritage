<!DOCTYPE html>
<?php
$size=150;
if (isset($_GET["size"])) {
    $size=(int)$_GET["size"];
}
$margin = intval(10*$size/150); // allow scaled margin
?><html><head>
    <title></title>
    <style>
    * {
        margin:0;
        padding:0;
    }
    #photos-wlm {
        margin: 0;
        padding: 0;
    }

    #photos-wlm li {
        list-style-type: none;
    }

    #photos-wlm a {
        float: left;
        width: <?php echo $size; ?>px;
        height: <?php echo $size; ?>px;
        margin: 9px;
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
            var photo = data[i];
            
            var li = document.createElement( 'li' );
            var a = document.createElement( 'a' );
            a.href = photo.url;
            a.target = '_blank';
            a.title = 'By: ' + photo.uploader;
            a.style.backgroundImage = 'url("' + photo.image + '")';
            li.appendChild(a);

            photos.appendChild(li);
        }
    }

    function loadPhotos() {
        var s = document.createElement('script');
        s.id = 'achterkamer';
        s.src = 'http://toolserver.org/~erfgoed/tools/wlmlast.php?callback=jscallback';
        s.src = s.src + '<?php if (isset($_GET['country'])) { echo '&country=' . htmlspecialchars(urlencode($_GET['country'])); } if (isset($_GET['number'])) { echo '&number=' . htmlspecialchars(urlencode($_GET['number'])); } echo '&size=' . htmlspecialchars(urlencode($size)); ?>';
        document.getElementsByTagName("head")[0].appendChild(s);
    }
    if (photosDiv) {
        photos = document.createElement('ul');
        photosDiv.appendChild(photos);
        loadPhotos();
    }
</script>

</body></html>
