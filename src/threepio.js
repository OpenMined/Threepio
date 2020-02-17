import * as tf from '@tensorflow/tfjs';
import tfMap from '../docs-crawler/docs/output/tfjs/1.5.1.json';
import { MISSING_ARGUMENTS } from './_errors';
import { NORMALIZATION_REGEX } from './_constants';

export default class Threepio {
  constructor(from, version) {
    this.form = from;
    this.version = version;
    this.tfMap = tfMap;
    this.tf = tf;
  }

  normalizeFunctionName(name) {
    return name
      .match(NORMALIZATION_REGEX)
      .join('')
      .toLowerCase();
  }

  matchArgs(args, argMap) {
    // Sort args by index
    argMap.args.sort((a, b) =>
      a.index === b.index ? 0 : a.index < b.index ? -1 : 1
    );
    for (const [i, arg] of args.entries()) {
      // TODO: match args based on fromLibrary name
      // TODO: Ensure order is preserved
      // TODO: Ensure there are not any missing required arguments
      console.log(i, arg);
      continue;
    }

    return args;
  }

  translate(func) {
    if (
      !('code' in func) ||
      !('function_name' in func) ||
      !('args' in func) ||
      !('kwargs' in func)
    ) {
      throw new Error(MISSING_ARGUMENTS);
    }

    const command = this.tfMap[this.normalizeFunctionName(func.function_name)];
    if (command) {
      tf[command.function_name](...func.args);
    }
  }
}
