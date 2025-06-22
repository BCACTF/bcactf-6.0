package main

import (
	"bufio"
	"crypto/rand"
	"fmt"
	"os"
	"strings"
)

// Generated constants for main.go
var encryptedFlag = []byte{
	0xdd, 0x7f, 0xdf, 0x3d, 0x93, 0x04, 0x77, 0x55,
	0x4a, 0x9b, 0xab, 0x9d, 0xef, 0xcc, 0x5b, 0x71,
	0xff, 0xe7, 0xeb, 0xb4, 0xb8, 0xc0, 0xff, 0xe1,
	0x60, 0x10, 0xa7, 0x1b, 0x05, 0xd1, 0x54, 0x3c,
	0xc0, 0xac, 0xdc, 0xcc, 0x41,
}
var flagLength = 37

// Decoy constants for obfuscation
const (
	magicConst1 = 0xDEADBEEF
	magicConst2 = 0xCAFEBABE
	magicConst3 = 0x1337C0DE
)

// Anti-tampering check
func environmentCheck() bool {
	// Simple entropy check to make analysis harder
	buf := make([]byte, 4)
	rand.Read(buf)
	return len(buf) == 4
}

// Main decryption function
func decryptFlag(encrypted []byte) string {
	if !environmentCheck() {
		return ""
	}

	// Stage 1: Reverse nibble swap and position XOR
	stage1 := make([]byte, len(encrypted))
	for i, b := range encrypted {
		// Reverse position XOR
		posXor := byte((i*3 + 0x55) & 0xFF)
		unxored := b ^ posXor
		// Reverse nibble swap
		original := ((unxored & 0x0F) << 4) | ((unxored & 0xF0) >> 4)
		stage1[i] = original
	}

	// Stage 2: Subtract rotating offset
	stage2 := make([]byte, len(stage1))
	for i, b := range stage1 {
		offset := byte((i*7 + 23) & 0xFF)
		stage2[i] = (b - offset) & 0xFF
	}

	// Stage 3: Reverse XOR with key
	key := []byte{0x13, 0x37, 0x42, 0x69, 0x88, 0xAA, 0xBB, 0xCC}
	final := make([]byte, len(stage2))
	for i, b := range stage2 {
		final[i] = b ^ key[i%len(key)]
	}

	return string(final)
}

// Decoy functions to confuse static analysis
func checkFormat(input string) bool {
	return strings.HasPrefix(input, "bcactf{") && strings.HasSuffix(input, "}")
}

func checkLength(input string) bool {
	return len(input) == flagLength
}

func checkCharacters(input string) bool {
	allowed := "abcdefghijklmnopqrstuvwxyz0123456789_{}"
	for _, c := range input {
		found := false
		for _, a := range allowed {
			if c == a {
				found = true
				break
			}
		}
		if !found {
			return false
		}
	}
	return true
}

// Main verification logic
func verifyFlag(input string) bool {
	// Basic checks first
	if !checkFormat(input) || !checkLength(input) || !checkCharacters(input) {
		return false
	}

	// Decrypt the stored flag and compare
	correctFlag := decryptFlag(encryptedFlag)
	return input == correctFlag
}

func printBanner() {
	fmt.Println(`
 ██████╗  ██████╗       ██████╗ ███████╗████████╗████████╗███████╗██████╗ 
██╔════╝ ██╔═══██╗     ██╔════╝ ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
██║  ███╗██║   ██║     ██║  ███╗█████╗     ██║      ██║   █████╗  ██████╔╝
██║   ██║██║   ██║     ██║   ██║██╔══╝     ██║      ██║   ██╔══╝  ██╔══██╗
╚██████╔╝╚██████╔╝     ╚██████╔╝███████╗   ██║      ██║   ███████╗██║  ██║
 ╚═════╝  ╚═════╝       ╚═════╝ ╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
`)
}

func main() {
	printBanner()

	// Anti-analysis: Use the magic constants
	_ = magicConst1 ^ magicConst2 ^ magicConst3

	fmt.Print("Enter the flag: ")
	reader := bufio.NewReader(os.Stdin)
	input, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("error reading input")
		return
	}

	input = strings.TrimSpace(input)

	if verifyFlag(input) {
		fmt.Println("\ngood boy.")
	} else {
		fmt.Println("\nbad boy.")
	}
}
