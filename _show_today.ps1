$json = Get-Content '_today_raw.json' -Raw | ConvertFrom-Json
foreach ($info in $json.value.matchInfoList) {
    foreach ($sub in $info.subMatchList) {
        $mid = $sub.matchNumStr
        $date = $sub.matchDate
        $time = $sub.matchTime
        $league = $sub.leagueAllName
        $home = $sub.homeTeamAllName
        $away = $sub.awayTeamAllName
        $gl = $sub.hhad.goalLine
        $h = $sub.had.h; $d = $sub.had.d; $a = $sub.had.a
        $rh = $sub.hhad.h; $rd = $sub.hhad.d; $ra = $sub.hhad.a
        $ts = $date.Substring(5) + ' ' + $time.Substring(0,5)
        Write-Host ("{0,-12} {1,-18} {2,-14} {3,-14}vs {4,-14} {5,4}  {6,4}/{7,4}/{8,4}" -f $mid,$league,$ts,$home,$away,$gl,$h,$d,$a)
        if ($rh) {
            Write-Host ("{0,-12} {1,-18} {2,-14} {3,-14}{4,-16} {5,4}  {6,4}/{7,4}/{8,4}" -f '','','','','',$gl,$rh,$rd,$ra)
        }
        Write-Host ''
    }
}
$count = ($json.value.matchInfoList | ForEach-Object { $_.subMatchList.Count } | Measure-Object -Sum).Sum
Write-Host "共 $count 场比赛"
