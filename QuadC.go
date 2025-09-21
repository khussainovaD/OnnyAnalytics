package piscine

import "fmt"

func QuadC(x, y int) {
	if x <= 0 || y <= 0 {
		return
	}

	mas1 := make([]string, x)
	for i := range mas1 { 			// заполнение массива "-"
		mas1[i] = "B"
	}

	mas2 := make([]string, x) 		// заполнение массива " "
	for i := range mas2 {
		mas2[i] = " "
	}
 
	mas1[x-1] = "A"
	mas1[0] = "A"
	mas2[0] = "B"
	mas2[x-1] = "B"
 
	for _, ch := range mas1 {		 // вывод крышки
		fmt.Print(ch)
	}
	fmt.Println()

	for i := 1; i <= y-2; i++ { 	// вывод средних строк
		for _, ch := range mas2 {
			fmt.Print(ch)
		}
		fmt.Println()
	}

	if y > 1 { 						// вывод дна
		mas1[x-1] = "C"
		mas1[0] = "C"
		for _, i := range mas1 {
			fmt.Print(i)
		}
		fmt.Println()
	}
}
