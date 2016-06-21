module.exports = function ( grunt ) {

	grunt.loadNpmTasks( 'grunt-jsonlint' );
	grunt.loadNpmTasks( 'grunt-banana-checker' );
	grunt.loadNpmTasks( 'grunt-stylelint' );

	grunt.initConfig( {

		jsonlint: {
			all: [
				'**/*.json',
				'!node_modules/**',
				'!vendor/**'
			]
		},

		banana: {
			'monumentsapi': [
				'i18n',
			]
		},

		stylelint: {
			options: {
				syntax: 'css'
			},
			src: [
				'api/jscss/*.css',
				'toolbox/css/*.css'
			]
		}

	} );

	grunt.registerTask( 'test', [ 'jsonlint', 'stylelint', 'banana' ] );
	grunt.registerTask( 'default', 'test' );
};
