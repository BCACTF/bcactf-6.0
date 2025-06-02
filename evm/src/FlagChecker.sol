// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract FlagChecker {
    // Group 1 keys (16 bytes)
    bytes16 private constant K1  = hex"c5d71484f8cf9bf4b76f47904730804b";
    bytes16 private constant OB1 = hex"a8b576e88daae1c2885f77f57702fa15";

    // Group 2 keys (16 bytes)
    bytes16 private constant K2  = hex"9e3225a9f133b5dea168f4e2851f072f";
    bytes16 private constant OB2 = hex"10659bdc6368e83dd4d62a13f3523aa1";

    // Group 3 keys (12 bytes)
    bytes12 private constant K3  = hex"cc00fcaa7ca62061717a48e5";
    bytes12 private constant OB3 = hex"ff64a39c4c96443e1b4a7098";

    // Extra sum check
    uint16 private constant SUM_CHECK = 260;

    function checkFlag(string memory input) external pure returns (bool) {
        bytes memory b = bytes(input);
        if (b.length != 44) {
            return false;
        }

        // ── Group 1 (indices 0..15) ──
        //   (use uint16 to avoid overflow when adding 1)
        for (uint256 i = 0; i < 16; i++) {
            uint8 obfByte = uint8(uint128(OB1) >> ((15 - i) * 8));
            uint8 keyByte = uint8(uint128(K1)  >> ((15 - i) * 8));

            // do XOR in uint8, then cast to uint16 before adding 1, then truncate to uint8
            uint16 tmp = uint16(uint8(b[i]) ^ keyByte) + 1;
            uint8 calc  = uint8(tmp & 0xFF);

            if (calc != obfByte) {
                return false;
            }
        }

        // ── Group 2 (indices 16..31) ──
        //   (use uint16 to force-wrap on overflow)
        for (uint256 i = 16; i < 32; i++) {
            uint256 idx     = i - 16;  // 0..15
            uint8   obfByte = uint8(uint128(OB2) >> ((15 - idx) * 8));
            uint8   keyByte = uint8(uint128(K2)  >> ((15 - idx) * 8));

            // wrap in uint16, then truncate back to uint8
            uint16 tmp = uint16(uint8(b[i])) + uint16(keyByte);
            uint8  calc = uint8(tmp & 0xFF);

            if (calc != obfByte) {
                return false;
            }
        }

        // ── Group 3 (indices 32..43) ──
        for (uint256 i = 32; i < 44; i++) {
            uint256 idx     = i - 32;  // 0..11
            uint8   obfByte = uint8(uint96(OB3) >> ((11 - idx) * 8));
            uint8   keyByte = uint8(uint96(K3)  >> ((11 - idx) * 8));
            uint8   calc    = uint8(b[i]) ^ keyByte;

            if (calc != obfByte) {
                return false;
            }
        }

        // ── Extra sum check ──
        uint16 sum3 = uint16(uint8(b[4])) + uint16(uint8(b[10])) + uint16(uint8(b[15]));
        if (sum3 != SUM_CHECK) {
            return false;
        }

        return true;
    }
}
