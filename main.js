const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

app.on('ready', function() {
  // call python?
  var subpy = require('child_process').spawn('/Users/riteshkadmawala/.virtualenvs/irctc-bot/bin/python', ['./irctc.py']);
});
