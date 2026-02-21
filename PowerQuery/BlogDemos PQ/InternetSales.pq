let
    Origen = Csv.Document(Web.Contents("https://raw.githubusercontent.com/ibarrau/PowerBi-code/master/DatosPrueba/InternetSales.csv"),[Delimiter=";", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Encabezados promovidos" = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    //Remove time custom format from text
    #"Extracted Text (Date) Before Delimiter" = Table.TransformColumns(#"Encabezados promovidos", {{"Order Date", each Text.BeforeDelimiter(_, " "), type text},{"Due Date", each Text.BeforeDelimiter(_, " "), type text},{"Delivery Date", each Text.BeforeDelimiter(_, " "), type text}}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Extracted Text (Date) Before Delimiter",{{"StoreKey", Int64.Type}, {"ProductKey", Int64.Type}, {"CustomerKey", Int64.Type}, {"Quantity", Int64.Type}, {"Unit Price", Currency.Type}, {"Unit Discount", Currency.Type}, {"Unit Cost", Currency.Type}, {"Net Price", Currency.Type}, {"Order Date", type date}, {"Due Date", type date}, {"Delivery Date", type date}}),
    //Filter OrderDate with parameters to reduce rows and work with sample
    #"Filtered Rows By OrderDate > Param" = Table.SelectRows(#"Tipo cambiado", each [Order Date] > ReduccionFilas)
in
    #"Filtered Rows By OrderDate > Param"