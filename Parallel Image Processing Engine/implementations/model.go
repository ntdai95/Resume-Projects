package implementations

import (
	"encoding/json"
	"errors"
	"io"
)

type EffectData struct {
	InPath  string   `json:"inPath"`
	OutPath string   `json:"outPath"`
	Effects []string `json:"effects"`
}

func LoadEffectData(decoder *json.Decoder) ([]EffectData, error) {
	effectDataList := []EffectData{}
	for {
		effectData := EffectData{}
		err := decoder.Decode(&effectData)
		if errors.Is(err, io.EOF) {
			return effectDataList, nil
		} else if err != nil {
			return nil, err
		}

		effectDataList = append(effectDataList, effectData)
	}
}
