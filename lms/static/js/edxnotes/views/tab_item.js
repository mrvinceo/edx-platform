;(function (define, undefined) {
'use strict';
define(['gettext', 'underscore', 'backbone'],
function (gettext, _, Backbone) {
    var TabItemView = Backbone.View.extend({
        tagName: 'li',
        className: 'tab-item',
        activeClassName: 'is-active',

        events: {
            'click': 'selectHandler',
            'click a': function (event) { event.preventDefault(); },
            'click .btn-close': 'closeHandler'
        },

        initialize: function (options) {
            _.bindAll(this);
            this.template = _.template($('#tab-item-tpl').text());
            this.options = options;
            this.$el.addClass(this.model.get('class_name'));
            this.bindEvents();
        },

        render: function () {
            var html = this.template(this.model.toJSON());
            this.$el.html(html);
            return this;
        },

        bindEvents: function () {
            this.model.on({
                'change:is_active': _.bind(function (model, value) {
                    if (value) {
                        this.$el.addClass(this.activeClassName);
                    } else {
                        this.$el.removeClass(this.activeClassName);
                    }
                }, this),
                'destroy': this.remove
            });
        },

        selectHandler: function (event) {
            event.preventDefault();
            this.select();
        },

        closeHandler: function (event) {
            event.preventDefault();
            event.stopPropagation();
            this.close();
        },

        select: function () {
            this.model.activate();
        },

        close: function () {
            this.model.destroy();
        }
    });

    return TabItemView;
});
}).call(this, define || RequireJS.define);
