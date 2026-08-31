param(
  [string[]]$QueryId = @(
    'flag_13__predictive__long_duration_value',
    'flag_19__predictive__declined_expense',
    'flag_20__predictive__declined_travel_expense',
    'flag_28__predictive__high_goal_achievement',
    'healthcare_visit_notes__predictive__high_urgency',
    'imdb_movie_reviews__causal__audience_dissatisfaction',
    'yelp_polarity_reviews__causal__improve_satisfaction'
  ),
  [int]$Throttle = 3,
  [string]$RunName = 'opus47_direct_newgt_V9_20260601',
  [string]$Model = 'copilot/claude-opus-4.7-xhigh',
  [string]$Python = 'C:\Users\v-xintaolin\AppData\Local\anaconda3\python.exe',
  [string]$Runner = 'lab8/skill-v9/scripts/reference_comparison.py',
  [int]$RunTimeout = 3600,
  [int]$ClaudeTimeout = 900,
  [int]$WatchdogSeconds = 90,
  [switch]$Force,
  [switch]$AttachExisting
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path .).Path
$active = @{}
$completed = @()

function Get-RunDirForQuery {
  param([string]$Query, [string]$RunName)
  $matches = @(Get-ChildItem 'lab8/benchmark_data/newData/datasets' -Recurse -Directory -Filter $Query -ErrorAction SilentlyContinue)
  foreach ($match in $matches) {
    $candidate = Join-Path $match.FullName (Join-Path 'skill_v9_runs' $RunName)
    if (Test-Path $candidate) {
      return $candidate
    }
  }
  if ($matches.Count -gt 0) {
    return (Join-Path $matches[0].FullName (Join-Path 'skill_v9_runs' $RunName))
  }
  return $null
}

function Start-V9ReferenceJob {
  param([string]$Query)
  $job = Start-Job -Name $Query -ArgumentList $repoRoot,$Python,$Runner,$Query,$RunName,$Model,$RunTimeout,$ClaudeTimeout,[bool]$Force -ScriptBlock {
    param($RepoRoot,$Python,$Runner,$Query,$RunName,$Model,$RunTimeout,$ClaudeTimeout,$ForceRun)
    Set-Location $RepoRoot
    $env:PYTHONIOENCODING = 'utf-8'
    $started = Get-Date
    Write-Output "JOB_START query=$Query time=$($started.ToString('o'))"
    $cmdArgs = @(
      $Runner,
      '--query-id', $Query,
      '--model', $Model,
      '--run-name', $RunName,
      '--max-workers', '1',
      '--attempts', '2',
      '--claude-timeout', [string]$ClaudeTimeout,
      '--run-timeout', [string]$RunTimeout,
      '--output-format', 'csv',
      '--continue-on-error',
      '--no-summary-update'
    )
    if ($ForceRun) {
      $cmdArgs += '--force'
    }
    & $Python @cmdArgs 2>&1
    $exitCode = $LASTEXITCODE
    $finished = Get-Date
    Write-Output "JOB_END query=$Query rc=$exitCode seconds=$([math]::Round(($finished - $started).TotalSeconds,2)) time=$($finished.ToString('o'))"
    exit $exitCode
  }
  $script:active[$job.Id] = [pscustomobject]@{ Query = $Query; Job = $job; Started = Get-Date }
  Write-Output "SCHED_START query=$Query job=$($job.Id) time=$((Get-Date).ToString('o'))"
}

function Test-CompletedReferenceRun {
  param([string]$Query)
  $runDir = Get-RunDirForQuery -Query $Query -RunName $RunName
  if ($null -eq $runDir -or -not (Test-Path $runDir)) {
    return $false
  }
  return ((Test-Path (Join-Path $runDir 'augment.csv')) -and (Test-Path (Join-Path $runDir 'BT_COMPARISON.json')))
}

$querySet = @{}
foreach ($query in $QueryId) {
  $querySet[$query] = $true
}

if ($AttachExisting) {
  foreach ($job in Get-Job) {
    if ($querySet.ContainsKey($job.Name) -and $job.State -eq 'Running') {
      $active[$job.Id] = [pscustomobject]@{ Query = $job.Name; Job = $job; Started = $job.PSBeginTime }
      Write-Output "ATTACH_EXISTING query=$($job.Name) job=$($job.Id) time=$((Get-Date).ToString('o'))"
    }
  }
}

