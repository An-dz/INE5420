# Requirements
- Python 3.9 or greater
- PyQT 6
- numpy

## Poetry
This project uses poetry as a package manager, installing only production
dependencies can be done with `poetry install --no-root --without dev`

# Shortcuts
Available shortcuts:

- `Ctrl`+`Q`: Close the app
- `Shift`+`A`: Open the interface to create an object
- `Num+`/`Num-`: Zoom in/out
- `Ctrl`+`Num+`/`Num-`: Zoom in/out
- `Mouse Scroll`: Zoom in/out
- `Ctrl`+(`Num2`|`Num4`|`Num6`|`Num8`): Pan the window around
- `Shift`+`Middle Mouse Button`: Pan the window around
- `Ctrl`+`Middle Mouse Button`: Zoom the window
- `Del`: Deletes the currently selected object
- `N`/`G`: Open transform window on translate
- `R`: Open transform window on rotate
- `S`: Open transform window on scale
- `Num6`: Yaw camera left
- `Num4`: Yaw camera right
- `Num8`: Pitch camera down
- `Num2`: Pitch camera up
- `Shift+Num6`: Roll camera clockwise
- `Shift+Num4`: Roll camera anti-clockwise
- `Ctrl+Num6`: Move camera left
- `Ctrl+Num4`: Move camera right
- `Ctrl+Num8`: Move camera up
- `Ctrl+Num2`: Move camera down
- `Num1`: Front ortographic view (XZ plane)
- `Ctrl+Num1`: Back ortographic view (XZ plane)
- `Num3`: Right ortographic view (YZ plane)
- `Ctrl+Num3`: Left ortographic view (YZ plane)
- `Num7`: Top ortographic view (XY plane)
- `Ctrl+Num7`: Bottom ortographic view (XY plane)
- `Ctrl+O`: Import Wavefront (.obj)
- `Ctrl+S`: Export Wavefront (.obj)

# Example Objects
- `(54,62)`
- `(-30,-25),(-26,-79)`
- `(-10,-10),(-10,10),(10,10),(10,-10),(-10,-10)`

# Generating Python UI classes
Example usage:

```bash
pyuic6 ui/main.ui -o src/ui/generated/main.py
```
