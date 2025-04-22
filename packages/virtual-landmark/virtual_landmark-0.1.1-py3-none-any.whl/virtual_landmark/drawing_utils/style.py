import mediapipe as mp
from mediapipe.python.solutions.drawing_styles import get_default_pose_landmarks_style

def get_extended_pose_landmarks_style(landmarks):
    """
    Returns a landmark drawing style dictionary with:
    - Default MediaPipe styles for real landmarks (0–32)
    - Custom color-coded styles for dynamically added landmarks:
        - Orange for left-side points
        - Green for right-side points
        - Gray for center/virtual points

    Args:
        landmarks (CustomLandmark): An instance of a CustomLandmark or DefaultCustomLandmark

    Returns:
        Dict[int, DrawingSpec]: Drawing styles for each landmark index
    """
    plm = mp.solutions.pose.PoseLandmark
    base_style = get_default_pose_landmarks_style()

    # Base reference styles (copied, not tupled)
    left_style = base_style[plm.LEFT_SHOULDER.value]
    right_style = base_style[plm.RIGHT_SHOULDER.value]
    center_style = base_style[plm.NOSE.value]

    # Only style custom landmarks (index >= 33)
    for idx in range(len(plm), len(landmarks)):
        point = landmarks[idx]
        x = point.x

        style = next(
            s
            for cond, s in [
                (x < 0.45, right_style),
                (x > 0.55, left_style),
                (True, center_style),
            ]
            if cond
        )

        base_style[idx] = style

    return base_style
