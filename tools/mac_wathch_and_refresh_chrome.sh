#!/usr/bin/env bash

# 监控文件变化然后刷新浏览器
# alias watch_refresh_chrome=" when-changed -v -r -1 -s ./ osascript -e 'tell application \"Google Chrome\" to tell the active tab of its first window to reload' "

fswatch -o ./templates | xargs -n1 -I {} osascript -e 'tell application "Google Chrome" to tell the active tab of its first window to reload'
