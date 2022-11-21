const express = require('express');
const app = express();
const appRouter = require('./router/index');

app.use(appRouter);

module.exports = app;