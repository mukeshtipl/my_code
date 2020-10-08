Write-Host "Hello World"
$myarray=@("abc" , "xyz" , "pqr" , "dcb")
# Write-Host $myarray
$myarray
# Hash Tables
$slist=@{1="Rahul";2="Raja";3='Aman'}
# $slist
$slist[4]='Manoj'
# $slist
$slist.Remove(2)
# $slist
foreach ($item in $slist.GetEnumerator()) {
    Write-Host  "$($item.Key) => $($item.Value)"
}
For($i=1; $i -lt 4; $i++){
    If ($slist[$i]){
    Write-Host  "$i. $($slist[$i])"
    }
}