## About MeshCore

MeshCore is a lightweight, portable C++ library that enables multi-hop packet routing for embedded projects using LoRa and other packet radios. It is designed for developers who want to create resilient, decentralized communication networks that work without the internet.

> [!IMPORTANT]
> This repo embeds a few customizations, which are not bullet-proof.

## Wi-Fi support for ESP32 repeaters

I have the use case of maintaining a repeater remotely, where I cannot use LoRa.
This customization make a ESP32 repeater available on Wi-Fi, without authentication.

### Build
Use VSCode with platform.io extension and build `Tbeam_SX1276_wifi_repeater` project.

Provide Wi-Fi SSID and password at compilation time. Default TCP port is `5000`.

```txt
[env:Tbeam_SX1276_wifi_repeater]
extends = LilyGo_TBeam_SX1276
build_flags =
  -I src/helpers/esp32
  ${LilyGo_TBeam_SX1276.build_flags}
  -D MAX_NEIGHBOURS=50
  -D PERSISTANT_GPS=1
  -D WIFI_SSID='"SSID"'
  -D TCP_PORT='"5000"'
  -D WIFI_PWD='"password"'
build_src_filter = ${LilyGo_TBeam_SX1276.build_src_filter}
  +<helpers/esp32/*.cpp>
  +<../examples/simple_repeater>
lib_deps =
  ${LilyGo_TBeam_SX1276.lib_deps}
  ${esp32_ota.lib_deps}
```

Once the TBeam is connected on your local area network, TCP connections can be made to launch [commands](https://docs.meshcore.io/cli_commands/).

```bash
$ python3 cmd.py --ip 192.168.1.19 --port 5000 --payload "stats-packets"
Sent frame: length=13, payload='stats-packets'
Received frame: type=62, length=89, payload='{"recv":0,"sent":1,"flood_tx":0,"direct_tx":1,"flood_rx":0,"direct_rx":0,"recv_errors":0}'
```

