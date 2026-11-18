# CodeCraftHub API Test Script for PowerShell
$baseUrl = "http://localhost:5000"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Testing CodeCraftHub Learning Platform API" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Test 1: Add a New Course
Write-Host "`n[Test 1] Add a New Course (POST /api/courses)" -ForegroundColor Yellow
$body = @{
    name = "Python Basics"
    description = "Learn Python fundamentals including variables, loops, and functions"
    target_date = "2025-12-31"
    status = "Not Started"
} | ConvertTo-Json
Invoke-RestMethod -Uri "$baseUrl/api/courses" -Method Post -Body $body -ContentType "application/json" | ConvertTo-Json -Depth 5

# Test 2: Get All Courses
Write-Host "`n[Test 2] Get All Courses (GET /api/courses)" -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/courses" -Method Get | ConvertTo-Json -Depth 5

# Test 3: Get Specific Course
Write-Host "`n[Test 3] Get Specific Course (GET /api/courses/1)" -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/courses/1" -Method Get | ConvertTo-Json -Depth 5

# Test 4: Update Course
Write-Host "`n[Test 4] Update Course (PUT /api/courses/1)" -ForegroundColor Yellow
$updateBody = @{ status = "In Progress" } | ConvertTo-Json
Invoke-RestMethod -Uri "$baseUrl/api/courses/1" -Method Put -Body $updateBody -ContentType "application/json" | ConvertTo-Json -Depth 5

# Test 5: Bonus - Course Statistics
Write-Host "`n[Test 5] Course Statistics (GET /api/courses/stats)" -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/courses/stats" -Method Get | ConvertTo-Json -Depth 5

# Test 6: Bonus - Search Courses
Write-Host "`n[Test 6] Search Courses (GET /api/courses/search?q=python)" -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/courses/search?q=python" -Method Get | ConvertTo-Json -Depth 5

# Test 7: Delete Course
Write-Host "`n[Test 7] Delete Course (DELETE /api/courses/1)" -ForegroundColor Yellow
Invoke-RestMethod -Uri "$baseUrl/api/courses/1" -Method Delete | ConvertTo-Json -Depth 5

Write-Host "`nAll tests completed successfully!" -ForegroundColor Green
