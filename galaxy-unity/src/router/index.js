const express = require('express');
const appRouter = express.Router();
const galaxyRoutes = require('./routes/galaxy');
const webxrRoutes = require('./routes/webxr');
const cors = require('cors');

appRouter.use(cors());

appRouter.use('/galaxy', galaxyRoutes);
appRouter.use('/webxr', webxrRoutes);

module.exports = appRouter;