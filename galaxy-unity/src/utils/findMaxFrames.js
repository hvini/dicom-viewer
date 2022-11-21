const split2 = require('split2');
const fs = require('fs');
const { once } = require('events');
const path = require('path');

require('dotenv').config({
    path: path.join(__basedir, `./.env.${process.env.NODE_ENV}`)
});

module.exports = {
    /**
     * Find the maximum number of frames in the galaxy
     * @returns {Promise<number>} The maximum number of frames in the galaxy or null if could not find it
     */
    FindMaxFrames: async function () {
        const stream = fs.createReadStream(process.env.PERSONAVARS_LOCATION);
        const lineReader = stream.pipe(split2());

        let result = null;
        lineReader.on('data', async function (line) {
            const [key, value] = line.split('=').map(item => item.trim());
            if (key === 'DHCP_LG_FRAMES_MAX') {
                result = value;
                stream.destroy();
            }
        });

        await once(stream, 'close');
        return result;
    }
}