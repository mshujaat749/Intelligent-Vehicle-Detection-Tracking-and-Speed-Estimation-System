import streamlit as st
import cv2
from ultralytics import YOLO, solutions
import tempfile
import os


# Custom CSS for background image and text color
def add_bg_from_url(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            color: white;  /* Set text color to white */
        }}
        .stButton>button {{
            color: black !important;  /* Set button text color to black */
            font-size: 2.5em !important;  /* Increase button text size */
        }}

        .stTextInput>div>div>input {{
            font-size: 2.5em !important;  /* Increase input text size */
        }}
        .stMarkdown h1 {{
            font-size: 4em !important;  /* Increase title size */
        }}
        .stMarkdown p {{
            font-size: 1.5em !important;  /* Increase paragraph text size */
        }}
        .stDownloadButton>button {{
            color: red !important; /* Set download button label text color to red */
            font-size: 2.5em !important; /* Increase download button text size */
        }}
        .stAlert {{
            color: white !important;  /* Set success message text color to white */
            font-size: 2.5em !important;  /* Increase success message text size */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Streamlit app
st.title("Vehicle Tracker & Speed Estimator")
st.markdown("""<style>h1{color: white;}</style>""", unsafe_allow_html=True)

# Custom background image
add_bg_from_url('https://img.freepik.com/premium-photo/red-car-red-room-with-red-background_916191-10521.jpg')

# Video upload
uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi"], label_visibility='collapsed')

if uploaded_video is not None:
    # Save uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_video_file:
        tmp_video_file.write(uploaded_video.read())
        tmp_video_path = tmp_video_file.name


    # Function to let the user draw a line on the video frame
    def draw_line_on_frame(video_path):
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            st.error("Failed to read video")
            return None

        line_pts = []

        def draw_line(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                line_pts.append((x, y))
                if len(line_pts) == 2:
                    cv2.line(frame, line_pts[0], line_pts[1], (0, 255, 0), 2)
                    cv2.imshow("Draw Line", frame)

        cv2.imshow("Draw Line", frame)
        cv2.setMouseCallback("Draw Line", draw_line)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if len(line_pts) == 2:
            return line_pts
        else:
            st.error("Please draw a complete line")
            return None


    # Function to process the video
    def process_video(video_path, line_pts):
        model = YOLO("yolov8n.pt")
        names = model.model.names

        cap = cv2.VideoCapture(video_path)
        assert cap.isOpened(), "Error reading video file"
        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

        # Video writer
        output_path = os.path.join(tempfile.gettempdir(), "speed_estimation.avi")
        video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        # Init speed-estimation obj
        speed_obj = solutions.SpeedEstimator(
            reg_pts=line_pts,
            names=names,
            view_img=False,
        )

        while cap.isOpened():
            success, im0 = cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            tracks = model.track(im0, persist=True, show=False)

            im0 = speed_obj.estimate_speed(im0, tracks)
            video_writer.write(im0)

        cap.release()
        video_writer.release()
        cv2.destroyAllWindows()

        return output_path


    # Let the user draw the line
    st.write("Draw a line for speed estimation")
    if st.button("Draw Line", key="draw_line_button"):
        line_pts = draw_line_on_frame(tmp_video_path)
        if line_pts is not None:
            st.write(f"Line points: {line_pts}")

            # Process the uploaded video
            with st.spinner("Processing video..."):
                processed_video_path = process_video(tmp_video_path, line_pts)

            st.markdown('<div class="stAlert"><strong>Video processed successfully!</strong></div>',
                        unsafe_allow_html=True)  # Success message in white color and larger font

            # Provide download link for the processed video
            with open(processed_video_path, "rb") as processed_video_file:
                processed_video_bytes = processed_video_file.read()
                st.download_button(label="Download Processed Video", data=processed_video_bytes,
                                   file_name="processed_video.avi", mime="video/avi")

else:
    st.markdown("Please upload a video file to start.", unsafe_allow_html=True)  # Info message in white color
