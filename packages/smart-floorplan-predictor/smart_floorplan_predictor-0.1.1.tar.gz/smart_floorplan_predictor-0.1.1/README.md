# Smart Floorplan Predictor

A Python package for making predictions using a pre-trained ONNX floorplan model.

## Installation

```bash
pip install smart-floorplan-predictor
```

## Usage

```python
from smart_floorplan_predictor import FloorplanPredictor

# Initialize the predictor
predictor = FloorplanPredictor()

# Make a prediction
# Replace input_data with your actual input data format
result = predictor.predict(input_data)
print(result)
```

## Features

- Automatic model downloading if not present locally
- Easy-to-use prediction interface
- ONNX runtime integration
- Built-in input preprocessing

## Requirements

- Python >= 3.7
- onnxruntime
- numpy
- requests

## License

MIT License

## Author

Oliver Brown