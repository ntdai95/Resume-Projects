# Parallel Image Processing Engine

This project applies grayscale, blur, sharpen, and edge-detection effects to
PNG images through three execution models written in Go: sequential,
fan-in/fan-out, and bulk synchronous parallel.

The original benchmark processed batches of more than 30 images. The
fan-in/fan-out pipeline reduced runtime by 20%, while the bulk synchronous model
reduced it by 30%, relative to sequential execution on the same workload.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/runtime-dark.png">
  <img alt="Runtime relative to sequential execution: 100 percent sequential, 80 percent fan-out, and 70 percent bulk synchronous" src="docs/runtime-light.png">
</picture>

The chart reports relative runtime because the benchmark record preserves the
measured reductions but not the original machine specification or raw timing
table.

## Execution models

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/execution-models-dark.png">
  <img alt="A workshop analogy comparing sequential processing, fan-in and fan-out with immediate saving, and bulk synchronous processing with a wait-for-all barrier" src="docs/execution-models-light.png">
</picture>

Think of a folder of photos as a stack of orders in a photo workshop. Every
photo must be opened, edited, and saved. All three models do the same work; the
difference is when those steps overlap and when a finished photo is allowed to
leave the workshop.

### Sequential

One editor handles the entire first photo before touching the second one. The
editor opens the photo, applies every requested effect, saves the result, and
then repeats the process for the next photo. This model is the easiest to
follow, but the waiting photos receive no work while the current one is being
processed.

### Fan-in/fan-out

This model works like a workshop with one intake line, several editors, and one
finishing desk. The intake line keeps supplying photos to whichever editor is
free. When an editor finishes a photo, the finishing desk saves it immediately
while the other editors continue working. Opening, editing, and saving can
therefore overlap, and a quick photo does not have to wait for the slowest photo
in the batch.

In the Go implementation, one goroutine loads tasks into a shared channel, a
worker pool applies the effects, and a result channel sends completed photos to
one writer.

### Bulk synchronous parallel

This model separates the job into two group phases. It first opens the entire
batch and places every photo on a workbench. Several editors then claim photos
and process them in parallel. Even if one editor finishes early, no result is
saved until every editor has completed the batch and reached the shared
finishing line. The program then saves all results together.

In the Go implementation, workers claim the next photo through one atomic
counter. A `WaitGroup` acts as the finishing line between the editing phase and
the saving phase.

| Question | Sequential | Fan-in/fan-out | Bulk synchronous |
|---|---|---|---|
| When are photos opened? | The program opens one photo only when it is ready to process it. | The intake goroutine opens photos while the worker pool consumes the shared line. | The program opens the complete batch before editing begins. |
| How are photos edited? | One photo receives all of its effects before the next photo starts. | Several workers edit different photos as they arrive. | Several workers claim different photos from the prepared batch. |
| When are results saved? | Each photo is saved before the next photo starts. | Each photo is saved as soon as its worker finishes. | All saving waits until every worker has finished editing. |
| What is the simplest mental model? | One person completes one order at a time. | A live workshop moves orders through intake, several editors, and a finishing desk. | A team prepares the whole batch, works together, and packages everything after the shift ends. |

Both parallel models add a second layer of shared work inside each photo. An
editor can divide a photo into horizontal strips so several helpers process its
rows at the same time. The sequential model processes the whole photo in one
pass.

## Image effects

The engine supports four effect codes:

| Code | Effect | Implementation |
|---|---|---|
| `G` | Grayscale | This averages the red, green, and blue channels. |
| `E` | Edge detection | This applies a 3×3 Laplacian kernel. |
| `S` | Sharpening | This applies a 3×3 centre-weighted sharpening kernel. |
| `B` | Blur | This applies a 3×3 box-blur kernel. |

`png/effects.go` evaluates the convolution kernels directly. Row-band workers
write disjoint output rows while still reading neighbouring pixels across band
boundaries, so a worker boundary does not become an artificial image edge.

## Run the included example

The repository includes one PNG fixture and four tasks in `data/effects.txt`.
Run commands from the `editor` directory because the program resolves `data/`
relative to that directory.

Sequential execution:

```bash
cd editor
go run . small
```

Fan-out pipeline with four workers:

```bash
go run . small pipeline 4
```

Bulk synchronous execution with four workers:

```bash
go run . small bsp 4
```

The generated files are written to `data/out/` with the data-directory prefix,
such as `small_test_img_edge.png`.

## Add a workload

Input images belong under one of these directories:

```text
data/in/small/
data/in/mixture/
data/in/big/
```

Each line in `data/effects.txt` is one JSON task:

```json
{"inPath":"test_img.png","outPath":"test_img_edge.png","effects":["E"]}
```

Multiple directories can share the same task list by joining their names with a
plus sign:

```bash
go run . small+big pipeline 8
```

The task list is decoded once and then reused for every selected directory.

## Correctness details

- The bulk synchronous worker claim uses `atomic.AddInt64`, so concurrent
  workers cannot read the same counter value and process one task twice.
- Convolution workers validate neighbours against the complete image bounds,
  not the current row band. This prevents seams at worker boundaries.
- The command-line parser checks its argument count before indexing `os.Args`.
- Invalid modes and unreadable task files fail explicitly instead of producing
  no output.

## Repository layout

| Path | Purpose |
|---|---|
| `editor/editor.go` | This file parses the command line and selects an execution model. |
| `implementations/sequential.go` | This file contains the single-threaded image loop. |
| `implementations/fanInFanOut.go` | This file contains the channel-based reader, worker pool, and writer. |
| `implementations/bulkSynchronousParallel.go` | This file contains the atomic task scheduler and barrier. |
| `png/effects.go` | This file contains grayscale processing and the 3×3 convolution kernels. |
| `png/png.go` | This file loads, stores, clamps, and saves 16-bit RGBA images. |
| `data/` | This directory contains the example input, task list, and generated outputs. |
