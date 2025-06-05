import time
import serial
import matplotlib.pyplot as plt
import re
import math

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

if ser.isOpen():
    print('Serial port is open and ready.')
else:
    print('Failed to open serial port.')

accuracy_values = []
time_stamps = []
x_coords = []
y_coords = []

pattern_est = r"est\[(.*?)\]"
pattern_coords = r"\[([^\]]+)\]"

# Plotting setup
plt.ion()  # Interactive mode for real-time updating
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Set titles and labels for the plots
ax1.set_title("Accuracy Over Time")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Accuracy")

ax2.set_title("2D Location (X, Y)")
ax2.set_xlabel("X Coordinate")
ax2.set_ylabel("Y Coordinate")

print('Reading data... Insert "exit" to leave.')

# Define accuracy threshold
accuracy_threshold = 75  # Adjust as needed
# Define movement threshold for the location (e.g., 0.1 units)
movement_threshold = 0.1

# Variable to store the previous location
previous_location = None  # Initialize as None for the first update

# Read data and extract values
start_time = time.time()

try:
    while True:
        try:
            # Read a line of data from the serial port
            data = ser.readline().decode('utf-8').strip()

            if data:
                print(data)  # Optional: print the data line for debugging

                # Search for the pattern for 'est' (estimated location) and coordinates
                match_est = re.search(pattern_est, data)
                match_coords = re.findall(pattern_coords, data)

                if match_est:
                    # Extract estimated location (x, y, z, quality_factor)
                    est_values = match_est.group(1).split(',')

                    try:
                        x_tag = float(est_values[0])
                        y_tag = float(est_values[1])
                        z_tag = float(est_values[2])
                        quality_factor = int(est_values[3])

                        # Only process data if the quality factor is above the threshold
                        if quality_factor >= accuracy_threshold:
                            # Add data to accuracy plot lists
                            elapsed_time = time.time() - start_time
                            accuracy_values.append(quality_factor)  # Use the quality factor as accuracy
                            time_stamps.append(elapsed_time)

                            # Update the accuracy plot
                            ax1.cla()  # Clear the current plot
                            ax1.plot(time_stamps, accuracy_values, label="Accuracy", color='b')
                            ax1.set_title("Accuracy Over Time")
                            ax1.set_xlabel("Time (s)")
                            ax1.set_ylabel("Accuracy")
                            ax1.legend()
                            ax1.grid(True)

                            # Only add the new location if it exceeds the movement threshold
                            if previous_location is None:  # First data point, add directly
                                x_coords.append(x_tag)
                                y_coords.append(y_tag)
                                previous_location = (x_tag, y_tag)  # Update previous location
                            else:
                                distance = math.sqrt((x_tag - previous_location[0]) ** 2 + (y_tag - previous_location[1]) ** 2)
                                if distance >= movement_threshold:
                                    # Add data to 2D location plot lists
                                    x_coords.append(x_tag)
                                    y_coords.append(y_tag)
                                    previous_location = (x_tag, y_tag)  # Update previous location

                            # Update the 2D location plot
                            ax2.cla()  # Clear the current plot
                            ax2.plot(x_coords, y_coords, label="Location", color='r')

                            # Plot the last segment in blue (if there are at least 2 points)
                            if len(x_coords) > 1:
                                ax2.plot([x_coords[-2], x_coords[-1]], [y_coords[-2], y_coords[-1]], color='b', linewidth=2)

                            ax2.set_title("2D Location (X, Y)")
                            ax2.set_xlabel("X Coordinate")
                            ax2.set_ylabel("Y Coordinate")
                            ax2.legend()
                            ax2.grid(True)

                    except (ValueError, IndexError) as e:
                        print(f"Data parsing error: {e}")

                # Draw both plots
                plt.draw()
                plt.pause(0.1)

            # Allow exit via keyboard input
            if 'exit' in data.lower():
                print("Exiting application...")
                break

        except Exception as e:
            print(f"Error during data processing: {e}")

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    ser.close()
    print("Serial port closed.")
