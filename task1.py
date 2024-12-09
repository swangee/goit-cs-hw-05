import argparse

import asyncio
import os
from shutil import SameFileError
from collections import deque

import aiofiles
from aiopath import AsyncPath

async def read_folder(path: AsyncPath, dest: AsyncPath):
    tasks = []

    files = deque()
    files.appendleft(path)

    while files:
        dir = files.pop()
        async for file in dir.iterdir():
            if await file.is_file():
                tasks.append(asyncio.create_task(copy_file(file, dest)))

                continue

            if await file.is_dir():
                files.appendleft(file)


    await asyncio.wait(tasks)


async def copy_file(file: AsyncPath, dest: AsyncPath) -> None:
    ext = file.suffix
    if ext == "":
        ext = "none"
    ext = ext.lstrip(".")

    target_dir = os.path.join(dest, ext)
    target_dir_path = AsyncPath(target_dir)

    target_file = os.path.join(target_dir, file.name)
    target_file_path = AsyncPath(target_file)

    try:
        if not await target_dir_path.is_dir():
            await target_dir_path.mkdir(parents=True)


        async with aiofiles.open(file, 'rb') as src_file:
            async with aiofiles.open(target_file_path, 'wb') as dst_file:
                while chunk := await src_file.read(1024 * 1024):  # Read in chunks (1MB in this case)
                    await dst_file.write(chunk)

        print(f"file {file} was successfully copied to {target_file}")
    except SameFileError:
        print(f"file {target_file} already exists")
    except PermissionError as e:
        print(e)
    except Exception as e:
        print(f"failed to copy file {file} to {target_file}, error: {e}")

async def main():
    parser = argparse.ArgumentParser(
        prog='fgroup',
        description='Recursively copies files from target to dist based on a file extension')

    parser.add_argument('source')
    parser.add_argument('-d', '--destination', default='dist', required=False, help='Destination directory')

    args = parser.parse_args()

    src = AsyncPath(os.path.abspath(args.source))
    dist = AsyncPath(os.path.abspath(args.destination))

    await read_folder(src, dist)

if __name__ == '__main__':
    asyncio.run(main())