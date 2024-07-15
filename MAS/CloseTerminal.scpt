tell application "Terminal"
    set all_windows to every window
    repeat with cur_window in all_windows
        if name of cur_window contains "USER" then
            tell cur_window
                do script "end" in selected tab
                delay 2
            end tell
        end if
    end repeat
    close every window
end tell
