import { MISSING_ARGUMENTS, NOT_TRANSLATED } from './_errors';

export default class Command {
  constructor(code, functionName, args, kwargs) {
    if (!code || !functionName || !args || !kwargs) {
      throw new Error(MISSING_ARGUMENTS);
    }

    this.code = code;
    this.functionName = functionName;
    this.args = args;
    this.kwargs = kwargs;
    this.execFn = undefined;
  }

  executeRoutine() {
    if (typeof this.execFn === 'undefined') {
      throw new TypeError(NOT_TRANSLATED);
    }

    return this.execFn(...this.args);
  }
}
