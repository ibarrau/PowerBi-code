= (InputTable as table) =>
let
	Source = InputTable,
    #"UnPivotTable" = Table.UnpivotOtherColumns(Source, {}, "Attribute", "Value"),
    #"KeyColumn" = "Attribute",
	#"Added Custom" = Table.AddColumn(#"UnPivotTable", "Custom", each _),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom", {{KeyColumn, "KeyColumn"}}),
	#"Added Custom1" = Table.AddColumn(#"Renamed Columns", "Errors", each Record.ToTable([Custom]) ),
    #"Removed Other Columns" = Table.SelectColumns(#"Added Custom1", {"KeyColumn", "Errors"}),
    #"Expand Column Columns Desc" = Table.ExpandTableColumn(#"Removed Other Columns", "Errors", {"Name", "Value"}, {"Errors.Columns", "Errors.Desc"}),
    #"Kept Errors New" = Table.SelectRowsWithErrors(#"Expand Column Columns Desc", {"Errors.Desc"}),
    #"Added Custom2" = Table.AddColumn(#"Kept Errors New", "Format", each try [Errors.Desc]),
    #"Expand Column Format" = Table.ExpandRecordColumn(#"Added Custom2", "Format", {"Error"}, {"Format.Error"}),
    #"Expand Column Format.Error" = Table.ExpandRecordColumn(#"Expand Column Format", "Format.Error", {"Reason", "Message", "Detail"}, {"Error.Reason", "Error.Message", "Error.Detail"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Expand Column Format.Error",{{"Error.Reason", type text}, {"Error.Message", type text}, {"Error.Detail", type text}, {"Errors.Columns", type text}, {"Errors.Desc", type text}})
in
    #"Changed Type"