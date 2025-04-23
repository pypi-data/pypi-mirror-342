import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { inspectorIcon } from '@jupyterlab/ui-components';
import { requestAPI } from './handler';
import { MpiJobLauncherWidget } from './widgets/MpiJobLauncherWidget';
import { Widget } from '@lumino/widgets';


const PLUGIN_ID = 'jupyterlab-mpi-job-launcher:plugin';
const PALETTE_CATEGORY = 'Admin tools';

namespace CommandIDs {
  export const createNew = 'jupyterlab-mpi-job-launcher:open-form';
}

function activate(
  app: JupyterFrontEnd,
  settingRegistry: ISettingRegistry | null,
  launcher: ILauncher | null,
  palette: ICommandPalette | null
) {
  console.log('JupyterLab extension jupyterlab-mpi-job-launcher is activated!');

  if (settingRegistry) {
    settingRegistry
      .load(plugin.id)
      .then(settings => {
        console.log('jupyterlab-mpi-job-launcher settings loaded:', settings.composite);
      })
      .catch(reason => {
        console.error('Failed to load settings for jupyterlab-mpi-job-launcher.', reason);
      });
  }

  requestAPI<any>('get-example')
    .then(data => {
      console.log(data);
    })
    .catch(reason => {
      console.error(
        `The jupyterlab_mpi_job_launcher server extension appears to be missing.\n${reason}`
      );
    });

  const { commands } = app;
  const command = CommandIDs.createNew;

  commands.addCommand(command, {
    label: 'Launch MPI Job',
    caption: 'Launch MPI Job',
    icon: args => (args['isPalette'] ? undefined : inspectorIcon),
    execute: async args => {
      console.log('Command executed');

      const widget = new MpiJobLauncherWidget();
      widget.id = 'mpi-job-launcher-form';
      widget.title.label = 'Launch MPI Job';
      widget.title.closable = true;

      Widget.attach(widget, document.body);
    }
  });

  if (launcher) {
    launcher.add({
      command,
      category: 'Admin tools',
      rank: 1
    });
  }

  if (palette) {
    palette.addItem({
      command,
      args: { isPalette: true },
      category: PALETTE_CATEGORY
    });
  }
}

/**
 * Initialization data for the jupyterlab-mpi-job-launcher extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ISettingRegistry, ILauncher, ICommandPalette],
  activate
};

export default plugin;