import cv2
import os

def extract_frames_from_video(video_path, output_dir, timestamps=None, margin_start=0, margin_end=0):
    """
    Extracts frames from a video.
    If timestamps are provided (list of seconds), extracts frames at those timestamps.
    If timestamps are provided (list of seconds), extracts frames at those timestamps.
    Otherwise, extracts first, middle, and last frames and returns their timestamps (in seconds).
    margin_start: number of frames to skip from the beginning.
    margin_end: number of frames to skip from the end.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return None

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps if fps > 0 else 0
    
    print(f"Processing {video_path}: {frame_count} frames, {fps:.2f} fps, {duration:.2f}s")

    if frame_count == 0 or fps == 0:
        print(f"Video {video_path} has 0 frames or 0 fps.")
        return None

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    extracted_timestamps = []

    if timestamps is None:
        # Strategy for 'edited' videos: extract first, mid, last
        # Apply margins
        start_idx = margin_start
        end_idx = max(0, frame_count - 1 - margin_end)
        
        if start_idx > end_idx:
            print(f"Warning: margins too large for video {video_path} (frames={frame_count}), using default 0, mid, last")
            start_idx = 0
            end_idx = frame_count - 1
            
        mid_idx = (start_idx + end_idx) // 2
        
        indices = {
            "0": start_idx,
            "mid": mid_idx,
            "last": end_idx
        }
        
        for name, idx in indices.items():
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            # Calculate timestamp manually: frame_index / fps
            timestamp = idx / fps
            ret, frame = cap.read()
            if ret:
                output_filename = os.path.join(output_dir, f"{base_name}_frame_{name}.jpg")
                cv2.imwrite(output_filename, frame)
                print(f"Saved {output_filename} at {timestamp:.3f}s (Frame {idx})")
                extracted_timestamps.append(timestamp)
            else:
                print(f"Error reading frame {idx} from {video_path}")
                extracted_timestamps.append(None)
    else:
        # Strategy for 'origin' videos: extract at specific timestamps
        names = ["0", "mid", "last"]
        
        for i, timestamp in enumerate(timestamps):
            if timestamp is None:
                continue
            
            # Calculate target frame index: timestamp * fps
            target_idx = int(round(timestamp * fps))
            target_idx = max(0, min(target_idx, frame_count - 1))
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_idx)
            ret, frame = cap.read()
            if ret:
                output_filename = os.path.join(output_dir, f"{base_name}_frame_{names[i]}.jpg")
                cv2.imwrite(output_filename, frame)
                print(f"Saved {output_filename} at {timestamp:.3f}s (Frame {target_idx})")
            else:
                print(f"Error reading frame at {timestamp}s (Frame {target_idx}) from {video_path}")

    cap.release()
    return extracted_timestamps

def process_folders(root_dir):
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == 'edited':
            origin_dir = os.path.join(os.path.dirname(dirpath), 'origin')
            
            if not os.path.exists(origin_dir):
                print(f"Warning: 'origin' directory not found for {dirpath}, skipping...")
                continue
                
            print(f"Found pair: {dirpath} <-> {origin_dir}")
            
            for file in filenames:
                if os.path.splitext(file)[1].lower() in video_extensions:
                    edited_video_path = os.path.join(dirpath, file)
                    origin_video_path = os.path.join(origin_dir, file)
                    
                    if not os.path.exists(origin_video_path):
                        print(f"Warning: Corresponding origin video not found: {origin_video_path}")
                        continue
                        
                    # 1. Process edited video and get timestamps
                    print(f"\nDistilling from EDITED: {edited_video_path}")
                    
                    # Check if we are in 'instance insertion' folder
                    margin_start = 0
                    margin_end = 0
                    if "instance insertion" in dirpath:
                         margin_start = 10
                         margin_end = 10
                         print(f"Applying margins: start={margin_start}, end={margin_end} for 'instance insertion'")
                    
                    timestamps = extract_frames_from_video(edited_video_path, dirpath, timestamps=None, margin_start=margin_start, margin_end=margin_end)
                    
                    # 2. Process origin video with those timestamps
                    if timestamps:
                        print(f"Extracting from ORIGIN: {origin_video_path}")
                        extract_frames_from_video(origin_video_path, origin_dir, timestamps=timestamps)

def main():
    process_folders(".")

if __name__ == "__main__":
    main()
