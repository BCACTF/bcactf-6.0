function createFlagChecker() {
    // Hardcoded secrets
    var secretA = 123;
    var secretB = 45;
    var secretC = 67;
    var secretD = 89;
    
    // This function will check if a given flag is correct
    function checkFlag(flag) {
        var checksum = 1337;
        var i = 0;
        
        // Process each character in the flag
        while (i < flag.length) {
            var charCode = flag.charCodeAt(i);
            
            // Apply different transformations based on position
            if (i % 4 == 0) {
                charCode = (charCode * 7 + 3) % 256;
            }
            if (i % 4 == 1) {
                charCode = (charCode * 3 + 5) % 256;
            }
            if (i % 4 == 2) {
                charCode = (charCode * 11 - 7) % 256;
            }
            if (i % 4 == 3) {
                charCode = (charCode * 5 + 9) % 256;
            }
            
            // Apply position-based secret
            if (i % 4 == 0) {
                charCode = (charCode + secretA) % 256;
            }
            if (i % 4 == 1) {
                charCode = (charCode + secretB) % 256;
            }
            if (i % 4 == 2) {
                charCode = (charCode + secretC) % 256;
            }
            if (i % 4 == 3) {
                charCode = (charCode + secretD) % 256;
            }
            
            // Update checksum
            checksum = (checksum * 31 + charCode) % 65521;
            
            i = i + 1;
        }
        
        // The expected checksum for the real flag
        // Replace this with the checksum for your actual flag
        var expectedChecksum = 63740;
        
        // Compare and return result
        return checksum == expectedChecksum;
    }
    
    return checkFlag;
}

// Create the checker function
var verifyFlag = createFlagChecker();

// Test with a flag
var result = verifyFlag("bcactf{FAKE_FLAG}");
console.log("Flag check result:", result);
