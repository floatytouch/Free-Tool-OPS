#!/usr/bin/env python3
"""Lay out the OBS "6 · Dual Screen" scene to match themes/dual-pro.html (run with obsws-python installed)."""
import json
import logging
import os

import obsws_python as obs

logging.disable(logging.CRITICAL)  # obsws-python logs the websocket password at INFO
CONFIG = os.path.expanduser("~/Library/Application Support/obs-studio/plugin_config/obs-websocket/config.json")
SCENE = "6 · Dual Screen"
OVERLAY_URL = "http://127.0.0.1:18793/themes/dual-pro.html"


def main() -> None:
    cfg = json.load(open(CONFIG))
    client = obs.ReqClient(host="127.0.0.1", port=cfg["server_port"],
                           password=cfg.get("server_password") or None, timeout=5).base_client
    items = {i["sourceName"]: i["sceneItemId"] for i in
             client.req("GetSceneItemList", {"sceneName": SCENE})["responseData"]["sceneItems"]}

    def place(source, x, y, w, h, bounds, crop=(0, 0, 0, 0)):
        left, right, top, bottom = crop
        client.req("SetSceneItemTransform", {"sceneName": SCENE, "sceneItemId": items[source], "sceneItemTransform": {
            "positionX": x, "positionY": y, "alignment": 5, "boundsType": bounds, "boundsAlignment": 0,
            "boundsWidth": w, "boundsHeight": h, "cropToBounds": True,
            "cropLeft": left, "cropRight": right, "cropTop": top, "cropBottom": bottom}})

    for name in ("Display · Left", "Display · Right"):
        # Without this the display showing OBS captures its own preview and recurses.
        client.req("SetInputSettings", {"inputName": name, "inputSettings": {"hide_obs": True}, "overlay": True})
    place("Display · Left", 32, 32, 850, 552, "OBS_BOUNDS_STRETCH")
    place("Display · Right", 906, 32, 982, 552, "OBS_BOUNDS_STRETCH")
    place("Camera", 32, 608, 782, 200, "OBS_BOUNDS_SCALE_OUTER", crop=(470, 340, 400, 200))  # eyes-only strip
    place("Overlay · dual", 0, 0, 1920, 1080, "OBS_BOUNDS_NONE")
    client.req("SetSceneItemLocked", {"sceneName": SCENE, "sceneItemId": items["Overlay · dual"], "sceneItemLocked": True})
    client.req("SetSceneItemEnabled", {"sceneName": SCENE, "sceneItemId": items["Nền"], "sceneItemEnabled": False})
    client.req("SetInputSettings", {"inputName": "Overlay · dual", "overlay": True, "inputSettings": {
        "url": OVERLAY_URL, "width": 1920, "height": 1080, "reroute_audio": True, "fps": 30}})
    client.req("SetInputAudioMonitorType", {"inputName": "Overlay · dual",
                                            "monitorType": "OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT"})


if __name__ == "__main__":
    main()
