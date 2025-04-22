import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os
import pyautogui
import sys
import time
from typing import Literal, Optional
import pydash
from flowjson.utils.index import execRun, findOnScreen, imagesDirPath, printDebug


async def bootstrap():
    # confidence 取值 预期是 选中能识别 未选中 不能识别
    # confidence = 0.99
    # [res1, res2, res3] = await asyncio.gather(
    #     *[
    #         # n 选中
    #         findOnScreen(
    #             os.path.join(imagesDirPath, "dmr/ck/job2/7-1-n-selected-include.png"),
    #             confidence=confidence,
    #         ),
    #         # n 未选中
    #         findOnScreen(
    #             os.path.join(imagesDirPath, "dmr/ck/job2/3-1-n-unselected-click.png"),
    #             confidence=confidence,
    #         ),
    #         # 模糊 能匹配
    #         findOnScreen(
    #             os.path.join(
    #                 imagesDirPath, "dmr/ck/job2/6-1-breakdown-prompt-click.png"
    #             ),
    #             confidence=0.8,
    #         ),
    #     ]
    # )
    # printDebug(res1, res2, res3)
    # pyautogui.press("e")
    # pyautogui.press("space")

    return


def main():
    startTime = int(time.time() * 1000)
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())
    printDebug(f"整体任务耗时：{int(time.time() * 1000) - startTime} ms")


main()
