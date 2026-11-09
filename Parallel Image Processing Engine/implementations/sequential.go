package implementations

import (
	"PhotoEditor/png"
	"fmt"
)

func SequentialImplementation(data_dir []string, effectDataList []EffectData) {
	for _, directory := range data_dir {
		for _, effectData := range effectDataList {
			pngImg, err := png.Load(fmt.Sprintf("../data/in/%s/%s", directory, effectData.InPath))
			if err != nil {
				panic(err)
			}

			pngImg.In, pngImg.Out = pngImg.Out, pngImg.In
			for _, effect := range effectData.Effects {
				if effect == "G" {
					pngImg.Grayscale(0)
				} else if effect == "E" {
					pngImg.ApplyConvolution([9]float64{-1, -1, -1, -1, 8, -1, -1, -1, -1}, 0)
				} else if effect == "S" {
					pngImg.ApplyConvolution([9]float64{0, -1, 0, -1, 5, -1, 0, -1, 0}, 0)
				} else if effect == "B" {
					pngImg.ApplyConvolution([9]float64{1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0, 1 / 9.0}, 0)
				}
			}

			err = pngImg.Save(fmt.Sprintf("../data/out/%s_%s", directory, effectData.OutPath))
			if err != nil {
				panic(err)
			}
		}
	}
}
