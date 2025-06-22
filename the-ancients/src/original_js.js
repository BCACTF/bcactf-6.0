function createFlagChecker() {
  // Simple transformation keys
  var key1 = 11;
  var key2 = 22;
  var key3 = 33;
  var key4 = 44;
  
  // Store encoded version of flag to check against
  var encodedFlag = [109,121,130,143,127,124,156,153,132,117,87,158,62,74,88,139,65,136,84,96,66,117,87,158,62,74,88,139,65,136,84,96,66,117,87,158,62,74,88,139,65,136,84,96,66,117,87,158,62,74,88,139,65,136,85,154,111,124,85,99,115,73,147,139,123,136,81,98,125,74,142,153,62,122,128,99,115,71,86,169];
  
  function encodeFlag(flag) {
    var result = [];
    var i = 0;
    
    while (i < flag.length) {
      var charCode = flag.charCodeAt(i);
      var encoded;
      
      // Simple reversible transformations based on position
      if (i % 4 == 0) {
        encoded = (charCode + key1) % 256;
      } else if (i % 4 == 1) {
        encoded = (charCode + key2) % 256;
      } else if (i % 4 == 2) {
        encoded = (charCode + key3) % 256;
      } else {
        encoded = (charCode + key4) % 256;
      }
      
      result.push(encoded);
      i = i + 1;
    }
    
    return result;
  }
  // Check if the provided flag matches the expected flag
  function checkFlag(flag) {
    var encoded = encodeFlag(flag);
    
    return (encoded.toString() == encodedFlag.toString());
  }
  
  return checkFlag;
}

// Create the checker
var flagChecker = createFlagChecker();


// Test the checker
var result = flagChecker("bcactf{my_6r347_6r347_6r347_6r347_6r347_6r347_6r347_6r4ndf47h3r_pr06r4mm3d_7h15}");
console.log("Flag check result:", result);
