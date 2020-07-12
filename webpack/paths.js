const path = require('path');

const baseDir       = path.resolve();
const baseOutputDir = path.join(baseDir, 'website', 'static');
const baseInputDir  = path.join(baseDir, 'website', 'assets');

module.exports = {
    baseDir:        baseDir,
    baseOutputDir:  baseOutputDir,
    baseInputDir:   baseInputDir,
    localOutputDir: path.join(baseOutputDir, 'local'),
    distOutputDir:  path.join(baseOutputDir, 'dist')
}
