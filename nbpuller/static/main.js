define(['jquery'], function ($) {

    var readHello = function() {
        console.log('nbpuller is loaded');
    }

    var load_ipython_extension = function () {
        readHello();
    };

    return {
        load_ipython_extension : load_ipython_extension,
    };
});
