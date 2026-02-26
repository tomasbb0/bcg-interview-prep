' ============================================================
' DIAGNOSTIC TEST MACRO
' Paste this into Word VBA editor (Tools > Macro > Visual Basic Editor)
' Then run: Tools > Macro > Macros > TestMacro > Run
'
' Expected behavior: 
'   1. A message box should appear saying "VBA WORKS!"
'   2. After clicking OK, another box shows document info
'   3. After clicking OK, tries InputBox (same as CV Editor uses)
'
' If NOTHING happens: VBA is completely blocked on your Mac
' If step 1 works but 2 or 3 fails: partial compatibility issue
' ============================================================

Sub TestMacro()
    ' Step 1: Basic message box
    MsgBox "VBA WORKS! Step 1 of 3 passed.", vbInformation, "Test"
    
    ' Step 2: Document info
    Dim info As String
    info = "Document: " & ActiveDocument.Name & vbCrLf
    info = info & "Tables: " & ActiveDocument.Tables.Count & vbCrLf
    info = info & "Paragraphs: " & ActiveDocument.Paragraphs.Count
    MsgBox info, vbInformation, "Document Info (Step 2)"
    
    ' Step 3: InputBox (same as CVEditor uses)
    Dim result As String
    result = InputBox("Type anything and click OK to confirm InputBox works:", "InputBox Test (Step 3)")
    
    If result = "" Then
        MsgBox "You cancelled or typed nothing. InputBox works but returned empty.", vbInformation, "Step 3 Result"
    Else
        MsgBox "InputBox returned: " & result & vbCrLf & vbCrLf & "ALL 3 STEPS PASSED!", vbInformation, "Step 3 Result"
    End If
End Sub

' Quick test for the RIBBON buttons
Sub TestRibbon()
    MsgBox "RIBBON button connected successfully!", vbInformation, "Ribbon Test"
End Sub
