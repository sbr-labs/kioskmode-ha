# Kiosk Mode — Home Assistant integration

Turn an Android tablet running the **Kiosk Mode** app into a first-class Home Assistant
device: a live camera, motion/face/noise binary sensors, battery, FPS, screen control
and more — all over local polling, no cloud and no MQTT.

This is the companion integration for the Kiosk Mode Android app. It talks to the app's
on-device web server (`http://<tablet-ip>:2323`) and exposes everything as entities.

## What you get

| Entity | Type |
|---|---|
| `camera.kioskcam` | Live H.264 stream (RTSP) + JPEG snapshots |
| `binary_sensor` | Streaming, Motion, Face, Noise, Charging, Screen On, Dark Mode |
| `sensor` | Battery, Battery Temperature, Camera FPS, Noise Level, Version, Wi-Fi Signal, Wi-Fi Network, Wi-Fi Band, Wi-Fi Link Speed, Memory Free, Storage Free, Uptime, Orientation, Power Source |
| `switch` | Screen on/off |

## Install (HACS)

1. HACS → ⋮ → **Custom repositories** → add this repo, category **Integration**.
2. Install **Kiosk Mode**, restart Home Assistant.
3. **Settings → Devices & Services → Add Integration → Kiosk Mode**, enter the tablet's IP.

## Manual install

Copy `custom_components/kioskcam/` into your HA `config/custom_components/` folder and
restart, then add the integration from the UI.

## Requirements

- The [Kiosk Mode Android app](https://github.com/sbr-labs/kioskmode-android) installed on the tablet.
- Tablet and HA on the same network.

## License

Free for personal and other **noncommercial** use under the
[PolyForm Noncommercial License 1.0.0](LICENSE). **Commercial use requires a paid
license** — contact software@str-performance.com for commercial / royalty terms.
