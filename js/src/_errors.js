export const MISSING_ARGUMENTS = `Translation must receive an object containing 'code', 'function_name', 'args', and 'kwargs'`;
export const NOT_TRANSLATED = `Translation must be completed before executing`;
export const translationMissing = c =>
  `Translation for the command ${c} is not currently supported`;
