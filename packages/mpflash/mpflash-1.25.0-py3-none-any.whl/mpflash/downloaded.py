from pathlib import Path
from typing import Dict, List, Optional

import jsonlines
from loguru import logger as log

from mpflash.common import PORT_FWTYPES, FWInfo
from mpflash.db.downloads import downloaded
from mpflash.versions import clean_version

from .config import config

# #########################################################################################################


def clean_downloaded_firmwares(fw_folder: Path) -> None:
    """
    Remove duplicate entries from the firmware.jsonl file, keeping the latest one
    uniqueness is based on the filename
    """
    # Duplication should no longer happen,
    # but is would be a good idea to check the consistence between the DB and the downloads folder sometimes 
    pass 


def find_downloaded_firmware(
    *,
    board_id: str,
    version: str = "",  # v1.2.3
    port: str = "",
    variants: bool = False,
    db_path: Optional[Path] = None,
    trie: int = 1,
    selector: Optional[Dict[str, str]] = None,
) -> List[FWInfo]:
    if selector is None:
        selector = {}
    
    # Use the information in firmwares.jsonl to find the firmware file
    log.debug(f"{trie}] Looking for firmware for {board_id} {version} ")
    fw_list = downloaded()
    if not fw_list:
        log.error("No firmware files found. Please download the firmware first.")
        return []
    # filter by version
    version = clean_version(version)
    fw_list = filter_downloaded_fwlist(fw_list, board_id, version, port, variants, selector)

    if not fw_list and trie < 3:
        log.info(f"Try ({trie+1}) to find a firmware for the board {board_id}")
        if trie == 1:
            # ESP board naming conventions have changed by adding a PORT prefix
            if port.startswith("esp") and not board_id.startswith(port.upper()):
                board_id = f"{port.upper()}_{board_id}"
            # RP2 board naming conventions have changed by adding a _RPI prefix
            if port == "rp2" and not board_id.startswith("RPI_"):
                board_id = f"RPI_{board_id}"
        elif trie == 2:
            board_id = board_id.replace("_", "-")

        fw_list = find_downloaded_firmware(
            db_path=db_path,
            board_id=board_id,
            version=version,
            port=port,
            trie=trie + 1,
            selector=selector,
        )
        # hope we have a match now for the board
    # sort by filename
    fw_list.sort(key=lambda x: x.filename)
    return fw_list


def filter_downloaded_fwlist(
    fw_list: List[FWInfo],
    board_id: str,
    version: str,  # v1.2.3
    port: str,
    # preview: bool,
    variants: bool,
    selector: dict,
) -> List[FWInfo]:
    """Filter the downloaded firmware list based on the provided parameters"""
    if "preview" in version:
        # never get a preview for an older version
        fw_list = [fw for fw in fw_list if fw.preview]
    else:
        # older FWInfo version has no v1.2.3 prefix
        either = [clean_version(version, drop_v=False), clean_version(version, drop_v=True)]
        fw_list = [fw for fw in fw_list if fw.version in either]
    log.trace(f"Filtering firmware for {version} : {len(fw_list)} found.")
    # filter by port
    if port:
        fw_list = [fw for fw in fw_list if fw.port == port and Path(fw.firmware).suffix in PORT_FWTYPES[port]]
        log.trace(f"Filtering firmware for {port} : {len(fw_list)} found.")

    if board_id:
        if variants:
            # any variant of this board_id
            fw_list = [fw for fw in fw_list if fw.board == board_id]
        else:
            # the firmware variant should match exactly the board_id
            fw_list = [fw for fw in fw_list if fw.variant == board_id]
        log.trace(f"Filtering firmware for {board_id} : {len(fw_list)} found.")

    if selector and port in selector:
        fw_list = [fw for fw in fw_list if fw.filename.endswith(selector[port])]
    return fw_list


# #########################################################################################################
#
