
# Virtual Landmark 

**virtual-landmark** is a modular and extensible system for working with custom landmarks on top of [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html). It enables developers to define additional pose points through geometric relationships, access them like native MediaPipe landmarks, and extend pose rendering and analysis.


The complete documentation can be found on the [documentation page](https://cvpose.github.io/virtual_landmark_python/)

---

## Features

- 🧩 Create virtual landmarks with `@landmark` decorator
- 📐 Measure 2D and 3D joint angles
- 🎨 Extend pose drawings with new connections and styles
- 📚 Seamlessly integrate with MediaPipe’s landmark list
- 🧠 Named access to all landmarks via enum-like interface

---

## How It Works

The system works in three stages:

### 1. **Definition**
Virtual landmarks are declared using `@landmark("NAME", connection=[...])` decorators on methods that return a 3D point.

### 2. **Discovery**
Upon instantiating `VirtualLandmark`, all decorated methods are scanned, executed, and their results added to the landmark list.

### 3. **Access**
Virtual landmarks behave like native landmarks:
- Access index via `.NAME.value`
- Retrieve coordinates via landmark list
- Draw using standard MediaPipe rendering tools

---

## Getting Started

Install MediaPipe:

```bash
pip install mediapipe opencv-python virtual-landmark
```

Clone or copy this repo, then run the examples:

```bash
python examples/get_started.py
python examples/hello_world.py
python examples/video.py
python examples/web_cam.py
```

There are also a [Jupyter](https://jupyter.org) notebook that you can run through the follow command:

```bash
pip install jupyterlab matplotlib
jupyter lab examples
```

---