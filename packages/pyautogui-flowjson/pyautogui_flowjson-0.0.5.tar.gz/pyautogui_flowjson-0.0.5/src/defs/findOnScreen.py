import asyncio
import pyautogui
from flowjson.utils.index import findOnScreen
from utils.jsPy import getJsEnvArg, pyToJsArg


async def bootstrap():
    arg = await getJsEnvArg()
    res = await findOnScreen(**arg)
    if res is None:
        return await pyToJsArg("未能查找到图片")
    pyautogui.click(*res)
    return await pyToJsArg("操作成功")


def main():
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())


# 直接运行脚本的方式 而非包的调用
if __name__ == "__main__":
    main()
