# Login Page Bug Report

## Identified Issues

1. **Missing Password Masking**
   - Severity: Medium
   - Description: Password field shows plain text when typing
   - Expected: Password should be masked with bullets/asterisks
   - Reproduction Steps:
     1. Navigate to login page
     2. Type in password field
     3. Observe unmasked password

2. **No Rate Limiting on Failed Attempts**
   - Severity: High
   - Description: Can attempt unlimited failed logins
   - Expected: Account should lock after 3-5 failed attempts
   - Reproduction Steps:
     1. Enter invalid credentials
     2. Repeat login attempts continuously

3. **Inconsistent Error Messages**
   - Severity: Low
   - Description: Different error formats for similar validation cases
   - Expected: Consistent error message styling
   - Reproduction Steps:
     1. Test empty username vs empty password
     2. Compare error message displays

4. **No Session Timeout Warning**
   - Severity: Medium
   - Description: Session expires without warning
   - Expected: Should warn user before session expiration
   - Reproduction Steps:
     1. Login and remain idle
     2. Wait for session to expire
