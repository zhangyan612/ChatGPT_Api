from ultralytics import YOLO


# yolo image test success

# 0: 480x640 2 cats, 1 couch, 2 remotes, 35.0ms
# Speed: 5.9ms preprocess, 35.0ms inference, 3.0ms postprocess per image at shape (1, 3, 480, 640)


# Load a model
model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model

imagePath = 'D:/Download/000000039769.jpg'
# Run batched inference on a list of images
# results = model([imagePath])  # return a list of Results objects

# # Process results list
# for result in results:
#     boxes = result.boxes  # Boxes object for bbox outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     print(boxes)
#     print(masks)



from PIL import Image
# from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Run inference on 'bus.jpg'
results = model(imagePath)  # results list

# Show the results
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    # im.save('results.jpg')  # save image
