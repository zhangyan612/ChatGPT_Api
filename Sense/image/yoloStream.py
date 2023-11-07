# import cv2
# from ultralytics import YOLO

# # Load the YOLOv8 model
# model = YOLO('yolov8n.pt')

# # Open the video file
# video_path = "path/to/your/video/file.mp4"
# cap = cv2.VideoCapture(video_path)

# # Loop through the video frames
# while cap.isOpened():
#     # Read a frame from the video
#     success, frame = cap.read()

#     if success:
#         # Run YOLOv8 inference on the frame
#         results = model(frame)

#         # Visualize the results on the frame
#         annotated_frame = results[0].plot()

#         # Display the annotated frame
#         cv2.imshow("YOLOv8 Inference", annotated_frame)


# import cv2
# from ultralytics import YOLO

# def main():
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#     model = YOLO("yolov8n.pt")
#     while True:
#         ret, frame = cap.read()
#         result = model(frame, agnostic_nms=True)[0]
#         print(result)
#         if cv2.waitKey(30) == 27:
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()



# from ultralytics import YOLO
# import cv2

# # Load the pre-trained YOLOv8 model
# model = YOLO("yolov8n.pt")

# # Initialize the video capture object (0 for webcam, or path to video file)
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Perform object detection on the frame
#     results = model.predict(source=frame)

#     # Display the resulting frame with bounding boxes
#     cv2.imshow('YOLOv8 Object Detection', results)

#     # Break the loop on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the capture and destroy windows
# cap.release()
# cv2.destroyAllWindows()


from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
model = YOLO("yolov8n.pt")

layer_names = model.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in model.getUnconnectedOutLayers()]

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Perform object detection on the frame with YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    model.setInput(blob)
    outs = model.forward(output_layers)

    # Loop over each of the layer outputs and draw bounding boxes
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x, center_y, w, h = (detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])).astype('int')

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()



# import datetime
# from ultralytics import YOLO
# import cv2
# from helper import create_video_writer


# # define some constants
# CONFIDENCE_THRESHOLD = 0.8
# GREEN = (0, 255, 0)

# # initialize the video capture object
# video_cap = cv2.VideoCapture("2.mp4")
# # initialize the video writer object
# writer = create_video_writer(video_cap, "output.mp4")

# # load the pre-trained YOLOv8n model
# model = YOLO("yolov8n.pt")

# while True:
#     # start time to compute the fps
#     start = datetime.datetime.now()

#     ret, frame = video_cap.read()

#     # if there are no more frames to process, break out of the loop
#     if not ret:
#         break

#     # run the YOLO model on the frame
#     detections = model(frame)[0]
#     # loop over the detections
#     for data in detections.boxes.data.tolist():
#         # extract the confidence (i.e., probability) associated with the detection
#         confidence = data[4]

#         # filter out weak detections by ensuring the 
#         # confidence is greater than the minimum confidence
#         if float(confidence) < CONFIDENCE_THRESHOLD:
#             continue

#         # if the confidence is greater than the minimum confidence,
#         # draw the bounding box on the frame
#         xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
#         cv2.rectangle(frame, (xmin, ymin) , (xmax, ymax), GREEN, 2)
#     # end time to compute the fps
#     end = datetime.datetime.now()
#     # show the time it took to process 1 frame
#     total = (end - start).total_seconds()
#     print(f"Time to process 1 frame: {total * 1000:.0f} milliseconds")

#     # calculate the frame per second and draw it on the frame
#     fps = f"FPS: {1 / total:.2f}"
#     cv2.putText(frame, fps, (50, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)

#     # show the frame to our screen
#     cv2.imshow("Frame", frame)
#     writer.write(frame)
#     if cv2.waitKey(1) == ord("q"):
#         break

# video_cap.release()
# writer.release()
# cv2.destroyAllWindows()
