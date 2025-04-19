# DeepFace Anti-Spoofing

The **DeepFace Anti-Spoofing API** enables users to analyze images for face recognition and anti-spoofing detection. It provides predictions for age, gender, and whether the face is real or fake, making it ideal for secure authentication and identity verification applications. This API is designed for seamless integration into your Python applications, ensuring reliable and efficient image analysis.

## Features

- **Face Analysis**: Predict age and gender from uploaded images.
- **Anti-Spoofing Detection**: Determine whether a face is real or fake with high accuracy.
- **Simple Integration**: Integrate the API into your Python application effortlessly.

## Installation

To use the DeepFace Anti-Spoofing  in your Python application, install the required package:

```bash
pip install deepface-anti-spoofing
```

## Usage Example

Here is a simple example demonstrating how to upload an image for analysis using the DeepFace Anti-Spoofing :

```python
from deepface_anti_spoofing import DeepFaceAntiSpoofing

file_path = "C:/Users/Admin/Downloads/face_image.jpg"

deepface = DeepFaceAntiSpoofing()

response = deepface.upload_image(file_path)

print(response)
```

```json
{
  "id": 1,
  "age": 30,
  "gender": {
    "Male": 0.85,
    "Female": 0.15
  },
  "dominant_gender": "Male",
  "spoof": {
    "Fake": 0.02,
    "Real": 0.98
  },
  "dominant_spoof": "Real",
  "timestamp": "2025-04-18 12:34:56"
}
```

## Key Points

- Ensure the uploaded image contains a clear face for accurate analysis.
- Follow the documentation for detailed endpoint specifications and advanced features.

## Support

If you encounter any issues or have questions, please contact at [ipsoftechsolutions@gmail.com](mailto:ipsoftechsolutions@gmail.com).

---

Thank you for choosing DeepFace Anti-Spoofing for your face recognition and anti-spoofing needs!