@echo off
title YouTube 音视频合并 20140127
echo 作者：Crexyer
echo 网站：http://www.crexyer.com/
echo.
set /p audio=请将【音频】文件拖拽到此处，按下回车确认：
set /p video=请将【视频】文件拖拽到此处，按下回车确认：
ffmpeg.exe -i %audio% -i %video% -acodec copy -vcodec copy output.mp4
echo.
echo 合并结束！
echo 文件已经输出到本地的 output.mp4 文件。
pause