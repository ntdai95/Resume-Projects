package implementations

import (
	"PhotoEditor/png"
	"fmt"
	"sync"
	"sync/atomic"
)

type BSPContext struct {
	ImageTasksDoneCounter int64
	ImageTaskPointers     []*png.ImageTask
}

func initBSPContext(data_dir []string, effectDataList []EffectData) BSPContext {
	newBSPContext := BSPContext{ImageTasksDoneCounter: int64(0)}
	for _, directory := range data_dir {
		for _, effectData := range effectDataList {
			pngImg, err := png.Load(fmt.Sprintf("../data/in/%s/%s", directory, effectData.InPath))
			if err != nil {
				panic(err)
			}

			pngImg.OutPathWithDataDir = fmt.Sprintf("../data/out/%s_%s", directory, effectData.OutPath)
			pngImg.Effects = effectData.Effects
			newBSPContext.ImageTaskPointers = append(newBSPContext.ImageTaskPointers, pngImg)
		}
	}

	return newBSPContext
}

func ExecuteBSP(threads int, wg *sync.WaitGroup, ctx *BSPContext) {
	for {
		imageTasksDoneCounter := atomic.AddInt64(&ctx.ImageTasksDoneCounter, 1) - 1
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

func RunBSP(data_dir []string, threads int, effectDataList []EffectData) {
	var wg sync.WaitGroup
	ctx := initBSPContext(data_dir, effectDataList)
	for idx := 0; idx < threads; idx++ {
		wg.Add(1)
		go ExecuteBSP(threads, &wg, &ctx)
	}

	wg.Wait()
	for _, imageTaskPointer := range ctx.ImageTaskPointers {
		err := imageTaskPointer.Save(imageTaskPointer.OutPathWithDataDir)
		if err != nil {
			panic(err)
		}
	}
}
