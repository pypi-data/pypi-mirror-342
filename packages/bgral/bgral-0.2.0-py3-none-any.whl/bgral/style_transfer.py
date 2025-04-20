# bgral/video_style_transfer.py

import os
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import subprocess


def load_img(path_to_img, max_dim=512):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    scale = max_dim / max(shape)
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if tensor.ndim > 3:
        tensor = tensor[0]
    return Image.fromarray(tensor)


def extract_frames(video_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    idx = 0
    frame_paths = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_folder, f"frame_{idx:05d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
        idx += 1

    cap.release()
    return frame_paths


def stylize_image_with_model(content_path, style_image, model):
    content_image = load_img(content_path)
    stylized = model(tf.constant(content_image), tf.constant(style_image))[0]
    return tensor_to_image(stylized)


def stylize_video_frames(frame_paths, style_image_path, model, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    style_image = load_img(style_image_path)

    for i, path in enumerate(frame_paths):
        print(f"Stylizing frame {i+1}/{len(frame_paths)}...")
        styled_img = stylize_image_with_model(path, style_image, model)
        filename = os.path.basename(path)
        styled_img.save(os.path.join(output_folder, filename))


def frames_to_video(frame_folder, output_video_path, fps=30):
    frame_files = sorted([f for f in os.listdir(frame_folder) if f.endswith('.jpg')])
    if not frame_files:
        raise Exception("No frames found to compile into video.")

    first_frame = cv2.imread(os.path.join(frame_folder, frame_files[0]))
    height, width, _ = first_frame.shape

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for file in frame_files:
        frame = cv2.imread(os.path.join(frame_folder, file))
        out.write(frame)

    out.release()


def add_audio_to_video(original_video, styled_video, output_path):
    command = [
        "ffmpeg", "-y",
        "-i", original_video,
        "-i", styled_video,
        "-c:v", "copy",
        "-map", "0:a:0",
        "-map", "1:v:0",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def style_transfer(
    input_video: str,
    style_image_path: str,
    working_dir: str = "working_dir",
    fps: float = 30.0
):
    frame_dir = os.path.join(working_dir, "frames")
    styled_dir = os.path.join(working_dir, "styled_frames")
    styled_video = os.path.join(working_dir, "stylized_video.mp4")
    final_video = os.path.join(working_dir, "final_with_audio.mp4")

    print("[1] Loading TF Hub style transfer model...")
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    print("[2] Extracting frames from video...")
    frame_paths = extract_frames(input_video, frame_dir)

    print("[3] Applying style transfer to each frame...")
    stylize_video_frames(frame_paths, style_image_path, hub_model, styled_dir)

    print("[4] Compiling stylized video...")
    frames_to_video(styled_dir, styled_video, fps=fps)

    print("[5] Adding original audio back...")
    add_audio_to_video(input_video, styled_video, final_video)

    print(f"[✅] Done! Final video saved at: {final_video}")
    return final_video
