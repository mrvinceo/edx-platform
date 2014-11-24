define(['backbone', 'jquery', 'js/instructor_dashboard/ecommerce', 'js/common_helpers/template_helpers'],
    function (Backbone, $, ExpiryCouponView, TemplateHelpers) {
        'use strict';
        var expiryCouponView, createExpiryCoupon;
        describe("edx.instructor_dashboard.ecommerce.ExpiryCouponView", function() {
            beforeEach(function() {
                setFixtures('<li class="field full-width" id="add-coupon-modal-field-expiry"><input id="expiry-check" type="checkbox"/><label for="expiry-check"></label><input type="text" id="coupon_expiration_date" value="" class="field" name="expiration_date" aria-required="true"/></li>')
                expiryCouponView = new ExpiryCouponView();
            });

            it("expiration date checkbox defaults to False f", function () {
//                expect($('#add-coupon-modal-field-expiry').html()).toEqual('sad');
                expect(expiryCouponView.$el.html()).toEqual('sad');
                expiryCouponView.$el.find('input[type="checkbox"]').trigger('click');
                // Create a fake click event
//                var target = expiryCouponView.$('input[type="checkbox"]');
//                spyOn(expiryCouponView, 'clicked');
//                target.trigger('click');
//                expect(expiryCouponView.clicked).toHaveBeenCalled();
//                var clickEvent = $('#expiry-check').Event('click');
//                expiryCouponView.clicked(clickEvent);
//                expiryCouponView.$('#expiry-check').click();
                expect(expiryCouponView.$el.html()).toEqual('sad');
//                expect($('#expiry-check').val()).toEqual('');
            });
        });
    });
