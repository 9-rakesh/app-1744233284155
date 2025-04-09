# Login Functionality Test Cases

| ID | Test Case | Steps | Expected Result | Actual Result | Status |
|----|-----------|-------|-----------------|----------------|--------|
| TC01 | Valid Login | 1. Navigate to login page<br>2. Enter valid credentials<br>3. Click login | User should be logged in and redirected to dashboard | | |
| TC02 | Invalid Username | 1. Enter invalid username<br>2. Enter valid password<br>3. Click login | Error message "Invalid credentials" should appear | | |
| TC03 | Invalid Password | 1. Enter valid username<br>2. Enter invalid password<br>3. Click login | Error message "Invalid credentials" should appear | | |
| TC04 | Empty Username | 1. Leave username blank<br>2. Enter valid password<br>3. Click login | "Required" error should appear under username field | | |
| TC05 | Empty Password | 1. Enter valid username<br>2. Leave password blank<br>3. Click login | "Required" error should appear under password field | | |
| TC06 | Both Fields Empty | 1. Leave both fields blank<br>2. Click login | "Required" errors should appear under both fields | | |
| TC07 | Password Case Sensitivity | 1. Enter valid username<br>2. Enter password with wrong case<br>3. Click login | Error message "Invalid credentials" should appear | | |
| TC08 | Forgot Password Link | 1. Click "Forgot your password?" link | Should redirect to password reset page | | |
| TC09 | Login Page Title | 1. Navigate to login page | Page title should be "OrangeHRM" | | |
| TC10 | Remember Me Functionality | 1. Check "Remember Me"<br>2. Login successfully<br>3. Close and reopen browser<br>4. Navigate to login page | Username should be prefilled | | |
