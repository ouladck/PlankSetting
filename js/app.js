(function($) {

	var app = angular.module("app", []);

	app.directive('headerDir', function() {
		return {
			restrict: 'E',
			templateUrl: 'include/header.html'
		};
	});

	app.directive('aboutDir', function(){
		return {
			restrict: 'E',
			templateUrl: 'include/about.html'
		};
	})

	app.directive('installDir', function(){
		return {
			restrict: 'E',
			templateUrl: 'include/install.html'
		};
	});

	app.directive('contributeDir', function(){
		return {
			restrict: 'E',
			templateUrl: 'include/contribute.html'
		};
	});

	//$(window).scrollspy({target: '.navscroll'});
	$('[data-spy="scroll"]').each(function () {
	  var $spy = $(this).scrollspy('refresh')
	});
})(jQuery);