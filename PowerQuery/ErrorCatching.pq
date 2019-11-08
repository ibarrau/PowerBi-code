= (InputTable as table , KeyColumn as text) =>
let
	Source = InputTable,
	#"Kept Errors" = Table.SelectRowsWithErrors(Source),
	#"Added Custom" = Table.AddColumn(#"Kept Errors", "Custom", each _),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom", {{KeyColumn, "KeyColumn"}}),
	#"Added Custom1" = Table.AddColumn(#"Renamed Columns", "Errors", each Record.ToTable([Custom]) ),
    #"Removed Other Columns" = Table.SelectColumns(#"Added Custom1", {"KeyColumn", "Errors"}),
    #"Expand Column Columns Desc" = Table.ExpandTableColumn(#"Removed Other Columns", "Errors", {"Name", "Value"}, {"Errors.Columns", "Errors.Desc"}),
    #"Kept Errors New" = Table.SelectRowsWithErrors(#"Expand Column Columns Desc", {"Errors.Desc"}),
    #"Added Custom2" = Table.AddColumn(#"Kept Errors New", "Format", each try [Errors.Desc]),
    #"Expand Column Format" = Table.ExpandRecordColumn(#"Added Custom2", "Format", {"Error"}, {"Format.Error"}),
    #"Expand Column Format.Error" = Table.ExpandRecordColumn(#"Expand Column Format", "Format.Error", {"Reason", "Message", "Detail"}, {"Format.Error.Reason", "Format.Error.Message", "Format.Error.Detail"})
in
    #"Expand Column Format.Error"