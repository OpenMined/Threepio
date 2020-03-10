import * as tf from '@tensorflow/tfjs';
import mappedCommands from '../../static/mapped_commands.json';
import { translationMissing } from './_errors';
import { NORMALIZATION_REGEX, WORD_TRANSLATIONS } from './_constants';

export default class Threepio {
  constructor(from, version) {
    this.form = from;
    this.version = version;
    this.mappedCommands = mappedCommands;
    this.tf = tf;
  }

  _normalizeFunctionName(name, toLang) {
    const result = name
      .match(NORMALIZATION_REGEX)
      .join('')
      .toLowerCase();

    if (result in this.mappedCommands[toLang]) {
      return result;
    }

    if (result in WORD_TRANSLATIONS) {
      return WORD_TRANSLATIONS[result];
    }

    throw new Error(translationMissing(name));
  }

  translate(toLang, cmd) {
    const cmdInfo = this.mappedCommands[toLang][
      this._normalizeFunctionName(cmd.functionName, toLang)
    ];

    let translatedCmd = this[cmdInfo.attrs.shift()];
    while (cmdInfo.attrs.length > 0) {
      translatedCmd = translatedCmd[cmdInfo.attrs.shift()];
    }

    cmd.execFn = translatedCmd;
    return cmd;
  }
}
