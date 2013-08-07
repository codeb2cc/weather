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
      ' Licensed <%= pkg.license %> */\n',
    // Task configuration.
    watch: {
      gurntfile: {
        files: 'Gruntfile.js',
        tasks: ['jshint:gruntfile'],
      },
      sass: {
        files: ['lib/sass/*.scss'],
        tasks: ['sass:debug']
      },
      javascript: {
        files: ['lib/js/*.js'],
        tasks: ['concat']
      }
    },
    clean: ['dist'],
    copy: {
      vendor: {
        files: [
          { expand: true, cwd: 'lib/', src: ['js/vendor/**'], dest: 'dist/' }
        ]
      }
    },
    sass: {
      debug: {
        files: { 'dist/css/app.css': 'lib/sass/app.scss' },
      },
      release: {
        files: { 'dist/css/app.css': 'lib/sass/app.scss' },
        options: { style: 'compressed' }
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
    connect: {
      server: {
        options: {
          keepalive: true,
          port: 5000,
          base: '.'
        }
      }
    },
    karma: {
      unit: {
          configFile: 'test/karma.conf.js'
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-karma');

  // Default task.
  grunt.registerTask('default', ['jshint', 'clean', 'copy:vendor', 'sass:debug', 'concat']);
  grunt.registerTask('release', ['jshint', 'clean', 'copy:vendor', 'sass:release', 'concat', 'uglify']);

};
