' ============================================================
' CV EDITOR - COMPLETE MENU SYSTEM v2
' For: TomásBatalha Resume (table-based, nested tables)
' ============================================================
'
' INSTALLATION (Mac Word):
'   1. Open your CV .docm in Word
'   2. Tools > Macro > Visual Basic Editor
'   3. In left panel: find & double-click the existing "Module1"
'      (or right-click project > Insert > Module)
'   4. DELETE all old code, paste ALL of this code
'   5. Save (Cmd+S), close VBA editor
'   6. Your existing toolbar buttons will call these updated macros
'
' If buttons still don't work:
'   - Check Tools > Macro > Security > "Enable all macros"
'   - Or run CVEditor directly: Tools > Macro > Macros > CVEditor > Run
'
' ============================================================

Option Explicit

' ============================
' FORMATTING CONSTANTS
' These match your actual CV
' ============================
Private Const CV_FONT As String = "Arial"
Private Const CV_BODY_SIZE As Single = 7.5     ' Body text / bullets
Private Const CV_HEADER_SIZE As Single = 9     ' Section headers (WORK EXPERIENCE, etc.)
Private Const CV_TITLE_SIZE As Single = 11     ' Name at top

' Section headers exactly as in your CV
Private Const SEC_1 As String = "WORK EXPERIENCE"
Private Const SEC_2 As String = "EDUCATION"
Private Const SEC_3 As String = "LEADERSHIP EXPERIENCE"
Private Const SEC_4 As String = "SKILLS"

' Module-level variables for scan results (must be at top on Mac)
Dim gSections() As String
Dim gSectionCount As Integer
Dim gJobCompany() As String
Dim gJobRole() As String
Dim gJobSection() As String
Dim gJobStartPos() As Long
Dim gJobEndPos() As Long
Dim gJobCount As Integer

' ============================================================
' HELPER: Move Word window to primary screen
' Fixes dialogs appearing on disconnected external monitor
' ============================================================
Private Sub ForceWindowToPrimaryScreen()
    On Error Resume Next
    ' Use AppleScript to properly activate Word on macOS
    ' This forces dialogs to appear on the CURRENT screen (fixes dual-monitor issue)
    #If Mac Then
        AppleScriptTask "CVEditorDialogs", "ActivateWord", ""
    #End If
    Application.Activate
    DoEvents
    On Error GoTo 0
End Sub

' ============================================================
' MAIN MENU - Entry point
' ============================================================
Sub CVEditor()
    On Error GoTo ErrHandler
    
    ' Force Word window onto primary screen (fixes dialogs appearing on disconnected monitor)
    ForceWindowToPrimaryScreen
    
    Dim choice As Integer
    
    Do
        choice = ShowMainMenu()
        
        Select Case choice
            Case 1: AddBulletMenu
            Case 2: AddJobMenu
            Case 3: DeleteBulletMenu
            Case 4: DeleteJobMenu
            Case 5: SwapBulletMenu
            Case 6: SwapJobMenu
            Case 7: SwapSectionMenu
            Case 8: DatabaseMenu
            Case 9: ResizeCVMenu
            Case 10: ViewStructure
            Case 0: Exit Do
        End Select
    Loop
    Exit Sub
    
ErrHandler:
    MsgBox "Error in CVEditor: " & Err.Description & vbCrLf & _
           "Error #" & Err.Number, vbExclamation, "CV Editor Error"
End Sub

Private Function ShowMainMenu() As Integer
    ForceWindowToPrimaryScreen
    Dim msg As String
    
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "       CV EDITOR MENU" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "1. Add Bullet" & vbCrLf
    msg = msg & "2. Add New Job" & vbCrLf
    msg = msg & "3. Delete Bullet" & vbCrLf
    msg = msg & "4. Delete Job" & vbCrLf
    msg = msg & "5. Swap Bullet" & vbCrLf
    msg = msg & "6. Swap Job" & vbCrLf
    msg = msg & "7. Swap Section" & vbCrLf
    msg = msg & "8. Database" & vbCrLf
    msg = msg & "9. Resize CV" & vbCrLf
    msg = msg & "10. View Structure" & vbCrLf & vbCrLf
    msg = msg & "0. Exit" & vbCrLf & vbCrLf
    msg = msg & "Enter choice (0-10):"
    
    Dim result As String
    result = InputBox(msg, "CV Editor")
    
    If result = "" Then
        ShowMainMenu = 0
    Else
        ShowMainMenu = Val(result)
    End If
End Function


' ============================================================
' SECTION & JOB SCANNING (Table-Aware)
' ============================================================

Private Sub ScanDocument()
    ' Builds a complete map of sections and jobs by scanning ALL paragraphs.
    ' This approach works with any table nesting and avoids Mac VBA errors
    ' on horizontal lines and nested tables.
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' --- Find sections ---
    gSectionCount = 0
    ReDim gSections(1 To 10)
    
    Dim sectionNames As Variant
    sectionNames = Array(SEC_1, SEC_2, SEC_3, SEC_4)
    
    Dim i As Integer
    For i = LBound(sectionNames) To UBound(sectionNames)
        Dim rng As Range
        Set rng = doc.Content
        With rng.Find
            .Text = CStr(sectionNames(i))
            .MatchCase = False
            .MatchWholeWord = False
            If .Execute Then
                gSectionCount = gSectionCount + 1
                gSections(gSectionCount) = CStr(sectionNames(i))
            End If
        End With
    Next i
    
    If gSectionCount > 0 Then
        ReDim Preserve gSections(1 To gSectionCount)
    End If
    
    ' --- Find jobs by scanning ALL paragraphs for "Company | Location" ---
    gJobCount = 0
    ReDim gJobCompany(1 To 50)
    ReDim gJobRole(1 To 50)
    ReDim gJobSection(1 To 50)
    ReDim gJobStartPos(1 To 50)
    ReDim gJobEndPos(1 To 50)
    
    Dim currentSection As String
    currentSection = ""
    
    Dim seenCompanies As String
    seenCompanies = "|"  ' Track already-found companies to avoid duplicates from nested tables
    
    Dim p As Integer
    Dim totalParas As Integer
    totalParas = doc.Paragraphs.Count
    
    For p = 1 To totalParas
        On Error Resume Next
        Dim paraText As String
        paraText = ""
        paraText = CleanCellText(doc.Paragraphs(p).Range.Text)
        If Err.Number <> 0 Then
            Err.Clear
            GoTo NextPara
        End If
        On Error GoTo 0
        
        If Len(paraText) < 3 Then GoTo NextPara
        
        ' Check for section headers
        Dim s As Integer
        For s = 1 To gSectionCount
            If UCase(paraText) = gSections(s) Then
                currentSection = gSections(s)
            End If
        Next s
        
        ' Check for company lines: has " | ", not too long, and we're past the header
        ' Skip lines before any section header (e.g. contact info at top)
        If InStr(paraText, " | ") > 0 And Len(paraText) < 120 And currentSection <> "" Then
            ' Check if this is a role line (contains dates)
            Dim isRole As Boolean
            isRole = (InStr(paraText, "January") > 0 Or InStr(paraText, "February") > 0 Or _
                      InStr(paraText, "March") > 0 Or InStr(paraText, "April") > 0 Or _
                      InStr(paraText, "May 2") > 0 Or InStr(paraText, "June") > 0 Or _
                      InStr(paraText, "July") > 0 Or InStr(paraText, "August") > 0 Or _
                      InStr(paraText, "September") > 0 Or InStr(paraText, "October") > 0 Or _
                      InStr(paraText, "November") > 0 Or InStr(paraText, "December") > 0 Or _
                      InStr(paraText, "Present") > 0 Or _
                      InStr(paraText, "Jan 2") > 0 Or InStr(paraText, "Feb 2") > 0 Or _
                      InStr(paraText, "Mar 2") > 0 Or InStr(paraText, "Apr 2") > 0 Or _
                      InStr(paraText, "Sep 2") > 0 Or InStr(paraText, "Oct 2") > 0 Or _
                      InStr(paraText, "Nov 2") > 0 Or InStr(paraText, "Dec 2") > 0)
            
            If Not isRole Then
                ' Skip duplicates (nested tables cause same text to appear twice)
                If InStr(seenCompanies, "|" & paraText & "|") = 0 Then
                    seenCompanies = seenCompanies & paraText & "|"
                    
                    gJobCount = gJobCount + 1
                    gJobCompany(gJobCount) = paraText
                    gJobSection(gJobCount) = currentSection
                    gJobStartPos(gJobCount) = doc.Paragraphs(p).Range.Start
                    
                    ' Look for role in next paragraph
                    Dim roleText As String
                    roleText = ""
                    If p < totalParas Then
                        On Error Resume Next
                        roleText = CleanCellText(doc.Paragraphs(p + 1).Range.Text)
                        If Err.Number <> 0 Then
                            Err.Clear
                            roleText = ""
                        End If
                        On Error GoTo 0
                    End If
                    gJobRole(gJobCount) = roleText
                End If
            End If
        End If
