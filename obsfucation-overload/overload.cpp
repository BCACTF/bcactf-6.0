#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cstdint>
// bcactf RE + Crypto + Obfuscation Challenge
// Flag: bcactf{l33t_0bfusc4t3d_r3v_fun}


// Simple reversible encryption function
std::vector<uint8_t> simple_encrypt(const std::vector<uint8_t>& input, const std::vector<uint8_t>& key) {
    std::vector<uint8_t> encrypted(input);
    for (size_t i = 0; i < input.size(); ++i) {
        encrypted[i] ^= key[i % key.size()]; // XOR with the key
        encrypted[i] = (encrypted[i] + 0x10) & 0xFF; // Add 0x10 and wrap around to simulate a reversible transformation
    }
    return encrypted;
}

// Encode flag based on the user identifier
std::vector<uint8_t> encode_flag(const std::string& uname) {
    std::string seed = uname + "_bcactf2025";
    std::reverse(seed.begin(), seed.end());
    for (char& c : seed) c = ~c;

    std::vector<uint8_t> flag_data = {
        'b'^0x2A, 'c'^0x2A, 'a'^0x2A, 'c'^0x2A, 't'^0x2A, 'f'^0x2A, '{'^0x2A,
        'l'^0x2A, '3'^0x2A, '3'^0x2A, 't'^0x2A, '_'^0x2A,
        '0'^0x2A, 'b'^0x2A, 'f'^0x2A, 'u'^0x2A, 's'^0x2A, 'c'^0x2A, '4'^0x2A, 't'^0x2A, '3'^0x2A, 'd'^0x2A,
        '_'^0x2A, 'r'^0x2A, '3'^0x2A, 'v'^0x2A, '_'^0x2A, 'f'^0x2A, 'u'^0x2A, 'n'^0x2A, '}'^0x2A
    };

    std::vector<uint8_t> key(seed.begin(), seed.begin() + std::min<size_t>(seed.size(), 8));
    return simple_encrypt(flag_data, key);
}

std::string junky_message() {
    std::string m;
    for (int i = 0; i < 16; ++i)
        m += static_cast<char>((i % 26) + 'A');  // Replacing random with deterministic value
    return m;
}

void user_menu() {
    std::cout << "[Encrypted Communications v9.3]" << std::endl;
    std::cout << "1. Encode\n2. Decode\n3. Export Key\n4. License\n> ";
    int opt; std::cin >> opt; std::cin.ignore();
    if (opt == 4) {
        std::cout << "This tool is free to use for educational purposes.\n";
        return;
    }
    if (opt == 3) {
        std::ofstream fake("keyfile.dat", std::ios::binary);
        std::string k = junky_message();
        fake.write(k.c_str(), k.size());
        std::cout << "Keyfile saved.\n";
        return;
    }
    std::string msg;
    std::cout << "Enter data: ";
    std::getline(std::cin, msg);
    for (char& c : msg) c ^= 0x55;
    std::cout << ((opt == 1) ? "Encoded: " : "Decoded: ") << msg << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc == 2 && std::string(argv[1]) == "--access") {
        std::string name;
        std::cout << "Enter identifier > ";
        std::getline(std::cin, name);
        std::vector<uint8_t> encrypted = encode_flag(name);

        std::ofstream fout("payload.dat", std::ios::binary);
        fout.write(reinterpret_cast<const char*>(encrypted.data()), encrypted.size());
        fout.close();
        std::cout << "Encrypted payload saved.\n";
        return 0;
    }

    user_menu();
    return 0;
}