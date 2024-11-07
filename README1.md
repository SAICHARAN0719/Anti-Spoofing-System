# Silent Face Anti-Spoofing

This project is developed by MiniVision Technology for Silent Face Anti-Spoofing detection. The project includes an open-source model, training architecture, data preprocessing methods, testing scripts, and an APK for real-time testing.

## Updates
**2020-07-30:** Open-sourced Caffe models and shared the industrial-grade Silent Face Anti-Spoofing algorithm, including technical analysis and related files.

## Introduction
This project offers a comprehensive solution for face anti-spoofing detection. It aims to distinguish between real and fake faces. Fake faces may be presented using printed photos, electronic screens, silicone masks, or 3D face models. Current anti-spoofing solutions include two main types:

1. **Cooperative Detection**: Requires users to perform specific actions based on prompts to verify if the face is live.
2. **Non-Cooperative (Silent) Detection**: Performs liveness verification without requiring any user interaction, making it more versatile and user-friendly.

The detection method is based on Fourier Spectrogram-assisted supervision, where the model architecture consists of:
- **Primary Classification Branch**: Identifies whether the face is real or fake.
- **Fourier Spectrogram-assisted Supervision Branch**: Helps differentiate between true and fake faces based on frequency domain characteristics.

The model uses a custom pruning technique to reduce computational costs, improving performance without compromising accuracy.

| Model              | FLOPs  | Params |
| :----------------: | :----: | :----: |
| MobileFaceNet      | 0.224G | 0.991M |
| MiniFASNetV1       | 0.081G | 0.414M |
| MiniFASNetV2       | 0.081G | 0.435M |

## APK
### APK Source Code
The source code for deploying the Silent Face Anti-Spoofing algorithm on Android devices is open-sourced.

### Demo
A demonstration video or animation shows the system in action.

### Key Metrics
| Model (input 80x80) | FLOPs | Speed | FPR   | TPR   | Notes |
| :----------------:   | :---: | :---: | :---: | :---: | :---: |
| APK Model           | 84M   | 20ms  | 1e-5  | 97.8% | Open-source |
| High-precision Model| 162M  | 40ms  | 1e-5  | 99.7% | Not open-source |

### Testing Method
- **Displayed Information**: Speed (ms), confidence (0-1), and anti-spoofing results (real or fake face).
- **Threshold Adjustment**: Users can set a threshold for confidence. If the confidence exceeds the threshold, the face is considered real; otherwise, it is labeled as fake.

### Testing Notes
- All test images must be captured by a camera for accurate performance evaluation.
- The system’s robustness may vary depending on the camera model and usage environment.
- During testing, ensure the face is fully visible and its rotation is less than 30 degrees from the vertical axis for optimal results.

**Tested Mobile Phone Processors:**

| Model         | Kirin 990 5G | Kirin 990 | Snapdragon 845 | Kirin 810 | RK3288 |
| :-----------: | :----------: | :-------: | :------------: | :-------: | :----: |
| Speed (ms)    | 19           | 23        | 24             | 25        | 90     |

## Engineering Setup

### Install Dependencies
To install the required dependencies:
```
pip install -r requirements.txt
```

### Clone the Repository
To clone the repository:
```
git clone https://github.com/minivision-ai/Silent-Face-Anti-Spoofing  
cd Silent-Face-Anti-Spoofing
```

### Data Preprocessing
1. Split the training set into 3 categories, with images of the same category grouped into a folder.
2. The model uses a multi-scale fusion method, training on both original images and patches derived from the original images:
   - **Original Image**: Resize the image to a fixed size (width x height).
   - **Patch-based on Original Image**: Use a face detector to identify the face region, expand the face region by a specific scale, and resize the face region to a fixed size.

3. Fourier Spectrograms are generated for the images in the training set as auxiliary supervision.

**Directory structure for the dataset:**
```
├── datasets
    └── RGB_Images
        ├── org_1_80x60
            ├── 0
                ├── aaa.png
                ├── bbb.png
                └── ...
            ├── 1
                ├── ddd.png
                ├── eee.png
                └── ...
            └── 2
                ├── ggg.png
                ├── hhh.png
                └── ...
        ├── 1_80x80
        └── ...
```

### Training
To start training the model:
```
python train.py --device_ids 0 --patch_info your_patch
```

### Testing
To test the model:
- Use the fusion model for anti-spoofing detection located in `./resources/anti_spoof_models`.
- Use the face detection model located in `./resources/detection_model`.
- Provide test images from `./images/sample`.
```
python test.py --image_name your_image_name
```

## Related Resources  
- Industrial-grade Silent Face Anti-Spoofing Algorithm Technical Analysis and Live Video (internal resource).
- Mind map stored in the "files" directory.
- Open-source Caffe models stored in the "models" directory.

## References
- **Face Detector**: RetinaFace


