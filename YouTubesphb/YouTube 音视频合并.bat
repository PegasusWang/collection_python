@echo off
title YouTube ����Ƶ�ϲ� 20140127
echo ���ߣ�Crexyer
echo ��վ��http://www.crexyer.com/
echo.
set /p audio=�뽫����Ƶ���ļ���ק���˴������»س�ȷ�ϣ�
set /p video=�뽫����Ƶ���ļ���ק���˴������»س�ȷ�ϣ�
ffmpeg.exe -i %audio% -i %video% -acodec copy -vcodec copy output.mp4
echo.
echo �ϲ�������
echo �ļ��Ѿ���������ص� output.mp4 �ļ���
pause