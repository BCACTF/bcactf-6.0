function createFlagChecker() {
  // Simple transformation keys
  var key1 = 11;
  var key2 = 22;
  var key3 = 33;
  var key4 = 44;
  
  // Store encoded version of flag to check against
  var encodedFlag = [
    // These values will be filled in when you calculate your encoded flag
  ];
  
  // Encode function that transforms each character in a reversible way
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
  
  // Decode function to reverse the transformation
  function decodeFlag(encoded) {
    var result = "";
    var i = 0;
    
    while (i < encoded.length) {
      var value = encoded[i];
      var charCode;
      
      // Reverse the transformations
      if (i % 4 == 0) {
        charCode = (value - key1 + 256) % 256;
      } else if (i % 4 == 1) {
        charCode = (value - key2 + 256) % 256;
      } else if (i % 4 == 2) {
        charCode = (value - key3 + 256) % 256;
      } else {
        charCode = (value - key4 + 256) % 256;
      }
      
      result += String.fromCharCode(charCode);
      i = i + 1;
    }
    
    return result;
  }
  
  // Check if the provided flag matches the expected flag
  function checkFlag(flag) {
    var encoded = encodeFlag(flag);
    
    if (encoded.length != encodedFlag.length) {
      return false;
    }
    
    var i = 0;
    var correct = true;
    while (i < encoded.length) {
      if (encoded[i] != encodedFlag[i]) {
        correct = false;
        break;
      }
      i = i + 1;
    }
    
    return correct;
  }
  
  return {
    check: checkFlag,
    encode: encodeFlag,
    decode: decodeFlag
  };
}

// Create the checker
var flagChecker = createFlagChecker();

// SECTION TO CALCULATE ENCODED VALUES FOR YOUR FLAG
var myFlag = "bcactf{my_6r347_6r347_6r347_6r347_6r347_6r347_6r347_6r4ndf47h3r_pr06r4mm3d_7h15}";
var encoded = flagChecker.encode(myFlag);
console.log("Encoded flag array:", JSON.stringify(encoded));
console.log("Copy these values into the encodedFlag array in your challenge.");

// Test the checker
var result = flagChecker.check(myFlag);
console.log("Flag check result:", result);

// Demonstration of reversibility
var decoded = flagChecker.decode(encoded);
console.log("Decoded flag:", decoded);
console.log("Decoding matches original:", decoded === myFlag);
