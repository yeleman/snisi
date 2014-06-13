
module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    clean: { dist: ['css', 'js', 'fonts'] },
    less: {
        snisi: {
            options: {
                paths: ["src/less"],
                cleancss: true,
                compress: true
            },
            files: {
                "css/<%= pkg.name %>.css":
                    ["assets/bootstrap.less",
                     "src/less/snisi.less", ]
            }
        }
    },
    concat: {
        js: {
            options: {stripBanners: false},
            src: ['assets/jquery.1.8.2.min.js',
                  'assets/bootstrap-3.1.1/js/tooltip.js',
                  'assets/bootstrap-3.1.1/js/popover.js',
                  'src/js/*.js'],
            dest: 'js/<%= pkg.name %>.js'
        },
        css: {
            src: ['assets/font-awesome-4.0.3/css/font-awesome.min.css',
                  'assets/pure-min.css',
                  'css/<%= pkg.name %>.css'],
            dest: 'css/<%= pkg.name %>_all.css'
        },
        mapcss: {
            src: ['assets/mapbox.1.6.1.css', 'assets/leaflet.label.0.2.1.css'],
            dest: 'css/map.css'
        },
        mapjs: {
            options: {stripBanners: false},
            src: ['assets/mapbox.1.6.1.js', 'assets/leaflet.label.0.2.1.js',
                  'assets/leaflet.spin.js', 'assets/simple_statistics.js',
                  'assets/spin.min.js', 'assets/d3.v3.min.js',
                  'assets/leaflet-image.js'],
            dest: 'js/map.js'
        },
        chartjs: {
            options: {stripBanners: false},
            src: ['assets/highcharts.3.0.10.js', 'assets/exporting.3.0.10.js'],
            dest: 'js/chart.js'
        },
    },
    cssmin: {
        css:{
            src: 'css/<%= pkg.name %>_all.css',
            dest: 'css/<%= pkg.name %>_all.min.css'
        },
        mapcss:{
            src: 'css/map.css',
            dest: 'css/map.min.css'
        }
    },
    uglify: {
        options: {
            banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n',
            mangle: false,
            beautify: false,
            compress: true,
            wrap: false,
            preserveComments: false
        },
        pkg: {
            files: {
                'js/<%= pkg.name %>.min.js': ['<%= concat.js.dest %>']
            }
        },
        map: {
            files: {
                'js/map.min.js': ['js/map.js']
            }
        },
        chart: {
            files: {
                'js/chart.min.js': ['js/chart.js']
            }
        }
    },
    copy: {
      fonts: {
        files: [
            {expand: true, cwd: 'assets/droidsans/', src: ['**'], dest: 'fonts/', filter: 'isFile'},
            {expand: true, cwd: 'assets/font-awesome-4.0.3/fonts/', src: ['**'], dest: 'fonts/', filter: 'isFile'},
        ]
      }
    },
    jshint: {
      files: ['Gruntfile.js', 'src/**/*.js'],
      options: {
        // options here to override JSHint defaults
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true
        }
      }
    },
    watch: {
      files: ['<%= jshint.files %>', 'src/less/*.less', 'src/js/*.js', 'assets/bootstrap.less'],
      tasks: ['dist-css', 'dist-js']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-css');

  grunt.registerTask('test', ['jshint']);

  // JS distribution task.
  grunt.registerTask('dist-js', ['concat']);

  // CSS distribution task.
  grunt.registerTask('dist-css', ['copy', 'less', 'concat', 'cssmin']);

  // Fonts distribution task.
  grunt.registerTask('dist-fonts', ['copy']);

  // Full distribution task.
  grunt.registerTask('dist', ['clean', 'dist-css', 'dist-fonts', 'dist-js']);

  grunt.registerTask('default', ['dist']);

};