tell application "Terminal"
    set all_windows to every window
    repeat with cur_window in all_windows
        if name of cur_window contains "USER" then
            tell cur_window
                do script "end" in selected tab
                delay 2
            end tell
        end if
        if name of cur_window does not contain "MAS.command" then
            set tempID to id of cur_window
            tell the window id tempID to close
        end if
    end repeat
end tell
