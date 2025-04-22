"use strict";
(self["webpackChunkjupyterlab_bxplorer_v2"] = self["webpackChunkjupyterlab_bxplorer_v2"] || []).push([["lib_index_js"],{

/***/ "./lib/components/BasicTabs.js":
/*!*************************************!*\
  !*** ./lib/components/BasicTabs.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Tabs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Tabs */ "./node_modules/@mui/material/esm/Tabs/Tabs.js");
/* harmony import */ var _mui_material_Tab__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/Tab */ "./node_modules/@mui/material/esm/Tab/Tab.js");
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _CustomTabPanel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./CustomTabPanel */ "./lib/components/CustomTabPanel.js");
/* harmony import */ var _FMViewComponent__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./FMViewComponent */ "./lib/components/FMViewComponent.js");
/* harmony import */ var _contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/DownloadHistoryContext */ "./lib/contexts/DownloadHistoryContext.js");
/* harmony import */ var _DownloadHistory__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./DownloadHistory */ "./lib/components/DownloadHistory.js");








const BasicTabs = (props) => {
    const [value, setValue] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(0);
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };
    const a11yProps = (index) => ({
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_1__.DownloadHistoryProvider, null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_2__["default"], { sx: { width: '100%' } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_2__["default"], { sx: { borderBottom: 1, borderColor: 'divider' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tabs__WEBPACK_IMPORTED_MODULE_3__["default"], { value: value, onChange: handleChange, "aria-label": "basic tabs example" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tab__WEBPACK_IMPORTED_MODULE_4__["default"], { label: "Favorites", ...a11yProps(0) }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tab__WEBPACK_IMPORTED_MODULE_4__["default"], { label: "Private", ...a11yProps(1) }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tab__WEBPACK_IMPORTED_MODULE_4__["default"], { label: "Public", ...a11yProps(2) }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tab__WEBPACK_IMPORTED_MODULE_4__["default"], { label: "Download History", ...a11yProps(3) }))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CustomTabPanel__WEBPACK_IMPORTED_MODULE_5__["default"], { value: value, index: 0 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_FMViewComponent__WEBPACK_IMPORTED_MODULE_6__["default"], { downloadsFolder: props.downloadsFolder, clientType: "favorites", folderOptions: ['Open', '|', 'Remove from favorites', 'Details'] })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CustomTabPanel__WEBPACK_IMPORTED_MODULE_5__["default"], { value: value, index: 1 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_FMViewComponent__WEBPACK_IMPORTED_MODULE_6__["default"], { downloadsFolder: props.downloadsFolder, clientType: "private", folderOptions: ['Open', '|', 'Add to favorites', 'Details'] })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CustomTabPanel__WEBPACK_IMPORTED_MODULE_5__["default"], { value: value, index: 2 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_FMViewComponent__WEBPACK_IMPORTED_MODULE_6__["default"], { downloadsFolder: props.downloadsFolder, clientType: "public", folderOptions: ['Open', '|', 'Add to favorites', 'Details'] })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CustomTabPanel__WEBPACK_IMPORTED_MODULE_5__["default"], { value: value, index: 3 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_DownloadHistory__WEBPACK_IMPORTED_MODULE_7__["default"], null)))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (BasicTabs);


/***/ }),

/***/ "./lib/components/CustomTabPanel.js":
/*!******************************************!*\
  !*** ./lib/components/CustomTabPanel.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/esm/Box/Box.js");


const CustomTabPanel = (props) => {
    const { children, value, index, ...other } = props;
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { role: "tabpanel", hidden: value !== index, id: `simple-tabpanel-${index}`, "aria-labelledby": `simple-tab-${index}`, ...other, style: { height: "calc(100vh - 48px)" } }, value === index && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { p: 3, height: "100%", overflowY: "auto" } }, children))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CustomTabPanel);


/***/ }),

/***/ "./lib/components/DownloadHistory.js":
/*!*******************************************!*\
  !*** ./lib/components/DownloadHistory.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_Refresh__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/icons-material/Refresh */ "./node_modules/@mui/icons-material/esm/Refresh.js");
