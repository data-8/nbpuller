define(function(){
  return {
    // this will be called at extension loading time
    //---
    load_ipython_extension: function(){
        console.log("I have been loaded ! -- my nb extension");
    }
    //---
  };
})
