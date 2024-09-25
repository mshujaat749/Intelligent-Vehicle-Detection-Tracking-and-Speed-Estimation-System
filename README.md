# Vehicle Tracker & Speed Estimator

This project is a **Vehicle Tracking and Speed Estimation** application that uses **YOLOv8** for object detection and OpenCV for video processing. The app is built with **Streamlit**, providing an intuitive and user-friendly interface for vehicle speed estimation.

## 🖼️ Features
- **Vehicle Detection:** Uses YOLOv8 to detect vehicles in video footage.
- **Speed Estimation:** Allows users to draw a reference line and estimate vehicle speed based on it.
- **Custom Background:** An attractive UI with customizable background and styles.
- **Video Upload and Processing:** Upload videos in `mp4` or `avi` format and process them directly in the app.
- **Download Processed Video:** Download the processed video with the estimated speeds and tracking data.


## 🛠️ Technologies Used
- **Python**: The main programming language
- **Streamlit**: For building the web interface
- **OpenCV**: For video frame processing and drawing
- **YOLOv8**: For object detection
- **Ultralytics**: Used for handling YOLO model functionalities

## 🔧 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vehicle-tracker-speed-estimator.git
   cd vehicle-tracker-speed-estimator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Required Packages
Here are some of the main packages used:
- `streamlit`
- `opencv-python`
- `ultralytics`
- `numpy`

## ▶️ How to Run
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and go to `http://localhost:8501`.

## 📂 Project Structure
```
vehicle-tracker-speed-estimator/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python packages required
└── README.md              # Project documentation
```

## ✨ How to Use
1. **Upload a Video**: Upload your video file (supported formats: mp4, avi).
2. **Draw a Line**: Click the "Draw Line" button to draw a reference line for speed estimation.
3. **Process Video**: The app processes the video using YOLOv8 and displays results.
4. **Download**: Once processing is complete, download the processed video with estimated speeds.

## ⚠️ Notes
- Make sure to have a reliable internet connection if running the YOLOv8 model for the first time as it might need to download weights.
- Use videos with clear visibility for accurate speed estimation.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

```

