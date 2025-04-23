from datetime import datetime
from pathlib import Path

from renardo.settings_manager import settings
from renardo.gatherer.collection_download import download_files_from_json_index_concurrent

def is_default_spack_initialized():
    return (settings.get_path("SAMPLES_DIR") / settings.get("samples.DEFAULT_SAMPLES_PACK_NAME") / 'downloaded_at.txt').exists()





def download_default_sample_pack(logger=None):

    logger.write_line(f"Downloading Default Sample Pack {settings.get("samples.DEFAULT_SAMPLES_PACK_NAME")} from {settings.get("samples.SAMPLES_DOWNLOAD_SERVER")}\n")
    download_files_from_json_index_concurrent(
        json_url=f'{settings.get("SAMPLES_DOWNLOAD_SERVER")}/{settings.get("samples.DEFAULT_SAMPLES_PACK_NAME")}/collection_index.json',
        download_dir=settings.get("samples.SAMPLES_DIR"),
        logger=logger
    )

    try:
        with open(settings.get_path("SAMPLES_DIR") / settings.get("samples.DEFAULT_SAMPLES_PACK_NAME") / 'downloaded_at.txt', mode="w") as file:
            file.write(str(datetime.now()))
    except Exception as e:
        print(e)

