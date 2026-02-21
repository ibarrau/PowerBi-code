let
    Origen = Excel.Workbook(Web.Contents("https://raw.githubusercontent.com/ibarrau/PowerBi-code/master/DatosPrueba/Budget2019-compras.xlsx"), null, true),
    Tabla1_Table = Origen{[Item="Tabla1",Kind="Table"]}[Data],
    //Quitar pivoteo de columnas de fecha
    #"Anulación de dinamización de periodos" = Table.UnpivotOtherColumns(Tabla1_Table, {"Region", "Area", "Gerente"}, "Periodo", "Monto"),
    //Duplicar Periodo para no perderlo al dividirlo
    #"Columna duplicada (Periodo)" = Table.DuplicateColumn(#"Anulación de dinamización de periodos", "Periodo", "Periodo - Copia"),
    //Dividir copia de periodo en año y mes
    #"Dividir periodo por guion medio" = Table.SplitColumn(#"Columna duplicada (Periodo)", "Periodo - Copia", Splitter.SplitTextByDelimiter("-", QuoteStyle.Csv), {"Año", "Mes"}),
    #"Tipo cambiado" = Table.TransformColumnTypes(#"Dividir periodo por guion medio",{{"Region", type text}, {"Area", type text}, {"Gerente", type text}, {"Monto", type number}})
in
    #"Tipo cambiado"