/* harmony import */ var _mui_icons_material_Delete__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/icons-material/Delete */ "./node_modules/@mui/icons-material/esm/Delete.js");
/* harmony import */ var _mui_icons_material_DeleteSweep__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/icons-material/DeleteSweep */ "./node_modules/@mui/icons-material/esm/DeleteSweep.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var _contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../contexts/DownloadHistoryContext */ "./lib/contexts/DownloadHistoryContext.js");







const DownloadHistory = () => {
    const { history, loading, fetchHistory } = (0,_contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_2__.useDownloadHistory)();
    const [pollInterval, setPollInterval] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(2000);
    const timerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    // Borrar todos los registros
    const handleClearAll = async () => {
        try {
            const result = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('download_history?action=clean', {
                method: 'DELETE',
            });
            console.log(result.message);
            await fetchHistory();
        }
        catch (error) {
            console.error(error);
        }
    };
    // Borrar un ítem individual
    const handleDeleteItem = async (id) => {
        try {
            const result = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)(`download_history?id=${id}`, {
                method: 'DELETE',
            });
            console.log(result.message);
            await fetchHistory();
        }
        catch (error) {
            console.error(error);
        }
    };
    // Polling
    const pollHistory = async () => {
        const newHistory = await fetchHistory();
        const anyDownloading = newHistory.some((item) => item.status === 'downloading');
        if (anyDownloading) {
            const newInterval = Math.min(pollInterval * 1.5, 30000);
            setPollInterval(newInterval);
            timerRef.current = window.setTimeout(pollHistory, newInterval);
        }
        else {
            if (timerRef.current) {
                clearTimeout(timerRef.current);
                timerRef.current = null;
            }
            setPollInterval(2000);
        }
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        pollHistory();
        return () => {
            if (timerRef.current) {
                clearTimeout(timerRef.current);
            }
        };
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Box, { sx: {
            // Llenar el espacio disponible en el panel JupyterLab
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
            width: '100%',
            overflow: 'hidden',
            bgcolor: 'background.default',
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Box, { sx: {
                // Panel interno que se centrará horizontalmente si se quiere un ancho máx
                maxWidth: 600,
                width: '100%',
                margin: '0 auto',
                // Estructura en columna
                display: 'flex',
                flexDirection: 'column',
                flex: 1,
                minHeight: 0,
                bgcolor: 'background.paper',
                boxShadow: 3,
                borderRadius: 2,
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Box, { sx: {
                    flex: '0 0 auto',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    p: 1,
                    borderBottom: 1,
                    borderColor: 'divider',
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Typography, { variant: "h6", component: "h2" }, "Download History"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Box, null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: fetchHistory, color: "primary", "aria-label": "refresh", sx: { mr: 1 } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Refresh__WEBPACK_IMPORTED_MODULE_4__["default"], null)),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleClearAll, color: "secondary", "aria-label": "clear all" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_DeleteSweep__WEBPACK_IMPORTED_MODULE_5__["default"], null)))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Box, { sx: {
                    flex: '1 1 auto',
                    minHeight: 0,
                    overflowY: 'auto',
                    p: 1,
                } }, loading ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Box, { sx: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.CircularProgress, null))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.List, { sx: { p: 0 } }, history.length > 0 ? (history.map(download => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.ListItem, { key: download.id, divider: true },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.ListItemText, { primary: react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.95rem' } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null,
                            download.bucket,
                            "/",
                            download.key)), secondary: react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { fontSize: '0.85rem' } },
                        "Start: ",
                        new Date(download.start_time).toLocaleString(),
                        download.end_time ? ` | End: ${new Date(download.end_time).toLocaleString()}` : '',
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null),
                        "Status: ",
                        download.status,
                        download.error_message ? ` | Error: ${download.error_message}` : '') }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.ListItemSecondaryAction, null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { edge: "end", onClick: () => handleDeleteItem(download.id), "aria-label": "delete" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Delete__WEBPACK_IMPORTED_MODULE_6__["default"], null))))))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Typography, { sx: { textAlign: 'center', py: 2 } }, "No downloads available"))))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DownloadHistory);


