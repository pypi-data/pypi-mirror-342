import z from 'zod'
import { def, lfJoin } from '../utils'

// 业务
const Records: Record<
  string,
  {
    id: string
    content: string
  }
> = {
  key: {
    id: '999',
    content: '999的内容',
  },
}

export const SaveRecordDef = def({
  name: 'save-record',
  description: 'save 本地记录',
  argsSchema: {
    key: z.string().describe('本地记录 的 key'),
    content: z.string().describe('本地记录 的 content'),
  },
  async requestHandler({ key, content }) {
    Records[key] = {
      id: `${Object.keys(Records).length + 1}`,
      content,
    }

    return {
      content: [
        {
          type: 'text',
          text: `Save successfully id: ${Records[key].id} content: ${Records[key].content}`,
        },
      ],
    }
  },
})

// 无论mcpServer还是server 可选参数 必须在describe指定才能被模型识别
export const GetRecordDef = def({
  name: 'get-record',
  description: lfJoin('get 本地记录'),
  // 系统提示词 导致 模型 并不能准确 根据 inputSchema required 字段来识别哪些是可选参数
  // 所以 .optional() 声明了 在使用 describe 写提示词名称可选
  argsSchema: {
    key: z.string().optional().describe('本地记录 的 key'),
    id: z.string().optional().describe('本地记录 的 id'),
  },
  async requestHandler({ key, id }) {
    if (!key && !id) throw new Error('参数 key 和 id 至少要有一个')

    const obj = key
      ? Records[key]
      : Object.values(Records).find((item) => item.id === id)
    if (!obj)
      return {
        content: [
          {
            type: 'text',
            text: '未能检索预测数据',
          },
        ],
      }
    return {
      content: [
        {
          type: 'text',
          text: `get successfully id: ${obj.id} content: ${obj.content}`,
        },
      ],
    }
  },
})
