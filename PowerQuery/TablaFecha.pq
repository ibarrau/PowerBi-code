let
    Source = let
//Capture the date range from the parameters
    StartDate = #date(2010, 1, 1),
    EndDate = DateTime.Date(DateTime.LocalNow()),
//Get the number of dates that will be required for the table
    GetDateCount = Duration.Days(EndDate - StartDate),
//Take the count of dates and turn it into a list of dates
    GetDateList = List.Dates(StartDate, GetDateCount, 
    #duration(1,0,0,0)),
//Convert the list into a table
    DateListToTable = Table.FromList(GetDateList, 
    Splitter.SplitByNothing(), {"Fecha"}, null, ExtraValues.Error),
// Convert to Date
    ConvertToDate = Table.TransformColumns(DateListToTable,{{"Fecha", Date.From, type date}}),
// Date Key
    DateKey = Table.AddColumn(ConvertToDate, "IdFecha", each Number.FromText(Text.From(Date.Year([Fecha])) & Date.ToText([Fecha],"MM") & Date.ToText([Fecha],"dd") ) , Int32.Type ),
//Add Year Column
    YearNumber = Table.AddColumn(DateKey, "Año", 
    each Date.Year([Fecha]), Int32.Type),
//Add Month Number Column
    MonthNumber = Table.AddColumn(YearNumber , "IdMes", 
    each Date.Month([Fecha]), Int32.Type),
//Add Month Name Column
    MonthName = Table.AddColumn(MonthNumber , "Mes", 
    each Text.Proper(Date.ToText([Fecha],"MMMM", "es-es")), type text),
//Period
    AMes = Table.AddColumn(MonthName , "Periodo", 
    each Text.From([Año]) & Text.PadStart(Text.From([IdMes]),2,"0"), type text),
//Start of Month
    StartOfMonth = Table.AddColumn(AMes, "Inicio de Mes", 
    each Date.StartOfMonth([Fecha]), type date),
//Add Day Number Column
    DayNumber  = Table.AddColumn(StartOfMonth , "Dia", 
    each Date.Day([Fecha]), Int32.Type),
//Add Day Name Column
    DayName  = Table.AddColumn(DayNumber , "Nombre Dia", 
    each Text.Proper(Date.ToText([Fecha], "dddd")), type text)
in
    DayName
in
    Source