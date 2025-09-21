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

	for _, ch := range mas1 {
		fmt.Print(ch)
	}
	fmt.Println()

	for i := 1; i <= y-2; i++ {
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

func QuadB(x, y int) {
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

	mas1[0] = "/"
	mas1[x-1] = "\\"
	mas2[0] = "*"
	mas2[x-1] = "*"

	for _, i := range mas1 {
		fmt.Print(i)
	}
	fmt.Println()

	for i := 1; i <= y-2; i++ {
		for _, j := range mas2 {
			fmt.Print(j)
		}
		fmt.Println()
	}

	if y > 1 {
		mas1[0] = "\\"
		mas1[x-1] = "/"
		for _, i := range mas1 {
			fmt.Print(i)
		}
		fmt.Println()
	}
}

func QuadC(x, y int) {
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

	mas1[0] = "A"
	mas1[x-1] = "A"
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
		mas1[0] = "C"
		mas1[x-1] = "C"
		for _, i := range mas1 {
			fmt.Print(i)
		}
		fmt.Println()
	}
}

func QuadD(x, y int) {
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

	mas1[0] = "A"
	mas1[x-1] = "C"
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
		mas1[0] = "A"
		mas1[x-1] = "C"
		for _, ch := range mas1 {
			fmt.Print(ch)
		}
		fmt.Println()
	}
}

func QuadE(x, y int) {
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

	mas1[0] = "A"
	mas1[x-1] = "C"
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
		mas1[0] = "C"
		mas1[x-1] = "A"
		for _, ch := range mas1 {
			fmt.Print(ch)
		}
		fmt.Println()
	}
}