NextPara:
    Next p
    
    ' Calculate end positions (each job ends where the next job starts)
    Dim j As Integer
    For j = 1 To gJobCount
        If j < gJobCount Then
            gJobEndPos(j) = gJobStartPos(j + 1) - 1
        Else
            gJobEndPos(j) = doc.Content.End
        End If
    Next j
    
    If gJobCount > 0 Then
        ReDim Preserve gJobCompany(1 To gJobCount)
        ReDim Preserve gJobRole(1 To gJobCount)
        ReDim Preserve gJobSection(1 To gJobCount)
        ReDim Preserve gJobStartPos(1 To gJobCount)
        ReDim Preserve gJobEndPos(1 To gJobCount)
    End If
End Sub

Private Function CleanCellText(s As String) As String
    Dim result As String
    result = s
    result = Replace(result, Chr(13), "")
    result = Replace(result, Chr(7), "")
    result = Replace(result, Chr(11), "")
    result = Replace(result, vbCr, "")
    result = Replace(result, vbLf, "")
    CleanCellText = Trim(result)
End Function


' ============================================================
' SELECT SECTION DIALOG
' ============================================================
Private Function SelectSection(title As String) As String
    ScanDocument
    
    If gSectionCount = 0 Then
        MsgBox "No sections found in document!" & vbCrLf & vbCrLf & _
               "Make sure the document contains headers like:" & vbCrLf & _
               "WORK EXPERIENCE, EDUCATION, etc.", vbExclamation, "Error"
        SelectSection = ""
        Exit Function
    End If
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    " & title & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Found " & gSectionCount & " sections:" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To gSectionCount
        msg = msg & "  " & i & ". " & gSections(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter section number (or 0 to cancel):"
    
    Dim result As String
    result = InputBox(msg, title)
    
    If result = "" Or Val(result) = 0 Then
        SelectSection = ""
    ElseIf Val(result) >= 1 And Val(result) <= gSectionCount Then
        SelectSection = gSections(Val(result))
    Else
        MsgBox "Invalid selection", vbExclamation
        SelectSection = ""
    End If
End Function


' ============================================================
' SELECT JOB DIALOG
' ============================================================
Private Function SelectJob(title As String, Optional limitSection As String = "") As Integer
    ' Returns job index (1-based) or 0 if cancelled
    ScanDocument
    
    If gJobCount = 0 Then
        MsgBox "No jobs found in document!", vbExclamation
        SelectJob = 0
        Exit Function
    End If
    
    ' Build filtered list
    Dim validJobs() As Integer
    ReDim validJobs(1 To gJobCount)
    Dim validCount As Integer
    validCount = 0
    
    Dim i As Integer
    For i = 1 To gJobCount
        If limitSection = "" Or gJobSection(i) = limitSection Then
            validCount = validCount + 1
            validJobs(validCount) = i
        End If
    Next i
    
    If validCount = 0 Then
        MsgBox "No jobs found" & IIf(limitSection <> "", " in " & limitSection, "") & "!", vbExclamation
        SelectJob = 0
        Exit Function
    End If
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    " & title & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    Dim lastSec As String
    lastSec = ""
    
    For i = 1 To validCount
        Dim ji As Integer
        ji = validJobs(i)
        
        If gJobSection(ji) <> lastSec Then
            msg = msg & vbCrLf & "  " & gJobSection(ji) & ":" & vbCrLf
            lastSec = gJobSection(ji)
        End If
        
        msg = msg & "    " & i & ". " & Left(gJobCompany(ji), 55) & vbCrLf
        If gJobRole(ji) <> "" Then
            msg = msg & "       " & Left(gJobRole(ji), 55) & vbCrLf
        End If
    Next i
    
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, title)
    
    If result = "" Or Val(result) = 0 Or Val(result) > validCount Then
        SelectJob = 0
    Else
        SelectJob = validJobs(Val(result))
    End If
End Function


' ============================================================
' GET BULLETS FOR A JOB
' Returns collection of "text||paraStart||paraEnd"
' ============================================================
Private Function GetBulletsForJob(jobIdx As Integer) As Collection
    Dim bullets As New Collection
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Use stored start/end positions
    Dim startPos As Long
    Dim endPos As Long
    startPos = gJobStartPos(jobIdx)
    endPos = gJobEndPos(jobIdx)
    
    ' Scan paragraphs in range for bullets
    On Error Resume Next
    Dim searchRange As Range
    Set searchRange = doc.Range(startPos, endPos)
    If Err.Number <> 0 Then
        Err.Clear
        On Error GoTo 0
        Set GetBulletsForJob = bullets
        Exit Function
    End If
    On Error GoTo 0
    
    Dim para As Paragraph
    For Each para In searchRange.Paragraphs
        On Error Resume Next
        Dim listType As Long
        listType = wdListNoNumbering
        listType = para.Range.ListFormat.ListType
        If Err.Number <> 0 Then
            Err.Clear
            GoTo NextBulletPara
        End If
        On Error GoTo 0
        
        If listType <> wdListNoNumbering Then
            Dim bText As String
            bText = CleanCellText(para.Range.Text)
            If Len(bText) > 3 Then
                bullets.Add bText & "||" & CStr(para.Range.Start) & "||" & CStr(para.Range.End)
            End If
        End If
NextBulletPara:
    Next para
    
    Set GetBulletsForJob = bullets
End Function


' ============================================================
' SELECT BULLET DIALOG
' ============================================================
Private Function SelectBulletFromJob(jobIdx As Integer, title As String) As String
    Dim bullets As Collection
    Set bullets = GetBulletsForJob(jobIdx)
    
    If bullets.Count = 0 Then
        MsgBox "No bullets found for this job!" & vbCrLf & vbCrLf & _
               "Job: " & gJobCompany(jobIdx), vbExclamation
        SelectBulletFromJob = ""
        Exit Function
    End If
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    " & title & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Job: " & gJobCompany(jobIdx) & vbCrLf
    msg = msg & "Bullets:" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To bullets.Count
        Dim parts() As String
        parts = Split(bullets(i), "||")
        ' Show truncated text
        Dim displayText As String
        displayText = Left(parts(0), 75)
        If Len(parts(0)) > 75 Then displayText = displayText & "..."
        msg = msg & "  " & i & ". " & displayText & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, title)
    
    If result = "" Or Val(result) = 0 Or Val(result) > bullets.Count Then
        SelectBulletFromJob = ""
    Else
        SelectBulletFromJob = bullets(Val(result))
    End If
End Function


