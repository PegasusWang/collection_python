#!/usr/bin/env python3.7

"""
https://superuser.com/questions/1068105/iterm2-os-x-change-background-image-for-current-window-from-shell
https://github.com/gnachman/iTerm2/blob/master/api/library/python/iterm2/iterm2/profile.py
"""

import asyncio
import random
import iterm2

async def main(connection):
    """修改背景图"""
    while True:
        images = [
            '/Users/pegasus/Pictures/壁纸/低头.jpg',
            '/Users/pegasus/Pictures/壁纸/后背.jpg',
            '/Users/pegasus/Pictures/壁纸/双枪.jpg',
            '/Users/pegasus/Pictures/壁纸/射箭.jpg',
        ]
        image_path = random.choice(images)
        app = await iterm2.async_get_app(connection)
        session=app.current_terminal_window.current_tab.current_session
        profile=await session.async_get_profile()
        await profile.async_set_background_image_location(image_path)

        await asyncio.sleep(1)

# iterm2.run_forever(main)
iterm2.run_until_complete(main)
