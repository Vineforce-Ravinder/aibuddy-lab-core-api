$projectName = "app"

$folders = @(
    "$projectName/config",
    "$projectName/api/routes",
    "$projectName/api/middleware",
    "$projectName/core/llm",
    "$projectName/core/agents",
    "$projectName/core/services",
    "$projectName/core/prompts",
    "$projectName/infrastructure/db/models",
    "$projectName/infrastructure/auth",
    "$projectName/infrastructure/vectorstore",
    "$projectName/infrastructure/cache",
    "$projectName/tests"
)

$files = @(
    "$projectName/main.py",

    "$projectName/config/settings.py",
    "$projectName/config/logging.py",

    "$projectName/api/__init__.py",
    "$projectName/api/routes/auth.py",
    "$projectName/api/routes/llm.py",
    "$projectName/api/routes/agents.py",
    "$projectName/api/routes/lms.py",
    "$projectName/api/middleware/auth_middleware.py",
    "$projectName/api/middleware/error_handler.py",

    "$projectName/core/llm/base.py",
    "$projectName/core/llm/azure.py",
    "$projectName/core/llm/openai.py",
    "$projectName/core/llm/factory.py",

    "$projectName/core/agents/base_agent.py",
    "$projectName/core/agents/tutor_agent.py",
    "$projectName/core/agents/tool_registry.py",

    "$projectName/core/services/auth_service.py",
    "$projectName/core/services/lms_service.py",
    "$projectName/core/services/search_service.py",

    "$projectName/core/prompts/tutor_prompts.py",

    "$projectName/infrastructure/db/base.py",
    "$projectName/infrastructure/db/session.py",
    "$projectName/infrastructure/db/models/user.py",
    "$projectName/infrastructure/db/models/course.py",

    "$projectName/infrastructure/auth/jwt_provider.py",
    "$projectName/infrastructure/auth/password.py",

    "$projectName/infrastructure/vectorstore/base.py",
    "$projectName/infrastructure/vectorstore/azure_search.py",

    "$projectName/infrastructure/cache/redis.py",

    ".env",
    "requirements.txt"
)

Write-Host "Creating project structure..."

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created folder: $folder"
    }
}

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
        Write-Host "Created file: $file"
    }
}

Write-Host "Project scaffold created successfully!" -ForegroundColor Green
