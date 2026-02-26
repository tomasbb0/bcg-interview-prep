' ============================================================
' CV EDITOR v2 — TABLE-AWARE MACROS
' For: TomásBatalha_Resume (table-based CV, nested tables)
' ============================================================
'
' HOW TO INSTALL (Mac Word):
' ──────────────────────────
' 1. Open your CV .docm in Word
' 2. Tools menu > Macro > Visual Basic Editor
' 3. In the left panel (Project Explorer):
'    a) Right-click your document project
'    b) Insert > Module
'    c) Paste ALL of this code into the new Module1
' 4. Now in the left panel, double-click "ThisDocument"
' 5. Paste ONLY these 2 lines:
'       Private Sub Document_Open()
'           CreateCVMenu
'       End Sub
' 6. Save the document (must be .docm format)
' 7. Close and reopen — "CV Editor" menu appears in menu bar
'
' ALTERNATIVELY — Run manually:
'    Tools > Macro > Macros > select "CVMenu" > Run
'
' ============================================================

Option Explicit

' ============================
' CONSTANTS — match your CV
' ============================
Private Const BODY_FONT As String = "Arial"
Private Const BODY_SIZE As Single = 7.5
Private Const HEADER_SIZE As Single = 9
Private Const BULLET_CHAR As String = "-"

' Section names exactly as they appear
Private Const SEC_WORK As String = "WORK EXPERIENCE"
Private Const SEC_EDU As String = "EDUCATION"
Private Const SEC_LEAD As String = "LEADERSHIP EXPERIENCE"
Private Const SEC_SKILLS As String = "SKILLS"

' ============================================================
' MENU CREATION
' ============================================================
Sub CreateCVMenu()
    On Error Resume Next
    ' Remove existing menu if present
    Application.CommandBars("Menu Bar").Controls("CV Editor").Delete
    On Error GoTo 0
    
    Dim menuBar As CommandBar
    Set menuBar = Application.CommandBars("Menu Bar")
    
    Dim cvMenu As CommandBarPopup
    Set cvMenu = menuBar.Controls.Add(Type:=msoControlPopup, Temporary:=True)
    cvMenu.Caption = "CV Editor"
    
    ' Add menu items
    Dim btn As CommandBarButton
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "View Structure"
    btn.OnAction = "ViewCV"
    btn.FaceId = 548
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "Edit Bullet..."
    btn.OnAction = "EditBulletFlow"
    btn.FaceId = 162
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "Add Bullet..."
    btn.OnAction = "AddBulletFlow"
    btn.FaceId = 137
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "Delete Bullet..."
    btn.OnAction = "DeleteBulletFlow"
    btn.FaceId = 162
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "---"
    btn.Enabled = False
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "Align All Bullets"
    btn.OnAction = "AlignAllBullets"
    btn.FaceId = 370
    
    Set btn = cvMenu.Controls.Add(Type:=msoControlButton)
    btn.Caption = "Format Selection as Bullet"
    btn.OnAction = "FormatAsBulletText"
    btn.FaceId = 197
End Sub

' Quick entry point (run from Macros dialog)
Sub CVMenu()
    CreateCVMenu
    MsgBox "CV Editor menu created!" & vbCrLf & vbCrLf & _
           "Look for 'CV Editor' in the menu bar.", vbInformation
End Sub


' ============================================================
' CORE: SCAN DOCUMENT STRUCTURE
' ============================================================
' Returns a string array describing the CV structure
' Each entry: "SECTION|Company|Role|BulletCount"

Private Function CleanText(s As String) As String
    ' Remove paragraph marks, special chars
    Dim result As String
    result = s
    result = Replace(result, Chr(13), "")
    result = Replace(result, Chr(7), "")  ' Table cell marker
    result = Replace(result, Chr(11), "")
    CleanText = Trim(result)
End Function

Private Function IsBulletParagraph(para As Paragraph) As Boolean
    ' Check if paragraph is a list item (has numbering)
    On Error GoTo NotBullet
    If para.Range.ListFormat.ListType <> wdListNoNumbering Then
        IsBulletParagraph = True
        Exit Function
    End If
NotBullet:
    IsBulletParagraph = False
End Function

