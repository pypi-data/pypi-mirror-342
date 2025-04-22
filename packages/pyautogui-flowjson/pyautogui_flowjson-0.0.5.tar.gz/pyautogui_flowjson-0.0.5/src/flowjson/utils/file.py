import aiofiles


async def readFile(filePath: str):
    # 使用 aiofiles 打开文件
    async with aiofiles.open(filePath, mode="r", encoding="utf-8") as file:
        # 读取文件内容
        content = await file.read()
    return content
