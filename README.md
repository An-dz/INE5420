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
- `Num6`: Rotate clockwise
- `Num4`: Rotate anti-clockwise
- `Num7`: Reset rotation
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
