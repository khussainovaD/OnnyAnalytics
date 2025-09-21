package piscine

import "fmt"

func QuadA(x, y int) {
	if x <= 0 || y <= 0 {
		return
	}

	mas1 := make([]string, x)
	for i := range mas1 {
		mas1[i] = "*"
	}

	mas2 := make([]string, x)
	for i := range mas2 {
		mas2[i] = " "
	}

	mas1[0] = "o"
	mas1[x-1] = "o"
	mas2[0] = "|"
	mas2[x-1] = "|"

	for _, ch := range mas1 { 			// вывод крышки
		fmt.Print(ch)
	}
	fmt.Println() 

	for i := 1; i <= y-2; i++ { 			// вывод средних строк
		for _, j := range mas2 {
			fmt.Print(j)
		}
		fmt.Println()
	}

	if y > 1 {
		for _, ch := range mas1 {
			fmt.Print(ch)
		}
		fmt.Println()
	}
}
