import * as tf from '@tensorflow/tfjs';
import mappedCommands from '../../static/mapped_commands.json';
import { translationMissing } from './_errors';
import { NORMALIZATION_REGEX, WORD_TRANSLATIONS } from './_constants';
import Command from './command';

export default class Threepio {
  constructor(from, to, version) {
    this.fromLang = from;
    this.toLang = to;
    this.version = version;
    this.mappedCommands = mappedCommands;
    this.tf = tf;
  }

  _normalizeFunctionName(name) {
    const result = name
      .match(NORMALIZATION_REGEX)
      .join('')
      .toLowerCase();

    if (result in this.mappedCommands[this.toLang]) {
      return result;
    }

    if (result in WORD_TRANSLATIONS) {
      return WORD_TRANSLATIONS[result];
    }

    throw new Error(translationMissing(name));
  }

  orderArgs(cmd, fromInfo, toInfo) {
    const newArgs = [];
    for (const [i, arg] of cmd.args.entries()) {
      const fArg = fromInfo.args.filter(a => a.index === i)[0];
      const tArg = toInfo.args.filter(a => a.name === fArg[this.toLang])[0];
      if (typeof tArg === 'undefined') {
        newArgs.push(arg);
        continue;
      }

      newArgs.splice(tArg.index, 0, arg);
    }

    for (const [, kwarg] of cmd.kwargs.entries()) {
      const [k, v] = kwarg;
      const fArg = fromInfo.args.filter(a => a.name === k)[0];
      const tArg = toInfo.args.filter(a => a.name === fArg[this.toLang])[0];

      if (typeof tArg === 'undefined') {
        // throw warning for kwarg translation missing
        console.warn(
          `Unable to translare kwarg ${k} for command ${cmd.functionName}`
        );
        continue;
      }

      newArgs.splice(tArg.index, 0, v);
    }

    return newArgs;
  }

  translate(cmd) {
    const toInfo = this.mappedCommands[this.toLang][
      this._normalizeFunctionName(cmd.functionName, this.toLang)
    ];
    const fromInfo = this.mappedCommands[this.fromLang][
      this._normalizeFunctionName(cmd.functionName, this.toLang)
    ];

    const attrs = [...toInfo.attrs];
    let translatedCmd = this[attrs.shift()];
    while (attrs.length > 0) {
      translatedCmd = translatedCmd[attrs.shift()];
    }

    const args = this.orderArgs(cmd, fromInfo, toInfo);

    return new Command(cmd.functionName, args, cmd.kwargs, translatedCmd);
  }
}