' ============================================================
' ADD BULLET MENU
' ============================================================
Sub AddBulletMenu()
    On Error GoTo ErrHandler
    
    ' Select job
    Dim jobIdx As Integer
    jobIdx = SelectJob("ADD BULLET - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    ' Get bullet text
    Dim msg As String
    msg = "Add bullet to: " & gJobCompany(jobIdx) & vbCrLf & vbCrLf
    msg = msg & "TIPS:" & vbCrLf
    msg = msg & "- Start with action verb" & vbCrLf
    msg = msg & "- Include numbers/metrics" & vbCrLf
    msg = msg & "- Keep under ~140 chars for 1 line" & vbCrLf & vbCrLf
    msg = msg & "ACTION VERBS:" & vbCrLf
    msg = msg & "Built, Led, Designed, Secured," & vbCrLf
    msg = msg & "Developed, Launched, Managed," & vbCrLf
    msg = msg & "Increased, Reduced, Created" & vbCrLf & vbCrLf
    msg = msg & "Enter bullet text:"
    
    Dim bulletText As String
    bulletText = InputBox(msg, "Add Bullet")
    If bulletText = "" Then Exit Sub
    
    ' Find the last bullet for this job and insert after it
    Dim bullets As Collection
    Set bullets = GetBulletsForJob(jobIdx)
    
    If bullets.Count > 0 Then
        Dim lastBullet As String
        lastBullet = bullets(bullets.Count)
        Dim parts() As String
        parts = Split(lastBullet, "||")
        
        Dim paraEnd As Long
        paraEnd = CLng(parts(2))
        
        ' Position at end of last bullet (before paragraph mark)
        Dim rng As Range
        Set rng = ActiveDocument.Range(paraEnd - 1, paraEnd - 1)
        rng.Select
        
        ' Insert new paragraph and text
        Selection.EndKey Unit:=wdLine
        Selection.TypeParagraph
        Selection.TypeText Text:=bulletText
        
        ' Apply formatting
        With Selection.Font
            .Name = CV_FONT
            .Size = CV_BODY_SIZE
            .Bold = False
        End With
        
        ' Apply dash bullet format (matching CV's existing dash style)
        ' First remove any default bullet
        Selection.Paragraphs(1).Range.ListFormat.RemoveNumbers
        
        ' Copy list format from an existing bullet in same job
        Dim existingBullet As String
        existingBullet = bullets(1)
        Dim eParts() As String
        eParts = Split(existingBullet, "||")
        Dim srcRange As Range
        Set srcRange = ActiveDocument.Range(CLng(eParts(1)), CLng(eParts(2)))
        
        ' Apply the same list template
        Dim lt As ListTemplate
        Set lt = srcRange.ListFormat.ListTemplate
        If Not lt Is Nothing Then
            Selection.Paragraphs(1).Range.ListFormat.ApplyListTemplate ListTemplate:=lt
        End If
        
        MsgBox "Bullet added to " & gJobCompany(jobIdx) & "!", vbInformation, "Success"
    Else
        MsgBox "No existing bullets found to insert after." & vbCrLf & vbCrLf & _
               "Please place cursor after the role line and" & vbCrLf & _
               "type your bullet manually.", vbExclamation
    End If
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Add Bullet Error"
End Sub


' ============================================================
' ADD JOB MENU (placeholder - complex due to table structure)
' ============================================================
Sub AddJobMenu()
    MsgBox "ADD NEW JOB" & vbCrLf & vbCrLf & _
           "Due to the table-based structure of your CV," & vbCrLf & _
           "adding a new job requires careful table manipulation." & vbCrLf & vbCrLf & _
           "Recommended approach:" & vbCrLf & _
           "1. Copy an existing job's row in the table" & vbCrLf & _
           "2. Paste it where you want the new job" & vbCrLf & _
           "3. Edit the company, role, dates, and bullets" & vbCrLf & vbCrLf & _
           "Or use the Python script for automated changes.", _
           vbInformation, "Add Job"
End Sub


