$User = "XXXXX@company.com"
$PW = "secret"

$SecPasswd = ConvertTo-SecureString $PW -AsPlainText -Force
$myCred = New-Object System.Management.Automation.PSCredential($User,$SecPasswd)

Connect-PowerBIServiceAccount -Credential $myCred

$DSIDRefresh = "XXXX-XXXX-XXXX-XXXX"
$WSIDAdmin = "XXXX-XXXX-XXXX-XXXX"

$RefreshDSURL = 'groups/' + $WSIDAdmin + '/datasets/' + $DSIDRefresh + '/refreshes'

Invoke-PowerBIRestMethod -Url $RefreshDSURL -Method Post