define(['backbone', 'jquery', 'js/models/file_uploader', 'js/views/file_uploader', 'js/common_helpers/template_helpers'],
    function (Backbone, $, FileUploaderModel, FileUploaderView, TemplateHelpers) {
        describe("FileUploaderView", function () {
            var verifyTitle, verifyInputLabel, verifyInputTip, verifySubmitButton, verifyExtensions, verifyText,
                verifyFileUploadOption, fileUploaderView;

            verifyText = function (css, expectedText) {
                expect(fileUploaderView.$(css).text().trim()).toBe(expectedText);
            };

            verifyTitle = function (expectedTitle) { verifyText('.form-title', expectedTitle); };

            verifyInputLabel = function (expectedLabel) { verifyText('.field-label', expectedLabel); };

            verifyInputTip = function (expectedTip) { verifyText('.tip', expectedTip); };

            verifySubmitButton = function (expectedButton) { verifyText('.submit-file-button', expectedButton); };

            verifyExtensions = function (expectedExtensions) {
                var acceptAttribute = fileUploaderView.$('input.input-file').attr('accept');
                if (expectedExtensions) {
                    expect(acceptAttribute).toBe(expectedExtensions);
                }
                else {
                    expect(acceptAttribute).toBe(undefined);
                }
            };

            verifyFileUploadOption = function (option, expectedValue) {
                expect(fileUploaderView.$('#file-upload-form').fileupload('option', option)).toBe(expectedValue);
            };

            beforeEach(function () {
                setFixtures("<div></div>");
                TemplateHelpers.installTemplate('templates/file-upload');
                fileUploaderView = new FileUploaderView({
                    model: new FileUploaderModel({})
                }).render();
            });

            it('has default values', function () {
                verifyTitle("");
                verifyInputLabel("");
                verifyInputTip("");
                verifySubmitButton("Upload File");
                verifyExtensions(null);
            });

            it ('can set text values, extensions, and url', function () {
                fileUploaderView = new FileUploaderView({
                    model: new FileUploaderModel({
                        title: "file upload title",
                        inputLabel: "test label",
                        inputTip: "test tip",
                        submitButtonText: "upload button text",
                        extensions: ".csv,.txt"
                    })
                }).render();

                verifyTitle("file upload title");
                verifyInputLabel("test label");
                verifyInputTip("test tip");
                verifySubmitButton("upload button text");
                verifyExtensions(".csv,.txt");
            });

            it ('can store upload URL', function () {
                fileUploaderView = new FileUploaderView({
                    model: new FileUploaderModel({
                        url: "http://upload"
                    })
                }).render();
                expect(fileUploaderView.$('#file-upload-form').attr('action')).toBe("http://upload");
            });

            it ('sets autoUpload to false', function () {
                verifyFileUploadOption('autoUpload', false);
            });

            it ('sets replaceFileInput to false', function () {
                verifyFileUploadOption('replaceFileInput', false);
            });
        });
    });
