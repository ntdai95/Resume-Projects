package main

import (
	"PhotoEditor/implementations"
	"encoding/json"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

const usage = "Usage: editor data_dir [mode] [number_of_threads]\n" +
	"data_dir = The data directories to use to load the images.\n" +
	"mode     = (bsp) run the BSP mode, (pipeline) run the pipeline mode\n" +
	"number_of_threads = Runs the parallel version of the program with the specified number of threads (i.e., goroutines)."

func main() {
	effectsFile, _ := os.Open("../data/effects.txt")
	defer effectsFile.Close()
	decoder := json.NewDecoder(effectsFile)

	commandLineArgumentsList := os.Args
	data_dir := strings.Split(commandLineArgumentsList[1], "+")
	for _, directory := range data_dir {
		if !slices.Contains([]string{"big", "mixture", "small"}, directory) {
			fmt.Println(usage)
			return
		}
	}

	if len(commandLineArgumentsList) == 2 {
		implementations.SequentialImplementation(data_dir, decoder)
	} else if len(commandLineArgumentsList) == 4 {
		threads, err := strconv.Atoi(commandLineArgumentsList[3])
		if err != nil {
			fmt.Println(usage)
			return
		} else if threads <= 0 {
			fmt.Println("Invalid number of threads! (i.e., goroutines to spawn)")
			return
		}

		if commandLineArgumentsList[2] == "pipeline" {
			implementations.FanInFanOutImplementation(data_dir, threads, decoder)
		} else if commandLineArgumentsList[2] == "bsp" {
			implementations.RunBSP(data_dir, threads, decoder)
		}
	} else {
		fmt.Println(usage)
	}
}
