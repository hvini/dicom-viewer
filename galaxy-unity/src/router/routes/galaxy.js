const express = require('express');
const router = express.Router();
const path = require("path");

router.use('/Build/galaxy.framework.js.gz', (req, res) => {
    res.contentType('application/x-javascript');
    res.setHeader('Content-Encoding', 'gzip');
    res.sendFile(path.join(__basedir, '/public/galaxy/Build/galaxy.framework.js.gz'));
});

router.use('/Build/galaxy.data.gz', (req, res) => {
    res.contentType('application/x-javascript');
    res.setHeader('Content-Encoding', 'gzip');
    res.sendFile(path.join(__basedir, '/public/galaxy/Build/galaxy.data.gz'));
});

router.use('/Build/galaxy.wasm.gz', (req, res) => {
    res.contentType('application/wasm');
    res.setHeader('Content-Encoding', 'gzip');
    res.sendFile(path.join(__basedir, '/public/galaxy/Build/galaxy.wasm.gz'));
});
router.use('/', express.static(__basedir + '/public/galaxy'));

module.exports = router