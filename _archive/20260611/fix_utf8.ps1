$ErrorActionPreference = 'Stop'

# Read the corrupted file as UTF-8
$utf8 = [System.Text.Encoding]::UTF8
$content = [System.IO.File]::ReadAllText("C:\Users\gjj\Desktop\v333\templates\index.html", $utf8)

# Get the CP936 encoding (System ANSI on zh-CN Windows)
$cp936 = [System.Text.Encoding]::GetEncoding(936)

# Step 1: encode each char as CP936 to get original bytes
# We need to do this char by char to handle PUA
$resultBytes = New-Object System.Collections.Generic.List[byte]

# Characters that can't be encoded as CP936
$encoder = $cp936.GetEncoder()
$encoder.Fallback = [System.Text.EncoderReplacementFallback]::new('?')

for ($i = 0; $i -lt $content.Length; $i++) {
    $c = $content[$i]
    $codePoint = [int]$c
    
    if ($codePoint -lt 128) {
        # ASCII - single byte
        $resultBytes.Add([byte]$codePoint)
    }
    elseif ($codePoint -ge 0xE000 -and $codePoint -le 0xF8FF) {
        # PUA char - skip (these are garbage from the corruption)
        # Write a placeholder '?' byte
        $resultBytes.Add([byte]0x3F)
    }
    else {
        # CJK or other non-ASCII - encode as CP936
        $charBytes = $cp936.GetBytes([char[]]@($c))
        foreach ($b in $charBytes) {
            $resultBytes.Add($b)
        }
    }
}

# Step 2: decode the bytes as UTF-8
$fixedText = $utf8.GetString($resultBytes.ToArray())

# Write the fixed file
[System.IO.File]::WriteAllText("C:\Users\gjj\Desktop\v333\templates\index.html", $fixedText, $utf8)

Write-Host "Fixed file written successfully"
Write-Host "File size: $($resultBytes.Count) bytes"
