routers.App = Backbone.Router.extend({
    routes: {
        '': 'browser',
        'filter/*filters': 'browser',
        'project/:id': 'project',
        'project/:id/output-:output': 'project',
        'widget/*options': 'widget',
        'about/*subnav': 'about',
        'top-donors': 'topDonors'
    },

    mainApp: function () {
        // Handle feedback form submission
        $('#feedback-form').submit(function (e) {
            // Set URL for feedback form

            $('#entry_3').val(window.location);

            var button = $('input[type=submit]', this),
                data = $(this).serialize(),
                form = this;

            $.ajax({
                type: 'POST',
                url: 'https://docs.google.com/spreadsheet/formResponse?formkey=dFRTYXNUMWIzbXRhVF94YW9rVmlZNVE6MQ&amp;ifq',
                data: data,
                complete: function () {
                    $('#feedback').modal('hide');
                    $('input[type=text], textarea', form).val('');
                }
            });
            return false;
        });
    },

    browser: function (route) {
        var that = this;

        // Load in the top donors info and feedbackform dets.
        this.mainApp();
        window.setTimeout(function() { $('html, body').scrollTop(0); }, 0);

        // Set up menu
        $('#app .view, #mainnav li, #aboutnav').hide();
        $('#profile .summary').addClass('off');
        $('#browser, #mainnav .browser, #mainnav').show();

        // Set up breadcrumbs
        $('#breadcrumbs ul').html('<li><a href="' + BASE_URL + '">All Projects</a></li>');

        // Load the main app view
        this.app = this.app || new views.App({
            el: '#browser'
        });

        // Save default description
        app.defaultDescription = app.defaultDescription || $('#intro p').html();

        // Parse hash
        var parts = (route) ? route.split('/') : [];
        var filters = _(parts).map(function (part) {
            var filter = part.split('-');
            return {
                collection: filter[0],
                id: filter[1]
            };
        });

        if (_.isEqual(this.app.filters, filters)) {
            $('html, body').scrollTop(0);
        } else {
            var filter = function (model) {
                if (!filters.length) return true;
                return _(filters).reduce(function (memo, filter) {
                    if (filter.collection === 'region') {
                        return memo && model.get(filter.collection) == filter.id;
                    } else {
                        return memo && (model.get(filter.collection) && model.get(filter.collection).indexOf(filter.id) >= 0);
                    }
                }, true);
            };
            this.app.filters = filters;

            var loadFilters = function() {
                var counter = 0;
                that.app.views = {};
                // Load filters
                _(facets).each(function (facet) {
                    $('#filter-items').append('<div id="' + facet.id + '" class="topics"></div>');

                    var collection = new models.Filters();
                    _(facet).each(function (v, k) {
                        collection[k] = v;
                    });

                    collection.fetch({
                        success: function () {
                            that.app.views[facet.id] = new views.Filters({
                                el: '#' + facet.id,
                                collection: collection
                            });
                            _.each(filters, function (obj) {
                                if (obj.collection === facet.id) {
                                    that.app.views[facet.id].active = true;
                                }
                            });
                            collection.watch();

                            counter++;
                            if (counter === facets.length) updateDescription();

                        }
                    });
                });
            };

            // Load projects
            if (!this.allProjects) {
                this.allProjects = new models.Projects();
                this.allProjects.fetch({
                    success: function () {
                        that.projects = new models.Projects(that.allProjects.filter(filter));
                        var view = new views.Projects({
                            collection: that.projects
                        });

                        that.projects.watch();
                        loadFilters();

                        that.projects.map = new views.Map({
                            el: '#homemap',
                            collection: that.projects
                        });

                        that.projects.widget = new views.Widget({
                            context: 'projects'
                        });
                    }
                });
            } else {
                // if projects are already present
                this.projects.reset(this.allProjects.filter(filter));
                updateDescription();
            }
        }

        function updateDescription() {

            // Clear search values on refresh
            $('#filters-search, #projects-search').val('');

            if (_(filters).find(function(f) {
                return f.collection === 'focus_area';
            })) {
                $('#chart-focus_area').hide();
            } else {
                $('#chart-focus_area').show();
            }

            if (app.description.length > 1) {
                $('#applied-filters').html('Selected Projects');
                $('#intro p').html(app.description.shift() + app.description.join(',') + '.');
            } else {
                $('#applied-filters').html('All Projects');
                $('#intro p').html(app.defaultDescription);
            }
            app.description = false;
        }

        $('#browser .summary').removeClass('off');
    },

    project: function (id, output) {
        var that = this;

        // Load in the top donors info and feedbackform dets.
        this.mainApp();

        window.setTimeout(function() { $('html, body').scrollTop(0); }, 0);

        // Set up menu
        $('#app .view, #mainnav li, #aboutnav').hide();
        $('#browser .summary').addClass('off');
        $('#mainnav, #mainnav .profile').show();

        // Set up this route
        this.project.model = new models.Project({
            id: id
        });

        this.project.model.fetch({
            success: function () {
                that.project.view = new views.ProjectProfile({
                    el: '#profile',
                    model: that.project.model,
                    gotoOutput: (output) ? output : false
                });

                that.project.widget = new views.Widget({
                    context: 'project'
                });
            }
        });
    },

    widget: function (route) {
        var that = this,
            parts = route.split('?'),
            options = parts[1],
            path = parts[0];

        path = (path) ? path.split('/') : [];
        options = (options) ? options.split('&') : [];

        if (path[0] === 'project') {
            this.widget.model = new models.Project({
                id: path[1]
            });

            this.widget.model.fetch({
               success: function() {
                    that.widgetOutput = new views.WidgetOutput({
                        context: 'project',
                        options: options,
                        model: that.widget.model
                    });
               }
            });
        } else {
            this.widgetOutput = new views.WidgetOutput({
                context: 'projects',
                options: options
            });

            var filters = _(path).map(function (f) {
                var filter = f.split('-');
                return {
                    id: filter[1],
                    collection: filter[0]
                };
            });

            this.defaultTitle = this.defaultTitle || $('.heading-title').html();
            this.widgetOutput.filters = filters;

            var filter = function (model) {
                if (!filters.length) return true;
                return _(filters).reduce(function (memo, filter) {
                    if (filter.collection === 'region') {
                        return memo && model.get(filter.collection) == filter.id;
                    } else {
                        return memo && (model.get(filter.collection) && model.get(filter.collection).indexOf(filter.id) >= 0);
                    }
                }, true);
            };

            // Load projects
            if (!this.allProjects) {
                this.allProjects = new models.Projects();
                this.allProjects.fetch({
                    success: function () {
                        that.projects = new models.Projects(that.allProjects.filter(filter));
                        var view = new views.WidgetProjects({
                            collection: that.projects
                        });

                        that.projects.watch();
                        that.projects.map = new views.WidgetMap({
                            el: '#embed-map',
                            collection: that.projects
                        });
                    }
                });
            } else {
                // if projects are already present
                this.projects.reset(this.allProjects.filter(filter));
            }
        }
    },

    about: function (route) {
      window.setTimeout(function () {
          $('html, body').scrollTop(0);
      }, 0);

      $('#breadcrumbs ul').html('<li><a href="#">Home</a></li>' + '<li><a href="' + BASE_URL + '">Our Projects</a></li>' + '<li><a href="#about/open">About</a></li>');

      $('#app .view, #mainnav').hide();
      $('#aboutnav li').removeClass('active');
      $('#about .section').hide();

      $('#about, #aboutnav').show();
      $('#aboutnav li a[href="#about/' + route + '"]').parent().addClass('active');
      $('#about #' + route).show();
    },

    topDonors: function () {
      window.setTimeout(function () {
          $('html, body').scrollTop(0);
      }, 0);

      $('#breadcrumbs ul').html('<li><a href="#">Home</a></li>' + '<li><a href="' + BASE_URL + '">Our Projects</a></li>' + '<li><a href="#top-donors">Top Donors</a></li>');

      $('#app .view').hide();
      $('#mainnav li').removeClass('active');

      $('#top-donors').show();
      $('#mainnav li a[href="#top-donors"]').parent().addClass('active');

      var donorsGross = new models.TopDonors();
      donorsGross.url = 'api/top-donor-gross-index.json';

      var donorsLocal = new models.TopDonors();
      donorsLocal.url = 'api/top-donor-local-index.json';
      donorsGross.fetch({
          success: function () {
              this.topDonorsGross = new views.TopDonors({
                  el: '#donor-gross-table',
                  collection: donorsGross
              });
          }
      });
      donorsLocal.fetch({
          success: function () {
              this.topDonorsLocal = new views.TopDonors({
                  el: '#donor-local-table',
                  collection: donorsLocal
              });
          }
      });
    }
});
