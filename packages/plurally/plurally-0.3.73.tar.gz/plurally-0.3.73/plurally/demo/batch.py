import json
import os
from pathlib import Path

import requests
from loguru import logger

from plurally.models.flow import Flow

is_dev = False
if is_dev:
    vet_urgentys_dev = "27f1017c-1cea-4d44-ba5e-814f8a30361a"
    v2tu_dev = "c82843f9-344a-4b83-a9d3-ad27fb5b1bf7"
    bearer = "972eadff-be14-49a0-8599-9bb10d6455bf"
    base_url = "apidev.tryplurally.com"
else:
    vet_urgentys_dev = "bf86e5ae-c3b6-4092-8290-2b7a24f4d7f5"
    v2tu_dev = "b80ea951-ad9e-4297-8109-43cc17d07db0"
    bearer = os.environ.get("ACCESS_TOKEN")
    base_url = "api.tryplurally.com"

url = f"https://{base_url}/api/v1/flows/{v2tu_dev}/form/submit"

headers = {"Authorization": f"Bearer {bearer}"}
root_dir = Path("/home/villqrd/veturgentys_cases/vet_urgentys_1")
for case_dir in root_dir.iterdir():
    if not case_dir.is_dir():
        logger.debug(f"Skipping {case_dir} as it is not a directory")
    logger.info(f"Processing {case_dir.name}")
    previous_run_id = None
    if not any(n in case_dir.name for n in ["natsu"]):
        # if not any(n in case_dir.name for n in ["manouch", "teddy", "chupa", "mickey", "natsu"]):
        continue

    for run_dir in sorted(case_dir.iterdir()):
        for i in range(1):
            # Adjust this path to point to the actual audio file you want to send
            audio_file_path = run_dir / "recording.m4a"
            meta = json.loads((run_dir / "meta.json").read_text())
            flow_json = json.loads((run_dir / "flow.json").read_text())

            if list(meta["form_data"].values())[0]["catégorie"] not in ("COMPTE RENDU STANDARD",):
                logger.debug(f"Skipping {case_dir} as it is not a directory")
                break

            flow = Flow.parse(flow_json)
            trigger = [node for node in flow.get_flatten_graph().nodes if node.is_trigger][0]

            # This mimics the structure of the JSON inside the form_data field
            form_data = meta["form_data"][trigger.node_id]
            form_data["PLURALLY_CASE_NAME"] = case_dir.name.partition("_")[-1].partition("_")[-1]
            files = {
                "form_data": (
                    None,
                    json.dumps(form_data),
                ),
                "files": (
                    ".compte_rendu.file_PLURALLY_KEY_filename_0.mp4",
                    open(audio_file_path, "rb"),
                ),
            }

            if previous_run_id:
                files["previous_run_id"] = (None, previous_run_id)

            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            # previous_run_id = response.json().get("run_id")
        break
