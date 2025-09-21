package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
	"piscine/quads"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if len(lines) == 0 {
		fmt.Println("Not a quad function")
		return
	}

	y := len(lines)
	x := len(lines[0])
	for _, l := range lines {
		if len(l) != x {
			fmt.Println("Not a quad function")
			return
		}
	}

	results := []string{}
	if generateAndCompare(piscine.QuadA, x, y, lines) {
		results = append(results, fmt.Sprintf("[quadA] [%d] [%d]", x, y))
	}
	if generateAndCompare(piscine.QuadB, x, y, lines) {
		results = append(results, fmt.Sprintf("[quadB] [%d] [%d]", x, y))
	}
	if generateAndCompare(piscine.QuadC, x, y, lines) {
		results = append(results, fmt.Sprintf("[quadC] [%d] [%d]", x, y))
	}
	if generateAndCompare(piscine.QuadD, x, y, lines) {
		results = append(results, fmt.Sprintf("[quadD] [%d] [%d]", x, y))
	}
	if generateAndCompare(piscine.QuadE, x, y, lines) {
		results = append(results, fmt.Sprintf("[quadE] [%d] [%d]", x, y))
	}

	if len(results) == 0 {
		fmt.Println("Not a quad function")
		return
	}

	sort.Strings(results)
	fmt.Println(strings.Join(results, " || "))
}

func generateAndCompare(quad func(int, int), x, y int, input []string) bool {
	save := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	quad(x, y)

	w.Close()
	os.Stdout = save

	var outLines []string
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		outLines = append(outLines, scanner.Text())
	}

	if len(outLines) != len(input) {
		return false
	}
	for i := range outLines {
		if outLines[i] != input[i] {
			return false
		}
	}
	return true
}
