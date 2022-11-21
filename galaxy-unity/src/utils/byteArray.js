module.exports = {
    /**
     * Converts a string to a byte array
     * @param {String} str String to be converted
     * @returns {Array<Array>} String byte array
     */
    ByteArray: function (str) {
        const byteArray = [];
        const buffer = Buffer.from(str, 'utf8');
        for (var i = 0; i < buffer.length; i++) {
            byteArray.push(buffer[i]);
        }
        return byteArray;
    }
}