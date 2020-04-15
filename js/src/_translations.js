import Command from './command';

export const CUSTOM_IMPLEMENTATIONS = {
  torch: {
    float: (cmd) => {
      return {
        command: new Command('cast', [...cmd.args, 'float32'], cmd.kwargs),
        attrs: ['tf', 'cast']
      };
    }
  }
};
