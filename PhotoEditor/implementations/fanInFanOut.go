package implementations

import (
	"PhotoEditor/png"
	"encoding/json"
	"fmt"
)

func ImageTaskGenerator(directory string, effectData EffectData) png.ImageTask {
	pngImg, err := png.Load(fmt.Sprintf("../data/in/%s/%s", directory, effectData.InPath))
	if err != nil {
		panic(err)
	}

	pngImg.OutPathWithDataDir = fmt.Sprintf("../data/out/" + directory + "_" + effectData.OutPath)
	pngImg.Effects = effectData.Effects
	return *pngImg
}

func FanIn(data_dir []string, decoder *json.Decoder) <-chan png.ImageTask {
	imageTaskChannel := make(chan png.ImageTask)
	go func() {
		for _, directory := range data_dir {
			for {
				effectData := EffectData{}
				err := decoder.Decode(&effectData)
				if err != nil && err.Error() == "EOF" {
					break
				} else if err != nil {
					panic(err)
				}

				imageTaskChannel <- ImageTaskGenerator(directory, effectData)
			}
		}

		close(imageTaskChannel)
	}()

	return imageTaskChannel
}

func Worker(imageTaskPointer *png.ImageTask, threads int) png.ImageTask {
	imageTaskPointer.In, imageTaskPointer.Out = imageTaskPointer.Out, imageTaskPointer.In
	for _, effect := range imageTaskPointer.Effects {
		if effect == "G" {
			imageTaskPointer.Grayscale(threads)
		} else if effect == "E" {
			imageTaskPointer.ApplyConvolution([9]float64{-1, -1, -1, -1, 8, -1, -1, -1, -1}, threads)
		} else if effect == "S" {
			imageTaskPointer.ApplyConvolution([9]float64{0, -1, 0, -1, 5, -1, 0, -1, 0}, threads)
		} else if effect == "B" {
			imageTaskPointer.ApplyConvolution([9]float64{1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0}, threads)
		}
	}

	return *imageTaskPointer
}

func FanOut(imageTaskChannel <-chan png.ImageTask, threads int) <-chan png.ImageTask {
	imageResultChannel := make(chan png.ImageTask)
	done := make(chan bool)
	for i := 0; i < threads; i++ {
		go func() {
			for {
				imageTask, inProgress := <-imageTaskChannel
				if inProgress {
					imageResultChannel <- Worker(&imageTask, threads)
				} else {
					done <- true
					break
				}
			}
		}()
	}

	go func() {
		for i := 0; i < threads; i++ {
			<-done
		}

		close(imageResultChannel)
	}()

	return imageResultChannel
}

func ResultsAggregator(imageResultPointer *png.ImageTask) {
	err := imageResultPointer.Save(fmt.Sprintf(imageResultPointer.OutPathWithDataDir))
	if err != nil {
		panic(err)
	}
}

func FanInFanOutImplementation(data_dir []string, threads int, decoder *json.Decoder) {
	imageTaskChannel := FanIn(data_dir, decoder)
	imageResultChannel := FanOut(imageTaskChannel, threads)
	done := make(chan bool)
	go func() {
		for {
			imageResult, inProgress := <-imageResultChannel
			if inProgress {
				ResultsAggregator(&imageResult)
			} else {
				done <- true
				break
			}
		}
	}()

	<-done
}
