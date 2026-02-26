' ============================================================
' CV EDITOR - COMPLETE MENU SYSTEM
' For: TomásBatalha Resume
' ============================================================
' 
' HOW TO INSTALL (Mac):
' 1. Open your CV in Word
' 2. Tools > Macro > Visual Basic Editor
' 3. In left panel, find "ThisDocument" under your document
' 4. Double-click "ThisDocument" to open it
' 5. Paste ALL this code
' 6. Save As .docm (Macro-Enabled Document)
' 7. Close and reopen - menu appears automatically!
'
' ============================================================

Option Explicit

' Global arrays to store sections found in document
Dim SectionNames() As String
Dim SectionCount As Integer

' ============================================================
' MAIN MENU - Entry point
' ============================================================
Sub CVEditor()
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
            Case 7: DatabaseMenu
            Case 8: ResizeCVMenu
            Case 9: ViewStructure
            Case 0: Exit Do
        End Select
    Loop
End Sub

' ============================================================
' MAIN MENU DISPLAY
' ============================================================
Private Function ShowMainMenu() As Integer
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
    msg = msg & "7. Database" & vbCrLf
    msg = msg & "8. Resize CV" & vbCrLf
    msg = msg & "9. View Structure" & vbCrLf & vbCrLf
    msg = msg & "0. Exit" & vbCrLf & vbCrLf
    msg = msg & "Enter choice (0-9):"
    
    Dim result As String
    result = InputBox(msg, "CV Editor")
    
    If result = "" Then
        ShowMainMenu = 0
    Else
        ShowMainMenu = Val(result)
    End If
End Function

' ============================================================
' SCAN DOCUMENT FOR SECTIONS
' ============================================================
Private Sub ScanSections()
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Reset
    SectionCount = 0
    ReDim SectionNames(1 To 10)
    
    ' Known section headers to look for
    Dim knownSections As Variant
    knownSections = Array("WORK EXPERIENCE", "EDUCATION", "LEADERSHIP EXPERIENCE", "SKILLS", "PROJECTS", "CERTIFICATIONS", "LANGUAGES", "INTERESTS")
    
    Dim i As Integer
    Dim rng As Range
    
    For i = LBound(knownSections) To UBound(knownSections)
        Set rng = doc.Content
        With rng.Find
            .Text = CStr(knownSections(i))
            .MatchCase = False
            .MatchWholeWord = False
            If .Execute Then
                SectionCount = SectionCount + 1
                SectionNames(SectionCount) = CStr(knownSections(i))
            End If
        End With
    Next i
    
    ' Resize array to actual count
    If SectionCount > 0 Then
        ReDim Preserve SectionNames(1 To SectionCount)
    End If
End Sub

