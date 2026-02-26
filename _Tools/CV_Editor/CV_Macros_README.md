# CV Editor VBA Macros

## How to Install

1. Open your CV in Word
2. Press `Alt + F11` (Windows) or `Tools > Macro > Visual Basic Editor` (Mac)
3. In the VBA Editor, go to `Insert > Module`
4. Paste the code from `CV_Macros.bas`
5. Save as `.docm` (macro-enabled document)

## How to Use

### Add a Bullet to Existing Job
1. Place cursor in the job section where you want to add a bullet
2. Run macro: `AddBullet`
3. Enter your bullet text when prompted

### Add a New Job
1. Run macro: `AddNewJob`
2. Select section (Work Experience, Education, Leadership)
3. Enter company, location, role, dates
4. The job will be added at the TOP of that section

## Keyboard Shortcuts (Optional)
- Go to `Tools > Customize Keyboard`
- Assign shortcuts like `Ctrl+Shift+B` for AddBullet
