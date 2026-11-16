<#
.SYNOPSIS
    inference-bench 一键基准：OpenVINO(NPU/GPU/CPU) + Ollama(CPU/iGPU)

.EXAMPLE
    .\run_all.ps1                       # 全跑，默认模型
    .\run_all.ps1 -SkipOllama           # 只测 OpenVINO 三设备
    .\run_all.ps1 -SkipNpu              # 跳过 NPU（首跑编译很慢）
    .\run_all.ps1 -OllamaModel qwen3:8b -Runs 3 -MaxTokens 128

.NOTES
    默认使用本目录的 .venv（3.14，openvino 支持的最高版本）。
    即使外面主版本是 3.15，在本目录跑也自动走 .venv。
#>
[CmdletBinding()]
param(
    [string]$Python = "",
    [string]$OvModel = "OpenVINO/Qwen2.5-1.5B-instruct-int4-ov",
    [string]$OllamaModel = "qwen3:8b",
    [int]$Runs = 3,
    [int]$MaxTokens = 128,
    [switch]$SkipOllama,
    [switch]$SkipNpu
)

$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot
[Console]::OutputEncoding = [Text.Encoding]::UTF8

# ALL_PROXY=socks5h://... 会让 httpx 抛 socksio ImportError
Remove-Item Env:ALL_PROXY -ErrorAction SilentlyContinue
Remove-Item Env:all_proxy -ErrorAction SilentlyContinue
$env:HF_HUB_DISABLE_TELEMETRY = '1'

# ---------------- 解析 Python 解释器 ----------------
# 优先级：-Python 显式指定 > 本目录 .venv > 报错
# （本机主版本已是 3.15，而 openvino 无 cp315 wheel，所以项目内必须走 .venv）
$venvPy = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not $Python) {
    if (Test-Path $venvPy) {
        $Python = $venvPy
    } else {
        throw @"
未找到虚拟环境：$venvPy
请先执行：
    uv venv --python 3.14 .venv
    uv pip install -r requirements.txt
（或显式指定解释器：-Python <path-to-python.exe>）
"@
    }
}

if (-not (Test-Path $Python)) {
    throw "找不到 Python: $Python（用 -Python 指定）"
}
function Invoke-Step {
    param([string]$Title, [scriptblock]$Body)
    Write-Host ""
    Write-Host ("=" * 72) -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host ("=" * 72) -ForegroundColor Cyan
    & $Body
    Write-Host ("  -> exit code: $LASTEXITCODE") -ForegroundColor DarkGray
}

$sw = [Diagnostics.Stopwatch]::StartNew()

# ---------------- OpenVINO ----------------
$ovDevices = if ($SkipNpu) { "GPU,CPU" } else { "all" }
Invoke-Step "OpenVINO GenAI  ($ovDevices)" {
    & $Python -u ov_bench.py --device $ovDevices --model $OvModel `
        --runs $Runs --max-tokens $MaxTokens
}

# ---------------- Ollama ----------------
if (-not $SkipOllama) {
    Invoke-Step "Ollama  CPU vs iGPU  ($OllamaModel)" {
        & $Python -u ollama_bench.py --model $OllamaModel `
            --runs $Runs --max-tokens $MaxTokens
    }
}

# ---------------- 汇总 ----------------
$sw.Stop()
Write-Host ""
Write-Host ("=" * 72) -ForegroundColor Green
Write-Host ("  全部完成，总耗时 {0:N1} 分钟" -f $sw.Elapsed.TotalMinutes) -ForegroundColor Green
Write-Host ("=" * 72) -ForegroundColor Green

if (Test-Path 'results\history.jsonl') {
    Write-Host "`n历史记录（results\history.jsonl）：" -ForegroundColor Yellow
    Get-Content 'results\history.jsonl' -Encoding UTF8 | ForEach-Object {
        try {
            $o = $_ | ConvertFrom-Json
            $parts = $o.results | ForEach-Object {
                $k = if ($_.device) { $_.device } else { $_.mode }
                "$k=$($_.avg_tok_per_s)"
            }
            "{0}  {1,-8} {2,-34} {3}" -f $o.ts, $o.engine, $o.model, ($parts -join '  ')
        } catch { }
    }
}
