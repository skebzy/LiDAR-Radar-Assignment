
import numpy as np
import matplotlib.pyplot as plt

r = 30
fov_deg = 120

# need radians for the circle formulas
theta = np.radians(fov_deg)
half = theta / 2

# the circular measure part
arc_length = r * theta
sector_area = 0.5 * r**2 * theta
perimeter = 2 * r + arc_length
triangle_area = 0.5 * r**2 * np.sin(theta)
segment_area = sector_area - triangle_area

print("LIDAR SENSOR")
print("------------")
print(f"Field of view: {fov_deg} degrees = {theta:.4f} radians")
print(f"Arc length: {arc_length:.2f} m")
print(f"Sector area: {sector_area:.2f} m^2")
print(f"Sector perimeter: {perimeter:.2f} m")
print(f"Triangle area: {triangle_area:.2f} m^2")
print(f"Segment area: {segment_area:.2f} m^2")

# obstacle coordinates (name, x, y)
obstacles = [
    ("Pedestrian", 10, 5),
    ("Car ahead", 25, 0),
    ("Cone", 20, 20),
    ("Dog", 15, -10),
    ("Cyclist", 5, -15),
    ("Truck", 40, 5),
    ("Bus behind", -20, 0),
    ("Pole", 28, 12),
    ("Child", 3, 8)
]

results = []

print("\nOBSTACLE SCAN")
print("-------------")
print(f"{'Obstacle':<14} {'Distance':>10} {'Angle':>10}  Result")
print("-" * 58)

for name, x, y in obstacles:
    # distance from (0, 0)
    d = np.hypot(x, y)

    # getting the angle, atan2 handles negative coordinates too
    a = np.arctan2(y, x)
    angle_deg = np.degrees(a)

    # checking range and angle together
    seen = (d <= r) and (abs(a) <= half)

    if seen:
        result = "DETECTED"
    elif d > r:
        result = "Too far"
    else:
        result = "Outside angle"

    results.append((name, x, y, seen, d, angle_deg))
    print(f"{name:<14} {d:>10.2f} {angle_deg:>9.1f}°  {result}")


# plotting the radar
angles = np.linspace(-half, half, 200)
arc_x = r * np.cos(angles)
arc_y = r * np.sin(angles)

plt.figure(figsize=(9, 7))

# joining the arc back to the centre to fill the radar area
sector_x = np.concatenate(([0], arc_x, [0]))
sector_y = np.concatenate(([0], arc_y, [0]))
plt.fill(sector_x, sector_y, alpha=0.2, label="Sensor coverage")

plt.plot(arc_x, arc_y, label="30 m range")
plt.plot([0, arc_x[0]], [0, arc_y[0]], "--")
plt.plot([0, arc_x[-1]], [0, arc_y[-1]], "--")

for name, x, y, seen, d, angle_deg in results:
    if seen:
        plt.scatter(x, y, color="red")
    else:
        plt.scatter(x, y, color="grey")

    plt.annotate(name, (x, y), xytext=(5, 5),
                 textcoords="offset points", fontsize=8)

plt.scatter(0, 0, color="black", marker="^", s=130, label="Car / sensor")
plt.xlabel("x position (m)")
plt.ylabel("y position (m)")
plt.title("LiDAR Radar - 120 degree field of view")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("lidar_radar.png", dpi=300) # save the image
plt.show()


print("\nEXTENSION QUESTIONS")
print("-------------------")

# E1 - seeing what changes at 150 degrees
wide_half = np.radians(150) / 2
new_detections = []

for name, x, y in obstacles:
    d = np.hypot(x, y)
    a = np.arctan2(y, x)

    if d <= r and abs(a) <= wide_half:
        # skip the ones already detected earlier
        if not (d <= r and abs(a) <= half):
            new_detections.append(name)

print("E1. Newly detected with 150 degree FOV:", ", ".join(new_detections))


# E2 - distance needed to detect the pole
pole_distance = np.hypot(28, 12)
print(f"E2. Minimum range for the Pole: {np.ceil(pole_distance * 10) / 10:.1f} m")


# E3 - same arc formula but using the truck's distance
truck_distance = np.hypot(40, 5)
truck_arc = truck_distance * theta
print(f"E3. Arc length at the Truck's distance: {truck_arc:.2f} m")


# E4 - rearranging s = r * theta to get r
one_degree = np.radians(1)
resolution_distance = 0.5 / one_degree
print(f"E4. Distance for a 0.5 m object to subtend 1 degree: {resolution_distance:.2f} m")


# E5 - comparing area and cost
sensors = [
    ("A", 30, 120, 40000),
    ("B", 50, 60, 55000),
    ("C", 20, 180, 25000)
]

print("E5. Sensor comparison:")

for name, sensor_range, angle, cost in sensors:
    area = 0.5 * sensor_range**2 * np.radians(angle)
    value = area / (cost / 1000)
    print(f"    Sensor {name}: area = {area:.2f} m^2, area per Rs. 1000 = {value:.2f}")

areas = [0.5 * sr**2 * np.radians(angle) for name, sr, angle, cost in sensors]
values = [area / (cost / 1000) for area, (name, sr, angle, cost) in zip(areas, sensors)]

print("    Largest coverage:", sensors[int(np.argmax(areas))][0])
print("    Best value:", sensors[int(np.argmax(values))][0])


# E6 - trying the extra coordinates
x, y = 15, 25
custom_distance = np.hypot(x, y)
custom_angle = np.arctan2(y, x)
custom_seen = (custom_distance <= r) and (abs(custom_angle) <= half)

print(
    f"E6. Custom obstacle (15, 25): distance = {custom_distance:.2f} m, "
    f"angle = {np.degrees(custom_angle):.2f} degrees, "
    f"{'DETECTED' if custom_seen else 'NOT DETECTED'}"
)