Private Function FindSectionForTable(tbl As Table) As String
    ' Determine which section a table belongs to by searching
    ' the text content for known section headers
    Dim rng As Range
    Set rng = tbl.Range
    
    Dim txt As String
    txt = UCase(CleanText(rng.Text))
    
    If InStr(txt, SEC_WORK) > 0 Then
        FindSectionForTable = SEC_WORK
    ElseIf InStr(txt, SEC_LEAD) > 0 Then
        FindSectionForTable = SEC_LEAD
    ElseIf InStr(txt, SEC_EDU) > 0 Then
        FindSectionForTable = SEC_EDU
    ElseIf InStr(txt, SEC_SKILLS) > 0 Then
        FindSectionForTable = SEC_SKILLS
    Else
        FindSectionForTable = ""
    End If
End Function

' ============================================================
' VIEW STRUCTURE
' ============================================================
Sub ViewCV()
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim msg As String
    msg = "===== CV STRUCTURE =====" & vbCrLf & vbCrLf
    
    Dim tblCount As Integer
    tblCount = doc.Tables.Count
    msg = msg & "Tables: " & tblCount & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To tblCount
        Dim tbl As Table
        Set tbl = doc.Tables(i)
        
        Dim sec As String
        sec = FindSectionForTable(tbl)
        
        If sec <> "" Then
            msg = msg & "--- " & sec & " ---" & vbCrLf
        End If
        
        ' Scan rows for job headers and bullets
        Dim r As Integer
        Dim bulletCount As Integer
        bulletCount = 0
        
        For r = 1 To tbl.Rows.Count
            On Error Resume Next
            Dim cellText As String
            cellText = CleanText(tbl.Cell(r, 1).Range.Text)
            On Error GoTo 0
            
            If Len(cellText) > 0 Then
                ' Check if it's a company line (bold, contains |)
                Dim isBold As Boolean
                On Error Resume Next
                isBold = tbl.Cell(r, 1).Range.Font.Bold
                On Error GoTo 0
                
                If InStr(cellText, " | ") > 0 And isBold And Len(cellText) < 120 Then
                    If bulletCount > 0 Then
                        msg = msg & "   (" & bulletCount & " bullets)" & vbCrLf
                        bulletCount = 0
                    End If
                    msg = msg & "  " & Left(cellText, 70) & vbCrLf
                End If
                
                ' Count bullets
                Dim para As Paragraph
                For Each para In tbl.Cell(r, 1).Range.Paragraphs
                    If IsBulletParagraph(para) Then
                        bulletCount = bulletCount + 1
                    End If
                Next para
            End If
        Next r
        
        If bulletCount > 0 Then
            msg = msg & "   (" & bulletCount & " bullets)" & vbCrLf
        End If
    Next i
    
    MsgBox msg, vbInformation, "CV Structure"
End Sub


' ============================================================
' FIND ALL JOBS IN DOCUMENT
' ============================================================
' Returns collection of arrays: (Company|Location, Role|Dates, TableIndex, RowIndex)

Private Type JobInfo
    CompanyLine As String
    RoleLine As String
    TableIndex As Integer
    RowIndex As Integer
    Section As String
End Type

Private Function GetAllJobs() As Collection
    Dim jobs As New Collection
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim currentSection As String
    currentSection = ""
    
    Dim i As Integer
    For i = 1 To doc.Tables.Count
        Dim tbl As Table
        Set tbl = doc.Tables(i)
        
        ' Check for section header
        Dim sec As String
        sec = FindSectionForTable(tbl)
        If sec <> "" Then currentSection = sec
        
        Dim r As Integer
        For r = 1 To tbl.Rows.Count
            On Error Resume Next
            Dim cellText As String
            cellText = CleanText(tbl.Cell(r, 1).Range.Text)
            On Error GoTo 0
            
            If Len(cellText) > 3 And InStr(cellText, " | ") > 0 Then
                Dim isBold As Boolean
                isBold = False
                On Error Resume Next
                isBold = tbl.Cell(r, 1).Range.Font.Bold
                On Error GoTo 0
                
                ' Company lines are bold and relatively short
                If isBold And Len(cellText) < 120 Then
                    ' Check if next text is a role line
                    Dim roleLine As String
                    roleLine = ""
                    
                    ' Look for role in same row or next row
                    Dim para As Paragraph
                    Dim paraIdx As Integer
                    paraIdx = 0
                    For Each para In tbl.Cell(r, 1).Range.Paragraphs
                        paraIdx = paraIdx + 1
                        If paraIdx = 2 Then
                            roleLine = CleanText(para.Range.Text)
                        End If
                    Next para
                    
                    ' If role not in same cell, check next row
                    If roleLine = "" And r < tbl.Rows.Count Then
                        On Error Resume Next
                        Dim nextText As String
                        nextText = CleanText(tbl.Cell(r + 1, 1).Range.Text)
                        On Error GoTo 0
                        If InStr(nextText, " | ") > 0 Or InStr(nextText, "20") > 0 Then
                            roleLine = nextText
                        End If
                    End If
                    
                    ' Store as "Section||Company|Role|TableIdx|RowIdx"
                    Dim entry As String
                    entry = currentSection & "||" & Left(cellText, 60) & "||" & Left(roleLine, 60) & "||" & CStr(i) & "||" & CStr(r)
                    jobs.Add entry
                End If
            End If
        Next r
    Next i
    
    Set GetAllJobs = jobs
