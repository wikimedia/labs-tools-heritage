/**
 * Created by Édouard Hue on 09/08/16.
 */
/* eslint-env jquery, knockout*/
/* global ko */
/* exported dailyUploads */

( function () {
	var $grid = $( '#images' ).isotope( {
		initLayout: false,
		itemSelector: '.grid-item',
		layoutMode: 'masonry',
		masonry: {
			columnWidth: '.grid-sizer'
		}
	} );

	$grid.imagesLoaded().progress( function () {
		$grid.isotope( 'layout' );
	} );
}() );

window.dailyUploads = function () {

	var urlParams = new URLSearchParams( window.location.search );

	function viewModel( urlParams ) {
		var self = this,
			today = new Date().toISOString().slice( 0, 10 ),
			day = urlParams.get( 'date' ) || today,
			category = urlParams.get( 'category' ) || 'Images from Wiki Loves Monuments 2018';

		self.day = ko.observable( day );
		self.category = ko.observable( category );
		self.images = ko.observableArray();

		self.updateImages = function () {
			var start, end;
			self.images.removeAll();
			start = new Date( self.day() );
			start.setHours( 0 );
			start.setMinutes( 0 );
			start.setSeconds( 0 );
			start.setMilliseconds( 0 );
			end = new Date( self.day() );
			end.setHours( 23 );
			end.setMinutes( 59 );
			end.setSeconds( 59 );
			end.setMilliseconds( 999 );
			self.continueUpdate( {
				start: start,
				end: end
			} );
		};

		self.continueUpdate = function ( boundaries, queryContinue ) {
			var data, attrname;

			data = {
				action: 'query',
				prop: 'imageinfo',
				iiprop: 'url',
				iiurlwidth: 320,
				generator: 'categorymembers',
				gcmtitle: 'Category:' + self.category(),
				gcmtype: 'file',
				gcmprop: 'title',
				gcmlimit: 50,
				gcmsort: 'timestamp',
				gcmstart: boundaries.start.toUTCString(),
				gcmend: boundaries.end.toUTCString(),
				format: 'json'
			};

			if ( queryContinue ) {
				for ( attrname in queryContinue ) {
					data[ attrname ] = queryContinue[ attrname ];
				}
			} else {
				data.continue = '';
			}

			$.getJSON( '//commons.wikimedia.org/w/api.php?callback=?', data, function ( data ) {
				$.each( data.query.pages, function ( index, file ) {
					var image = {
						title: file.title,
						thumburl: file.imageinfo[ 0 ].thumburl,
						descurl: file.imageinfo[ 0 ].descriptionurl
					};
					self.images.push( image );
				} );
				if ( 'continue' in data ) {
					self.continueUpdate( boundaries, data.continue );
				}
			} );
		};
	}

	ko.applyBindings( viewModel( urlParams ) );

	if ( urlParams.get( 'load' ) === 'true' ) {
		self.updateImages();
	}

};
