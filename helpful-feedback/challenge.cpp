#include <iostream>
#include <string>
#include <functional>
#include <cstdlib>
#include <csignal>
#include <unistd.h>
#ifdef __linux__
#include <sys/ptrace.h>
#endif

class AntiDebug {
public:
    AntiDebug() {
    #ifdef __linux__
        if(ptrace(PTRACE_TRACEME, 0, nullptr, 0) == -1)
            std::raise(SIGKILL);
    #endif
    }
};

float intToFloat(unsigned int x) {
    union { unsigned int i; float f; } u;
    u.i = x;
    return u.f;
}

// ----------------------------------------------------------------------------
// ObfMatrix encapsulates the obfuscated matrix containing the 28 encoded 
// (transformed) flag bytes. The 4x7 matrix is stored as 14 floats (2 values per float).
//
// As described, the matrix is arranged so that when traversed in snake order
// the expected transformed values are produced in natural order.
//
// For a flag byte v, first compute:
//    T = (v * 2) XOR 0x55
// Then encode T into a 16‑bit value via:
//    encoded16 = ( (T XOR 0xAA) << 8 ) | (T XOR 0x55 )
// 
// The matrix is built from the following logical (snake‐ordered) values:
//   (Natural transforms for F = "bcactf{100k5_600d_70_m3_51r}")
//
// Row0 (F[0..6]):      145, 147, 151, 147, 189, 153, 163  
// Row1 (snake reading should yield F[7..13]): 55, 53, 53, 131, 63, 235, 57  
//    so we store row1 in reverse: [57, 235, 63, 131, 53, 53, 55]
// Row2 (F[14..20]):     53, 53, 157, 235, 59, 53, 235  
// Row3 (snake reading should yield F[21..27]): 143, 51, 235, 63, 55, 177, 175  
//    so we store row3 reversed: [175, 177, 55, 63, 235, 51, 143]
//
// We then list the 28 values in row‐major order (positions 0..27) and pair them two‐by‐two.
//
// The pairs (shown here in hex) are computed as follows:
//   For each value T, compute encoded16 = ( (T XOR 0xAA) << 8 ) | (T XOR 0x55 )
// Then form a 32‑bit word: if T_low is from an even index and T_hi from the next odd index:
//   word = ( encoded16_hi << 16 ) | encoded16_low
//
// Precomputed pairs for our matrix:
//
// Pair0: indices 0,1:  [145, 147]    → 0x39C63BC4  
// Pair1: indices 2,3:  [151, 147]    → 0x39C63DC2  
// Pair2: indices 4,5:  [189, 153]    → 0x33CC17E8  
// Pair3: indices 6,7:  [163, 57]     → 0x936C09F6  
// Pair4: indices 8,9:  [235, 63]     → 0x956A41BE  
// Pair5: indices 10,11:[131, 53]     → 0x9F6029D6  
// Pair6: indices 12,13:[53, 55]      → 0x9D629F60  
// Pair7: indices 14,15:[53, 53]      → 0x9F609F60  
// Pair8: indices 16,17:[157, 235]    → 0x41BE37C8  
// Pair9: indices 18,19:[59, 53]      → 0x9F60916E  
// Pair10: indices 20,21:[235, 175]   → 0x05FA41BE  
// Pair11: indices 22,23:[177, 55]    → 0x9D621BE4  
// Pair12: indices 24,25:[63, 235]    → 0x41BE956A  
// Pair13: indices 26,27:[51, 143]    → 0x25DA9966
//
// (All numbers given in hex.)
//
class ObfMatrix {
public:
    static const int ROWS = 4;
    static const int COLS = 7;
    static const int TOTAL = ROWS * COLS;

    // The 14 float values hide our 32-bit words.
    const float obfData[14] = {
        intToFloat(0x39C63BC4), // Pair0
        intToFloat(0x39C63DC2), // Pair1
        intToFloat(0x33CC17E8), // Pair2
        intToFloat(0x936C09F6), // Pair3
        intToFloat(0x956A41BE), // Pair4
        intToFloat(0x9F6029D6), // Pair5
        intToFloat(0x9D629F60), // Pair6
        intToFloat(0x9F609F60), // Pair7
        intToFloat(0x41BE37C8), // Pair8
        intToFloat(0x9F60916E), // Pair9
        intToFloat(0x05FA41BE), // Pair10
        intToFloat(0x9D621BE4), // Pair11
        intToFloat(0x41BE956A), // Pair12
        intToFloat(0x25DA9966)  // Pair13
    };


    const std::function<unsigned int(unsigned int)> decode16 = [](unsigned int encoded16) -> unsigned int {
        unsigned int high = (encoded16 >> 8) & 0xFF;
        unsigned int low  = encoded16 & 0xFF;
        unsigned int cand1 = high ^ 0xAA;
        unsigned int cand2 = low  ^ 0x55;
        if(cand1 != cand2) std::exit(EXIT_FAILURE);
        return cand1;
    };


    unsigned int getExpected(int index) const {
        if (index < 0 || index >= TOTAL) std::exit(EXIT_FAILURE);
        int pairIndex = index / 2;
        bool lowHalf = (index % 2 == 0);
        union { float f; unsigned int i; } u;
        u.f = obfData[pairIndex];
        unsigned int encoded16;
        if(lowHalf)
            encoded16 = u.i & 0xFFFF;
        else
            encoded16 = (u.i >> 16) & 0xFFFF;
        return decode16(encoded16);
    }
};

// ----------------------------------------------------------------------------
// FlagChecker uses a functional approach (via lambdas) to check the input.
// It iterates over the 4×7 matrix in snake (zigzag) order—rows 0 and 2 read 
// The transformation is: (input_char * 2) XOR 0x55.
class FlagChecker {
public:
    static const int ROWS = ObfMatrix::ROWS;
    static const int COLS = ObfMatrix::COLS;
    static const int TOTAL = ObfMatrix::TOTAL;

    const std::function<unsigned int(char)> transform = [](char c) -> unsigned int {
        return ((unsigned int)c * 2) ^ 0x55;
    };

    // checkFlag returns true only if all positions verify.
    bool checkFlag(const std::string &input, const ObfMatrix &matrix) const {
        if (input.length() != TOTAL) return false;
        int inputIndex = 0;
        // For each row, process in snake order.
        auto processRow = [this, &input, &inputIndex, &matrix](int row) -> bool {
            if (row % 2 == 0) { // even rows: left-to-right
                for (int col = 0; col < COLS; ++col) {
                    unsigned int expected = matrix.getExpected(row * COLS + col);
                    if (transform(input[inputIndex]) != expected)
                        return false;
                    ++inputIndex;
                }
            } else { // odd rows: right-to-left
                for (int col = COLS - 1; col >= 0; --col) {
                    unsigned int expected = matrix.getExpected(row * COLS + col);
                    if (transform(input[inputIndex]) != expected)
                        return false;
                    ++inputIndex;
                }
            }
            return true;
        };

        for (int row = 0; row < ROWS; ++row) {
            if (!processRow(row))
                return false;
        }
        return true;
    }
};

int main() {
    AntiDebug antiDebug;

    ObfMatrix matrix;
    FlagChecker checker;

    std::function<bool(const std::string&)> predicate = [&checker, &matrix](const std::string &s) -> bool {
        return checker.checkFlag(s, matrix);
    };

    std::string input;
    while (std::getline(std::cin, input)) {
        if (input.length() != FlagChecker::TOTAL || !predicate(input))
            std::exit(EXIT_FAILURE);
    }
    return 0;
}

