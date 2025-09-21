package piscine

import "fmt"

func QuadB(x, y int) {
	if x <= 0 || y <= 0 {
		return
	}

	mas1 := make([]string, x)
	for i := range mas1 { // заполнение массива "-"
		mas1[i] = "*"
	}

	mas2 := make([]string, x) // заполнение массива " "
	for i := range mas2 {
		mas2[i] = " "
	}

	mas1[0] = "/"
	mas1[x-1] = "\\"
	mas2[0] = "*"
	mas2[x-1] = "*"
	
	for _, i := range mas1 { // вывод крышки
		fmt.Print(i)
	}
	fmt.Println()

	for i := 1; i <= y-2; i++ { // вывод средних строк
		for _, j := range mas2 {
			fmt.Print(j)
		}
		fmt.Println()
	}

	if y > 1 { // вывод дна
		mas1[0] = "\\"
		mas1[x-1] = "/"
		for _, i := range mas1 {
			fmt.Print(i)
		}
		fmt.Println()
	}
}
