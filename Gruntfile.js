/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
      '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
      '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
      '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;' +
      ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */\n',
    // Task configuration.
    clean: ['dist'],
    copy: {
      dist: {
        files: [
          { expand: true, cwd: 'lib/', src: ['js/vendor/**'], dest: 'dist/' }
        ]
      }
    },
    sass: {
      options: {
        style: 'compressed',
      },
      dist: {
        files: {
          'dist/css/app.css': 'lib/sass/app.scss'
        }
      }
    },
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      foundation: {
        src: [
          'lib/js/foundation/foundation.min.js',
          'lib/js/foundation/foundation.orbit.js',
          'lib/js/foundation/foundation.section.js'
        ],
        dest: 'dist/js/foundation.js'
      },
      plugins: {
        src: ['lib/js/plugins.js', 'lib/js/plugins/*'],
        dest: 'dist/js/plugins.js'
      },
      app: {
        src: ['lib/js/app.js'],
        dest: 'dist/js/app.js'
      }
    },
    uglify: {
      options: {
        banner: '<%= banner %>',
        mangle: {
          except: ['$scope']
        },
        preserveComments: false
      },
      foundation: {
        src: '<%= concat.foundation.dest %>',
        dest: '<%= concat.foundation.dest %>'
      },
      plugins: {
        src: '<%= concat.plugins.dest %>',
        dest: '<%= concat.plugins.dest %>',
      },
      app: {
        src: '<%= concat.app.dest %>',
        dest: '<%= concat.app.dest %>',
      }
    },
    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        sub: true,
        undef: true,
        unused: true,
        boss: true,
        eqnull: true,
        browser: true,
        globals: {}
      },
      gruntfile: {
        src: 'Gruntfile.js'
      }
    },
    watch: {}
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task.
  grunt.registerTask('default', ['jshint', 'clean', 'copy', 'sass', 'concat']);
  grunt.registerTask('release', ['jshint', 'clean', 'copy', 'sass', 'concat', 'uglify']);

};
