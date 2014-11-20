var edx = edx || {};

(function(Backbone, $, _) {
    'use strict';

    edx.instructor_dashboard = edx.instructor_dashboard || {};
    edx.instructor_dashboard.ecommerce = {};

    edx.instructor_dashboard.ecommerce.AddExpiryCouponView = Backbone.View.extend({
        el: 'li#add-coupon-modal-field-expiry',
        events: {
            'click input[type="checkbox"]': 'clicked'
        },
        initialize: function() {
          _.bindAll(this, 'clicked');
          $( "#coupon_expiration_date" ).datepicker({
            minDate: 0
          });
          $('li#add-coupon-modal-field-expiry input[name="expiration_date"]').hide();
        },
        clicked: function (event) {
            if (event.currentTarget.checked) {
                this.$el.find('#coupon_expiration_date').show();
                this.$el.find('#coupon_expiration_date').focus();
            }
            else {
                this.$el.find('#coupon_expiration_date').hide();
            }
        }
    });

    $(function() {
        var view = new edx.instructor_dashboard.ecommerce.AddExpiryCouponView();
    });
}).call(this, Backbone, $, _);