End Function


' ============================================================
' SELECT JOB DIALOG
' ============================================================
Private Function SelectJob(title As String) As String
    Dim jobs As Collection
    Set jobs = GetAllJobs()
    
    If jobs.Count = 0 Then
        MsgBox "No jobs found in document!", vbExclamation
        SelectJob = ""
        Exit Function
    End If
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    " & title & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    Dim i As Integer
    Dim lastSection As String
    lastSection = ""
    
    For i = 1 To jobs.Count
        Dim parts() As String
        parts = Split(jobs(i), "||")
        
        If parts(0) <> lastSection Then
            msg = msg & vbCrLf & "  " & parts(0) & ":" & vbCrLf
            lastSection = parts(0)
        End If
        
        msg = msg & "    " & i & ". " & parts(1) & vbCrLf
        If parts(2) <> "" Then
            msg = msg & "       " & parts(2) & vbCrLf
        End If
    Next i
    
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, title)
    
    If result = "" Or Val(result) = 0 Or Val(result) > jobs.Count Then
        SelectJob = ""
    Else
        SelectJob = jobs(Val(result))
    End If
End Function


' ============================================================
' GET BULLETS FOR A JOB
' ============================================================
Private Function GetBulletsForJob(jobEntry As String) As Collection
    Dim bullets As New Collection
    Dim parts() As String
    parts = Split(jobEntry, "||")
    
    Dim tblIdx As Integer
    Dim rowIdx As Integer
    tblIdx = CInt(parts(3))
    rowIdx = CInt(parts(4))
    
    Dim doc As Document
    Set doc = ActiveDocument
    Dim tbl As Table
    Set tbl = doc.Tables(tblIdx)
    
    ' Look for bullets starting from this row and the rows below it
    Dim r As Integer
    Dim startRow As Integer
    startRow = rowIdx
    
    ' Check current row and subsequent rows
    For r = startRow To tbl.Rows.Count
        On Error Resume Next
        Dim cellRange As Range
        Set cellRange = tbl.Cell(r, 1).Range
        On Error GoTo 0
        
        If cellRange Is Nothing Then GoTo NextRow
        
        Dim para As Paragraph
        For Each para In cellRange.Paragraphs
            If IsBulletParagraph(para) Then
                Dim bulletText As String
                bulletText = CleanText(para.Range.Text)
                If Len(bulletText) > 3 Then
                    ' Store as "text||tableIdx||rowIdx||paraStart||paraEnd"
                    bullets.Add bulletText & "||" & CStr(tblIdx) & "||" & CStr(r) & "||" & CStr(para.Range.Start) & "||" & CStr(para.Range.End)
                End If
            End If
        Next para
        
        ' Stop if we hit the next job header (bold line with |)
        If r > startRow Then
            Dim nextCellText As String
            On Error Resume Next
            nextCellText = CleanText(tbl.Cell(r, 1).Range.Text)
            On Error GoTo 0
            
            Dim nextIsBold As Boolean
            On Error Resume Next
            nextIsBold = tbl.Cell(r, 1).Range.Font.Bold
            On Error GoTo 0
            
            If nextIsBold And InStr(nextCellText, " | ") > 0 And Len(nextCellText) < 120 Then
                Exit For ' Hit next job
            End If
        End If
