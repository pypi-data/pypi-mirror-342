import z from 'zod'
import { def, lfJoin, toPyStrArg } from '../utils'
import { PythonShell } from 'python-shell'

export const clickDef = def({
  name: 'click',
  description: lfJoin(
    '执行按下鼠标按钮然后立即释放的操作。',
    '当没有传递任何参数时，主鼠标按钮将在鼠标光标当前位置处点击。'
  ),
  argsSchema: {
    x: z
      .union([
        z.number().optional(),
        // z.string(),
        z.tuple([z.number(), z.number()]),
      ])
      .describe(
        lfJoin(
          '如果同时传递了 x 和 y 的整数值，点击将在该 x,y 坐标处发生',
          // PyAutoGUI 没有做mac 分辨率处理
          // '如果 x 是一个字符串，则该字符串是图像文件名，PyAutoGUI 将尝试在屏幕上定位该文件并点击其中心',
          '如果 x 是由两个坐标组成的数组，这些坐标将被用于 x,y 坐标点击'
        )
      ),
    y: z
      .number()
      .optional()
      .describe(
        lfJoin('如果同时传递了 x 和 y 的整数值，点击将在该 x,y 坐标处发生')
      ),
    clicks: z
      .number()
      .optional()
      .describe(lfJoin('默认为 1', '表示要点击次数的整数')),
    interval: z
      .number()
      .optional()
      .describe(
        lfJoin(
          '如果 clicks > 1 它默认为 0 表示点击之间没有暂停',
          '表示每次点击之间等待多少秒的数量'
        )
      ),
    button: z
      .enum(['left', 'middle', 'right', 'primary', 'secondary'])
      .optional()
      .describe(
        lfJoin(
          "默认为'primary'(这是鼠标左键，除非操作系统已经设置为左撇子的用户。)",
          "可以是字符串常量 'left'、'middle'、'right'、'primary'或'secondary'之一"
        )
      ),
    duration: z
      .number()
      .optional()
      .describe(
        lfJoin(
          '默认为 0 即时移动',
          '如果指定了 x 和 y 并且 点击不在鼠标光标的当前位置发生 表示将鼠标移动到 x,y 需要多少秒'
        )
      ),
  },
  async requestHandler(arg) {
    const pyArgument = toPyStrArg(arg)
    await PythonShell.runString(
      lfJoin('import pyautogui', `pyautogui.click(${pyArgument})`)
    )
    return {
      content: [
        {
          type: 'text',
          text: '操作成功',
        },
      ],
    }
  },
})
