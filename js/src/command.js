import * as tf from '@tensorflow/tfjs';
import { MISSING_ARGUMENTS } from './_errors';

export default class Command {
  constructor(code, functionName, args, kwargs) {
    if (!code || !functionName || !args || !kwargs) {
      throw new Error(MISSING_ARGUMENTS);
    }

    this.code = code;
    this.functionName = functionName;
    this.args = args;
    this.kwargs = kwargs;
  }

  execute() {
    tf[this.functionPath](...this.args);
  }
}
