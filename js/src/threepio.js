import * as tf from '@tensorflow/tfjs';
import mappedCommands from '../../static/mapped_commands.json';
import { NORMALIZATION_REGEX } from './_constants';

export default class Threepio {
  constructor(from, version) {
    this.form = from;
    this.version = version;
    this.mappedCommands = mappedCommands;
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

  translate(toLang, cmd) {
    const cmdInfo = this.mappedCommands[toLang][
      this.normalizeFunctionName(cmd.functionName)
    ];

    let translatedCmd = this[cmdInfo.attrs.shift()];
    while (cmdInfo.attrs.length > 0) {
      translatedCmd = translatedCmd[cmdInfo.attrs.shift()];
    }

    cmd.execFn = translatedCmd;
    return cmd;
  }
}
