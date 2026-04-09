package implementations

import (
	"PhotoEditor/png"
	"encoding/json"
	"fmt"
	"sync"
	"sync/atomic"
)

type BSPContext struct {
	ImageTasksDoneCounter int64
	ImageTaskPointers     []*png.ImageTask
}

func initBSPContext(data_dir []string, decoder *json.Decoder) BSPContext {
	newBSPContext := BSPContext{ImageTasksDoneCounter: int64(0)}
	for _, directory := range data_dir {
		for {
			effectData := EffectData{}
			err := decoder.Decode(&effectData)
			if err != nil && err.Error() == "EOF" {
				break
			} else if err != nil {
				panic(err)
			}

			pngImg, err := png.Load(fmt.Sprintf("../data/in/%s/%s", directory, effectData.InPath))
			if err != nil {
				panic(err)
			}

			pngImg.OutPathWithDataDir = fmt.Sprintf("../data/out/" + directory + "_" + effectData.OutPath)
			pngImg.Effects = effectData.Effects
			newBSPContext.ImageTaskPointers = append(newBSPContext.ImageTaskPointers, pngImg)
		}
	}

	return newBSPContext
}

func ExecuteBSP(threads int, wg *sync.WaitGroup, ctx *BSPContext) {
	for {
		imageTasksDoneCounter := atomic.SwapInt64(&ctx.ImageTasksDoneCounter, atomic.LoadInt64(&ctx.ImageTasksDoneCounter)+1)
		if imageTasksDoneCounter >= int64(len(ctx.ImageTaskPointers)) {
			wg.Done()
			return
		}

		currentImageTaskPointer := ctx.ImageTaskPointers[imageTasksDoneCounter]
		currentImageTaskPointer.In, currentImageTaskPointer.Out = currentImageTaskPointer.Out, currentImageTaskPointer.In
		for _, effect := range currentImageTaskPointer.Effects {
			if effect == "G" {
				currentImageTaskPointer.Grayscale(threads)
			} else if effect == "E" {
				currentImageTaskPointer.ApplyConvolution([9]float64{-1, -1, -1, -1, 8, -1, -1, -1, -1}, threads)
			} else if effect == "S" {
				currentImageTaskPointer.ApplyConvolution([9]float64{0, -1, 0, -1, 5, -1, 0, -1, 0}, threads)
			} else if effect == "B" {
				currentImageTaskPointer.ApplyConvolution([9]float64{1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0}, threads)
			}
		}
	}
}

func RunBSP(data_dir []string, threads int, decoder *json.Decoder) {
	var wg sync.WaitGroup
	ctx := initBSPContext(data_dir, decoder)
	for idx := 0; idx < threads; idx++ {
		wg.Add(1)
		go ExecuteBSP(threads, &wg, &ctx)
	}

	wg.Wait()
	for _, imageTaskPointer := range ctx.ImageTaskPointers {
		err := imageTaskPointer.Save(fmt.Sprintf(imageTaskPointer.OutPathWithDataDir))
		if err != nil {
			panic(err)
		}
	}
}
