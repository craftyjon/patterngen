<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>OpenLights Server</title>

    <link href="/static/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
    body {
    	padding-top: 48px;
    }

    .navbar-form a {

    	margin-left: 8px;
    }
    </style>
    <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">

    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

  </head>
  <body>
  	<div class="navbar navbar-fixed-top">
  		<div class="navbar-inner">
  			<div class="container-fluid">
  				<a class="brand" href="#">OpenLights Server</a>
				<form class="navbar-form pull-right">
					<a class="btn" id="btn-settings" title="Settings"><i class="icon-cog"></i></a>
					<a class="btn" id="btn-presets" title="Presets"><i class="icon-list-alt"></i></a>
					<a class="btn" id="btn-beatdetect" title="Beat Detection is On"><i class="icon-volume-up"></i></a>
					<a class="btn" id="btn-blackout" title="Blackout"><i class="icon-eye-close"></i></a>
					<a class="btn" id="btn-playpause" title="Pause"><i class="icon-pause"></i></a></li>
				</form>
  			</div>
  		</div>
  	</div>
  	<div class="container-fluid">

  	</div>
  	<div class="navbar navbar-fixed-bottom">

  	</div>
  	<script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/bootstrap.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {

    	$('#btn-blackout').click(function() {
    		$.getJSON('/rpc/blackout', function(data) {
    			if(data['blacked_out']) {
    				$('#btn-blackout i').removeClass('icon-eye-close').addClass('icon-eye-open');
    			} else {
    				$('#btn-blackout i').removeClass('icon-eye-open').addClass('icon-eye-close');
    			}
    		});
    	});

    	$('#btn-playpause').click(function() {
    		$.getJSON('/rpc/playpause', function(data) {
    			if(data['running']) {
    				$('#btn-playpause i').removeClass('icon-play').addClass('icon-pause');
    			} else {
    				$('#btn-playpause i').removeClass('icon-pause').addClass('icon-play');
    			}
    		});
    	});

    });
    </script>
  </body>
</html>