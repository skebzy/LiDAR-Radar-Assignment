# LiDAR Radar Assignment

## About the project

This project is a simple simulation of a car's front radar using Python.

The sensor is placed at `(0, 0)` and faces the positive x direction. It has a range of 30 metres and a viewing angle of 120 degrees.

The program checks the obstacles one by one and finds their distance and angle from the car. Based on these values, it decides whether the sensor can detect them. It also draws a graph showing the radar area and all the obstacles.

## Requirements

- Python 3
- NumPy
- Matplotlib

I'm using a virtual environment so the packages don't get installed into Arch's system Python.

Open the terminal in the project folder and run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install numpy matplotlib
```

You only have to create the environment once. Next time, just activate it:

```bash
source .venv/bin/activate
```

## Running it

Run the file using:

```bash
python radar_submission.py
```

The calculations and obstacle results will be printed in the terminal. It will also open a graph showing the radar coverage.

In the graph:
- The black triangle in the centre is the car.
- The shaded area is what the sensor can see.
- Red points are detected obstacles.
- Grey points are obstacles that were not detected.

## Calculations used

First, the field of view is converted from degrees to radians because the circular measure formulas use radians.

```python
theta = np.radians(fov_deg)
```

These are the formulas used in the program:

| Calculation | Formula |
|---|---|
| Arc length | `s = r * theta` |
| Sector area | `A = 0.5 * r**2 * theta` |
| Sector perimeter | `P = 2*r + r*theta` |
| Triangle area | `0.5 * r**2 * sin(theta)` |
| Segment area | Sector area - Triangle area |
| Distance | `sqrt(x**2 + y**2)` |

Here, `r` is the sensor range and `theta` is the angle in radians.

For finding the angle of an obstacle, I used:

```python
a = np.arctan2(y, x)
```

This is useful because it gives the correct angle even when the obstacle has negative x or y coordinates.

The sensor checks two things before detecting an obstacle:

```python
d <= r and abs(a) <= half
```

The first checks whether the obstacle is within 30 metres. The second checks whether its angle is between -60 and +60 degrees.

Both conditions have to be true.

## Obstacle results

These are the results for the nine obstacles given in the assignment:

| Obstacle | Distance | Angle | Result |
|---|---:|---:|---|
| Pedestrian | 11.18 m | 26.6° | Detected |
| Car ahead | 25.00 m | 0.0° | Detected |
| Cone | 28.28 m | 45.0° | Detected |
| Dog | 18.03 m | -33.7° | Detected |
| Cyclist | 15.81 m | -71.6° | Outside angle |
| Truck | 40.31 m | 7.1° | Too far |
| Bus behind | 20.00 m | 180.0° | Outside angle |
| Pole | 30.46 m | 23.2° | Too far |
| Child | 8.54 m | 69.4° | Outside angle |

One thing to notice is that being close to the car doesn't always mean an obstacle will be detected. For example, the Cyclist is within 30 metres but is outside the viewing angle.

## Extension questions

### E1. What happens when the FOV is changed to 150 degrees?

The half-angle becomes 75 degrees instead of 60 degrees.

The Cyclist and Child become detectable because they are now inside the viewing angle and within range. The Truck and Pole are still too far away, and the Bus is behind the car.

### E2. Minimum range needed for the Pole

The Pole is at `(28, 12)`.

Using the distance formula, its distance is approximately 30.46 metres. Rounding up to the next 0.1 metre gives **30.5 metres**.

### E3. Arc length at the Truck's distance

The Truck is approximately 40.31 metres away.

Using the same arc length formula with a 120 degree angle:

`s = r * theta`

The answer is **84.43 metres**.

### E4. Distance at which a 0.5 m object subtends 1 degree

Using the arc length formula:

`s = r * theta`

Rearranging it:

`r = s / theta`

After converting 1 degree into radians and substituting 0.5 metres, the answer is **28.65 metres**.

This means the object's angular size becomes smaller as it gets farther away, making it harder for a sensor to distinguish.

### E5. Comparing the three sensors

The sector area formula is used to calculate how much area each sensor covers. Then the area is compared with its cost.

| Sensor | Range | FOV | Coverage area | Cost | Area per Rs. 1,000 |
|---|---:|---:|---:|---:|---:|
| A | 30 m | 120° | 942.48 m² | Rs. 40,000 | 23.56 |
| B | 50 m | 60° | 1,309.00 m² | Rs. 55,000 | 23.80 |
| C | 20 m | 180° | 628.32 m² | Rs. 25,000 | 25.13 |

Sensor B covers the largest area, while Sensor C gives the best coverage for the money spent.

### E6. Testing an obstacle at (15, 25)

For the extra obstacle:

- Distance = 29.15 metres
- Angle = 59.04 degrees

Both values are within the sensor limits, so the obstacle is **DETECTED**.

## Python functions used

A few functions used in the program:

- `np.radians()` converts degrees to radians.
- `np.degrees()` converts radians back to degrees.
- `np.hypot(x, y)` calculates distance from the origin.
- `np.arctan2(y, x)` finds the angle of an obstacle.
- `np.sin()` and `np.cos()` are used for the circular calculations and radar drawing.
- `np.linspace()` creates equally spaced points to draw the curved edge.
- `plt.scatter()` places the obstacles on the graph.
- `plt.fill()` fills the radar coverage area.

The main logic is quite simple: the obstacle needs to be within 30 metres and inside the 120 degree viewing angle. If either condition is not satisfied, the sensor won't detect it.
