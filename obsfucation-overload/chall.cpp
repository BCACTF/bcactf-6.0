#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cstdint>
#include <algorithm>

std::vector<uint8_t> generateKey(const std::string& username1, const std::string& username2) {
    std::vector<uint8_t> key;
    size_t len = std::max(username1.size(), username2.size());

    for (size_t i = 0; i < len; ++i) {
        uint8_t byte1 = (i < username1.size()) ? username1[i] : 0;
        uint8_t byte2 = (i < username2.size()) ? username2[i] : 0;
        
        uint8_t xor_result = byte1 ^ byte2;
        key.push_back(xor_result);
    }

    for (size_t i = 0; i < key.size(); ++i) {
        key[i] = (key[i] << (i % 8)) | (key[i] >> (8 - (i % 8)));
    }

    std::reverse(key.begin(), key.end());

    return key;
}

std::vector<uint8_t> encryptText(const std::vector<uint8_t>& text_data, const std::vector<uint8_t>& key) {
    std::vector<uint8_t> encrypted_data(text_data.size());

    for (size_t i = 0; i < text_data.size(); ++i) {
        encrypted_data[i] = text_data[i] ^ key[i % key.size()];
    }
    
    return encrypted_data;
}

std::string toHex(const std::vector<uint8_t>& data) {
    std::string hex_str;
    for (uint8_t byte : data) {
        char buffer[3];
        snprintf(buffer, sizeof(buffer), "%02x", byte);
        hex_str += buffer;
    }
    return hex_str;
}

int main(int argc, char* argv[]) {
    bool accessGranted = false;
    if (argc >= 2 && std::string(argv[1]) == "--access") {
        accessGranted = true;
    }

    if (!accessGranted) {
        std::cout << "Access Denied! Please provide the correct flag to proceed." << std::endl;
        return 1;
    }

    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " --access <username1> <username2> <text_to_encrypt>\n";
        return 1;
    }

    std::string username1 = argv[2];
    std::string username2 = argv[3];
    std::string text_to_encrypt = argv[4];

    std::vector<uint8_t> text_data(text_to_encrypt.begin(), text_to_encrypt.end());
    std::vector<uint8_t> key = generateKey(username1, username2);

    std::vector<uint8_t> encrypted_data = encryptText(text_data, key);
    std::cout << "Encrypted Text: " << toHex(encrypted_data) << std::endl;

    return 0;
}
