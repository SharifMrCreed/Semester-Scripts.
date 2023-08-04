# Retrieve firestore data
# Download pdf files
# extract info from files
# Update fields

import asyncio


async def hello():
    print("Hello")
    await asyncio.sleep(3)
    print("World")


async def main():
    await asyncio.gather(hello(), hello(), hello())


asyncio.run(main())
