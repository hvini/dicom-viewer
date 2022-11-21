const express = require('express');
const router = express.Router();
const path = require("path");

router.use('/Build/webxr.framework.js.gz', (req, res) => {
    res.contentType('application/x-javascript');
    res.setHeader('Content-Encoding', 'gzip');
    res.sendFile(path.join(__basedir, '/public/webxr/Build/webxr.framework.js.gz'));
});

router.use('/Build/webxr.data.gz', (req, res) => {
    res.contentType('application/x-javascript');
    res.setHeader('Content-Encoding', 'gzip');
    res.sendFile(path.join(__basedir, '/public/webxr/Build/webxr.data.gz'));
});

router.use('/Build/webxr.wasm.gz', (req, res) => {
    res.contentType('application/wasm');
    res.setHeader('Content-Encoding', 'gzip');
    res.sendFile(path.join(__basedir, '/public/webxr/Build/webxr.wasm.gz'));
});
router.use('/', express.static(__basedir + '/public/webxr'));

module.exports = router