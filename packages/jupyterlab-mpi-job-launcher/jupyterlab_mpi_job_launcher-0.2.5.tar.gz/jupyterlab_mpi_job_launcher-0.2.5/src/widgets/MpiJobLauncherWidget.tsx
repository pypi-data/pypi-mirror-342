import { ReactWidget } from "@jupyterlab/apputils";
import React from 'react';
import MpiJobLauncherComponent from "../components/MpiJobLauncherComponent";

export class MpiJobLauncherWidget extends ReactWidget {
  constructor() {
    super()
  }

  render(): JSX.Element {
    return (
      <div
        style={{
          width: '100%',
        }}
      >
        <MpiJobLauncherComponent />
      </div>
    )
  }
}