from dataclasses import dataclass
from typing import Iterable, NamedTuple
from aoc.parsers import digits, transform


class File(NamedTuple):
    file_id: int
    block_count: int


@dataclass
class FreeSpace:
    block_count: int


def expand_blocks(disk_map: list[int]):
    expanded_map = list[int | None]()
    for index, block_count in enumerate(disk_map):
        file_id = index // 2 if index % 2 == 0 else None
        expanded_map.extend([file_id] * block_count)
    return expanded_map


def expand_files(disk_map: list[int]):
    disk = list[File | FreeSpace]()
    for index, block_count in enumerate(disk_map):
        file_id = index // 2 if index % 2 == 0 else None
        if file_id is not None:
            disk.append(File(file_id, block_count))
        else:
            disk.append(FreeSpace(block_count))
    return disk


def compact_filesystem(disk: list[int | None]):
    result: list[int] = []
    left = 0
    right = len(disk) - 1

    while left <= right:
        file_id = disk[left]
        if file_id is not None:
            result.append(file_id)
            left += 1
            continue
        else:
            file_id = disk[right]
            if file_id is not None:
                result.append(file_id)
                left += 1
            right -= 1

    return result


def move_file(disk: list[File | FreeSpace], file: File, target_position: int):
    old_pos = disk.index(file)
    disk[old_pos] = FreeSpace(file.block_count)
    target = disk[target_position]
    if file.block_count == target.block_count:
        disk[target_position] = file
    else:
        assert isinstance(target, FreeSpace)
        disk.insert(target_position, file)
        target.block_count -= file.block_count


def defrag_file(disk: list[File | FreeSpace], file: File):
    for position, target in enumerate(disk):
        if isinstance(target, FreeSpace) and file.block_count <= target.block_count:
            move_file(disk, file, position)
            break
        if target == file:
            break


def defrag(disk: list[File | FreeSpace]):
    files = [file for file in reversed(disk) if isinstance(file, File)]

    for file in files:
        defrag_file(disk, file)


def files_to_blocks(disk: list[File | FreeSpace]):
    result = list[int | None]()
    for item in disk:
        match item:
            case File(file_id, block_count):
                result.extend([file_id] * block_count)
            case FreeSpace(block_count):
                result.extend([None] * block_count)
    return result


def checksum(expanded_map: Iterable[int | None]):
    return sum(
        index * file_id
        for index, file_id in enumerate(expanded_map)
        if file_id is not None
    )


@transform(digits)
def part_1(disk_map: list[int]):
    disk = expand_blocks(disk_map)
    compacted = compact_filesystem(disk)
    return checksum(compacted)


@transform(digits)
def part_2(disk_map: list[int]):
    disk = expand_files(disk_map)
    defrag(disk)
    return checksum(files_to_blocks(disk))