NextRow:
    Next r
    
    ' Also check nested tables in those rows
    ' (Pairwire bullets are in a nested table)
    For r = startRow To tbl.Rows.Count
        On Error Resume Next
        Set cellRange = tbl.Cell(r, 1).Range
        On Error GoTo 0
        
        If cellRange Is Nothing Then GoTo NextRow2
        
        Dim nestedTbl As Table
        For Each nestedTbl In cellRange.Tables
            Dim nr As Integer
            For nr = 1 To nestedTbl.Rows.Count
                On Error Resume Next
                Dim nestedRange As Range
                Set nestedRange = nestedTbl.Cell(nr, 1).Range
                On Error GoTo 0
                
                If Not nestedRange Is Nothing Then
                    For Each para In nestedRange.Paragraphs
                        If IsBulletParagraph(para) Then
                            bulletText = CleanText(para.Range.Text)
                            If Len(bulletText) > 3 Then
                                bullets.Add bulletText & "||" & CStr(tblIdx) & "||" & CStr(r) & "||" & CStr(para.Range.Start) & "||" & CStr(para.Range.End)
                            End If
                        End If
                    Next para
                End If
            Next nr
        Next nestedTbl
NextRow2:
    Next r
    
    Set GetBulletsForJob = bullets
End Function


' ============================================================
' SELECT BULLET DIALOG
' ============================================================
Private Function SelectBullet(jobEntry As String, title As String) As String
    Dim bullets As Collection
    Set bullets = GetBulletsForJob(jobEntry)
    
    If bullets.Count = 0 Then
        MsgBox "No bullets found for this job!", vbExclamation
        SelectBullet = ""
        Exit Function
    End If
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    " & title & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To bullets.Count
        Dim parts() As String
        parts = Split(bullets(i), "||")
        msg = msg & i & ". " & Left(parts(0), 80) & vbCrLf
        If Len(parts(0)) > 80 Then
            msg = msg & "   ..." & Mid(parts(0), 81, 80) & vbCrLf
        End If
    Next i
    
    msg = msg & vbCrLf & "Enter number (0=cancel):"
    
    Dim result As String
    result = InputBox(msg, title)
    
    If result = "" Or Val(result) = 0 Or Val(result) > bullets.Count Then
        SelectBullet = ""
    Else
        SelectBullet = bullets(Val(result))
    End If
End Function


' ============================================================
' EDIT BULLET FLOW
' ============================================================
Sub EditBulletFlow()
    On Error GoTo ErrHandler
    
    ' Step 1: Select job
    Dim jobEntry As String
    jobEntry = SelectJob("EDIT BULLET - Select Job")
    If jobEntry = "" Then Exit Sub
    
    ' Step 2: Select bullet
    Dim bulletEntry As String
    bulletEntry = SelectBullet(jobEntry, "EDIT BULLET - Select Bullet")
    If bulletEntry = "" Then Exit Sub
    
    ' Step 3: Show current text and get new text
    Dim parts() As String
    parts = Split(bulletEntry, "||")
    
    Dim currentText As String
    currentText = parts(0)
    
    Dim newText As String
    newText = InputBox("Current bullet:" & vbCrLf & vbCrLf & _
        currentText & vbCrLf & vbCrLf & _
        "Enter new text (or leave empty to cancel):", _
        "Edit Bullet", currentText)
    
    If newText = "" Or newText = currentText Then Exit Sub
    
    ' Step 4: Find and replace the text
    Dim paraStart As Long
    Dim paraEnd As Long
    paraStart = CLng(parts(3))
    paraEnd = CLng(parts(4))
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim rng As Range
    Set rng = doc.Range(paraStart, paraEnd - 1) ' -1 to exclude paragraph mark
    
    ' Replace the text content
    rng.Text = newText
    
    ' Reapply formatting
    With rng.Font
        .Name = BODY_FONT
        .Size = BODY_SIZE
        .Bold = False
    End With
    
    MsgBox "Bullet updated!", vbInformation, "Success"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description & vbCrLf & vbCrLf & _
           "Try placing your cursor in the document and running again.", _
           vbExclamation, "Error"
End Sub


