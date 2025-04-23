import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogProps, DialogTitle, TextField, Typography } from '@mui/material';
import React from 'react'
import { requestAPI } from '../handler';
import { Notification } from '@jupyterlab/apputils';

const MpiJobLauncherComponent: React.FC = (props): JSX.Element => {
     const [open, setOpen] = React.useState(true);
     // const [image, setImage] = React.useState('image01');
     const [fullWidth] = React.useState(true);
     const [maxWidth] = React.useState<DialogProps['maxWidth']>('md');

     const handleClose = () => {
          setOpen(false);
     };
     return (
          <React.Fragment>
               <Dialog
                    open={open}
                    onClose={handleClose}
                    fullWidth={fullWidth}
                    maxWidth={maxWidth}
                    PaperProps={{
                         component: 'form',
                         onSubmit: async (event: React.FormEvent<HTMLFormElement>) => {
                              event.preventDefault();
                              const formData = new FormData(event.currentTarget);
                              const formJson = Object.fromEntries((formData as any).entries());

                              // Se arma el payload con la estructura deseada:
                              const payload = {
                                   launcher: {
                                        cpu: formJson['launcher-cpu'],
                                        memory: formJson['launcher-memory'],
                                        image: formJson['launcher-image'],
                                        command: formJson['launcher-command'],
                                   },
                                   worker: {
                                        cpu: formJson['worker-cpu'],
                                        memory: formJson['worker-memory'],
                                        image: formJson['worker-image'],
                                        replicas: Number(formJson['worker-replicas']),
                                   },
                              };

                              console.log(payload);

                              Notification.promise(
                                   requestAPI<any>('submit', {
                                        method: 'POST',
                                        body: JSON.stringify(payload),
                                   }),
                                   {
                                        pending: {
                                             message: 'Sending info to gRPC server',
                                        },
                                        success: {
                                             message: (result: any, data) => result.message,
                                             options: { autoClose: 3000 },
                                        },
                                        error: {
                                             message: (reason, data) =>
                                                  `Error sending info. Reason: ${reason}`,
                                             options: { autoClose: 3000 },
                                        },
                                   }
                              );

                              handleClose();
                         },
                    }}
               >
                    <DialogTitle>Parameters</DialogTitle>
                    <DialogContent>
                         <DialogContentText>
                              Please fill the form with your parameters.
                         </DialogContentText>
                         {/* Sección Launcher */}
                         <Typography variant="h6" style={{ marginTop: '16px' }}>
                              Launcher
                         </Typography>
                         <TextField
                              required
                              id="launcher-cpu"
                              name="launcher-cpu"
                              label="Launcher CPU"
                              variant="standard"
                              margin="dense"
                              fullWidth
                         />
                         <TextField
                              required
                              id="launcher-memory"
                              name="launcher-memory"
                              label="Launcher Memory"
                              variant="standard"
                              margin="dense"
                              fullWidth
                         />
                         <TextField
                              required
                              id="launcher-image"
                              name="launcher-image"
                              label="Launcher Image"
                              variant="standard"
                              margin="dense"
                              fullWidth
                         />
                         <TextField
                              required
                              id="launcher-command"
                              name="launcher-command"
                              label="Launcher Command"
                              variant="standard"
                              margin="dense"
                              fullWidth
                              multiline
                              rows={4}
                              sx={{
                                   '& .MuiInputBase-input': {
                                        overflowY: 'auto',
                                        scrollbarWidth: 'thin',
                                        '&::-webkit-scrollbar': {
                                             width: '8px',
                                        },
                                        '&::-webkit-scrollbar-thumb': {
                                             backgroundColor: '#ccc',
                                             borderRadius: '4px',
                                        },
                                   },
                              }}
                         />

                         {/* Sección Worker */}
                         <Typography variant="h6" style={{ marginTop: '16px' }}>
                              Worker
                         </Typography>
                         <TextField
                              required
                              id="worker-cpu"
                              name="worker-cpu"
                              label="Worker CPU"
                              variant="standard"
                              margin="dense"
                              fullWidth
                         />
                         <TextField
                              required
                              id="worker-memory"
                              name="worker-memory"
                              label="Worker Memory"
                              variant="standard"
                              margin="dense"
                              fullWidth
                         />
                         <TextField
                              required
                              id="worker-image"
                              name="worker-image"
                              label="Worker Image"
                              variant="standard"
                              margin="dense"
                              fullWidth
                         />
                         <TextField
                              required
                              id="worker-replicas"
                              name="worker-replicas"
                              label="Worker Replicas"
                              variant="standard"
                              margin="dense"
                              fullWidth
                              type="number"
                         />
                    </DialogContent>
                    <DialogActions>
                         <Button onClick={handleClose}>Cancel</Button>
                         <Button type="submit">Send</Button>
                    </DialogActions>
               </Dialog>
          </React.Fragment>);
}

export default MpiJobLauncherComponent;