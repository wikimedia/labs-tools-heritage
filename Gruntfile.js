/* eslint-env node */
module.exports = function ( grunt ) {

	grunt.loadNpmTasks( 'grunt-eslint' );
	grunt.loadNpmTasks( 'grunt-jsonlint' );
	grunt.loadNpmTasks( 'grunt-banana-checker' );
	grunt.loadNpmTasks( 'grunt-stylelint' );

	grunt.initConfig( {

		eslint: {
			fix: {
				options: {
					fix: true
				},
				src: [
					'<%= eslint.main %>'
				]
			},
			main: [
				'**/*.js',
				'!node_modules/**',
				'!vendor/**',
				'!coverage/**',
				'!api/tripplanner/**',
				'!common/**',
				'!map/**',
				'!prox_search/**',
				'!tools/browser/**'
			]
		},

		jsonlint: {
			all: [
				'**/*.json',
				'!node_modules/**',
				'!vendor/**'
			]
		},

		banana: {
			monumentsapi: [
				'i18n'
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

	grunt.registerTask( 'test', [ 'eslint:main', 'jsonlint', 'stylelint', 'banana' ] );
	grunt.registerTask( 'default', 'test' );
};
