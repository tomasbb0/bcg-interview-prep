-- CVEditorDialogs.applescript
-- Handlers called from Word VBA via AppleScriptTask
-- Ensures dialogs appear on the CURRENT active screen

on ActivateWord(ignored)
	tell application "Microsoft Word"
		activate
	end tell
	delay 0.1
	return "OK"
end ActivateWord

on ShowInputBox(thePrompt)
	tell application "Microsoft Word" to activate
	try
		display dialog thePrompt default answer "" with title "CV Editor"
		return text returned of result
	on error
		return ""
	end try
end ShowInputBox

on ShowAlert(theMessage)
	tell application "Microsoft Word" to activate
	display dialog theMessage with title "CV Editor" buttons {"OK"} default button "OK"
	return "OK"
end ShowAlert