' ============================================================
' SELECT SECTION DIALOG
' ============================================================
Private Function SelectSection(title As String) As String
    ScanSections
    
    If SectionCount = 0 Then
        MsgBox "No sections found in document!", vbExclamation
        SelectSection = ""
        Exit Function
    End If
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    " & title & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Found " & SectionCount & " sections:" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To SectionCount
        msg = msg & "  " & i & ". " & SectionNames(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter section number (or 0 to cancel):"
    
    Dim result As String
    result = InputBox(msg, title)
    
    If result = "" Or Val(result) = 0 Then
        SelectSection = ""
    ElseIf Val(result) >= 1 And Val(result) <= SectionCount Then
        SelectSection = SectionNames(Val(result))
    Else
        MsgBox "Invalid selection", vbExclamation
        SelectSection = ""
    End If
End Function

' ============================================================
' FIND JOBS IN SECTION
' ============================================================
Private Function GetJobsInSection(sectionName As String) As Variant
    Dim jobs() As String
    ReDim jobs(1 To 20)
    Dim jobCount As Integer
    jobCount = 0
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Find section start
    Dim rng As Range
    Set rng = doc.Content
    
    With rng.Find
        .Text = sectionName
        If Not .Execute Then
            GetJobsInSection = Array()
            Exit Function
        End If
    End With
    
    ' Search for lines with " | " pattern (company | location format)
    Dim searchRng As Range
    Set searchRng = doc.Content
    searchRng.Start = rng.End
    
    ' Find next section to limit search
    Dim nextSectionPos As Long
    nextSectionPos = doc.Content.End
    
    Dim i As Integer
    For i = 1 To SectionCount
        If SectionNames(i) <> sectionName Then
            Dim tempRng As Range
            Set tempRng = doc.Content
            tempRng.Start = rng.End
            With tempRng.Find
                .Text = SectionNames(i)
                If .Execute Then
                    If tempRng.Start < nextSectionPos Then
                        nextSectionPos = tempRng.Start
                    End If
                End If
            End With
        End If
    Next i
    
    ' Now search for job patterns in this range
    Set searchRng = doc.Range(rng.End, nextSectionPos)
    
    Dim para As Paragraph
    For Each para In searchRng.Paragraphs
        Dim txt As String
        txt = Trim(para.Range.Text)
        ' Job lines typically have | and are short (company | location)
        If InStr(txt, " | ") > 0 And Len(txt) < 100 And Len(txt) > 5 Then
            ' Check if it looks like a company line (not a role line with dates)
            If Not (InStr(txt, "20") > 0 And InStr(txt, "–") > 0) Then
                jobCount = jobCount + 1
                If jobCount <= 20 Then
                    jobs(jobCount) = Left(txt, 60)
                End If
            End If
        End If
    Next para
    
    If jobCount > 0 Then
        ReDim Preserve jobs(1 To jobCount)
        GetJobsInSection = jobs
    Else
        GetJobsInSection = Array()
    End If
End Function

' ============================================================
' ADD BULLET MENU
' ============================================================
Sub AddBulletMenu()
    ' Select section
    Dim sectionName As String
    sectionName = SelectSection("ADD BULLET - Select Section")
    If sectionName = "" Then Exit Sub
    
    ' Get jobs in section
    Dim jobs As Variant
    jobs = GetJobsInSection(sectionName)
    
    If Not IsArray(jobs) Or UBound(jobs) < 1 Then
        MsgBox "No jobs found in " & sectionName, vbExclamation
        Exit Sub
    End If
    
    ' Show jobs
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT JOB" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Jobs in " & sectionName & ":" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = LBound(jobs) To UBound(jobs)
        msg = msg & "  " & i & ". " & jobs(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter job number:"
    
    Dim jobChoice As String
    jobChoice = InputBox(msg, "Select Job")
    
    If jobChoice = "" Or Val(jobChoice) < 1 Or Val(jobChoice) > UBound(jobs) Then
        Exit Sub
    End If
    
    Dim selectedJob As String
    selectedJob = jobs(Val(jobChoice))
    
    ' Get bullet text
    Dim bulletMsg As String
    bulletMsg = "-----------------------------------" & vbCrLf
    bulletMsg = bulletMsg & "    ADD BULLET" & vbCrLf
    bulletMsg = bulletMsg & "-----------------------------------" & vbCrLf & vbCrLf
    bulletMsg = bulletMsg & "Adding to: " & selectedJob & vbCrLf & vbCrLf
    bulletMsg = bulletMsg & "TIPS:" & vbCrLf
    bulletMsg = bulletMsg & "- Start with action verb" & vbCrLf
    bulletMsg = bulletMsg & "- Include metrics/numbers" & vbCrLf
    bulletMsg = bulletMsg & "- Keep under 2 lines" & vbCrLf & vbCrLf
    bulletMsg = bulletMsg & "ACTION VERBS:" & vbCrLf
    bulletMsg = bulletMsg & "Built, Led, Designed, Secured," & vbCrLf
    bulletMsg = bulletMsg & "Developed, Launched, Managed," & vbCrLf
    bulletMsg = bulletMsg & "Increased, Reduced, Created" & vbCrLf & vbCrLf
    bulletMsg = bulletMsg & "Enter bullet text:"
    
    Dim bulletText As String
    bulletText = InputBox(bulletMsg, "Add Bullet")
    
    If bulletText = "" Then Exit Sub
    
    ' Find the job and navigate there
    ' Get the bullets for this job so we can find the LAST one
    Dim jobBullets As Variant
    jobBullets = GetBulletsForJob(selectedJob)
    
    If IsArray(jobBullets) And UBound(jobBullets) >= 1 Then
        ' Find the last bullet and insert after it
        Dim lastBullet As String
        lastBullet = jobBullets(UBound(jobBullets))
        
        If NavigateToText(Left(lastBullet, 40)) Then
            ' Move to end of this paragraph and insert
            Selection.EndKey Unit:=wdLine
            InsertBullet bulletText
            
            MsgBox "OK: Bullet added successfully!" & vbCrLf & vbCrLf & _
                   "Added to: " & selectedJob, vbInformation, "Success"
        Else
            ' Fallback: show text to copy
            MsgBox "Could not find last bullet." & vbCrLf & vbCrLf & _
                   "Please manually add this bullet:" & vbCrLf & vbCrLf & _
                   "- " & bulletText, vbInformation, "Manual Add Required"
        End If
    Else
        ' No existing bullets - insert after role line
        If NavigateToJob(selectedJob) Then
            ' Move to role line (next line after company)
            Selection.MoveDown Unit:=wdLine, Count:=1
            Selection.EndKey Unit:=wdLine
            InsertBullet bulletText
            
            MsgBox "OK: Bullet added successfully!" & vbCrLf & vbCrLf & _
                   "Added to: " & selectedJob, vbInformation, "Success"
        Else
            MsgBox "Could not navigate to job." & vbCrLf & vbCrLf & _
                   "Please manually add this bullet:" & vbCrLf & vbCrLf & _
                   "- " & bulletText, vbInformation, "Manual Add Required"
        End If
    End If
End Sub

' ============================================================
' ADD JOB MENU
' ============================================================
Sub AddJobMenu()
    ' Select section
    Dim sectionName As String
    sectionName = SelectSection("ADD NEW JOB - Select Section")
    If sectionName = "" Then Exit Sub
    
    ' Get job details
    Dim msg As String
    
    ' Company
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    NEW JOB - Step 1/5" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Section: " & sectionName & vbCrLf & vbCrLf
    msg = msg & "Enter COMPANY/INSTITUTION name:" & vbCrLf & vbCrLf
    msg = msg & "(e.g., Google, McKinsey, Harvard)"
    
    Dim company As String
    company = InputBox(msg, "New Job - Company")
    If company = "" Then Exit Sub
    
    ' Location
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    NEW JOB - Step 2/5" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Company: " & company & vbCrLf & vbCrLf
    msg = msg & "Enter LOCATION:" & vbCrLf & vbCrLf
    msg = msg & "(e.g., New York, USA)"
    
    Dim location As String
    location = InputBox(msg, "New Job - Location")
    If location = "" Then Exit Sub
    
    ' Role
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    NEW JOB - Step 3/5" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Company: " & company & " | " & location & vbCrLf & vbCrLf
    msg = msg & "Enter ROLE/TITLE:" & vbCrLf & vbCrLf
    msg = msg & "(e.g., Senior Consultant, Co-Founder)"
    
    Dim role As String
    role = InputBox(msg, "New Job - Role")
    If role = "" Then Exit Sub
    
    ' Dates
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    NEW JOB - Step 4/5" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & company & " | " & location & vbCrLf
    msg = msg & role & vbCrLf & vbCrLf
    msg = msg & "Enter DATES:" & vbCrLf & vbCrLf
    msg = msg & "(e.g., January 2024 – Present)"
    
    Dim dates As String
    dates = InputBox(msg, "New Job - Dates")
    If dates = "" Then Exit Sub
    
    ' First bullet
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    NEW JOB - Step 5/5" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & company & " | " & location & vbCrLf
    msg = msg & role & " | " & dates & vbCrLf & vbCrLf
    msg = msg & "Enter FIRST BULLET:" & vbCrLf & vbCrLf
    msg = msg & "(Start with action verb + metrics)"
    
    Dim bullet1 As String
    bullet1 = InputBox(msg, "New Job - First Bullet")
    If bullet1 = "" Then Exit Sub
    
    ' Confirm
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    CONFIRM NEW JOB" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Section: " & sectionName & vbCrLf & vbCrLf
    msg = msg & company & " | " & location & vbCrLf
    msg = msg & role & " | " & dates & vbCrLf
    msg = msg & "- " & bullet1 & vbCrLf & vbCrLf
    msg = msg & "Add this job?"
    
    If MsgBox(msg, vbYesNo + vbQuestion, "Confirm") = vbNo Then Exit Sub
    
    ' Navigate to section and insert
    If NavigateToSection(sectionName) Then
        ' Move past section header
        Selection.MoveDown Unit:=wdLine, Count:=1
        Selection.HomeKey Unit:=wdLine
        
        ' Insert job
        InsertNewJob company, location, role, dates, bullet1
        
        MsgBox "OK: Job added successfully!" & vbCrLf & vbCrLf & _
               company & " | " & location & vbCrLf & _
               role, vbInformation, "Success"
    Else
        ' Fallback
        MsgBox "Could not navigate automatically." & vbCrLf & vbCrLf & _
               "Please manually add:" & vbCrLf & vbCrLf & _
               company & " | " & location & vbCrLf & _
               role & " | " & dates & vbCrLf & _
               "- " & bullet1, vbInformation, "Manual Add Required"
    End If
End Sub

' ============================================================
' EDIT BULLET MENU
' ============================================================
Sub EditBulletMenu()
    MsgBox "EDIT BULLET" & vbCrLf & vbCrLf & _
           "1. Select the bullet text you want to edit" & vbCrLf & _
           "2. Type your new text" & vbCrLf & vbCrLf & _
           "Tip: Use Find & Replace (Ctrl+H) for" & vbCrLf & _
           "quick edits across multiple bullets.", _
           vbInformation, "Edit Bullet"
End Sub

' ============================================================
' DELETE BULLET MENU
' ============================================================
Sub DeleteBulletMenu()
    ' Step 1: Select section
    Dim sectionName As String
    sectionName = SelectSection("DELETE BULLET - Select Section")
    If sectionName = "" Then Exit Sub
    
    ' Step 2: Get jobs in section
    Dim jobs As Variant
    jobs = GetJobsInSection(sectionName)
    
    If Not IsArray(jobs) Or UBound(jobs) < 1 Then
        MsgBox "No jobs found in " & sectionName, vbExclamation
        Exit Sub
    End If
    
    ' Show jobs
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT JOB" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Jobs in " & sectionName & ":" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = LBound(jobs) To UBound(jobs)
        msg = msg & "  " & i & ". " & jobs(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter job number:"
    
    Dim jobChoice As String
    jobChoice = InputBox(msg, "Select Job")
    
    If jobChoice = "" Or Val(jobChoice) < 1 Or Val(jobChoice) > UBound(jobs) Then
        Exit Sub
    End If
    
    Dim selectedJob As String
    selectedJob = jobs(Val(jobChoice))
    
    ' Step 3: Get bullets for this job
    Dim bullets As Variant
    bullets = GetBulletsForJob(selectedJob)
    
    If Not IsArray(bullets) Or UBound(bullets) < 1 Then
        MsgBox "No bullets found for " & selectedJob, vbExclamation
        Exit Sub
    End If
    
    ' Show bullets
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT BULLET TO DELETE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Job: " & selectedJob & vbCrLf & vbCrLf
    msg = msg & "Bullets:" & vbCrLf & vbCrLf
    
    For i = LBound(bullets) To UBound(bullets)
        msg = msg & "  " & i & ". " & Left(bullets(i), 50) & "..." & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter bullet number to DELETE:"
    
    Dim bulletChoice As String
    bulletChoice = InputBox(msg, "Select Bullet")
    
    If bulletChoice = "" Or Val(bulletChoice) < 1 Or Val(bulletChoice) > UBound(bullets) Then
        Exit Sub
    End If
    
    Dim selectedBullet As String
    selectedBullet = bullets(Val(bulletChoice))
    
    ' Confirm deletion
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    CONFIRM DELETE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Are you sure you want to DELETE:" & vbCrLf & vbCrLf
    msg = msg & Chr(34) & Left(selectedBullet, 80) & "..." & Chr(34) & vbCrLf & vbCrLf
    msg = msg & "This cannot be undone!"
    
    If MsgBox(msg, vbYesNo + vbExclamation, "Confirm Delete") = vbNo Then Exit Sub
    
    ' Save to database BEFORE deleting
    SaveToDatabase "BULLET", selectedBullet, selectedJob
    
    ' Find and delete the bullet
    If DeleteBullet(selectedBullet) Then
        MsgBox "OK: Bullet deleted!" & vbCrLf & vbCrLf & _
               "Saved to database - you can restore it later" & vbCrLf & _
               "via Swap Bullet or Database menu.", vbInformation, "Success"
    Else
        MsgBox "Could not delete automatically." & vbCrLf & vbCrLf & _
               "Please manually find and delete:" & vbCrLf & vbCrLf & _
               Left(selectedBullet, 60) & "...", vbInformation, "Manual Delete Required"
    End If
End Sub

' ============================================================
' GET BULLETS FOR A JOB
' ============================================================
Private Function GetBulletsForJob(jobText As String) As Variant
    Dim bullets() As String
    ReDim bullets(1 To 20)
    Dim bulletCount As Integer
    bulletCount = 0
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Extract company name to search for
    Dim searchText As String
    If InStr(jobText, " | ") > 0 Then
        searchText = Trim(Left(jobText, InStr(jobText, " | ") - 1))
    Else
        searchText = Left(jobText, 30)
    End If
    
    ' Find the job
    Dim rng As Range
    Set rng = doc.Content
    
    With rng.Find
        .Text = searchText
        .MatchCase = False
        If Not .Execute Then
            GetBulletsForJob = Array()
            Exit Function
        End If
    End With
    
    ' Now look at paragraphs after the job until we hit next job/section
    Dim searchRng As Range
    Set searchRng = doc.Content
    searchRng.Start = rng.End
    
    Dim para As Paragraph
    Dim foundRole As Boolean
    foundRole = False
    
    For Each para In searchRng.Paragraphs
        Dim txt As String
        txt = Trim(para.Range.Text)
        
        ' Skip role line (has dates)
        If InStr(txt, "20") > 0 And (InStr(txt, "–") > 0 Or InStr(txt, "-") > 0) And Len(txt) < 100 Then
            foundRole = True
            GoTo NextPara
        End If
        
        ' Check if we hit next job or section (stop)
        If InStr(txt, " | ") > 0 And Len(txt) < 100 And Len(txt) > 5 Then
            If Not (InStr(txt, "20") > 0 And InStr(txt, "–") > 0) Then
                Exit For
            End If
        End If
        
        ' Check for section header
        If UCase(Left(Trim(txt), 5)) = Left(Trim(txt), 5) And Len(Trim(txt)) > 5 Then
            If InStr(txt, "EXPERIENCE") > 0 Or InStr(txt, "EDUCATION") > 0 Or InStr(txt, "SKILLS") > 0 Or InStr(txt, "LEADERSHIP") > 0 Then
                Exit For
            End If
        End If
        
        ' This looks like a bullet (starts with - or has substantial text after role)
        If Len(txt) > 20 And foundRole Then
            ' Clean up the text (remove bullet char if present)
            If Left(txt, 1) = "-" Then txt = Trim(Mid(txt, 2))
            If Left(txt, 1) = Chr(9) Then txt = Trim(Mid(txt, 2))
            
            bulletCount = bulletCount + 1
            If bulletCount <= 20 Then
                bullets(bulletCount) = txt
            End If
        End If
        
NextPara:
    Next para
    
    If bulletCount > 0 Then
        ReDim Preserve bullets(1 To bulletCount)
        GetBulletsForJob = bullets
    Else
        GetBulletsForJob = Array()
    End If
End Function

' ============================================================
' DELETE JOB MENU
' ============================================================
Sub DeleteJobMenu()
    ' Step 1: Select section
    Dim sectionName As String
    sectionName = SelectSection("DELETE JOB - Select Section")
    If sectionName = "" Then Exit Sub
    
    ' Step 2: Get jobs in section
    Dim jobs As Variant
    jobs = GetJobsInSection(sectionName)
    
    If Not IsArray(jobs) Or UBound(jobs) < 1 Then
        MsgBox "No jobs found in " & sectionName, vbExclamation
        Exit Sub
    End If
    
    ' Show jobs
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT JOB TO DELETE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Jobs in " & sectionName & ":" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = LBound(jobs) To UBound(jobs)
        msg = msg & "  " & i & ". " & jobs(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter job number to DELETE:"
    
    Dim jobChoice As String
    jobChoice = InputBox(msg, "Select Job")
    
    If jobChoice = "" Or Val(jobChoice) < 1 Or Val(jobChoice) > UBound(jobs) Then
        Exit Sub
    End If
    
    Dim selectedJob As String
    selectedJob = jobs(Val(jobChoice))
    
    ' Get bullet count for confirmation
    Dim bullets As Variant
    bullets = GetBulletsForJob(selectedJob)
    Dim bulletCount As Integer
    If IsArray(bullets) And UBound(bullets) >= 1 Then
        bulletCount = UBound(bullets)
    Else
        bulletCount = 0
    End If
    
    ' Confirm deletion
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    CONFIRM DELETE JOB" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Are you sure you want to DELETE:" & vbCrLf & vbCrLf
    msg = msg & Chr(34) & selectedJob & Chr(34) & vbCrLf & vbCrLf
    msg = msg & "This will remove:" & vbCrLf
    msg = msg & "  - Company line" & vbCrLf
    msg = msg & "  - Role/dates line" & vbCrLf
    msg = msg & "  - " & bulletCount & " bullet(s)" & vbCrLf & vbCrLf
    msg = msg & "This cannot be undone!"
    
    If MsgBox(msg, vbYesNo + vbExclamation, "Confirm Delete") = vbNo Then Exit Sub
    
    ' Find and delete the entire job
    If DeleteJob(selectedJob) Then
        MsgBox "OK: Job deleted successfully!" & vbCrLf & vbCrLf & _
               "Removed: " & selectedJob, vbInformation, "Success"
    Else
        MsgBox "Could not delete automatically." & vbCrLf & vbCrLf & _
               "Please manually find and delete:" & vbCrLf & vbCrLf & _
               selectedJob, vbInformation, "Manual Delete Required"
    End If
End Sub

' ============================================================
' DELETE A JOB (company + role + all bullets)
' ============================================================
Private Function DeleteJob(jobText As String) As Boolean
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Extract company name to search for
    Dim searchText As String
    If InStr(jobText, " | ") > 0 Then
        searchText = Trim(Left(jobText, InStr(jobText, " | ") - 1))
    Else
        searchText = Left(jobText, 30)
    End If
    
    ' Find the company line
    Dim rng As Range
    Set rng = doc.Content
    
    With rng.Find
        .Text = searchText
        .MatchCase = False
        If Not .Execute Then
            DeleteJob = False
            Exit Function
        End If
    End With
    
    ' Expand to paragraph (company line)
    rng.Expand Unit:=wdParagraph
    Dim startPos As Long
    startPos = rng.Start
    
    ' Now find where this job ends (next job or section)
    Dim endPos As Long
    endPos = rng.End
    
    ' Look through subsequent paragraphs
    Dim searchRng As Range
    Set searchRng = doc.Content
    searchRng.Start = rng.End
    
    Dim para As Paragraph
    Dim foundRole As Boolean
    foundRole = False
    
    For Each para In searchRng.Paragraphs
        Dim txt As String
        txt = Trim(para.Range.Text)
        
        ' Skip empty lines
        If Len(txt) < 3 Then
            endPos = para.Range.End
            GoTo NextJobPara
        End If
        
        ' Role line (has dates) - include it
        If InStr(txt, "20") > 0 And (InStr(txt, Chr(150)) > 0 Or InStr(txt, "-") > 0) And Len(txt) < 100 Then
            foundRole = True
            endPos = para.Range.End
            GoTo NextJobPara
        End If
        
        ' Check if we hit next job (has | but no dates = company line)
        If InStr(txt, " | ") > 0 And Len(txt) < 100 And Len(txt) > 5 Then
            If Not (InStr(txt, "20") > 0 And (InStr(txt, Chr(150)) > 0 Or InStr(txt, "-") > 0)) Then
                Exit For
            End If
        End If
        
        ' Check for section header (all caps keywords)
        If InStr(txt, "EXPERIENCE") > 0 Or InStr(txt, "EDUCATION") > 0 Or _
           InStr(txt, "SKILLS") > 0 Or InStr(txt, "LEADERSHIP") > 0 Or _
           InStr(txt, "PROJECTS") > 0 Or InStr(txt, "CERTIFICATIONS") > 0 Then
            Exit For
        End If
        
        ' This is a bullet - include it
        If Len(txt) > 10 And foundRole Then
            endPos = para.Range.End
        End If
        
NextJobPara:
    Next para
    
    ' Delete the entire range
    Set rng = doc.Range(startPos, endPos)
    rng.Select
    Selection.Delete
    
    DeleteJob = True
End Function

' ============================================================
' DELETE A BULLET
' ============================================================
Private Function DeleteBullet(bulletText As String) As Boolean
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Search for first 40 chars of bullet
    Dim searchText As String
    searchText = Left(bulletText, 40)
    
    Dim rng As Range
    Set rng = doc.Content
    
    With rng.Find
        .Text = searchText
        .MatchCase = False
        If .Execute Then
            ' Expand to full paragraph
            rng.Expand Unit:=wdParagraph
            rng.Select
            
            ' Delete the paragraph
            Selection.Delete
            
            DeleteBullet = True
        Else
            DeleteBullet = False
        End If
    End With
End Function

' ============================================================
' SWAP BULLET MENU
' ============================================================
Sub SwapBulletMenu()
    ' Step 1: Select section
    Dim sectionName As String
    sectionName = SelectSection("SWAP BULLET - Select Section")
    If sectionName = "" Then Exit Sub
    
    ' Step 2: Get jobs in section
    Dim jobs As Variant
    jobs = GetJobsInSection(sectionName)
    
    If Not IsArray(jobs) Or UBound(jobs) < 1 Then
        MsgBox "No jobs found in " & sectionName, vbExclamation
        Exit Sub
    End If
    
    ' Show jobs
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT JOB" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = LBound(jobs) To UBound(jobs)
        msg = msg & "  " & i & ". " & jobs(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter job number:"
    
    Dim jobChoice As String
    jobChoice = InputBox(msg, "Select Job")
    
    If jobChoice = "" Or Val(jobChoice) < 1 Or Val(jobChoice) > UBound(jobs) Then
        Exit Sub
    End If
    
    Dim selectedJob As String
    selectedJob = jobs(Val(jobChoice))
    
    ' Step 3: Get bullets for this job
    Dim bullets As Variant
    bullets = GetBulletsForJob(selectedJob)
    
    If Not IsArray(bullets) Or UBound(bullets) < 1 Then
        MsgBox "No bullets found for " & selectedJob, vbExclamation
        Exit Sub
    End If
    
    ' Show bullets
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT BULLET TO SWAP OUT" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Job: " & selectedJob & vbCrLf & vbCrLf
    
    For i = LBound(bullets) To UBound(bullets)
        msg = msg & "  " & i & ". " & Left(bullets(i), 45) & "..." & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter bullet number:"
    
    Dim bulletChoice As String
    bulletChoice = InputBox(msg, "Select Bullet")
    
    If bulletChoice = "" Or Val(bulletChoice) < 1 Or Val(bulletChoice) > UBound(bullets) Then
        Exit Sub
    End If
    
    Dim oldBullet As String
    oldBullet = bullets(Val(bulletChoice))
    
    ' Step 4: Show database bullets or enter new
    Dim dbBullets As Variant
    dbBullets = GetDatabaseBullets()
    
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT REPLACEMENT" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Swapping out:" & vbCrLf
    msg = msg & Left(oldBullet, 50) & "..." & vbCrLf & vbCrLf
    
    If IsArray(dbBullets) And UBound(dbBullets) >= 1 Then
        msg = msg & "FROM DATABASE:" & vbCrLf
        For i = LBound(dbBullets) To UBound(dbBullets)
            msg = msg & "  " & i & ". " & Left(dbBullets(i), 40) & "..." & vbCrLf
        Next i
        msg = msg & vbCrLf & "Or enter 0 to type new bullet" & vbCrLf
        msg = msg & "Enter choice:"
        
        Dim dbChoice As String
        dbChoice = InputBox(msg, "Select Replacement")
        
        If dbChoice = "" Then Exit Sub
        
        Dim newBullet As String
        If Val(dbChoice) = 0 Then
            newBullet = InputBox("Enter new bullet text:", "New Bullet")
            If newBullet = "" Then Exit Sub
        ElseIf Val(dbChoice) >= 1 And Val(dbChoice) <= UBound(dbBullets) Then
            newBullet = dbBullets(Val(dbChoice))
            ' Remove from database
            RemoveFromDatabase "BULLET", newBullet
        Else
            Exit Sub
        End If
    Else
        msg = msg & "No bullets in database." & vbCrLf & vbCrLf
        msg = msg & "Enter new bullet text:"
        newBullet = InputBox(msg, "New Bullet")
        If newBullet = "" Then Exit Sub
    End If
    
    ' Perform swap
    If SwapBulletText(oldBullet, newBullet) Then
        ' Save old bullet to database
        SaveToDatabase "BULLET", oldBullet, selectedJob
        MsgBox "OK: Bullet swapped!" & vbCrLf & vbCrLf & _
               "Old bullet saved to database.", vbInformation, "Success"
    Else
        MsgBox "Could not swap automatically.", vbExclamation
    End If
End Sub

' ============================================================
' SWAP JOB MENU
' ============================================================
Sub SwapJobMenu()
    ' Step 1: Select section
    Dim sectionName As String
    sectionName = SelectSection("SWAP JOB - Select Section")
    If sectionName = "" Then Exit Sub
    
    ' Get jobs in section
    Dim jobs As Variant
    jobs = GetJobsInSection(sectionName)
    
    If Not IsArray(jobs) Or UBound(jobs) < 1 Then
        MsgBox "No jobs found in " & sectionName, vbExclamation
        Exit Sub
    End If
    
    ' Show jobs
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT JOB TO SWAP OUT" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = LBound(jobs) To UBound(jobs)
        msg = msg & "  " & i & ". " & jobs(i) & vbCrLf
    Next i
    
    msg = msg & vbCrLf & "Enter job number:"
    
    Dim jobChoice As String
    jobChoice = InputBox(msg, "Select Job")
    
    If jobChoice = "" Or Val(jobChoice) < 1 Or Val(jobChoice) > UBound(jobs) Then
        Exit Sub
    End If
    
    Dim oldJob As String
    oldJob = jobs(Val(jobChoice))
    
    ' Get full job data before deleting
    Dim oldJobBullets As Variant
    oldJobBullets = GetBulletsForJob(oldJob)
    
    ' Show database jobs
    Dim dbJobs As Variant
    dbJobs = GetDatabaseJobs()
    
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    SELECT REPLACEMENT JOB" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Swapping out: " & oldJob & vbCrLf & vbCrLf
    
    If IsArray(dbJobs) And UBound(dbJobs) >= 1 Then
        msg = msg & "FROM DATABASE:" & vbCrLf
        For i = LBound(dbJobs) To UBound(dbJobs)
            msg = msg & "  " & i & ". " & Left(dbJobs(i), 50) & vbCrLf
        Next i
        msg = msg & vbCrLf & "Or enter 0 to add new job" & vbCrLf
        msg = msg & "Enter choice:"
        
        Dim dbChoice As String
        dbChoice = InputBox(msg, "Select Replacement")
        
        If dbChoice = "" Then Exit Sub
        
        If Val(dbChoice) = 0 Then
            ' Save current job to database first
            SaveJobToDatabase oldJob, oldJobBullets
            ' Delete current job
            DeleteJob oldJob
            ' Navigate and add new job
            AddJobMenu
            Exit Sub
        ElseIf Val(dbChoice) >= 1 And Val(dbChoice) <= UBound(dbJobs) Then
            ' Get job from database
            Dim newJobData As String
            newJobData = GetFullJobFromDatabase(Val(dbChoice))
            
            ' Save current to database
            SaveJobToDatabase oldJob, oldJobBullets
            
            ' Delete old job
            DeleteJob oldJob
            
            ' Insert new job from database
            InsertJobFromDatabase newJobData, sectionName
            
            ' Remove from database
            RemoveJobFromDatabase Val(dbChoice)
            
            MsgBox "OK: Job swapped!" & vbCrLf & vbCrLf & _
                   "Old job saved to database.", vbInformation, "Success"
        End If
    Else
        msg = msg & "No jobs in database." & vbCrLf & vbCrLf
        msg = msg & "Enter 1 to add new job, or cancel:"
        
        If InputBox(msg, "No Database Jobs") = "1" Then
            SaveJobToDatabase oldJob, oldJobBullets
            DeleteJob oldJob
            AddJobMenu
        End If
    End If
End Sub

' ============================================================
' DATABASE MENU
' ============================================================
Sub DatabaseMenu()
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    CV DATABASE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "1. View Stored Bullets" & vbCrLf
    msg = msg & "2. View Stored Jobs" & vbCrLf
    msg = msg & "3. Add Bullet to Database" & vbCrLf
    msg = msg & "4. Clear Database" & vbCrLf & vbCrLf
    msg = msg & "0. Back" & vbCrLf & vbCrLf
    msg = msg & "Enter choice:"
    
    Dim choice As String
    choice = InputBox(msg, "Database")
    
    Select Case Val(choice)
        Case 1: ViewDatabaseBullets
        Case 2: ViewDatabaseJobs
        Case 3: AddBulletToDatabase
        Case 4: ClearDatabase
    End Select
End Sub

' ============================================================
' RESIZE CV MENU
' ============================================================
Sub ResizeCVMenu()
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    RESIZE CV" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Need more space? Shrink elements." & vbCrLf
    msg = msg & "Too sparse? Grow elements." & vbCrLf & vbCrLf
    msg = msg & "1. Shrink Bullets    (font -0.5pt)" & vbCrLf
    msg = msg & "2. Grow Bullets      (font +0.5pt)" & vbCrLf
    msg = msg & "3. Shrink Jobs       (font -0.5pt)" & vbCrLf
    msg = msg & "4. Grow Jobs         (font +0.5pt)" & vbCrLf
    msg = msg & "5. Shrink Margins    (-0.1 inch)" & vbCrLf
    msg = msg & "6. Grow Margins      (+0.1 inch)" & vbCrLf
    msg = msg & "7. Shrink Line Space (-0.5pt)" & vbCrLf
    msg = msg & "8. Grow Line Space   (+0.5pt)" & vbCrLf
    msg = msg & "9. SHRINK ALL        (compact mode)" & vbCrLf & vbCrLf
    msg = msg & "0. Back" & vbCrLf & vbCrLf
    msg = msg & "Enter choice:"
    
    Dim choice As String
    choice = InputBox(msg, "Resize CV")
    
    Select Case Val(choice)
        Case 1: ResizeBullets -0.5
        Case 2: ResizeBullets 0.5
        Case 3: ResizeJobs -0.5
        Case 4: ResizeJobs 0.5
        Case 5: ResizeMargins -0.1
        Case 6: ResizeMargins 0.1
        Case 7: ResizeLineSpacing -0.5
        Case 8: ResizeLineSpacing 0.5
        Case 9: ShrinkAll
    End Select
End Sub

' ============================================================
' RESIZE FUNCTIONS
' ============================================================
Private Sub ResizeBullets(delta As Single)
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim para As Paragraph
    Dim count As Integer
    count = 0
    
    For Each para In doc.Paragraphs
        Dim txt As String
        txt = Trim(para.Range.Text)
        ' Bullets are longer lines (>30 chars) that don't have |
        If Len(txt) > 30 And InStr(txt, " | ") = 0 Then
            Dim newSize As Single
            newSize = para.Range.Font.Size + delta
            If newSize >= 6 And newSize <= 12 Then
                para.Range.Font.Size = newSize
                count = count + 1
            End If
        End If
    Next para
    
    MsgBox "OK: Resized " & count & " bullets" & vbCrLf & _
           "New size: " & Format(newSize, "0.0") & "pt", vbInformation
End Sub

Private Sub ResizeJobs(delta As Single)
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim para As Paragraph
    Dim count As Integer
    count = 0
    
    For Each para In doc.Paragraphs
        Dim txt As String
        txt = Trim(para.Range.Text)
        ' Job lines have | and are short
        If InStr(txt, " | ") > 0 And Len(txt) < 100 Then
            Dim newSize As Single
            newSize = para.Range.Font.Size + delta
            If newSize >= 6 And newSize <= 12 Then
                para.Range.Font.Size = newSize
                count = count + 1
            End If
        End If
    Next para
    
    MsgBox "OK: Resized " & count & " job lines" & vbCrLf & _
           "New size: " & Format(newSize, "0.0") & "pt", vbInformation
End Sub

Private Sub ResizeMargins(delta As Single)
    With ActiveDocument.PageSetup
        Dim newMargin As Single
        newMargin = .LeftMargin + InchesToPoints(delta)
        If newMargin >= InchesToPoints(0.3) And newMargin <= InchesToPoints(1.5) Then
            .LeftMargin = newMargin
            .RightMargin = newMargin
        End If
    End With
    
    MsgBox "OK: Margins adjusted by " & delta & " inch", vbInformation
End Sub

Private Sub ResizeLineSpacing(delta As Single)
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        Dim newSpace As Single
        newSpace = para.Range.ParagraphFormat.SpaceAfter + delta
        If newSpace >= 0 And newSpace <= 12 Then
            para.Range.ParagraphFormat.SpaceAfter = newSpace
        End If
    Next para
    
    MsgBox "OK: Line spacing adjusted", vbInformation
End Sub

Private Sub ShrinkAll()
    Dim msg As String
    msg = "SHRINK ALL will:" & vbCrLf & vbCrLf
    msg = msg & "- Reduce all fonts by 0.5pt" & vbCrLf
    msg = msg & "- Reduce margins by 0.1 inch" & vbCrLf
    msg = msg & "- Reduce line spacing" & vbCrLf & vbCrLf
    msg = msg & "Continue?"
    
    If MsgBox(msg, vbYesNo + vbQuestion) = vbNo Then Exit Sub
    
    ' Shrink all fonts
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        If para.Range.Font.Size > 6 Then
            para.Range.Font.Size = para.Range.Font.Size - 0.5
        End If
        If para.Range.ParagraphFormat.SpaceAfter > 0 Then
            para.Range.ParagraphFormat.SpaceAfter = para.Range.ParagraphFormat.SpaceAfter - 0.5
        End If
    Next para
    
    ' Shrink margins
    With doc.PageSetup
        If .LeftMargin > InchesToPoints(0.4) Then
            .LeftMargin = .LeftMargin - InchesToPoints(0.1)
            .RightMargin = .RightMargin - InchesToPoints(0.1)
        End If
        If .TopMargin > InchesToPoints(0.4) Then
            .TopMargin = .TopMargin - InchesToPoints(0.1)
            .BottomMargin = .BottomMargin - InchesToPoints(0.1)
        End If
    End With
    
    MsgBox "OK: CV compacted!" & vbCrLf & vbCrLf & _
           "Run again if you need more space.", vbInformation
End Sub

' ============================================================
' DATABASE STORAGE FUNCTIONS
' Uses document variables to store data
' ============================================================
Private Sub SaveToDatabase(itemType As String, content As String, context As String)
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Get current count
    Dim countVar As String
    countVar = "DB_" & itemType & "_COUNT"
    
    Dim count As Integer
    On Error Resume Next
    count = Val(doc.Variables(countVar).Value)
    On Error GoTo 0
    
    count = count + 1
    
    ' Store the item
    doc.Variables(countVar).Value = CStr(count)
    doc.Variables("DB_" & itemType & "_" & count).Value = content
    doc.Variables("DB_" & itemType & "_" & count & "_CTX").Value = context
    
    doc.Save
End Sub

Private Sub SaveJobToDatabase(jobHeader As String, bullets As Variant)
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Get current count
    Dim count As Integer
    On Error Resume Next
    count = Val(doc.Variables("DB_JOB_COUNT").Value)
    On Error GoTo 0
    
    count = count + 1
    
    ' Store job header
    doc.Variables("DB_JOB_COUNT").Value = CStr(count)
    doc.Variables("DB_JOB_" & count & "_HEADER").Value = jobHeader
    
    ' Store bullets
    If IsArray(bullets) And UBound(bullets) >= 1 Then
        Dim bulletCount As Integer
        bulletCount = UBound(bullets)
        doc.Variables("DB_JOB_" & count & "_BULLETS").Value = CStr(bulletCount)
        
        Dim i As Integer
        For i = 1 To bulletCount
            doc.Variables("DB_JOB_" & count & "_B" & i).Value = bullets(i)
        Next i
    End If
    
    doc.Save
End Sub

Private Function GetDatabaseBullets() As Variant
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim count As Integer
    On Error Resume Next
    count = Val(doc.Variables("DB_BULLET_COUNT").Value)
    On Error GoTo 0
    
    If count = 0 Then
        GetDatabaseBullets = Array()
        Exit Function
    End If
    
    Dim bullets() As String
    ReDim bullets(1 To count)
    
    Dim i As Integer
    For i = 1 To count
        On Error Resume Next
        bullets(i) = doc.Variables("DB_BULLET_" & i).Value
        On Error GoTo 0
    Next i
    
    GetDatabaseBullets = bullets
End Function

Private Function GetDatabaseJobs() As Variant
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim count As Integer
    On Error Resume Next
    count = Val(doc.Variables("DB_JOB_COUNT").Value)
    On Error GoTo 0
    
    If count = 0 Then
        GetDatabaseJobs = Array()
        Exit Function
    End If
    
    Dim jobs() As String
    ReDim jobs(1 To count)
    
    Dim i As Integer
    For i = 1 To count
        On Error Resume Next
        jobs(i) = doc.Variables("DB_JOB_" & i & "_HEADER").Value
        On Error GoTo 0
    Next i
    
    GetDatabaseJobs = jobs
End Function

Private Function GetFullJobFromDatabase(index As Integer) As String
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim result As String
    On Error Resume Next
    result = doc.Variables("DB_JOB_" & index & "_HEADER").Value & "||"
    
    Dim bulletCount As Integer
    bulletCount = Val(doc.Variables("DB_JOB_" & index & "_BULLETS").Value)
    
    Dim i As Integer
    For i = 1 To bulletCount
        result = result & doc.Variables("DB_JOB_" & index & "_B" & i).Value & "||"
    Next i
    On Error GoTo 0
    
    GetFullJobFromDatabase = result
End Function

Private Sub RemoveFromDatabase(itemType As String, content As String)
    ' Simple removal - mark as empty
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim count As Integer
    On Error Resume Next
    count = Val(doc.Variables("DB_" & itemType & "_COUNT").Value)
    On Error GoTo 0
    
    Dim i As Integer
    For i = 1 To count
        On Error Resume Next
        If doc.Variables("DB_" & itemType & "_" & i).Value = content Then
            doc.Variables("DB_" & itemType & "_" & i).Value = ""
        End If
        On Error GoTo 0
    Next i
    
    doc.Save
End Sub

Private Sub RemoveJobFromDatabase(index As Integer)
    Dim doc As Document
    Set doc = ActiveDocument
    
    On Error Resume Next
    doc.Variables("DB_JOB_" & index & "_HEADER").Value = ""
    doc.Variables("DB_JOB_" & index & "_BULLETS").Value = "0"
    On Error GoTo 0
    
    doc.Save
End Sub

Private Sub InsertJobFromDatabase(jobData As String, sectionName As String)
    ' Parse job data (header||bullet1||bullet2||...)
    Dim parts() As String
    parts = Split(jobData, "||")
    
    If UBound(parts) < 0 Then Exit Sub
    
    ' Navigate to section
    If Not NavigateToSection(sectionName) Then Exit Sub
    
    Selection.MoveDown Unit:=wdLine, Count:=1
    Selection.HomeKey Unit:=wdLine
    
    ' Insert header
    Selection.TypeParagraph
    Selection.TypeText Text:=parts(0)
    
    With Selection.Font
        .Name = "Arial"
        .Size = 7.5
        .Bold = True
    End With
    
    ' Insert bullets
    Dim i As Integer
    For i = 1 To UBound(parts)
        If Len(Trim(parts(i))) > 0 Then
            InsertBullet parts(i)
        End If
    Next i
End Sub

Private Function SwapBulletText(oldText As String, newText As String) As Boolean
    Dim doc As Document
    Set doc = ActiveDocument
    
    Dim rng As Range
    Set rng = doc.Content
    
    With rng.Find
        .Text = Left(oldText, 40)
        .MatchCase = False
        If .Execute Then
            rng.Expand Unit:=wdParagraph
            ' Keep the bullet character
            Dim bulletChar As String
            bulletChar = Left(rng.Text, 2)
            If Left(bulletChar, 1) = "-" Then
                rng.Text = "-" & Chr(9) & newText & vbCrLf
            Else
                rng.Text = newText & vbCrLf
            End If
            SwapBulletText = True
        Else
            SwapBulletText = False
        End If
    End With
End Function

Private Sub ViewDatabaseBullets()
    Dim bullets As Variant
    bullets = GetDatabaseBullets()
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    STORED BULLETS" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    If Not IsArray(bullets) Or UBound(bullets) < 1 Then
        msg = msg & "(No bullets stored)" & vbCrLf
    Else
        Dim i As Integer
        For i = LBound(bullets) To UBound(bullets)
            If Len(bullets(i)) > 0 Then
                msg = msg & i & ". " & Left(bullets(i), 45) & "..." & vbCrLf
            End If
        Next i
    End If
    
    MsgBox msg, vbInformation, "Database Bullets"
End Sub

Private Sub ViewDatabaseJobs()
    Dim jobs As Variant
    jobs = GetDatabaseJobs()
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    STORED JOBS" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    If Not IsArray(jobs) Or UBound(jobs) < 1 Then
        msg = msg & "(No jobs stored)" & vbCrLf
    Else
        Dim i As Integer
        For i = LBound(jobs) To UBound(jobs)
            If Len(jobs(i)) > 0 Then
                msg = msg & i & ". " & Left(jobs(i), 50) & vbCrLf
            End If
        Next i
    End If
    
    MsgBox msg, vbInformation, "Database Jobs"
End Sub

Private Sub AddBulletToDatabase()
    Dim bullet As String
    bullet = InputBox("Enter bullet text to save:" & vbCrLf & vbCrLf & _
                      "(You can use this later in swaps)", "Add to Database")
    
    If bullet = "" Then Exit Sub
    
    SaveToDatabase "BULLET", bullet, "Manual"
    MsgBox "OK: Bullet saved to database!", vbInformation
End Sub

Private Sub ClearDatabase()
    If MsgBox("Clear ALL stored bullets and jobs?" & vbCrLf & vbCrLf & _
              "This cannot be undone!", vbYesNo + vbExclamation) = vbNo Then Exit Sub
    
    Dim doc As Document
    Set doc = ActiveDocument
    
    On Error Resume Next
    doc.Variables("DB_BULLET_COUNT").Delete
    doc.Variables("DB_JOB_COUNT").Delete
    On Error GoTo 0
    
    MsgBox "OK: Database cleared!", vbInformation
End Sub

' ============================================================
' VIEW STRUCTURE
' ============================================================
Sub ViewStructure()
    ScanSections
    
    Dim msg As String
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    CV STRUCTURE" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    
    Dim i As Integer
    For i = 1 To SectionCount
        msg = msg & "[+] " & SectionNames(i) & vbCrLf
        
        Dim jobs As Variant
        jobs = GetJobsInSection(SectionNames(i))
        
        If IsArray(jobs) And UBound(jobs) >= 1 Then
            Dim j As Integer
            For j = LBound(jobs) To UBound(jobs)
                msg = msg & "     > " & Left(jobs(j), 40) & vbCrLf
            Next j
        End If
        msg = msg & vbCrLf
    Next i
    
    MsgBox msg, vbInformation, "CV Structure"
End Sub

' ============================================================
' FORMAT HELPER MENU
' ============================================================
Sub FormatHelper()
    Dim choice As String
    Dim msg As String
    
    msg = "-----------------------------------" & vbCrLf
    msg = msg & "    FORMAT HELPER" & vbCrLf
    msg = msg & "-----------------------------------" & vbCrLf & vbCrLf
    msg = msg & "Select text first, then choose:" & vbCrLf & vbCrLf
    msg = msg & "1. Format as Company Header" & vbCrLf
    msg = msg & "   (Bold, Arial 10pt)" & vbCrLf & vbCrLf
    msg = msg & "2. Format as Role/Date" & vbCrLf
    msg = msg & "   (Italic, Arial 9pt)" & vbCrLf & vbCrLf
    msg = msg & "3. Format as Bullet Text" & vbCrLf
    msg = msg & "   (Regular, Arial 9pt)" & vbCrLf & vbCrLf
    msg = msg & "Enter choice (1-3):"
    
    choice = InputBox(msg, "Format Helper")
    
    Select Case Val(choice)
        Case 1: FormatAsCompany
        Case 2: FormatAsRole
        Case 3: FormatAsBullet
    End Select
End Sub

' ============================================================
' HELPER FUNCTIONS
' ============================================================

Private Function NavigateToSection(sectionName As String) As Boolean
    Dim rng As Range
    Set rng = ActiveDocument.Content
    
    With rng.Find
        .Text = sectionName
        .MatchCase = False
        If .Execute Then
            rng.Select
            NavigateToSection = True
        Else
            NavigateToSection = False
        End If
    End With
End Function

Private Function NavigateToJob(jobText As String) As Boolean
    ' Extract just the company name (before |)
    Dim searchText As String
    If InStr(jobText, " | ") > 0 Then
        searchText = Trim(Left(jobText, InStr(jobText, " | ") - 1))
    Else
        searchText = Left(jobText, 30)
    End If
    
    Dim rng As Range
    Set rng = ActiveDocument.Content
    
    With rng.Find
        .Text = searchText
        .MatchCase = False
        If .Execute Then
            rng.Select
            NavigateToJob = True
        Else
            NavigateToJob = False
        End If
    End With
End Function

Private Function NavigateToText(searchText As String) As Boolean
    ' Find specific text in document and select it
    Dim rng As Range
    Set rng = ActiveDocument.Content
    
    With rng.Find
        .Text = searchText
        .MatchCase = False
        If .Execute Then
            rng.Select
            NavigateToText = True
        Else
            NavigateToText = False
        End If
    End With
End Function

Private Sub MoveToEndOfJob()
    ' Find the last bullet of the current job
    ' We're currently at the company line (e.g., "Pairwire | New York")
    ' Need to move past role line, then past all bullets, then stop BEFORE next job
    
    Dim i As Integer
    Dim foundRoleLine As Boolean
    foundRoleLine = False
    
    ' First, move down to find the role line (has | and dates)
    For i = 1 To 3
        Selection.MoveDown Unit:=wdLine, Count:=1
        Dim txt As String
        txt = Trim(Selection.Paragraphs(1).Range.Text)
        
        ' Role line has | AND year
        If InStr(txt, " | ") > 0 And (InStr(txt, "202") > 0 Or InStr(txt, "201") > 0) Then
            foundRoleLine = True
            Exit For
        End If
    Next i
    
    If Not foundRoleLine Then
        ' Fallback - just stay where we are
        Selection.EndKey Unit:=wdLine
        Exit Sub
    End If
    
    ' Now move through bullets until we hit next company or section
    For i = 1 To 10
        ' Peek at next line without moving
        Selection.MoveDown Unit:=wdLine, Count:=1
        txt = Trim(Selection.Paragraphs(1).Range.Text)
        
        ' Empty or very short - might be spacing, keep going
        If Len(txt) < 5 Then
            GoTo NextLine
        End If
        
        ' Next company line: has | but NO year digits nearby
        ' Pattern: "Google | Lisbon, Portugal" vs "Role | May 2024 - August 2024"
        If InStr(txt, " | ") > 0 Then
            ' Check if this has a year (role line) or not (company line)
            If InStr(txt, "202") = 0 And InStr(txt, "201") = 0 And InStr(txt, "200") = 0 Then
                ' This is next company - go back one line and stop
                Selection.MoveUp Unit:=wdLine, Count:=1
                Exit For
            End If
        End If
        
        ' Section header
        If InStr(UCase(txt), "EDUCATION") > 0 Or InStr(UCase(txt), "LEADERSHIP") > 0 Or _
           InStr(UCase(txt), "SKILLS") > 0 Or InStr(UCase(txt), "PROJECTS") > 0 Then
            Selection.MoveUp Unit:=wdLine, Count:=1
            Exit For
        End If
        
NextLine:
    Next i
    
    ' Now we should be on the last bullet - go to end of line
    Selection.EndKey Unit:=wdLine
End Sub

Private Sub InsertBullet(bulletText As String)
    ' Strategy: Find existing bullet, duplicate it, then replace text
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' Find an existing bullet paragraph to use as template
    Dim templatePara As Paragraph
    Set templatePara = Nothing
    
    Dim para As Paragraph
    For Each para In doc.Paragraphs
        Dim txt As String
        txt = para.Range.Text
        ' Look for bullet pattern (dash at start, long text)
        If Left(txt, 1) = "-" And Len(txt) > 40 Then
            Set templatePara = para
            Exit For
        End If
    Next para
    
    If templatePara Is Nothing Then
        ' No template found - use simple insert
        Selection.EndKey Unit:=wdLine
        Selection.TypeParagraph
        Selection.TypeText Text:="-" & Chr(9) & bulletText
        Exit Sub
    End If
    
    ' Copy the template paragraph
    templatePara.Range.Copy
    
    ' Move to end of current line and paste
    Selection.EndKey Unit:=wdLine
    Selection.TypeParagraph
    Selection.Paste
    
    ' Now select the pasted paragraph and replace its text
    Selection.HomeKey Unit:=wdLine
    Selection.EndKey Unit:=wdLine, Extend:=wdExtend
    
    ' Replace text but keep formatting
    Dim newText As String
    newText = "-" & Chr(9) & bulletText
    Selection.TypeText Text:=newText
    
    ' Move cursor to end
    Selection.EndKey Unit:=wdLine
End Sub

Private Sub InsertNewJob(company As String, location As String, role As String, dates As String, bullet As String)
    ' Your CV uses Table Paragraph style within table cells
    ' This matches the existing formatting
    
    ' Company line (Bold, link-styled)
    Selection.TypeParagraph
    Selection.TypeText Text:=company & " | " & location
    
    With Selection.Font
        .Name = "Arial"
        .Size = 7.5
        .Bold = True
        .Italic = False
    End With
    
    On Error Resume Next
    Selection.Style = "Table Paragraph"
    On Error GoTo 0
    
    ' Role line (Italic)
    Selection.TypeParagraph
    Selection.TypeText Text:=role & " | " & dates
    
    With Selection.Font
        .Name = "Arial"
        .Size = 7.5
        .Bold = False
        .Italic = True
    End With
    
    On Error Resume Next
    Selection.Style = "Table Paragraph"
    On Error GoTo 0
    
    ' First bullet
    InsertBullet bullet
End Sub

Private Sub FormatAsCompany()
    With Selection.Font
        .Name = "Arial"
        .Size = 10
        .Bold = True
        .Italic = False
    End With
End Sub

Private Sub FormatAsRole()
    With Selection.Font
        .Name = "Arial"
        .Size = 9
        .Bold = False
        .Italic = True
    End With
End Sub

Private Sub FormatAsBullet()
    With Selection.Font
        .Name = "Arial"
        .Size = 9
        .Bold = False
        .Italic = False
    End With
End Sub

' ============================================================
' RIBBON BUTTONS - Add these to your CV Editing tab
' RIBBON1-5 = Core buttons (recommended)
' RIBBON6-7 = Optional buttons
' ============================================================

' RIBBON1 - CV Menu (Home icon)
' Opens the full menu with all options
Sub RIBBON1_Menu()
    CVEditor
End Sub

' RIBBON2 - Add Bullet (Green arrow / document icon)
' Quick add bullet to any job
Sub RIBBON2_AddBullet()
    AddBulletMenu
End Sub

' RIBBON3 - Add Job (Folder icon)
' Add new job entry
Sub RIBBON3_AddJob()
    AddJobMenu
End Sub

' RIBBON4 - Resize (Scale/magnifier icon)
' Shrink/grow CV elements for space management
Sub RIBBON4_Resize()
    ResizeCVMenu
End Sub

' RIBBON5 - Database (Piggy bank / save icon)
' Access stored bullets and jobs
Sub RIBBON5_DB()
    DatabaseMenu
End Sub

' RIBBON6 - Delete Bullet (Minus / X icon) [OPTIONAL]
' Quick delete bullet (also accessible via Menu)
Sub RIBBON6_DelBullet()
    DeleteBulletMenu
End Sub

' RIBBON7 - Delete Job (Red X icon) [OPTIONAL]
' Quick delete job (also accessible via Menu)
Sub RIBBON7_DelJob()
    DeleteJobMenu
End Sub