' ============================================================
' ADD BULLET FLOW
' ============================================================
Sub AddBulletFlow()
    On Error GoTo ErrHandler
    
    ' Step 1: Select job
    Dim jobEntry As String
    jobEntry = SelectJob("ADD BULLET - Select Job")
    If jobEntry = "" Then Exit Sub
    
    ' Step 2: Get existing bullets to find insertion point
    Dim bullets As Collection
    Set bullets = GetBulletsForJob(jobEntry)
    
    ' Step 3: Get new bullet text
    Dim msg As String
    msg = "Add bullet to: " & Split(jobEntry, "||")(1) & vbCrLf & vbCrLf
    msg = msg & "Current bullets: " & bullets.Count & vbCrLf & vbCrLf
    msg = msg & "TIPS:" & vbCrLf
    msg = msg & "- Start with action verb" & vbCrLf
    msg = msg & "- Include numbers/metrics" & vbCrLf
    msg = msg & "- Keep under ~140 chars for 1 line" & vbCrLf & vbCrLf
    msg = msg & "Enter bullet text:"
    
    Dim newText As String
    newText = InputBox(msg, "Add Bullet")
    If newText = "" Then Exit Sub
    
    ' Step 4: Find the last bullet's range and insert after it
    If bullets.Count > 0 Then
        Dim lastBullet As String
        lastBullet = bullets(bullets.Count)
        Dim parts() As String
        parts = Split(lastBullet, "||")
        
        Dim paraEnd As Long
        paraEnd = CLng(parts(4))
        
        Dim doc As Document
        Set doc = ActiveDocument
        
        ' Position cursor at end of last bullet
        Dim rng As Range
        Set rng = doc.Range(paraEnd - 1, paraEnd - 1)
        
        ' Insert new paragraph
        rng.InsertAfter vbCr
        
        ' Move to new paragraph
        Set rng = doc.Range(paraEnd, paraEnd + Len(newText))
        rng.Text = newText
        
        ' Apply bullet formatting
        With rng
            .Font.Name = BODY_FONT
            .Font.Size = BODY_SIZE
            .Font.Bold = False
            .ListFormat.ApplyBulletDefault
        End With
        
        MsgBox "Bullet added!" & vbCrLf & vbCrLf & _
               "NOTE: You may need to manually adjust" & vbCrLf & _
               "the bullet character to '-' and check indent.", _
               vbInformation, "Success"
    Else
        MsgBox "No existing bullets found to insert after." & vbCrLf & _
               "Please add the bullet manually.", vbExclamation
    End If
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Error"
End Sub


' ============================================================
' DELETE BULLET FLOW
' ============================================================
Sub DeleteBulletFlow()
    On Error GoTo ErrHandler
    
    ' Step 1: Select job
    Dim jobEntry As String
    jobEntry = SelectJob("DELETE BULLET - Select Job")
    If jobEntry = "" Then Exit Sub
    
    ' Step 2: Select bullet
    Dim bulletEntry As String
    bulletEntry = SelectBullet(jobEntry, "DELETE BULLET")
    If bulletEntry = "" Then Exit Sub
    
    ' Step 3: Confirm
    Dim parts() As String
    parts = Split(bulletEntry, "||")
    
    If MsgBox("Delete this bullet?" & vbCrLf & vbCrLf & _
              Left(parts(0), 100), _
              vbYesNo + vbQuestion, "Confirm Delete") = vbNo Then
        Exit Sub
    End If
    
    ' Step 4: Delete the paragraph
    Dim paraStart As Long
    Dim paraEnd As Long
    paraStart = CLng(parts(3))
    paraEnd = CLng(parts(4))
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim rng As Range
    Set rng = doc.Range(paraStart, paraEnd)
    rng.Delete
    
    MsgBox "Bullet deleted!", vbInformation, "Success"
    Exit Sub
    
ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Error"
End Sub


' ============================================================
' ALIGN ALL BULLETS
' ============================================================
' This is the VBA port of the Python indent normalization.
' It makes all bullet dashes align vertically across all tables.
Sub AlignAllBullets()
    On Error GoTo ErrHandler
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Target: abs_text = 854 twips, hanging = 425 twips
    ' para_left = 854 - SUM(all ancestor table indents)
    Const TARGET_ABS As Long = 854
    Const TARGET_HANG As Long = 425
    
    Dim fixCount As Integer
    fixCount = 0
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        ' Only process bullet paragraphs
        If para.Range.ListFormat.ListType <> wdListNoNumbering Then
            ' Calculate total table indent for this paragraph
            Dim totalIndent As Long
            totalIndent = GetTotalTableIndent(para.Range)
            
            ' Compute needed paragraph left
            Dim neededLeft As Long
            neededLeft = TARGET_ABS - totalIndent
            
            ' Convert twips to points (1 pt = 20 twips... wait, no)
            ' In VBA: IndentCharWidth is in points, but ParagraphFormat uses points
            ' Actually, ParagraphFormat.LeftIndent is in POINTS
            ' And in OOXML, indent is in TWIPS (1/20 of a point)
            ' So: neededLeft_points = neededLeft / 20
            
            Dim neededLeftPt As Single
            Dim hangPt As Single
            neededLeftPt = CSng(neededLeft) / 20#
            hangPt = CSng(TARGET_HANG) / 20#
            
            ' Set indent
            With para.Format
                .LeftIndent = neededLeftPt
                .FirstLineIndent = -hangPt  ' Negative = hanging
            End With
            
            fixCount = fixCount + 1
        End If
    Next para
    
    MsgBox fixCount & " bullets aligned!" & vbCrLf & vbCrLf & _
           "All dashes should now be on the same vertical line.", _
           vbInformation, "Align Complete"
    Exit Sub

