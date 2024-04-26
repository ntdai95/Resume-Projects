package png

import (
	"image"
	"image/color"
	"image/png"
	"math"
	"os"
)

type ImageTask struct {
	In                 *image.RGBA64
	Out                *image.RGBA64
	Bounds             image.Rectangle
	OutPathWithDataDir string
	Effects            []string
}

func Load(filePath string) (*ImageTask, error) {

	inReader, err := os.Open(filePath)

	if err != nil {
		return nil, err
	}
	defer inReader.Close()

	inOrig, err := png.Decode(inReader)

	if err != nil {
		return nil, err
	}

	bounds := inOrig.Bounds()

	outImg := image.NewRGBA64(bounds)
	inImg := image.NewRGBA64(bounds)

	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, a := inOrig.At(x, y).RGBA()
			inImg.Set(x, y, color.RGBA64{uint16(r), uint16(g), uint16(b), uint16(a)})
		}
	}
	task := &ImageTask{}
	task.In = inImg
	task.Out = outImg
	task.Bounds = bounds
	return task, nil
}

func (img *ImageTask) Save(filePath string) error {

	outWriter, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer outWriter.Close()

	err = png.Encode(outWriter, img.Out)
	if err != nil {
		return err
	}
	return nil
}

func clamp(comp float64) uint16 {
	return uint16(math.Min(65535, math.Max(0, comp)))
}
