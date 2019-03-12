<div class="container-fluid" style="margin-top:90px">
<h1 class="display-6">Better a video that a thousand words ...</h1>	

<div class="card" >
  
<div id="vid0Container" class="embed-responsive embed-responsive-16by9">
	 <video id="vid0" width="640" height="360" controls onclick="this.play();" poster="imgs/pobshare-green.png">
	  <source src="video/pobshare.webm" type="video/webm" >
			Your browser does not support the video tag.
	 </video> 
</div>
  
  <div class="card-body">
	 <div id="alert" class="alert alert-warning" role="alert" style="display: None">This video comes from YouTube.</div> 
    <h5 class="card-title">Pobshare at work</h5>
    <p class="card-text">In this video you will see how to use Pobshare to share files and folders. You will also see how to set the various security levels.</p>
    <a href="https://www.youtube.com/watch?v=aK5AGP2MNqI" class="btn btn-success">Watch the video on Youtube</a>
  </div>
</div>



</div>
<script>
	embedcode='<iframe width="560" height="315" src="https://www.youtube.com/embed/aK5AGP2MNqI?autoplay=1&enable_js=1" frameborder="0" allow="accelerometer; autoplay=1; encrypted-media; gyroscope; picture-in-picture" allowfullscreen allow=autoplay></iframe>'
	
	$( document ).ready(function() {
		$('#vid0 source').last().on('error', function() {
			$("#vid0Container").html(embedcode);
			$("#alert").show();
		});
		
	});
	
</script>

<?php include('pages/footer.php'); ?>