ErrHandler:
    MsgBox "Error: " & Err.Description, vbExclamation, "Error"
End Sub

' Helper: Sum all ancestor table indents for a range
Private Function GetTotalTableIndent(rng As Range) As Long
    Dim total As Long
    total = 0
    
    ' Check if range is inside any tables
    ' VBA makes this tricky — we check via range nesting
    On Error Resume Next
    
    Dim tbl As Table
    Dim checkRange As Range
    Set checkRange = rng.Duplicate
    
    ' Walk up table nesting
    Dim depth As Integer
    depth = 0
    
    Do
        depth = depth + 1
        If depth > 5 Then Exit Do ' Safety limit
        
        Set tbl = Nothing
        Set tbl = checkRange.Tables(1)
        
        If tbl Is Nothing Then Exit Do
        
        ' Get table indent
        ' Table.LeftPadding is cell padding, not table indent
        ' Table.Rows.LeftIndent is the table indent from margin
        Dim tblIndent As Single
        tblIndent = 0
        tblIndent = tbl.Rows(1).LeftIndent
        
        total = total + CLng(tblIndent * 20) ' Convert points to twips
        
        ' Move to parent table's range
        Set checkRange = tbl.Range
        checkRange.Start = checkRange.Start - 1
        
        If checkRange.Start < 0 Then Exit Do
    Loop
    
    On Error GoTo 0
    GetTotalTableIndent = total
End Function


' ============================================================
' FORMAT AS BULLET TEXT (quick formatting)
' ============================================================
Sub FormatAsBulletText()
    If Selection.Type = wdSelectionNormal Then
        With Selection.Font
            .Name = BODY_FONT
            .Size = BODY_SIZE
            .Bold = False
            .Italic = False
        End With
        MsgBox "Formatted as bullet text (" & BODY_FONT & " " & BODY_SIZE & "pt)", vbInformation
    Else
        MsgBox "Select some text first!", vbExclamation
    End If
End Sub


' ============================================================
' QUICK DIAGNOSTICS
' ============================================================
Sub DiagnoseCV()
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim msg As String
    msg = "===== CV DIAGNOSTICS =====" & vbCrLf & vbCrLf
    msg = msg & "File: " & doc.Name & vbCrLf
    msg = msg & "Tables: " & doc.Tables.Count & vbCrLf
    msg = msg & "Paragraphs: " & doc.Paragraphs.Count & vbCrLf & vbCrLf
    
    ' Count bullets
    Dim bulletCount As Integer
    bulletCount = 0
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        If para.Range.ListFormat.ListType <> wdListNoNumbering Then
            bulletCount = bulletCount + 1
        End If
    Next para
    msg = msg & "Bullet paragraphs: " & bulletCount & vbCrLf & vbCrLf
    
    ' Table details
    Dim i As Integer
    For i = 1 To doc.Tables.Count
        Dim tbl As Table
        Set tbl = doc.Tables(i)
        
        On Error Resume Next
        Dim indent As Single
        indent = tbl.Rows(1).LeftIndent
        On Error GoTo 0
        
        Dim nested As Integer
        nested = 0
        On Error Resume Next
        nested = tbl.Tables.Count
        On Error GoTo 0
        
        msg = msg & "Table " & i & ": " & tbl.Rows.Count & " rows"
        msg = msg & ", indent=" & Format(indent, "0.0") & "pt"
        If nested > 0 Then msg = msg & ", " & nested & " nested"
        msg = msg & vbCrLf
    Next i
    
    MsgBox msg, vbInformation, "CV Diagnostics"
End Sub