' ============================================================
' DELETE BULLET MENU
' ============================================================
Sub DeleteBulletMenu()
    On Error GoTo ErrHandler
    
    ' Select job
    Dim jobIdx As Integer
    jobIdx = SelectJob("DELETE BULLET - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    ' Select bullet
    Dim bulletEntry As String
    bulletEntry = SelectBulletFromJob(jobIdx, "DELETE BULLET")
    If bulletEntry = "" Then Exit Sub
    
    ' Confirm
    Dim parts() As String
    parts = Split(bulletEntry, "||")
    
    If MsgBox("Delete this bullet?" & vbCrLf & vbCrLf & _
              Left(parts(0), 100) & IIf(Len(parts(0)) > 100, "...", ""), _
              vbYesNo + vbQuestion, "Confirm Delete") = vbNo Then
        Exit Sub
    End If
    
    ' Delete the paragraph
    Dim paraStart As Long
    Dim paraEnd As Long
    paraStart = CLng(parts(1))
    paraEnd = CLng(parts(2))
    
    Dim rng As Range
    Set rng = ActiveDocument.Range(paraStart, paraEnd)
    rng.Delete
    
    MsgBox "Bullet deleted!", vbInformation, "Success"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Delete Bullet Error"
End Sub


' ============================================================
' DELETE JOB MENU (placeholder)
' ============================================================
Sub DeleteJobMenu()
    On Error GoTo ErrHandler
    
    Dim jobIdx As Integer
    jobIdx = SelectJob("DELETE JOB - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    If MsgBox("Delete entire job?" & vbCrLf & vbCrLf & _
              gJobCompany(jobIdx) & vbCrLf & _
              gJobRole(jobIdx) & vbCrLf & vbCrLf & _
              "WARNING: This will delete the company header," & vbCrLf & _
              "role line, and ALL bullets for this job." & vbCrLf & vbCrLf & _
              "This cannot be undone (Cmd+Z to undo).", _
              vbYesNo + vbExclamation, "Confirm Delete Job") = vbNo Then
        Exit Sub
    End If
    
    ' Delete the range from this job to next job using stored positions
    Dim deleteRange As Range
    Set deleteRange = ActiveDocument.Range(gJobStartPos(jobIdx), gJobEndPos(jobIdx))
    deleteRange.Delete
    
    MsgBox "Job deleted! Use Cmd+Z to undo if needed.", vbInformation, "Success"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Delete Job Error"
End Sub


' ============================================================
' SWAP BULLET MENU
' ============================================================
Sub SwapBulletMenu()
    On Error GoTo ErrHandler
    
    Dim jobIdx As Integer
    jobIdx = SelectJob("SWAP BULLETS - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    Dim bullets As Collection
    Set bullets = GetBulletsForJob(jobIdx)
    
    If bullets.Count < 2 Then
        MsgBox "Need at least 2 bullets to swap!", vbExclamation
        Exit Sub
    End If
    
    ' Show bullets
    Dim msg As String
    msg = "SWAP BULLETS" & vbCrLf & vbCrLf
    msg = msg & "Job: " & gJobCompany(jobIdx) & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To bullets.Count
        Dim parts() As String
        parts = Split(bullets(i), "||")
        msg = msg & i & ". " & Left(parts(0), 70) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter FIRST bullet number to swap:"
    
    Dim first As String
    first = InputBox(msg, "Swap Bullet 1")
    If first = "" Or Val(first) < 1 Or Val(first) > bullets.Count Then Exit Sub
    
    Dim second As String
    second = InputBox("Enter SECOND bullet number to swap with #" & first & ":", "Swap Bullet 2")
    If second = "" Or Val(second) < 1 Or Val(second) > bullets.Count Then Exit Sub
    If Val(first) = Val(second) Then Exit Sub
    
    ' Get the two bullets
    Dim p1() As String, p2() As String
    p1 = Split(bullets(Val(first)), "||")
    p2 = Split(bullets(Val(second)), "||")
    
    ' Swap texts using Range
    Dim rng1 As Range, rng2 As Range
    Set rng1 = ActiveDocument.Range(CLng(p1(1)), CLng(p1(2)) - 1) ' -1 for para mark
    Set rng2 = ActiveDocument.Range(CLng(p2(1)), CLng(p2(2)) - 1)
    
    Dim text1 As String, text2 As String
    text1 = rng1.Text
    text2 = rng2.Text
    
    ' Do the swap (swap text 2 first since it's later in doc, won't shift positions of text 1)
    If CLng(p1(1)) < CLng(p2(1)) Then
        rng2.Text = text1
        Set rng1 = ActiveDocument.Range(CLng(p1(1)), CLng(p1(1)) + Len(text1))
        rng1.Text = text2
    Else
        rng1.Text = text2
        Set rng2 = ActiveDocument.Range(CLng(p2(1)), CLng(p2(1)) + Len(text2))
        rng2.Text = text1
    End If
    
    MsgBox "Bullets swapped!", vbInformation, "Success"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Swap Bullet Error"
End Sub


' ============================================================
' SWAP JOB MENU (placeholder)
' ============================================================
Sub SwapJobMenu()
    MsgBox "SWAP JOBS" & vbCrLf & vbCrLf & _
           "Swapping entire jobs in a table-based CV" & vbCrLf & _
           "requires moving table rows." & vbCrLf & vbCrLf & _
           "Recommended: Cut and paste the entire" & vbCrLf & _
           "job row in Word, or use the Python script.", _
           vbInformation, "Swap Jobs"
End Sub


' ============================================================
' SWAP SECTION MENU
' Moves body-level sections (EDUCATION, WORK EXPERIENCE, SKILLS)
' using Range Cut/Paste. Sections whose header is nested inside
' another section's table (e.g. LEADERSHIP EXPERIENCE inside
' Fintech table) cannot be swapped — use the Python script.
'
' Python alternative for complex structural swaps:
'   _Tools/CV_Editor/swap_education_first.py
'
' See: Context/CV_DOCX_CHEAT_SHEET.md for table map.
' ============================================================
Sub SwapSectionMenu()
    On Error GoTo ErrHandler
    
    ForceWindowToPrimaryScreen
    ScanDocument
    
    If gSectionCount < 2 Then
        MsgBox "Need at least 2 sections to swap!" & vbCrLf & _
               "Found: " & gSectionCount & " section(s).", vbExclamation, "Swap Sections"
        Exit Sub
    End If
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' --- Find positions and check body-level status for each section ---
    Dim secPos() As Long        ' Character position of header text
    Dim secTblPos() As Long     ' Start position of containing table
    Dim secBodyLvl() As Boolean ' True if header is in the first cell of its table
    ReDim secPos(1 To gSectionCount)
    ReDim secTblPos(1 To gSectionCount)
    ReDim secBodyLvl(1 To gSectionCount)
    
    Dim sc As Integer
    For sc = 1 To gSectionCount
        Dim rng As Range
        Set rng = doc.Content
        With rng.Find
            .Text = gSections(sc)
            .MatchCase = False
            .MatchWholeWord = False
            .Wrap = wdFindStop
            If .Execute Then
                secPos(sc) = rng.Start
                
                If rng.Information(wdWithInTable) Then
                    Dim tbl As Table
                    Set tbl = rng.Tables(1)
                    secTblPos(sc) = tbl.Range.Start
                    
                    ' Body-level check: is section header in the first cell?
                    Dim fc As String
                    fc = tbl.Cell(1, 1).Range.Text
                    ' Strip paragraph mark (Chr 13) and cell marker (Chr 7)
                    fc = Replace(Replace(fc, Chr(13), ""), Chr(7), "")
                    fc = Trim(fc)
                    secBodyLvl(sc) = (InStr(1, fc, gSections(sc), vbTextCompare) > 0)
                Else
                    secTblPos(sc) = rng.Paragraphs(1).Range.Start
                    secBodyLvl(sc) = True
                End If
            End If
        End With
    Next sc
    
    ' --- Show menu ---
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "       SWAP SECTIONS" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Sections found:" & vbCrLf & vbCrLf
    
    For sc = 1 To gSectionCount
        Dim tag As String
        If secBodyLvl(sc) Then tag = "" Else tag = " (nested)"
        msg = msg & sc & ". " & gSections(sc) & tag & vbCrLf
    Next sc
    
    msg = msg & vbCrLf & "Section to MOVE? (number):"
    
    Dim c1 As String
    c1 = InputBox(msg, "Swap - Step 1")
    If c1 = "" Then Exit Sub
    
    Dim srcIdx As Integer
    srcIdx = Val(c1)
    If srcIdx < 1 Or srcIdx > gSectionCount Then
        MsgBox "Invalid section number!", vbExclamation
        Exit Sub
    End If
    
    If Not secBodyLvl(srcIdx) Then
        MsgBox "'" & gSections(srcIdx) & "' is nested inside" & vbCrLf & _
               "another section's table." & vbCrLf & vbCrLf & _
               "Use the Python script instead:" & vbCrLf & _
               "_Tools/CV_Editor/swap_education_first.py", _
               vbExclamation, "Nested Section"
        Exit Sub
    End If
    
    Dim c2 As String
    c2 = InputBox("Move '" & gSections(srcIdx) & "'" & vbCrLf & _
                  "BEFORE which section? (number)", "Swap - Step 2")
    If c2 = "" Then Exit Sub
    
    Dim destIdx As Integer
    destIdx = Val(c2)
    If destIdx < 1 Or destIdx > gSectionCount Or destIdx = srcIdx Then
        MsgBox "Invalid section number!", vbExclamation
        Exit Sub
    End If
    
    If Not secBodyLvl(destIdx) Then
        MsgBox "'" & gSections(destIdx) & "' is nested — " & vbCrLf & _
               "can't use as target.", vbExclamation
        Exit Sub
    End If
    
    ' --- Calculate source section range ---
    ' Start: the table containing the section header
    Dim srcStart As Long
    srcStart = secTblPos(srcIdx)
    
    ' Include separator paragraph before the table (if empty)
    If srcStart >= 3 Then
        Dim prevP As Range
        Set prevP = doc.Range(srcStart - 2, srcStart)
        prevP.MoveStart wdParagraph, -1
        Dim prevTxt As String
        prevTxt = Trim(Replace(Replace(prevP.Text, Chr(13), ""), Chr(7), ""))
        If Len(prevTxt) = 0 Then
            srcStart = prevP.Start
        End If
    End If
    
    ' End: start of next body-level section (by document position)
    ' Find the body-level section whose table position is closest after ours
    Dim srcEnd As Long
    srcEnd = doc.Content.End
    
    For sc = 1 To gSectionCount
        If sc <> srcIdx And secBodyLvl(sc) Then
            If secTblPos(sc) > secTblPos(srcIdx) And secTblPos(sc) < srcEnd Then
                srcEnd = secTblPos(sc)
            End If
        End If
    Next sc
    
    ' Walk back to include separator before next section
    If srcEnd < doc.Content.End And srcEnd >= 3 Then
        Set prevP = doc.Range(srcEnd - 2, srcEnd)
        prevP.MoveStart wdParagraph, -1
        prevTxt = Trim(Replace(Replace(prevP.Text, Chr(13), ""), Chr(7), ""))
        If Len(prevTxt) = 0 Then
            srcEnd = prevP.Start
        End If
    End If
    
    ' --- Confirm ---
    If MsgBox("Move '" & gSections(srcIdx) & "'" & vbCrLf & _
              "before '" & gSections(destIdx) & "'?" & vbCrLf & vbCrLf & _
              "Undo with Cmd+Z if needed.", _
              vbYesNo + vbQuestion, "Confirm Swap") = vbNo Then Exit Sub
    
    ' --- CUT source section ---
    doc.Range(srcStart, srcEnd).Cut
    
    ' --- Find destination after cut (positions have shifted) ---
    Set rng = doc.Content
    With rng.Find
        .Text = gSections(destIdx)
        .MatchCase = False
        .MatchWholeWord = False
        .Wrap = wdFindStop
        If Not .Execute Then
            MsgBox "Cannot find destination after cut!" & vbCrLf & _
                   "Press Cmd+Z to undo.", vbCritical, "Error"
            Exit Sub
        End If
    End With
    
    Dim destPos As Long
    If rng.Information(wdWithInTable) Then
        destPos = rng.Tables(1).Range.Start
    Else
        destPos = rng.Paragraphs(1).Range.Start
    End If
    
    ' Include separator before destination
    If destPos >= 3 Then
        Set prevP = doc.Range(destPos - 2, destPos)
        prevP.MoveStart wdParagraph, -1
        prevTxt = Trim(Replace(Replace(prevP.Text, Chr(13), ""), Chr(7), ""))
        If Len(prevTxt) = 0 Then
            destPos = prevP.Start
        End If
    End If
    
    ' --- PASTE at destination ---
    doc.Range(destPos, destPos).Paste
    
    MsgBox "Done! Moved '" & gSections(srcIdx) & "'" & vbCrLf & _
           "before '" & gSections(destIdx) & "'." & vbCrLf & vbCrLf & _
           "Press Cmd+Z to undo if needed.", _
           vbInformation, "Swap Complete"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description & vbCrLf & _
           "Error #" & Err.Number & vbCrLf & vbCrLf & _
           "Press Cmd+Z to undo." & vbCrLf & _
           "For complex swaps, use Python:" & vbCrLf & _
           "_Tools/CV_Editor/swap_education_first.py", _
           vbExclamation, "Swap Error"
End Sub


' ============================================================
' DATABASE MENU
' Store/retrieve bullet points from a text file
' File location: ~/Documents/CV_Bullet_Database.txt
' Format: CATEGORY||BULLET_TEXT (one per line)
' ============================================================

Private Function GetDBPath() As String
    GetDBPath = "/Users/tomasbatalha/Documents/CV_Bullet_Database.txt"
End Function

' Helper: Read all DB entries into arrays. Returns count.
' Format: CATEGORY||BULLET_TEXT||TAG1,TAG2 (tags optional)
Private Function DB_ReadAll(ByRef cats() As String, ByRef bullets() As String, ByRef tags() As String) As Integer
    Dim dbPath As String
    dbPath = GetDBPath()
    
    ReDim cats(1 To 500)
    ReDim bullets(1 To 500)
    ReDim tags(1 To 500)
    Dim cnt As Integer
    cnt = 0
    
    If Dir(dbPath) = "" Then
        DB_ReadAll = 0
        Exit Function
    End If
    
    Dim fNum As Integer
    fNum = FreeFile
    Open dbPath For Input As #fNum
    Do While Not EOF(fNum)
        Dim lineText As String
        Line Input #fNum, lineText
        If Len(lineText) > 3 And InStr(lineText, "||") > 0 Then
            cnt = cnt + 1
            Dim parts() As String
            parts = Split(lineText, "||")
            cats(cnt) = parts(0)
            bullets(cnt) = parts(1)
            If UBound(parts) >= 2 Then
                tags(cnt) = parts(2)
            Else
                tags(cnt) = ""
            End If
        End If
    Loop
    Close #fNum
    DB_ReadAll = cnt
End Function

' Helper: Get unique categories from read data
Private Function DB_GetCategories(cats() As String, cnt As Integer) As String
    ' Returns pipe-delimited string of unique categories
    Dim result As String
    result = "|"
    Dim i As Integer
    For i = 1 To cnt
        If InStr(result, "|" & cats(i) & "|") = 0 Then
            result = result & cats(i) & "|"
        End If
    Next i
    DB_GetCategories = result
End Function

' Helper: Count bullets in a category
Private Function DB_CountInCategory(cats() As String, cnt As Integer, catName As String) As Integer
    Dim c As Integer
    c = 0
    Dim i As Integer
    For i = 1 To cnt
        If cats(i) = catName Then c = c + 1
    Next i
    DB_CountInCategory = c
End Function

Sub DatabaseMenu()
    On Error GoTo ErrHandler
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    BULLET DATABASE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "1. Browse by company/category" & vbCrLf
    msg = msg & "2. Browse by tag" & vbCrLf
    msg = msg & "3. Search by keyword" & vbCrLf
    msg = msg & "4. Add bullet manually" & vbCrLf
    msg = msg & "5. Save bullet from CV" & vbCrLf
    msg = msg & "6. Save ALL bullets from a job" & vbCrLf
    msg = msg & "7. Insert from database into CV" & vbCrLf & vbCrLf
    msg = msg & "0. Back" & vbCrLf & vbCrLf
    msg = msg & "Enter choice:"
    
    Dim result As String
    result = InputBox(msg, "Bullet Database")
    
    Select Case Val(result)
        Case 1: DB_BrowseByCategory
        Case 2: DB_BrowseByTag
        Case 3: DB_Search
        Case 4: DB_AddManual
        Case 5: DB_SaveBullet
        Case 6: DB_SaveAllBullets
        Case 7: DB_InsertBullet
    End Select
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Database Error"
End Sub

' ---- BROWSE BY CATEGORY (2-step) ----
Private Sub DB_BrowseByCategory()
    Dim cats() As String, bullets() As String, tags() As String
    Dim cnt As Integer
    cnt = DB_ReadAll(cats, bullets, tags)
    
    If cnt = 0 Then
        MsgBox "Database is empty.", vbInformation
        Exit Sub
    End If
    
    ' Step 1: Show categories
    Dim catList As String
    catList = DB_GetCategories(cats, cnt)
    
    Dim msg As String
    msg = "SELECT A CATEGORY:" & vbCrLf & vbCrLf
    
    ' Parse categories into numbered list
    Dim catArr() As String
    catArr = Split(Mid(catList, 2, Len(catList) - 2), "|")
    
    Dim i As Integer
    For i = 0 To UBound(catArr)
        If Len(catArr(i)) > 0 Then
            Dim catCount As Integer
            catCount = DB_CountInCategory(cats, cnt, catArr(i))
            msg = msg & (i + 1) & ". " & catArr(i) & " (" & catCount & " bullets)" & vbCrLf
        End If
    Next i
    
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, "Browse Database")
    If result = "" Or Val(result) < 1 Or Val(result) > UBound(catArr) + 1 Then Exit Sub
    
    Dim selectedCat As String
    selectedCat = catArr(Val(result) - 1)
    
    ' Step 2: Show all bullets in that category
    DB_ShowCategory selectedCat, cats, bullets, tags, cnt
End Sub

Private Sub DB_ShowCategory(catName As String, cats() As String, bullets() As String, tags() As String, cnt As Integer)
    ' Show bullets for one category, paginated if needed
    Dim msg As String
    msg = "[" & catName & "]" & vbCrLf & vbCrLf
    
    Dim bulletNum As Integer
    bulletNum = 0
    Dim i As Integer
    For i = 1 To cnt
        If cats(i) = catName Then
            bulletNum = bulletNum + 1
            Dim tagDisplay As String
            If Len(tags(i)) > 0 Then
                tagDisplay = " {" & tags(i) & "}"
            Else
                tagDisplay = ""
            End If
            msg = msg & bulletNum & "." & tagDisplay & " " & bullets(i) & vbCrLf & vbCrLf
            
            ' Paginate every 5 bullets to avoid MsgBox overflow
            If bulletNum Mod 5 = 0 And i < cnt Then
                Dim hasMore As Boolean
                hasMore = False
                Dim k As Integer
                For k = i + 1 To cnt
                    If cats(k) = catName Then hasMore = True: Exit For
                Next k
                
                If hasMore Then
                    msg = msg & "(More bullets...)" & vbCrLf
                    If MsgBox(msg, vbOKCancel + vbInformation, catName & " - Page " & (bulletNum \ 5)) = vbCancel Then
                        Exit Sub
                    End If
                    msg = "[" & catName & "] (continued)" & vbCrLf & vbCrLf
                End If
            End If
        End If
    Next i
    
    If bulletNum > 0 Then
        msg = msg & "---" & vbCrLf & bulletNum & " total bullets in " & catName
        MsgBox msg, vbInformation, catName
    End If
End Sub

' ---- BROWSE BY TAG ----
Private Sub DB_BrowseByTag()
    Dim cats() As String, bullets() As String, tags() As String
    Dim cnt As Integer
    cnt = DB_ReadAll(cats, bullets, tags)
    
    If cnt = 0 Then
        MsgBox "Database is empty.", vbInformation
        Exit Sub
    End If
    
    ' Collect unique tags
    Dim allTags As String
    allTags = ","
    Dim i As Integer
    For i = 1 To cnt
        If Len(tags(i)) > 0 Then
            Dim tagParts() As String
            tagParts = Split(tags(i), ",")
            Dim t As Integer
            For t = 0 To UBound(tagParts)
                Dim oneTag As String
                oneTag = Trim(tagParts(t))
                If Len(oneTag) > 0 And InStr(allTags, "," & oneTag & ",") = 0 Then
                    allTags = allTags & oneTag & ","
                End If
            Next t
        End If
    Next i
    
    If allTags = "," Then
        MsgBox "No tags found. Add tags when saving bullets.", vbInformation
        Exit Sub
    End If
    
    ' Show tags
    Dim msg As String
    msg = "SELECT A TAG:" & vbCrLf & vbCrLf
    
    Dim tagArr() As String
    tagArr = Split(Mid(allTags, 2, Len(allTags) - 2), ",")
    
    For i = 0 To UBound(tagArr)
        If Len(tagArr(i)) > 0 Then
            ' Count entries with this tag
            Dim tagCount As Integer
            tagCount = 0
            Dim j As Integer
            For j = 1 To cnt
                If InStr(1, "," & tags(j) & ",", "," & tagArr(i) & ",", vbTextCompare) > 0 Then
                    tagCount = tagCount + 1
                End If
            Next j
            msg = msg & (i + 1) & ". " & tagArr(i) & " (" & tagCount & " bullets)" & vbCrLf
        End If
    Next i
    
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, "Browse by Tag")
    If result = "" Or Val(result) < 1 Or Val(result) > UBound(tagArr) + 1 Then Exit Sub
    
    Dim selectedTag As String
    selectedTag = tagArr(Val(result) - 1)
    
    ' Show bullets with this tag
    msg = "Tag: {" & selectedTag & "}" & vbCrLf & vbCrLf
    
    Dim bulletNum As Integer
    bulletNum = 0
    For i = 1 To cnt
        If InStr(1, "," & tags(i) & ",", "," & selectedTag & ",", vbTextCompare) > 0 Then
            bulletNum = bulletNum + 1
            msg = msg & bulletNum & ". [" & cats(i) & "] " & bullets(i) & vbCrLf & vbCrLf
            
            If bulletNum Mod 5 = 0 Then
                msg = msg & "(More...)"
                If MsgBox(msg, vbOKCancel + vbInformation, "Tag: " & selectedTag) = vbCancel Then Exit Sub
                msg = "Tag: {" & selectedTag & "} (continued)" & vbCrLf & vbCrLf
            End If
        End If
    Next i
    
    If bulletNum > 0 Then
        msg = msg & "---" & vbCrLf & bulletNum & " total bullets with tag {" & selectedTag & "}"
        MsgBox msg, vbInformation, "Tag: " & selectedTag
    End If
End Sub

' ---- SEARCH BY KEYWORD ----
Private Sub DB_Search()
    Dim cats() As String, bullets() As String, tags() As String
    Dim cnt As Integer
    cnt = DB_ReadAll(cats, bullets, tags)
    
    If cnt = 0 Then
        MsgBox "Database is empty.", vbInformation
        Exit Sub
    End If
    
    Dim keyword As String
    keyword = InputBox("Enter search keyword:" & vbCrLf & vbCrLf & _
        "Searches bullet text, categories, and tags." & vbCrLf & _
        "(Case-insensitive)", "Search Database")
    If keyword = "" Then Exit Sub
    
    ' Find matches
    Dim msg As String
    msg = "Results for '" & keyword & "':" & vbCrLf & vbCrLf
    
    Dim matchCount As Integer
    matchCount = 0
    Dim i As Integer
    For i = 1 To cnt
        If InStr(1, bullets(i), keyword, vbTextCompare) > 0 Or _
           InStr(1, cats(i), keyword, vbTextCompare) > 0 Or _
           InStr(1, tags(i), keyword, vbTextCompare) > 0 Then
            matchCount = matchCount + 1
            Dim tagDisp As String
            If Len(tags(i)) > 0 Then tagDisp = " {" & tags(i) & "}" Else tagDisp = ""
            msg = msg & matchCount & ". [" & cats(i) & "]" & tagDisp & " " & Left(bullets(i), 70)
            If Len(bullets(i)) > 70 Then msg = msg & "..."
            msg = msg & vbCrLf & vbCrLf
            
            ' Paginate every 5
            If matchCount Mod 5 = 0 Then
                msg = msg & "(More results...)"
                If MsgBox(msg, vbOKCancel + vbInformation, "Search Results") = vbCancel Then
                    Exit Sub
                End If
                msg = "Results for '" & keyword & "' (continued):" & vbCrLf & vbCrLf
            End If
        End If
    Next i
    
    If matchCount = 0 Then
        MsgBox "No results for '" & keyword & "'", vbInformation, "Search"
    Else
        msg = msg & "---" & vbCrLf & matchCount & " total matches"
        MsgBox msg, vbInformation, "Search Results"
    End If
End Sub

' ---- ADD BULLET MANUALLY ----
Private Sub DB_AddManual()
    ' Step 1: Show existing categories for reference
    Dim cats() As String, bullets() As String, tags() As String
    Dim cnt As Integer
    cnt = DB_ReadAll(cats, bullets, tags)
    
    Dim catList As String
    catList = ""
    If cnt > 0 Then
        Dim uniqueCats As String
        uniqueCats = DB_GetCategories(cats, cnt)
        catList = Replace(Mid(uniqueCats, 2, Len(uniqueCats) - 2), "|", ", ")
    End If
    
    ' Step 2: Ask for category
    Dim cat As String
    Dim catPrompt As String
    catPrompt = "Enter category for the bullet:" & vbCrLf & vbCrLf
    If Len(catList) > 0 Then
        catPrompt = catPrompt & "Existing categories: " & catList & vbCrLf & vbCrLf
    End If
    catPrompt = catPrompt & "Or type a new category name:"
    
    cat = InputBox(catPrompt, "Add Bullet - Category")
    If cat = "" Then Exit Sub
    
    ' Step 3: Ask for bullet text
    Dim bulletText As String
    bulletText = InputBox("Enter bullet text:" & vbCrLf & vbCrLf & _
        "Category: [" & UCase(cat) & "]" & vbCrLf & vbCrLf & _
        "Tips:" & vbCrLf & _
        "  Start with action verb" & vbCrLf & _
        "  Include metrics/numbers" & vbCrLf & _
        "  Keep under ~140 chars for 1 line", _
        "Add Bullet - Text")
    If bulletText = "" Then Exit Sub
    
    ' Step 4: Ask for tags (optional)
    Dim tagInput As String
    tagInput = InputBox("Tags (optional, comma-separated):" & vbCrLf & vbCrLf & _
        "Examples: SALES, CONSULTING, AE, SDR, LINKEDIN" & vbCrLf & vbCrLf & _
        "Leave empty for no tags:", _
        "Add Bullet - Tags")
    
    ' Append to file
    Dim fNum As Integer
    fNum = FreeFile
    Open GetDBPath() For Append As #fNum
    Dim lineOut As String
    lineOut = UCase(cat) & "||" & bulletText
    If Len(tagInput) > 0 Then lineOut = lineOut & "||" & UCase(tagInput)
    Print #fNum, lineOut
    Close #fNum
    
    MsgBox "Saved!" & vbCrLf & vbCrLf & _
           "[" & UCase(cat) & "] " & Left(bulletText, 80), vbInformation, "Added"
End Sub

' ---- SAVE BULLET FROM CV ----
Private Sub DB_SaveBullet()
    Dim jobIdx As Integer
    jobIdx = SelectJob("SAVE BULLET - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    Dim bulletEntry As String
    bulletEntry = SelectBulletFromJob(jobIdx, "SAVE BULLET")
    If bulletEntry = "" Then Exit Sub
    
    Dim parts() As String
    parts = Split(bulletEntry, "||")
    Dim bulletText As String
    bulletText = parts(0)
    
    Dim cat As String
    cat = InputBox("Category for this bullet:" & vbCrLf & vbCrLf & _
        Left(bulletText, 120) & vbCrLf & vbCrLf & _
        "Enter category:", "Category", _
        Left(gJobCompany(jobIdx), InStr(gJobCompany(jobIdx) & " |", " |") - 1))
    If cat = "" Then Exit Sub
    
    Dim tagInput As String
    tagInput = InputBox("Tags (optional, comma-separated):" & vbCrLf & vbCrLf & _
        "e.g. SALES, AE, SDR, CONSULTING" & vbCrLf & vbCrLf & _
        "Leave empty for no tags:", "Tags")
    
    Dim fNum As Integer
    fNum = FreeFile
    Open GetDBPath() For Append As #fNum
    Dim lineOut As String
    lineOut = UCase(cat) & "||" & bulletText
    If Len(tagInput) > 0 Then lineOut = lineOut & "||" & UCase(tagInput)
    Print #fNum, lineOut
    Close #fNum
    
    MsgBox "Saved to [" & UCase(cat) & "]!", vbInformation, "Saved"
End Sub

' ---- SAVE ALL BULLETS FROM JOB ----
Private Sub DB_SaveAllBullets()
    Dim jobIdx As Integer
    jobIdx = SelectJob("SAVE ALL BULLETS - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    Dim bul As Collection
    Set bul = GetBulletsForJob(jobIdx)
    
    If bul.Count = 0 Then
        MsgBox "No bullets found!", vbExclamation
        Exit Sub
    End If
    
    Dim cat As String
    cat = InputBox(bul.Count & " bullets found for:" & vbCrLf & _
        gJobCompany(jobIdx) & vbCrLf & vbCrLf & _
        "Enter category for all:", "Category", _
        Left(gJobCompany(jobIdx), InStr(gJobCompany(jobIdx) & " |", " |") - 1))
    If cat = "" Then Exit Sub
    
    Dim tagInput As String
    tagInput = InputBox("Tags for all bullets (optional, comma-separated):" & vbCrLf & vbCrLf & _
        "e.g. SALES, AE, CV-CURRENT" & vbCrLf & vbCrLf & _
        "Leave empty for no tags:", "Tags")
    
    Dim fNum As Integer
    fNum = FreeFile
    Open GetDBPath() For Append As #fNum
    
    Dim i As Integer
    For i = 1 To bul.Count
        Dim parts() As String
        parts = Split(bul(i), "||")
        Dim lineOut As String
        lineOut = UCase(cat) & "||" & parts(0)
        If Len(tagInput) > 0 Then lineOut = lineOut & "||" & UCase(tagInput)
        Print #fNum, lineOut
    Next i
    Close #fNum
    
    MsgBox bul.Count & " bullets saved to [" & UCase(cat) & "]!", vbInformation, "Saved"
End Sub

' ---- INSERT FROM DATABASE INTO CV ----
Private Sub DB_InsertBullet()
    Dim cats() As String, bullets() As String, tags() As String
    Dim cnt As Integer
    cnt = DB_ReadAll(cats, bullets, tags)
    
    If cnt = 0 Then
        MsgBox "Database is empty.", vbInformation
        Exit Sub
    End If
    
    ' Step 1: Pick category
    Dim catList As String
    catList = DB_GetCategories(cats, cnt)
    Dim catArr() As String
    catArr = Split(Mid(catList, 2, Len(catList) - 2), "|")
    
    Dim msg As String
    msg = "INSERT FROM DATABASE" & vbCrLf & vbCrLf
    msg = msg & "Step 1: Pick a category" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 0 To UBound(catArr)
        If Len(catArr(i)) > 0 Then
            msg = msg & (i + 1) & ". " & catArr(i) & " (" & DB_CountInCategory(cats, cnt, catArr(i)) & ")" & vbCrLf
        End If
    Next i
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, "Insert - Category")
    If result = "" Or Val(result) < 1 Or Val(result) > UBound(catArr) + 1 Then Exit Sub
    
    Dim selectedCat As String
    selectedCat = catArr(Val(result) - 1)
    
    ' Step 2: Pick bullet from that category
    msg = "INSERT FROM [" & selectedCat & "]" & vbCrLf & vbCrLf
    msg = msg & "Step 2: Pick a bullet" & vbCrLf & vbCrLf
    
    Dim bulletIdxs() As Integer
    ReDim bulletIdxs(1 To cnt)
    Dim bCount As Integer
    bCount = 0
    
    For i = 1 To cnt
        If cats(i) = selectedCat Then
            bCount = bCount + 1
            bulletIdxs(bCount) = i
            msg = msg & bCount & ". " & Left(bullets(i), 70)
            If Len(bullets(i)) > 70 Then msg = msg & "..."
            msg = msg & vbCrLf
        End If
    Next i
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    result = InputBox(msg, "Insert - Bullet")
    If result = "" Or Val(result) < 1 Or Val(result) > bCount Then Exit Sub
    
    Dim selectedText As String
    selectedText = bullets(bulletIdxs(Val(result)))
    
    ' Step 3: Pick job to insert into
    Dim jobIdx As Integer
    jobIdx = SelectJob("INSERT INTO - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    ' Insert as last bullet
    Dim bul As Collection
    Set bul = GetBulletsForJob(jobIdx)
    
    If bul.Count > 0 Then
        Dim lastBullet As String
        lastBullet = bul(bul.Count)
        Dim parts() As String
        parts = Split(lastBullet, "||")
        
        Dim paraEnd As Long
        paraEnd = CLng(parts(2))
        
        Dim rng As Range
        Set rng = ActiveDocument.Range(paraEnd - 1, paraEnd - 1)
        rng.Select
        
        Selection.EndKey Unit:=wdLine
        Selection.TypeParagraph
        Selection.TypeText Text:=selectedText
        
        With Selection.Font
            .Name = CV_FONT
            .Size = CV_BODY_SIZE
            .Bold = False
        End With
        
        ' Copy list format from existing bullet
        Selection.Paragraphs(1).Range.ListFormat.RemoveNumbers
        Dim eParts() As String
        eParts = Split(bul(1), "||")
        Dim srcRange As Range
        Set srcRange = ActiveDocument.Range(CLng(eParts(1)), CLng(eParts(2)))
        Dim lt As ListTemplate
        Set lt = srcRange.ListFormat.ListTemplate
        If Not lt Is Nothing Then
            Selection.Paragraphs(1).Range.ListFormat.ApplyListTemplate ListTemplate:=lt
        End If
        
        MsgBox "Inserted into " & gJobCompany(jobIdx) & "!", vbInformation, "Success"
    Else
        MsgBox "No existing bullets found to insert after.", vbExclamation
    End If
End Sub


' ============================================================
' RESIZE CV MENU
' ============================================================
Sub ResizeCVMenu()
    On Error GoTo ErrHandler
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    RESIZE CV" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Adjust spacing to fit 1 page:" & vbCrLf & vbCrLf
    msg = msg & "1. Shrink bullet text (-0.5pt)" & vbCrLf
    msg = msg & "2. Grow bullet text (+0.5pt)" & vbCrLf
    msg = msg & "3. Reduce line spacing" & vbCrLf
    msg = msg & "4. Increase line spacing" & vbCrLf
    msg = msg & "5. Tighten character spacing" & vbCrLf
    msg = msg & "6. Loosen character spacing" & vbCrLf & vbCrLf
    msg = msg & "Enter choice (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, "Resize CV")
    
    Select Case Val(result)
        Case 1: ResizeBullets -0.5
        Case 2: ResizeBullets 0.5
        Case 3: AdjustLineSpacing -0.5
        Case 4: AdjustLineSpacing 0.5
        Case 5: AdjustCharSpacing -0.25
        Case 6: AdjustCharSpacing 0.25
    End Select
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Resize Error"
End Sub

Private Sub ResizeBullets(delta As Single)
    Dim doc As Document
    Set doc = ActiveDocument
    Dim count As Integer
    count = 0
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        If para.Range.ListFormat.ListType <> wdListNoNumbering Then
            para.Range.Font.Size = para.Range.Font.Size + delta
            count = count + 1
        End If
    Next para
    
    MsgBox count & " bullets resized by " & IIf(delta > 0, "+", "") & delta & "pt", vbInformation
End Sub

Private Sub AdjustLineSpacing(delta As Single)
    Dim doc As Document
    Set doc = ActiveDocument
    Dim count As Integer
    count = 0
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        If para.Range.ListFormat.ListType <> wdListNoNumbering Then
            Dim newSpacing As Single
            newSpacing = para.Format.SpaceBefore + delta
            If newSpacing < 0 Then newSpacing = 0
            para.Format.SpaceBefore = newSpacing
            count = count + 1
        End If
    Next para
    
    MsgBox count & " paragraphs adjusted by " & IIf(delta > 0, "+", "") & delta & "pt spacing", vbInformation
End Sub

Private Sub AdjustCharSpacing(delta As Single)
    Dim doc As Document
    Set doc = ActiveDocument
    Dim count As Integer
    count = 0
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        If para.Range.ListFormat.ListType <> wdListNoNumbering Then
            para.Range.Font.Spacing = para.Range.Font.Spacing + delta
            count = count + 1
        End If
    Next para
    
    MsgBox count & " paragraphs char spacing adjusted", vbInformation
End Sub


' ============================================================
' VIEW STRUCTURE
' ============================================================
Sub ViewStructure()
    On Error GoTo ErrHandler
    
    ScanDocument
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    CV STRUCTURE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Sections: " & gSectionCount & vbCrLf
    msg = msg & "Jobs: " & gJobCount & vbCrLf
    msg = msg & "Tables: " & ActiveDocument.Tables.Count & vbCrLf & vbCrLf
    
    Dim lastSec As String
    lastSec = ""
    
    Dim i As Integer
    For i = 1 To gJobCount
        If gJobSection(i) <> lastSec Then
            msg = msg & vbCrLf & "[+] " & gJobSection(i) & vbCrLf
            lastSec = gJobSection(i)
        End If
        
        msg = msg & "     > " & Left(gJobCompany(i), 45) & vbCrLf
        If gJobRole(i) <> "" Then
            msg = msg & "       " & Left(gJobRole(i), 45) & vbCrLf
        End If
        
        ' Count bullets
        Dim bullets As Collection
        Set bullets = GetBulletsForJob(i)
        msg = msg & "       (" & bullets.Count & " bullets)" & vbCrLf
    Next i
    
    MsgBox msg, vbInformation, "CV Structure"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "View Structure Error"
End Sub


' ============================================================
' FORMAT HELPER
' ============================================================
Sub FormatHelper()
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    FORMAT HELPER" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Select text first, then choose:" & vbCrLf & vbCrLf
    msg = msg & "1. Format as Section Header" & vbCrLf
    msg = msg & "   (Bold, " & CV_FONT & " " & CV_HEADER_SIZE & "pt)" & vbCrLf & vbCrLf
    msg = msg & "2. Format as Company Header" & vbCrLf
    msg = msg & "   (Bold, " & CV_FONT & " " & CV_BODY_SIZE & "pt)" & vbCrLf & vbCrLf
    msg = msg & "3. Format as Role Line" & vbCrLf
    msg = msg & "   (Regular, " & CV_FONT & " " & CV_BODY_SIZE & "pt)" & vbCrLf & vbCrLf
    msg = msg & "4. Format as Bullet Text" & vbCrLf
    msg = msg & "   (Regular, " & CV_FONT & " " & CV_BODY_SIZE & "pt)" & vbCrLf & vbCrLf
    msg = msg & "Enter choice (1-4):"
    
    Dim result As String
    result = InputBox(msg, "Format Helper")
    
    Select Case Val(result)
        Case 1: FormatAsSection
        Case 2: FormatAsCompany
        Case 3: FormatAsRole
        Case 4: FormatAsBullet
    End Select
End Sub

Private Sub FormatAsSection()
    With Selection.Font
        .Name = CV_FONT
        .Size = CV_HEADER_SIZE
        .Bold = True
        .Italic = False
    End With
End Sub

Private Sub FormatAsCompany()
    With Selection.Font
        .Name = CV_FONT
        .Size = CV_BODY_SIZE
        .Bold = True
        .Italic = False
    End With
End Sub

Private Sub FormatAsRole()
    With Selection.Font
        .Name = CV_FONT
        .Size = CV_BODY_SIZE
        .Bold = False
        .Italic = False
    End With
End Sub

Private Sub FormatAsBullet()
    With Selection.Font
        .Name = CV_FONT
        .Size = CV_BODY_SIZE
        .Bold = False
        .Italic = False
    End With
End Sub


' ============================================================
' EDIT BULLET (NEW - not in original, for RIBBON enhancement)
' ============================================================
Sub EditBulletMenu()
    On Error GoTo ErrHandler
    
    Dim jobIdx As Integer
    jobIdx = SelectJob("EDIT BULLET - Select Job")
    If jobIdx = 0 Then Exit Sub
    
    Dim bulletEntry As String
    bulletEntry = SelectBulletFromJob(jobIdx, "EDIT BULLET")
    If bulletEntry = "" Then Exit Sub
    
    Dim parts() As String
    parts = Split(bulletEntry, "||")
    
    Dim currentText As String
    currentText = parts(0)
    
    Dim newText As String
    newText = InputBox("Current bullet:" & vbCrLf & vbCrLf & _
        Left(currentText, 200) & vbCrLf & vbCrLf & _
        "Enter new text (or empty to cancel):", _
        "Edit Bullet", currentText)
    
    If newText = "" Or newText = currentText Then Exit Sub
    
    ' Replace the text
    Dim rng As Range
    Set rng = ActiveDocument.Range(CLng(parts(1)), CLng(parts(2)) - 1) ' -1 for para mark
    rng.Text = newText
    
    ' Reapply formatting
    With rng.Font
        .Name = CV_FONT
        .Size = CV_BODY_SIZE
        .Bold = False
    End With
    
    MsgBox "Bullet updated!", vbInformation, "Success"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Edit Bullet Error"
End Sub


' ============================================================
' RIBBON BUTTON ENTRY POINTS
' These are the subs your toolbar buttons call
' DO NOT RENAME THESE
' ============================================================

Sub RIBBON1_Menu()
    CVEditor
End Sub

Sub RIBBON2_AddBullet()
    AddBulletMenu
End Sub

Sub RIBBON3_AddJob()
    AddJobMenu
End Sub

Sub RIBBON4_Resize()
    ResizeCVMenu
End Sub

Sub RIBBON5_DB()
    DatabaseMenu
End Sub

Sub RIBBON6_DelBullet()
    DeleteBulletMenu
End Sub

Sub RIBBON7_DelJob()
    DeleteJobMenu
End Sub
