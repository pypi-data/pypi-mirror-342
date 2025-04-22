import z from 'zod'
import { def, execPyFile, lfJoin } from '../utils'

export const findOnScreenDef = def({
  name: 'findOnScreen-click',
  description: lfJoin('在屏幕中查询图片的位置并点击其中心'),
  argsSchema: {
    targetImagePath: z.string().describe(lfJoin('目标图片的绝对路径')),
    confidence: z
      .number()
      .optional()
      .describe(lfJoin('表示从当前屏幕中查询图片的相似度', '默认值 0.95')),
  },
  async requestHandler(arg, extra) {
    const res = await execPyFile('src/defs/findOnScreen.py', arg)
    return res
  },
})
