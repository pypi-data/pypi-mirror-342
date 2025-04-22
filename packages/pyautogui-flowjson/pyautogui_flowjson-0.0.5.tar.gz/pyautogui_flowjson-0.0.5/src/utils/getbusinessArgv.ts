import { argv } from '@zeroer/general-tools'
import { ServerType } from '../types'

export const getbusinessArgv = () => {
  if (argv.serverType && !Object.values(ServerType).includes(argv.serverType))
    throw new Error(`serverType 只能是 ${Object.values(ServerType).join(', ')}`)
  return {
    serverType: (argv.serverType ?? ServerType.mcpServer) as ServerType,
  }
}