/***/ }),

/***/ "./lib/components/FMViewComponent.js":
/*!*******************************************!*\
  !*** ./lib/components/FMViewComponent.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @syncfusion/ej2-react-filemanager */ "webpack/sharing/consume/default/@syncfusion/ej2-react-filemanager/@syncfusion/ej2-react-filemanager");
/* harmony import */ var _syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../contexts/DownloadHistoryContext */ "./lib/contexts/DownloadHistoryContext.js");
/**
 * FMViewComponent.tsx
 *
 * This component renders a file manager view using the Syncfusion FileManagerComponent.
 * It configures AJAX settings for communication with the JupyterLab Bxplorer API and handles
 * context menu actions such as file downloading.
 *
 * Props:
 *   - downloadsFolder: string representing the folder where downloads will be saved.
 *   - clientType: string representing the type of S3 client ('private' or 'public').
 */





/**
 * FMViewComponent React Functional Component.
 *
 * Renders a file manager interface with customized AJAX settings, context menu handlers,
 * and toolbar and details view configurations. It also modifies request data to include
 * the client type.
 *
 * @param {FMViewComponentProps} props - The component properties.
 * @returns {JSX.Element} The rendered component.
 */
const FMViewComponent = (props, ref) => {
    const { fetchHistory, startPolling } = (0,_contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_3__.useDownloadHistory)();
    const downloadsFolder = props.downloadsFolder || "downloads";
    const clientType = props.clientType || "private";
    const fileManagerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    // Allow parent to call refresh (if desired)
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useImperativeHandle)(ref, () => ({
        refresh: () => { var _a; return (_a = fileManagerRef.current) === null || _a === void 0 ? void 0 : _a.refresh(); },
    }));
    // Listens for the panel opening event and refreshes the FileManager
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const handlePanelOpen = () => {
            var _a;
            // Forcing recalculation and rendering of FileManager
            (_a = fileManagerRef.current) === null || _a === void 0 ? void 0 : _a.refresh();
        };
        window.addEventListener('filemanager-panel-open', handlePanelOpen);
        return () => {
            window.removeEventListener('filemanager-panel-open', handlePanelOpen);
        };
    }, []);
    /**
     * Computes the base URL for backend API requests.
     *
     * If the URL contains a "/user/" segment, it constructs the URL using the user path.
     * Otherwise, it returns the window's origin.
     *
     * @returns {string} The base URL.
     */
    const getBaseUrl = () => {
        const pathParts = window.location.pathname.split("/");
        const userIndex = pathParts.indexOf("user");
        if (userIndex !== -1 && pathParts.length > userIndex + 1) {
            return `${window.location.origin}/user/${pathParts[userIndex + 1]}`;
        }
        return window.location.origin;
    };
    const backendUrl = getBaseUrl();
    console.log(backendUrl);
    const ajaxSettings = {
        url: backendUrl + "/jupyterlab-bxplorer-v2/FileOperations",
    };
    /**
     * Retrieves a cookie value by its name.
     *
     * @param {any} name - The name of the cookie.
     * @returns {string | null} The cookie value if found, otherwise null.
     */
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }
    /**
     * Modifies AJAX request settings before sending the request.
     *
     * Sets the X-XSRFToken header and adds the client type to the request data.
     *
     * @param {any} args - The AJAX request arguments.
     */
    const onBeforeSend = (args) => {
        if (args.ajaxSettings) {
            const xsrfToken = getCookie('_xsrf');
            args.ajaxSettings.beforeSend = function (args) {
                args.httpRequest.setRequestHeader("X-XSRFToken", xsrfToken);
            };
        }
        console.log("ajaxBeforeSend action:", args.action);
        console.log("ajaxBeforeSend args:", args);
        let currentData = args.ajaxSettings.data;
        if (typeof currentData === "string") {
            try {
                currentData = JSON.parse(currentData);
            }
            catch (e) {
                console.error("Error parsing ajaxSettings.data:", e);
                currentData = {};
            }
        }
        const modifiedData = { ...currentData, client_type: clientType };
        args.ajaxSettings.data = JSON.stringify(modifiedData);
        console.log("ajaxBeforeSend modified args:", args);
    };
    /**
     * Handles context menu click events for the FileManager.
     *
     * If the "Download" option is selected, it initiates a download action by preparing
     * the payload and sending a request to the backend API. Displays dialogs for feedback.
     *
     * @param {any} args - The event arguments from the context menu click.
     */
    const contextMenuClickHandler = async (args) => {
        console.log("menuClick args:", args);
        if (args.item && args.item.text === "Add to favorites") {
            args.cancel = true;
            const currentPath = fileManagerRef.current.path || "/";
            const selectedItems = args.data || (fileManagerRef.current && fileManagerRef.current.selectedItems);
            console.log("current:", fileManagerRef.current);
            console.log("currentPath:", currentPath);
            console.log("selectedItems:", selectedItems);
            console.log("clientType:", clientType);
            if (currentPath !== "/") {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: "Not Allowed",
                    body: "You can only add buckets to favorites from the root.",
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: "OK" })],
                });
                return;
            }
            const selectedBucket = selectedItems === null || selectedItems === void 0 ? void 0 : selectedItems[0];
            if (!selectedBucket) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: "No Selection",
                    body: "No bucket selected to add to favorites.",
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: "OK" })],
                });
                return;
            }
            try {
                await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('favorites', {
                    method: 'POST',
                    body: JSON.stringify({ bucket: selectedBucket, client_type: clientType }),
                    headers: { 'Content-Type': 'application/json' },
                });
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Success',
                    body: `"${selectedBucket}" added to favorites.`,
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: 'OK' })]
                });
            }
            catch (error) {
                console.error("Add to favorites error:", error);
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)('Error', 'Failed to add bucket to favorites.');
            }
            return;
        }
        if (args.item && args.item.text === "Remove from favorites") {
            args.cancel = true;
            const currentPath = fileManagerRef.current.path || "/";
            const selectedItems = args.data || (fileManagerRef.current && fileManagerRef.current.selectedItems);
            if (currentPath !== "/") {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: "Not Allowed",
                    body: "You can only remove buckets from favorites from the root.",
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: "OK" })],
                });
                return;
            }
            const selectedBucket = selectedItems === null || selectedItems === void 0 ? void 0 : selectedItems[0];
            if (!selectedBucket) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: "No Selection",
                    body: "No bucket selected to remove from favorites.",
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: "OK" })],
                });
                return;
            }
            try {
                await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('favorites', {
                    method: 'DELETE',
                    body: JSON.stringify({ bucket: selectedBucket }),
                    headers: { 'Content-Type': 'application/json' },
                });
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Success',
                    body: `"${selectedBucket}" removed from favorites.`,
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: 'OK' })]
                });
                const fm = fileManagerRef.current;
                if (fm) {
                    const currentPath = fm.path;
                    fm.path = "/temp-refresh";
                    fm.path = currentPath;
                }
            }
            catch (error) {
                console.error("Remove from favorites error:", error);
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)('Error', 'Failed to remove bucket from favorites.');
            }
            return;
        }
        if (args.item && args.item.text === "Download") {
            args.cancel = true;
            const currentPath = fileManagerRef.current.path || "/";
            const selectedItems = args.data || (fileManagerRef.current && fileManagerRef.current.selectedItems);
            if (!selectedItems || selectedItems.length === 0) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Information',
                    body: 'No file selected',
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: 'OK' })]
                });
                return;
            }
            const payloadObj = {
                action: "download",
                path: currentPath,
                downloadsFolder: downloadsFolder,
                client_type: clientType,
                names: selectedItems.map((item) => item.name || item),
                data: selectedItems.map((item) => {
                    if (typeof item === "string") {
                        return {
                            name: item,
                            isFile: true,
                            path: currentPath.endsWith("/")
                                ? currentPath + item
                                : currentPath + "/" + item,
                        };
                    }
                    else {
                        return item;
                    }
                }),
            };
            const payload = JSON.stringify(payloadObj);
            const formData = new URLSearchParams();
            formData.append("downloadInput", payload);
            await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('FileOperations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString(),
            })
                .then(async (data) => {
                await fetchHistory();
                startPolling();
                let savedPath;
                if (typeof data === 'string') {
                    savedPath = data;
                }
                else if (data.file_saved) {
                    savedPath = data.file_saved;
                }
                else {
                    savedPath = downloadsFolder;
                }
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Successful Operation',
                    body: `File saved in: ${savedPath}`,
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: 'OK' })]
                });
            })
                .catch((error) => {
                console.error("Download error:", error);
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)('Download Error', 'An error occurred while downloading the file.');
            });
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "control-section", style: { height: "100%", width: '100%' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.FileManagerComponent, { ref: fileManagerRef, id: "file", ajaxSettings: ajaxSettings, beforeSend: onBeforeSend.bind(undefined), toolbarSettings: {
                items: ['SortBy', 'Refresh'],
                visible: true,
            }, contextMenuSettings: {
                file: ['Download', '|', 'Details'],
                folder: props.folderOptions,
                layout: [],
                visible: true,
            }, detailsViewSettings: {
                columns: [
                    { field: "name", headerText: "Name", minWidth: 200, width: "auto" },
                    { field: "region", headerText: "Region", minWidth: 10, width: "auto" },
                    { field: "dateModified", headerText: "Modified", minWidth: 10, width: "auto" },
                    { field: "size", headerText: "Size", minWidth: 10, width: "auto" },
                ],
            }, view: "Details", allowMultiSelection: false, height: "100%", ...{ menuClick: contextMenuClickHandler } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.Inject, { services: [_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.DetailsView, _syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.Toolbar] }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FMViewComponent);


/***/ }),

