<html>
<head>
<title>Trip Planner - Wiki Loves Monuments</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js" type="text/javascript"></script> 
<script type="text/javascript">
function newfield() {
   return '<div class="field"><select name="type"><option value="incity">In the city</option><option value="specific">Specific monument</option></select><input type="text"><input value="+" type="button" onClick="javascript:$(\'#box\').append(newfield());">';
}

$(document).ready(function () {
  $("#box").append(newfield());
});
</script>
</head>
<body>
<div id="box">

</div>
</body>
</html>
