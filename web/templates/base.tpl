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

    .navbar-fixed-bottom .navbar-inner {
    /*	padding-bottom: 8px;*/
    }

    .navbar-text {
    	color: #eee;
    	font-size: 120%;
    }

    #current-preset {
    	padding-right: 12px;
    	font-weight: bold;
    }
    </style>
    <!--<link href="/static/css/bootstrap-responsive.css" rel="stylesheet">-->

    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

  </head>
  <body>
  	<div class="navbar navbar-fixed-top">
  		<div class="navbar-inner">
  			<div class="container-fluid">
  				<a class="brand" href="#">OpenLights</a>
				<form class="navbar-form pull-right">
					<a class="btn" id="btn-preview" title="Preview" data-toggle="pill" href="#preview"><i class="icon-film"></i></a>
					<a class="btn" id="btn-settings" title="Settings" data-toggle="pill" href="#settings"><i class="icon-cog"></i></a>
					<a class="btn" id="btn-presets" title="Presets" data-toggle="pill" href="#presets"><i class="icon-list-alt"></i></a>
					<a class="btn" id="btn-beatdetect" title="Beat Detection is On"><i class="icon-volume-up"></i></a>
					<a class="btn" id="btn-blackout" title="Blackout"><i class="icon-eye-close"></i></a>
					<a class="btn" id="btn-playpause" title="Pause"><i class="icon-pause"></i></a>
				</form>
  			</div>
  		</div>
  	</div>
  	<div class="container-fluid">
  		<div class="tabbable">
  			<div class="tab-content">
  				<div class="tab-pane active" id="preview">
  					Pane 1: Preview video
  				</div>
  				<div class="tab-pane" id="presets">
  					%if preset_rows:
                        <table class="table table-striped">
                        <thead>
                            <tr><td>Name</td><td>Runtime</td><td>Fadetime</td><td>Active</td></tr>
                        </thead>
                        <tbody>
                        %for preset in preset_rows:
                            <tr><td>{{preset[1]}}</td><td>{{preset[3]}}</td><td>{{preset[4]}}</td><td>{{preset[2]}}</td></tr>
                        %end
                        </tbody>
                        </table>
                    %end
  				</div>
  				<div class="tab-pane" id="settings">
  					Pane 3: Settings
  				</div>
  			</div>
  		</div>
  	</div>
  	<div class="navbar navbar-fixed-bottom">
  		<div class="navbar-inner">
  			<div class="container-fluid">
  				
				<form class="navbar-form pull-right">
					<a class="btn" id="btn-preset-prev" title="Previous Preset"><i class="icon-chevron-left"></i></a>
					<a class="btn" id="btn-preset-next" title="Next Preset"><i class="icon-chevron-right"></i></a>
				</form>
				<p class="navbar-text pull-right">
  					Current Preset: <span id="current-preset">{{current_preset}}</span>
  				</p>
  			</div>
  		</div>
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
    				$('#btn-playpause i').removeClass('icon-play').addClass('icon-stop');
    				$('#btn-playpause').title = "Pause";
    			} else {
    				$('#btn-playpause i').removeClass('icon-stop').addClass('icon-play');
    				$('#btn-playpause').title = "Start";
    			}
    		});
    	});

    	$('#btn-preset-next').click(function() {
    		$.getJSON('/rpc/next', function(data) {
    			$('#current-preset').text(data['current_preset']);
    		});
    	});

    	$('#btn-preset-prev').click(function() {
    		$.getJSON('/rpc/prev', function(data) {
    			$('#current-preset').text(data['current_preset']);
    		});
    	});

    	window.setInterval(function() {
    		$.getJSON('/rpc/status', function(data) {
    			if(data['running']) {
    				$('#btn-playpause i').removeClass('icon-play').addClass('icon-stop');
    				$('#btn-playpause').title = "Pause";
    			} else {
    				$('#btn-playpause i').removeClass('icon-stop').addClass('icon-play');
    				$('#btn-playpause').title = "Start";
    			}
    			if(data['blacked_out']) {
    				$('#btn-blackout i').removeClass('icon-eye-close').addClass('icon-eye-open');
    			} else {
    				$('#btn-blackout i').removeClass('icon-eye-open').addClass('icon-eye-close');
    			}
    			$('#current-preset').text(data['current_preset']);
    		});
    	}, 250);

    });
    </script>
  </body>
</html>