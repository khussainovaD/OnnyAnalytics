package piscine

import "fmt"

func QuadD (x, y int) {
	if x <= 0 || y <= 0 {
		return
	}

	mas1 := make([]string, x)
	for i := range mas1 {
		mas1[i] = "B"
	}

	mas2 := make([]string, x)
	for i := range mas2 {
		mas2[i] = " "
	}

	mas1[x-1] = "C"
	mas1[0] = "A"
	mas2[0] = "B"
	mas2[x-1] = "B"

	for _, ch := range mas1 {
		fmt.Print(ch)
	}
	fmt.Println()

	for i := 1; i <= y-2; i++ {
		for _, ch := range mas2 {
			fmt.Print(ch)
		}
		fmt.Println()
	}

	if y > 1 {
		mas1[x-1] = "C"
		mas1[0] = "A"
		for _, ch := range mas1 {	
			fmt.Print(ch)
		}
		fmt.Println()
	}
}
