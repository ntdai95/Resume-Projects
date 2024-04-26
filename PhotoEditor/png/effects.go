package png

import (
	"image/color"
)

func (img *ImageTask) WorkerGrayscale(min_y, max_y, min_x, max_x int) {
	for y := min_y; y < max_y; y++ {
		for x := min_x; x < max_x; x++ {
			r, g, b, a := img.In.At(x, y).RGBA()
			greyC := clamp(float64(r+g+b) / 3)
			img.Out.Set(x, y, color.RGBA64{greyC, greyC, greyC, uint16(a)})
		}
	}
}

func (img *ImageTask) Grayscale(threads int) {
	img.In, img.Out = img.Out, img.In
	bounds := img.Bounds
	if threads == 0 {
		img.WorkerGrayscale(bounds.Min.Y, bounds.Max.Y, bounds.Min.X, bounds.Max.X)
	} else if threads > 0 {
		done := make(chan bool)
		rowsPerWorker := (bounds.Max.Y - bounds.Min.Y) / threads
		for i := 0; i < threads; i++ {
			min_y := bounds.Min.Y + i*rowsPerWorker
			max_y := min_y + rowsPerWorker
			if i == threads-1 {
				max_y = bounds.Max.Y
			}

			go func(min_y, max_y int) {
				img.WorkerGrayscale(min_y, max_y, bounds.Min.X, bounds.Max.X)
				done <- true
			}(min_y, max_y)
		}

		for i := 0; i < threads; i++ {
			<-done
		}
	}
}

func (img *ImageTask) WorkerApplyConvolution(kernel [9]float64, min_y, max_y, min_x, max_x int) {
	var a uint16
	for y := min_y; y < max_y; y++ {
		for x := min_x; x < max_x; x++ {
			r, g, b := 0.0, 0.0, 0.0

			for row := -1; row <= 1; row++ {
				for column := -1; column <= 1; column++ {
					px := x + column
					py := y + row

					d_r, d_g, d_b, d_a := img.In.At(px, py).RGBA()
					if min_x <= px && px < max_x && min_y <= py && py < max_y {
						r += float64(d_r) * kernel[(row+1)*3+(column+1)]
						g += float64(d_g) * kernel[(row+1)*3+(column+1)]
						b += float64(d_b) * kernel[(row+1)*3+(column+1)]
						a = uint16(d_a)
					}
				}
			}

			img.Out.Set(x, y, color.RGBA64{clamp(r), clamp(g), clamp(b), a})
		}
	}
}

func (img *ImageTask) ApplyConvolution(kernel [9]float64, threads int) {
	img.In, img.Out = img.Out, img.In
	bounds := img.Bounds
	if threads == 0 {
		img.WorkerApplyConvolution(kernel, bounds.Min.Y, bounds.Max.Y, bounds.Min.X, bounds.Max.X)
	} else if threads > 0 {
		done := make(chan bool)
		rowsPerWorker := (bounds.Max.Y - bounds.Min.Y) / threads
		for i := 0; i < threads; i++ {
			min_y := bounds.Min.Y + i*rowsPerWorker
			max_y := min_y + rowsPerWorker
			if i == threads-1 {
				max_y = bounds.Max.Y
			}

			go func(min_y, max_y int) {
				img.WorkerApplyConvolution(kernel, min_y, max_y, bounds.Min.X, bounds.Max.X)
				done <- true
			}(min_y, max_y)
		}

		for i := 0; i < threads; i++ {
			<-done
		}
	}
}
