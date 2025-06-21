package main

import (
	"bufio"
	"crypto/sha256"
	"fmt"
	"os"
	"strings"
)

// Generated encrypted flag - replace with output from genconst.py
var encryptedFlag = []byte{
	0x37, 0x9a, 0xb5, 0x3e, 0x6f, 0x11, 0xea, 0x91, 
	0x89, 0x52, 0x71, 0xbc, 0x4f, 0x7b, 0x2d, 0x97, 
	0x88, 0x52, 0x6c, 0x26, 0x3e, 0x3b, 0x26, 0xf7, 
	0x88, 0x7c, 0x74, 0x26, 0x3e, 0xed, 0x66, 0x79, 
	0x48, 0x88, 0x6c, 0xc6, 0xde, 
}

var flagLength = 37

// Obfuscated constants
const (
	magicNumber1 = 0x1337
	magicNumber2 = 0xDEADBEEF
	checksum1    = 0x42424242
	checksum2    = 0x13371337
)

// Anti-debug: Simple checksum validation
func validateEnvironment() bool {
	h := sha256.New()
	h.Write([]byte("go-getter-challenge"))
	hash := h.Sum(nil)
	return len(hash) == 32 // Always true, but obfuscates intent
}

// Decryption function - reverse of the encryption in genconst.py
func decryptFlag(encrypted []byte) string {
	if !validateEnvironment() {
		return "Environment validation failed"
	}

	// Stage 1: Reverse bit rotation
	stage1 := make([]byte, len(encrypted))
	for i, byte := range encrypted {
		rot := i % 8
		if rot == 0 {
			stage1[i] = byte
		} else {
			// Rotate right by rot positions (reverse of left rotation)
			rotated := ((byte >> rot) | (byte << (8 - rot))) & 0xFF
			stage1[i] = rotated
		}
	}

	// Stage 2: Reverse add/subtract operations
	stage2 := make([]byte, len(stage1))
	for i, byte := range stage1 {
		if i%2 == 0 {
			stage2[i] = (byte - 0x17) & 0xFF
		} else {
			stage2[i] = (byte + 0x23) & 0xFF
		}
	}

	// Stage 3: Reverse XOR with rotating key
	xorKey := []byte{0x42, 0x13, 0x37, 0x89, 0xAB, 0xCD, 0xEF, 0x21}
	final := make([]byte, len(stage2))
	for i, byte := range stage2 {
		final[i] = byte ^ xorKey[i%len(xorKey)]
	}

	return string(final)
}

// Fake flag checker functions for misdirection
func checkFlag1(input string) bool {
	return strings.HasPrefix(input, "flag{") && strings.HasSuffix(input, "}")
}

func checkFlag2(input string) bool {
	if len(input) < 10 {
		return false
	}
	checksum := 0
	for _, char := range input {
		checksum += int(char)
	}
	return checksum > 1000 // Meaningless check
}

func obfuscatedCheck(input string) bool {
	// Another layer of misdirection
	temp := make([]byte, len(input))
	for i, char := range input {
		temp[i] = byte(char) ^ 0xFF
	}
	return len(temp) == len(input) // Always true
}

// Main verification function
func verifyFlag(input string) bool {
	if len(input) != flagLength {
		return false
	}

	// Basic format checks (misdirection)
	if !checkFlag1(input) || !checkFlag2(input) || !obfuscatedCheck(input) {
		return false
	}

	// The real check - decrypt and compare
	decrypted := decryptFlag(encryptedFlag)
	return input == decrypted
}

// Welcome message with some ASCII art
func printWelcome() {
	fmt.Println(`
 ██████╗  ██████╗        ██████╗ ███████╗████████╗████████╗███████╗██████╗ 
██╔════╝ ██╔═══██╗      ██╔════╝ ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
██║  ███╗██║   ██║█████╗██║  ███╗█████╗     ██║      ██║   █████╗  ██████╔╝
██║   ██║██║   ██║╚════╝██║   ██║██╔══╝     ██║      ██║   ██╔══╝  ██╔══██╗
╚██████╔╝╚██████╔╝      ╚██████╔╝███████╗   ██║      ██║   ███████╗██║  ██║
 ╚═════╝  ╚═════╝        ╚═════╝ ╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                             
                          Reverse Engineering Challenge
                               Can you find the flag?
    `)
}

func main() {
	printWelcome()

	// Some anti-analysis tricks
	dummy1 := magicNumber1 ^ magicNumber2
	dummy2 := checksum1 + checksum2
	_ = dummy1 + dummy2 // Use the variables to prevent optimization

	fmt.Print("Enter the flag: ")
	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("Error reading input!")
		return
	}

	input = strings.TrimSpace(input)

	if verifyFlag(input) {
		fmt.Println("🎉 Congratulations! You found the correct flag!")
		fmt.Println("Great job reverse engineering the Go-Getter challenge!")
	} else {
		fmt.Println("❌ Wrong flag. Keep trying!")
		fmt.Println("Hint: The flag is encrypted using multiple stages...")
	}
}