/***/ "./lib/components/FileManagerPanelComponent.js":
/*!*****************************************************!*\
  !*** ./lib/components/FileManagerPanelComponent.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../contexts/DownloadHistoryContext */ "./lib/contexts/DownloadHistoryContext.js");
/* harmony import */ var _BasicTabs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./BasicTabs */ "./lib/components/BasicTabs.js");



const FileManagerPanelComponent = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { width: "100%", minWidth: "400px", height: "100vh" } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_contexts_DownloadHistoryContext__WEBPACK_IMPORTED_MODULE_1__.DownloadHistoryProvider, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_BasicTabs__WEBPACK_IMPORTED_MODULE_2__["default"], { downloadsFolder: props.downloadsFolder }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FileManagerPanelComponent);


/***/ }),

/***/ "./lib/contexts/DownloadHistoryContext.js":
/*!************************************************!*\
  !*** ./lib/contexts/DownloadHistoryContext.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DownloadHistoryProvider: () => (/* binding */ DownloadHistoryProvider),
/* harmony export */   useDownloadHistory: () => (/* binding */ useDownloadHistory)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");


const DownloadHistoryContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)(undefined);
const DownloadHistoryProvider = ({ children }) => {
    const [history, setHistory] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [pollInterval, setPollInterval] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(2000);
    const timerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const fetchHistory = async () => {
        setLoading(true);
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('download_history', {
                method: 'GET',
            });
            const historyData = data;
            setHistory(historyData);
            setLoading(false);
            return historyData;
        }
        catch (error) {
            console.error('Error fetching download history:', error);
            setLoading(false);
            return [];
        }
    };
    const pollHistory = async () => {
        await fetchHistory();
        const anyDownloading = history.some((item) => item.status === 'downloading');
        if (anyDownloading) {
            // Incremento geométrico del intervalo, hasta 30 segundos
            const newInterval = Math.min(pollInterval * 1.5, 30000);
            setPollInterval(newInterval);
            timerRef.current = window.setTimeout(pollHistory, newInterval);
        }
        else {
            if (timerRef.current) {
                clearTimeout(timerRef.current);
                timerRef.current = null;
            }
            setPollInterval(2000);
        }
    };
    const startPolling = () => {
        pollHistory();
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        // Opcionalmente, se puede iniciar el fetch inmediato al montar el provider:
        fetchHistory();
        return () => {
            if (timerRef.current) {
                clearTimeout(timerRef.current);
            }
        };
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(DownloadHistoryContext.Provider, { value: { history, loading, fetchHistory, startPolling } }, children));
};
const useDownloadHistory = () => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(DownloadHistoryContext);
    if (!context) {
        throw new Error('useDownloadHistory must be used within a DownloadHistoryProvider');
    }
    return context;
};


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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-bxplorer-v2', // API Namespace
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
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.a(module, async (__webpack_handle_async_dependencies__, __webpack_async_result__) => { try {
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widgets_FileManagerPanelWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets/FileManagerPanelWidget */ "./lib/widgets/FileManagerPanelWidget.js");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _syncfusion_ej2_base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @syncfusion/ej2-base */ "./node_modules/@syncfusion/ej2-base/index.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");






const config = (await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('config', {
    method: 'GET',
}));
(0,_syncfusion_ej2_base__WEBPACK_IMPORTED_MODULE_3__.registerLicense)(config.license);
const PLUGIN_ID = 'jupyterlab-bxplorer-v2:plugin';
async function activate(app, settingRegistry) {
    console.log('JupyterLab extension jupyterlab-bxplorer-v2 is activated!');
    let downloadsFolder = "";
    if (settingRegistry) {
        await settingRegistry
            .load(plugin.id)
            .then(settings => {
            console.log('jupyterlab-bxplorer-v2 settings loaded:', settings.composite);
            downloadsFolder = settings.get('download-folder').composite || "";
            console.log('downloadsFolder:', downloadsFolder);
        })
            .catch(reason => {
            console.error('Failed to load settings for jupyterlab-bxplorer-v2.', reason);
        });
    }
    const leftSideBarContent = new _widgets_FileManagerPanelWidget__WEBPACK_IMPORTED_MODULE_5__.FileManagerPanelWidget(downloadsFolder);
    const leftSideBarWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
        content: leftSideBarContent
    });
    leftSideBarWidget.id = 'filemanager-panel-widget';
    leftSideBarWidget.toolbar.hide();
    leftSideBarWidget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.runIcon;
    leftSideBarWidget.title.caption = 'File Manager';
    app.shell.add(leftSideBarWidget, 'left', { rank: 501 });
    const shell = app.shell;
    if (shell.leftCollapsed) {
        shell.expandLeft();
    }
}
const plugin = {
    id: PLUGIN_ID,
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);

