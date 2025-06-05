# Serial Data Plotter for Lidar Sensor

Dieses Python-Skript liest Positionsdaten (inkl. Genauigkeit) über eine serielle Verbindung und gibt sie mit `matplotlib` aus.

## Voraussetzungen

```bash
pip install pyserial matplotlib
````

---

## Serielle Verbindung herstellen

```python
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=1
)
```

> Öffnet die serielle Verbindung.

---

## Eingehende Daten analysieren

```python
pattern_est = r"est\[(.*?)\]"
```

> Sucht nach Mustern wie `est[x, y, z, quality]` in der seriellen Datenzeile.

```python
est_values = match_est.group(1).split(',')
x_tag = float(est_values[0])
y_tag = float(est_values[1])
z_tag = float(est_values[2])
quality_factor = int(est_values[3])
```

> Extrahiert und konvertiert Positions- und Qualitätsdaten.

---

## Genauigkeitsfilter

```python
accuracy_threshold = 75
if quality_factor >= accuracy_threshold:
    ...
```

> Nur Werte mit ausreichender Qualität (standardmäßig ≥ 75) werden geplottet.

---

## Bewegungserkennung

```python
movement_threshold = 0.1
distance = math.sqrt((x - prev_x)**2 + (y - prev_y)**2)
if distance >= movement_threshold:
    ...
```

> Neue Positionen werden nur geplottet, wenn sich das Objekt ausreichend bewegt hat.

---

## Live-Plotting mit `matplotlib`

```python
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1)
```

> Aktiviert interaktives Plotten. Zwei Plots:
>
> * `ax1`: Genauigkeit über Zeit
> * `ax2`: 2D-Position

```python
ax1.plot(time_stamps, accuracy_values)
ax2.plot(x_coords, y_coords)
```

> Regelmäßige Aktualisierung der Plots in Echtzeit.

---

## Beenden

```python
if 'exit' in data.lower():
    break
```

> Beendet die Schleife, wenn das Wort "exit" in den seriellen Daten erkannt wird.
