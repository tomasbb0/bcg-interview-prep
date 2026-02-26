' ============================================================
' CV EDITOR MACROS
' For: TomásBatalha_Resume_12_2025_POLISHED.docx
' ============================================================

Option Explicit

' ------------------------------------------------------------
' ADD BULLET TO CURRENT JOB
' Place cursor in a job section, run this to add a bullet
' ------------------------------------------------------------
Sub AddBullet()
    Dim bulletText As String
    Dim currentPara As Paragraph
    Dim newPara As Paragraph
    
    ' Prompt for bullet text
    bulletText = InputBox("Enter bullet text:" & vbCrLf & vbCrLf & _
        "Tip: Start with action verb (Built, Led, Designed, etc.)", _
        "Add New Bullet")
    
    If bulletText = "" Then Exit Sub
    
    ' Get current paragraph
    Set currentPara = Selection.Paragraphs(1)
    
    ' Insert new paragraph after current one
    Selection.EndKey Unit:=wdLine
    Selection.TypeParagraph
    
    ' Apply bullet formatting
    With Selection
        .Range.ListFormat.ApplyBulletDefault
        .TypeText Text:=bulletText
        
        ' Match formatting (Arial, 9pt typical for CV)
        .Font.Name = "Arial"
        .Font.Size = 9
        .Font.Bold = False
    End With
    
    MsgBox "Bullet added!", vbInformation
End Sub

' ------------------------------------------------------------
' ADD NEW JOB TO SECTION
' Adds a new job at the TOP of Work Experience, Education, or Leadership
' ------------------------------------------------------------
Sub AddNewJob()
    Dim section As String
    Dim company As String
    Dim location As String
    Dim role As String
    Dim dates As String
    Dim sectionChoice As Integer
    
    ' Choose section
    sectionChoice = MsgBox("Add job to which section?" & vbCrLf & vbCrLf & _
        "YES = Work Experience" & vbCrLf & _
        "NO = Education" & vbCrLf & _
        "CANCEL = Leadership Experience", _
        vbYesNoCancel + vbQuestion, "Select Section")
    
    Select Case sectionChoice
        Case vbYes
            section = "WORK EXPERIENCE"
        Case vbNo
            section = "EDUCATION"
        Case vbCancel
            section = "LEADERSHIP EXPERIENCE"
        Case Else
            Exit Sub
    End Select
    
    ' Get job details
    company = InputBox("Company/Institution name:", "New Job - Company")
    If company = "" Then Exit Sub
    
    location = InputBox("Location (e.g., New York, USA):", "New Job - Location")
    If location = "" Then Exit Sub
    
    role = InputBox("Role/Title:", "New Job - Role")
    If role = "" Then Exit Sub
    
    dates = InputBox("Dates (e.g., January 2024 – Present):", "New Job - Dates")
    If dates = "" Then Exit Sub
    
    ' Find section header and insert after it
    Dim found As Boolean
    found = FindAndMoveTo(section)
    
    If Not found Then
        MsgBox "Could not find section: " & section, vbExclamation
        Exit Sub
    End If
    
    ' Move to end of header line, then insert new content
    Selection.EndKey Unit:=wdLine
    Selection.MoveDown Unit:=wdLine, Count:=1
    
    ' Insert company line
    Selection.TypeParagraph
    Selection.TypeText Text:=company & " | " & location
    Selection.Range.Font.Bold = True
    Selection.Range.Font.Name = "Arial"
    Selection.Range.Font.Size = 10
    
    ' Insert role line
    Selection.TypeParagraph
    Selection.TypeText Text:=role & " | " & dates
    Selection.Range.Font.Bold = False
    Selection.Range.Font.Italic = True
    Selection.Range.Font.Name = "Arial"
    Selection.Range.Font.Size = 9
    
    ' Add placeholder bullet
    Selection.TypeParagraph
    Selection.Range.ListFormat.ApplyBulletDefault
    Selection.TypeText Text:="[Add your first bullet here]"
    Selection.Range.Font.Italic = False
    Selection.Range.Font.Name = "Arial"
    Selection.Range.Font.Size = 9
    
    MsgBox "New job added to " & section & "!" & vbCrLf & vbCrLf & _
        "Don't forget to:" & vbCrLf & _
        "1. Replace placeholder bullet" & vbCrLf & _
        "2. Add more bullets with AddBullet macro", vbInformation
End Sub

' ------------------------------------------------------------
' HELPER: Find text and move cursor there
' ------------------------------------------------------------
Private Function FindAndMoveTo(searchText As String) As Boolean
    With Selection.Find
        .ClearFormatting
        .Text = searchText
        .Forward = True
        .Wrap = wdFindContinue
        .Format = False
        .MatchCase = False
        .MatchWholeWord = False
        FindAndMoveTo = .Execute
    End With
End Function

' ------------------------------------------------------------
' QUICK ADD: Just add bullet text at cursor
' Simpler version - just types bullet without prompts
' ------------------------------------------------------------
Sub QuickBullet()
    Selection.Range.ListFormat.ApplyBulletDefault
    Selection.Font.Name = "Arial"
    Selection.Font.Size = 9
    Selection.Font.Bold = False
End Sub

' ------------------------------------------------------------
' FORMAT SELECTION AS COMPANY HEADER
' Select text, run this to format as company name
' ------------------------------------------------------------
Sub FormatAsCompany()
    With Selection.Font
        .Name = "Arial"
        .Size = 10
        .Bold = True
        .Italic = False
    End With
End Sub

' ------------------------------------------------------------
' FORMAT SELECTION AS ROLE/DATE
' Select text, run this to format as role line
' ------------------------------------------------------------
Sub FormatAsRole()
    With Selection.Font
        .Name = "Arial"
        .Size = 9
        .Bold = False
        .Italic = True
    End With
End Sub

' ------------------------------------------------------------
' FORMAT SELECTION AS BULLET TEXT
' Select text, run this to format as bullet content
' ------------------------------------------------------------
Sub FormatAsBullet()
    With Selection.Font
        .Name = "Arial"
        .Size = 9
        .Bold = False
        .Italic = False
    End With
End Sub
