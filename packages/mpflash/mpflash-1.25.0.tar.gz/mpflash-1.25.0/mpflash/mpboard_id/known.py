"""
KNOWN ports and boards are sourced from the micropython repo,
this info is stored in the board_info.json file
and is used to identify the board and port for flashing.
This module provides access to the board info and the known ports and boards."""

from functools import lru_cache
from typing import List, Optional, Tuple

from mpflash.db.boards import find_board_id, find_board_info
from mpflash.errors import MPFlashError
from mpflash.versions import clean_version
from mpflash.logger import log

from .board import Board
from .store import read_known_boardinfo


def get_known_ports() -> List[str]:
    # TODO: Filter for Version
    log.warning("get_known_ports() is deprecated")
    mp_boards = read_known_boardinfo()
    # select the unique ports from info
    ports = set({board.port for board in mp_boards if board.port})
    return sorted(list(ports))


def get_known_boards_for_port(port: Optional[str] = "", versions: Optional[List[str]] = None) -> List[Board]:
    """
    Returns a list of boards for the given port and version(s)

    port: The Micropython port to filter for
    versions:  Optional, The Micropython versions to filter for (actual versions required)
    """
    mp_boards = read_known_boardinfo()
    if versions:
        preview_or_stable = "preview" in versions or "stable" in versions
    else:
        preview_or_stable = False

    # filter for 'preview' as they are not in the board_info.json
    # instead use stable version
    versions = versions or []
    if "preview" in versions:
        versions.remove("preview")
        versions.append("stable")
    # filter for the port
    if port:
        mp_boards = [board for board in mp_boards if board.port == port]
    if versions:
        # make sure of the v prefix
        versions = [clean_version(v) for v in versions]
        # filter for the version(s)
        mp_boards = [board for board in mp_boards if board.version in versions]
        if not mp_boards and preview_or_stable:
            # nothing found - perhaps there is a newer version for which we do not have the board info yet
            # use the latest known version from the board info
            mp_boards = read_known_boardinfo()
            last_known_version = sorted({b.version for b in mp_boards})[-1]
            mp_boards = [board for board in mp_boards if board.version == last_known_version]

    return mp_boards


def known_stored_boards(port: str, versions: Optional[List[str]] = None) -> List[Tuple[str, str]]:
    """
    Returns a list of tuples with the description and board name for the given port and version

    port : str : The Micropython port to filter for
    versions : List[str] : The Micropython versions to filter for (actual versions required)
    """
    mp_boards = get_known_boards_for_port(port, versions)

    boards = set({(f"{board.version} {board.description}", board.board_id) for board in mp_boards})
    return sorted(list(boards))


@lru_cache(maxsize=20)
def find_known_board(board_id: str, version ="") -> Board:
    """Find the board for the given BOARD_ID or 'board description' and return the board info as a Board object"""
    # Some functional overlap with:
    # mpboard_id\board_id.py _find_board_id_by_description
    # TODO: Refactor to search the SQLite DB instead of the JSON file
    board_ids = find_board_id(board_id = board_id, version = version or "%")
    boards = []
    for board_id in board_ids:
        # if we have a board_id, use it to find the board info
        boards += [Board.from_dict(dict(r)) for r in find_board_info(board_id = board_id)]
  

    # if board_ids:
    #     # if we have a board_id, use it to find the board info
    #     board_id = board_ids[0]
    # info = read_known_boardinfo()
    # for board_info in info:
    #     if board_id in (
    #         board_info.board_id,
    #         board_info.description,
    #     ) or board_info.description.startswith(board_id):
    #         if not board_info.cpu:
    #             # failsafe for older board_info.json files
    #             print(f"Board {board_id} has no CPU info, using port as CPU")
    #             if " with " in board_info.description:
    #                 board_info.cpu = board_info.description.split(" with ")[-1]
    #             else:
    #                 board_info.cpu = board_info.port
    #         return board_info
    raise MPFlashError(f"Board {board_id} not found")
