let
  ActivityQuery = (ActDate as date) => 
let
    Start =
        Text.From(DateTime.ToText(
            #datetime(Date.Year(ActDate), Date.Month(ActDate), Date.Day(ActDate), 00, 00, 00)
            , "yyyy-MM-ddT00:00:00.000Z"
        )),
    End =
        Text.From(DateTime.ToText(
            #datetime(Date.Year(ActDate), Date.Month(ActDate), Date.Day(ActDate), 00, 00, 00)
            , "yyyy-MM-ddT23:59:59.000Z"
        )),
    Source = Json.Document(Web.Contents("https://api.powerbi.com/v1.0/myorg/", 
    [
        RelativePath="admin/activityevents",
        Query = [
            startDateTime= Text.Combine({"'", Start,"'"},""),
            endDateTime= Text.Combine({"'",End  ,"'"},"")
        ],
        Headers=[
            Authorization=Text.Combine({"Bearer ", AccessToken()}, "")
        ]
    ]))
in
    Source
in
  ActivityQuery