$pending = [System.Collections.Queue]::new()
foreach ($query in $QueryId) {
  $alreadyRunning = $false
  foreach ($entry in $active.Values) {
    if ($entry.Query -eq $query) {
      $alreadyRunning = $true
      break
    }
  }
  if (-not $alreadyRunning) {
    if ((Test-CompletedReferenceRun -Query $query) -and -not $Force) {
      Write-Output "SKIP_COMPLETED query=$query time=$((Get-Date).ToString('o'))"
      continue
    }
    [void]$pending.Enqueue($query)
  }
}

while (($active.Count -lt $Throttle) -and ($pending.Count -gt 0)) {
  Start-V9ReferenceJob -Query ([string]$pending.Dequeue())
}

while (($active.Count -gt 0) -or ($pending.Count -gt 0)) {
  $jobs = @($active.Values | ForEach-Object { $_.Job })
  if ($jobs.Count -eq 0) {
    while (($active.Count -lt $Throttle) -and ($pending.Count -gt 0)) {
      Start-V9ReferenceJob -Query ([string]$pending.Dequeue())
    }
    continue
  }

  $done = Wait-Job -Job $jobs -Any -Timeout $WatchdogSeconds
  if ($null -eq $done) {
    Write-Output "WATCHDOG no job completed running=$($active.Count) pending=$($pending.Count) time=$((Get-Date).ToString('o'))"
    foreach ($entry in $active.Values) {
      $runDir = Get-RunDirForQuery -Query $entry.Query -RunName $RunName
      $elapsed = [math]::Round(((Get-Date) - $entry.Started).TotalSeconds, 1)
      if ($null -eq $runDir -or -not (Test-Path $runDir)) {
        Write-Output "  RUNNING query=$($entry.Query) job=$($entry.Job.Id) elapsed_s=$elapsed workdir=not-created"
        continue
      }
      $latest = @(Get-ChildItem $runDir -Recurse -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 3)
      if ($latest.Count -eq 0) {
        Write-Output "  RUNNING query=$($entry.Query) job=$($entry.Job.Id) elapsed_s=$elapsed files=0"
        continue
      }
      $latestText = ($latest | ForEach-Object {
        "$($_.LastWriteTime.ToString('HH:mm:ss')) $($_.FullName.Substring($repoRoot.Length + 1)) $($_.Length)B"
      }) -join ' || '
      Write-Output "  RUNNING query=$($entry.Query) job=$($entry.Job.Id) elapsed_s=$elapsed latest=$latestText"
    }
    continue
  }

  foreach ($job in @($done)) {
    $entry = $active[$job.Id]
    Write-Output "SCHED_DONE query=$($entry.Query) job=$($job.Id) state=$($job.State) time=$((Get-Date).ToString('o'))"
    Receive-Job -Job $job | ForEach-Object { Write-Output "[$($entry.Query)] $_" }
    $completed += [pscustomobject]@{ Query = $entry.Query; JobId = $job.Id; State = $job.State; Finished = Get-Date }
    Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
    $active.Remove($job.Id)
  }

  while (($active.Count -lt $Throttle) -and ($pending.Count -gt 0)) {
    Start-V9ReferenceJob -Query ([string]$pending.Dequeue())
  }
}

Write-Output "ALL_V9_JOBS_DONE time=$((Get-Date).ToString('o'))"
$completed | Format-Table -AutoSize
Write-Output 'FINAL_V9_RUN_STATUS'
foreach ($query in $QueryId) {
  $runDir = Get-RunDirForQuery -Query $query -RunName $RunName
  $hasAug = $false
  $hasBT = $false
  if ($null -ne $runDir -and (Test-Path $runDir)) {
    $hasAug = Test-Path (Join-Path $runDir 'augment.csv')
    $hasBT = Test-Path (Join-Path $runDir 'BT_COMPARISON.json')
  }
  [pscustomobject]@{ Query = $query; HasAug = $hasAug; HasBT = $hasBT; Workdir = $runDir } | Format-List
}
