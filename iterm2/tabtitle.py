#!/usr/bin/env python3

import iterm2
import AppKit

# Launch the app
AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm2")

async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Foreground the app
    await app.async_activate()

    # Create a new tab or window
    myterm = app.current_terminal_window
    if not myterm:
        myterm = await iterm2.Window.async_create(connection)
    else:
        await myterm.async_create_tab()
    await myterm.async_activate()

    # Update the name and disable future updates by
    # control sequences.
    #
    # Changing the name this way is equivalent to
    # editing the Session Name field in
    # Session>Edit Session.
    session = myterm.current_tab.current_session
    update = iterm2.LocalWriteOnlyProfile()
    update.set_allow_title_setting(False)
    update.set_name("This is my customized session name")
    await session.async_set_profile_properties(update)

# Passing True for the second parameter means keep trying to
# connect until the app launches.
iterm2.run_until_complete(main, True)
