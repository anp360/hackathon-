# Quick Start Script for Windows PowerShell
# Run this after setting up your environment

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "🚨 CRISIS MANAGEMENT AI SYSTEM - QUICK START" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "Run: .\venv\Scripts\Activate`n" -ForegroundColor White
}

# Check if API key is set
if ($env:GEMINI_API_KEY -and $env:GEMINI_API_KEY -ne "your-api-key-here") {
    Write-Host "✓ GEMINI_API_KEY is set" -ForegroundColor Green
} else {
    Write-Host "⚠️  GEMINI_API_KEY not set!" -ForegroundColor Red
    Write-Host "Set it with: `$env:GEMINI_API_KEY='your-key-here'`n" -ForegroundColor White
}

Write-Host "`nChoose an option:" -ForegroundColor Cyan
Write-Host "1. Process test messages (populate database)"
Write-Host "2. Start web dashboard"
Write-Host "3. Both (process then start dashboard)`n"

$choice = Read-Host "Enter choice (1/2/3)"

switch ($choice) {
    "1" {
        Write-Host "`n🔄 Processing messages...`n" -ForegroundColor Yellow
        python process_messages.py
    }
    "2" {
        Write-Host "`n🚀 Starting web dashboard...`n" -ForegroundColor Yellow
        python app.py
    }
    "3" {
        Write-Host "`n🔄 Processing messages...`n" -ForegroundColor Yellow
        python process_messages.py
        Write-Host "`n🚀 Starting web dashboard...`n" -ForegroundColor Yellow
        python app.py
    }
    default {
        Write-Host "`nInvalid choice. Run the script again." -ForegroundColor Red
    }
}
