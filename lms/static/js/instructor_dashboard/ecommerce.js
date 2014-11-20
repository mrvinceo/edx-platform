var edx = edx || {};

(function(Backbone, $, _) {
    'use strict';

    edx.instructor_dashboard = edx.instructor_dashboard || {};
    edx.instructor_dashboard.ecommerce = {};

    edx.instructor_dashboard.ecommerce.AddExpiryCouponView = Backbone.View.extend({
        events: {
            'click input[type="checkbox"]': 'clicked'
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
        $( "#coupon_expiration_date" ).datepicker({
             minDate: 0
        });
        $('li#add-coupon-modal-field-expiry input[name="expiration_date"]').hide();
        var view = new edx.instructor_dashboard.ecommerce.AddExpiryCouponView({
            el: $('li#add-coupon-modal-field-expiry')
        });
    });
}).call(this, Backbone, $, _);