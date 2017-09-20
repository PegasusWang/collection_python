#!/usr/bin/env bash

# 监控文件变化然后刷新浏览器
# brew install fswatch

fswatch -o ./templates | xargs -n1 -I {} osascript -e 'tell application "Google Chrome" to tell the active tab of its first window to reload'
