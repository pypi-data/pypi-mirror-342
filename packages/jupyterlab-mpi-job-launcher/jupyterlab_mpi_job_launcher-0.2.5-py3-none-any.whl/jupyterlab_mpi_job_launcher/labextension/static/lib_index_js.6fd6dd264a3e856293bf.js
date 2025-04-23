"use strict";
(self["webpackChunkjupyterlab_mpi_job_launcher"] = self["webpackChunkjupyterlab_mpi_job_launcher"] || []).push([["lib_index_js"],{

/***/ "./lib/components/MpiJobLauncherComponent.js":
/*!***************************************************!*\
  !*** ./lib/components/MpiJobLauncherComponent.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);




const MpiJobLauncherComponent = (props) => {
    const [open, setOpen] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(true);
    // const [image, setImage] = React.useState('image01');
    const [fullWidth] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(true);
    const [maxWidth] = react__WEBPACK_IMPORTED_MODULE_1___default().useState('md');
    const handleClose = () => {
        setOpen(false);
    };
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Dialog, { open: open, onClose: handleClose, fullWidth: fullWidth, maxWidth: maxWidth, PaperProps: {
                component: 'form',
                onSubmit: async (event) => {
                    event.preventDefault();
                    const formData = new FormData(event.currentTarget);
                    const formJson = Object.fromEntries(formData.entries());
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
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Notification.promise((0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('submit', {
                        method: 'POST',
                        body: JSON.stringify(payload),
                    }), {
                        pending: {
                            message: 'Sending info to gRPC server',
                        },
                        success: {
                            message: (result, data) => result.message,
                            options: { autoClose: 3000 },
                        },
                        error: {
                            message: (reason, data) => `Error sending info. Reason: ${reason}`,
                            options: { autoClose: 3000 },
                        },
                    });
                    handleClose();
                },
            } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.DialogTitle, null, "Parameters"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.DialogContent, null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.DialogContentText, null, "Please fill the form with your parameters."),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Typography, { variant: "h6", style: { marginTop: '16px' } }, "Launcher"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "launcher-cpu", name: "launcher-cpu", label: "Launcher CPU", variant: "standard", margin: "dense", fullWidth: true }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "launcher-memory", name: "launcher-memory", label: "Launcher Memory", variant: "standard", margin: "dense", fullWidth: true }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "launcher-image", name: "launcher-image", label: "Launcher Image", variant: "standard", margin: "dense", fullWidth: true }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "launcher-command", name: "launcher-command", label: "Launcher Command", variant: "standard", margin: "dense", fullWidth: true, multiline: true, rows: 4, sx: {
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
                    } }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Typography, { variant: "h6", style: { marginTop: '16px' } }, "Worker"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "worker-cpu", name: "worker-cpu", label: "Worker CPU", variant: "standard", margin: "dense", fullWidth: true }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "worker-memory", name: "worker-memory", label: "Worker Memory", variant: "standard", margin: "dense", fullWidth: true }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "worker-image", name: "worker-image", label: "Worker Image", variant: "standard", margin: "dense", fullWidth: true }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { required: true, id: "worker-replicas", name: "worker-replicas", label: "Worker Replicas", variant: "standard", margin: "dense", fullWidth: true, type: "number" })),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.DialogActions, null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: handleClose }, "Cancel"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Button, { type: "submit" }, "Send")))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (MpiJobLauncherComponent);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-mpi-job-launcher', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widgets_MpiJobLauncherWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widgets/MpiJobLauncherWidget */ "./lib/widgets/MpiJobLauncherWidget.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);







const PLUGIN_ID = 'jupyterlab-mpi-job-launcher:plugin';
const PALETTE_CATEGORY = 'Admin tools';
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'jupyterlab-mpi-job-launcher:open-form';
})(CommandIDs || (CommandIDs = {}));
function activate(app, settingRegistry, launcher, palette) {
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
    (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('get-example')
        .then(data => {
        console.log(data);
    })
        .catch(reason => {
        console.error(`The jupyterlab_mpi_job_launcher server extension appears to be missing.\n${reason}`);
    });
    const { commands } = app;
    const command = CommandIDs.createNew;
    commands.addCommand(command, {
        label: 'Launch MPI Job',
        caption: 'Launch MPI Job',
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.inspectorIcon),
        execute: async (args) => {
            console.log('Command executed');
            const widget = new _widgets_MpiJobLauncherWidget__WEBPACK_IMPORTED_MODULE_6__.MpiJobLauncherWidget();
            widget.id = 'mpi-job-launcher-form';
            widget.title.label = 'Launch MPI Job';
            widget.title.closable = true;
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget.attach(widget, document.body);
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
const plugin = {
    id: PLUGIN_ID,
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widgets/MpiJobLauncherWidget.js":
/*!*********************************************!*\
  !*** ./lib/widgets/MpiJobLauncherWidget.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MpiJobLauncherWidget: () => (/* binding */ MpiJobLauncherWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_MpiJobLauncherComponent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/MpiJobLauncherComponent */ "./lib/components/MpiJobLauncherComponent.js");



class MpiJobLauncherWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor() {
        super();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: {
                width: '100%',
            } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_MpiJobLauncherComponent__WEBPACK_IMPORTED_MODULE_2__["default"], null)));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.6fd6dd264a3e856293bf.js.map