__webpack_async_result__();
} catch(e) { __webpack_async_result__(e); } }, 1);

/***/ }),

/***/ "./lib/widgets/FileManagerPanelWidget.js":
/*!***********************************************!*\
  !*** ./lib/widgets/FileManagerPanelWidget.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FileManagerPanelWidget: () => (/* binding */ FileManagerPanelWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_FileManagerPanelComponent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/FileManagerPanelComponent */ "./lib/components/FileManagerPanelComponent.js");



class FileManagerPanelWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(downloadsFolder) {
        super();
        this.downloadsFolder = downloadsFolder;
        this.node.style.minWidth = '600px';
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: {
                width: '100%',
            } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_FileManagerPanelComponent__WEBPACK_IMPORTED_MODULE_2__["default"], { downloadsFolder: this.downloadsFolder })));
    }
    /**
     * It is triggered when the user activates this widget in the UI (click on the tab).
     */
    onAfterShow(msg) {
        super.onAfterShow(msg);
        window.dispatchEvent(new CustomEvent("filemanager-panel-open"));
    }
}


/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/Delete.js":
/*!********************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/Delete.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/esm/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6zM19 4h-3.5l-1-1h-5l-1 1H5v2h14z"
}), 'Delete'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/DeleteSweep.js":
/*!*************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/DeleteSweep.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/esm/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M15 16h4v2h-4zm0-8h7v2h-7zm0 4h6v2h-6zM3 18c0 1.1.9 2 2 2h6c1.1 0 2-.9 2-2V8H3zM14 5h-3l-1-1H6L5 5H2v2h12z"
}), 'DeleteSweep'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/Refresh.js":
/*!*********************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/Refresh.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/esm/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"
}), 'Refresh'));

/***/ })

}]);
//# sourceMappingURL=lib_index_js.6eacca905030db6be7eb.js.map