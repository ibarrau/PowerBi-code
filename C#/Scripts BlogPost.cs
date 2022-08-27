/*---------------------------------------------------------------------------------------------------------------*/
//Let’s query our model to get the measures which name contains the string “Color” or “Sales”

Model.AllMeasures.Where(m => m.Name.Contains("Color")).Output();
Model.AllMeasures.Where(m => m.Name.Contains("Sales")).Output(); 


/*---------------------------------------------------------------------------------------------------------------*/
//Let’s query our model to get the measures which expression contains the string “VALUES”

Model.AllMeasures.Where(m => m.Expression.Contains("CALCULATE")).Output();
Model.AllMeasures.Where(m => m.DataType.Equals(DataType.Int64)).Output();

/*---------------------------------------------------------------------------------------------------------------*/
//Let’s pick a measure to make an operation for that specific selected item. In this case, rename.

Selected.Measures.Rename("Proyeccion","Projection"); 

/*---------------------------------------------------------------------------------------------------------------*/
//Let’s create our first measure with its properties in Tabular Editor.

var nuevita = Model.Tables["InternetSales"].AddMeasure("TabMedida", "SUM(InternetSales[Unit Cost])");
nuevita.FormatString ="$#0.0";
nuevita.Description = "Nuevita creada por tabular editor";

/*---------------------------------------------------------------------------------------------------------------*/
//Modify the expression of a measure TableCountConsecutive -> Consecutivos_v2 -> “diff”

Selected.Measure.Expression = Selected.Measure.Expression.Replace(“diff","__diff"); 

/*---------------------------------------------------------------------------------------------------------------*/
//Multiple replacement to improve modify timings.

foreach ( var medida in Model.AllMeasures.Where(m => m.Expression.Contains("SWITCH(_Units")) )
{
   medida.Expression = medida.Expression.Replace("SWITCH(_Units","–Changing units \nSWITCH(_Units");
}

/*---------------------------------------------------------------------------------------------------------------*/
//How create many useful measures at once.

//DAX OBJECT NAME property contains brackets []
var dateColumn = "'TablaFecha'[Fecha]";
foreach (var m in Selected.Measures)
{
    //YTD
    m.Table.AddMeasure(
        m.Name + " YTD",
        "TOTALYTD(" + m.DaxObjectName + ", " + dateColumn + ")"
    );
    //LY
    m.Table.AddMeasure(
    m.Name + " LY",
    FormatDax( "CALCULATE(" + m.DaxObjectName + "," + 
		"SAMEPERIODLASTYEAR(" + dateColumn + "))" )
    );
}

/*---------------------------------------------------------------------------------------------------------------*/
//If it’s easier for us to build custom scripts without clicking selected ítems we can build list and loop it 
//For each name of measures we can créate regular measures.

var medidaList = new List<string> { "Unit Cost", "Unit Price", "Unit Discount" };
var tableName = "InternetSales";
var dateColumn = "TablaFecha[Fecha]";
/* 
    Create new measures in the model. 
    For each String in the list adds AC, LY, LM, YoY, YTD
*/

foreach (string medida in medidaList) {
    var ac = Model.Tables[tableName].AddMeasure(medida + " AC", 
            "SUM('" + tableName + "'[" + medida + "])"
        );
        ac.FormatString ="$#0.0";
        ac.Description = "SUM of " + medida; 
        
    // Adding LY measure
    var ly = Model.Tables[tableName].AddMeasure(medida+" LY", 
        "CALCULATE(" +
        "\n\t["+medida+" AC]" +
        "\n\t, SAMEPERIODLASTYEAR(" + dateColumn + ")" +
        "\n)"
    );
    ly.FormatString ="$#0.0";
    ly.Description = "SUM of " + medida + " for same period last year"; 

    // Adding LM measure
    var lm = Model.Tables[tableName].AddMeasure(medida+" LM", 
        "CALCULATE(" +
        "\n\t["+medida+" AC]" +
        "\n\t, PREVIOUSMONTH(" + dateColumn + ")" +
        "\n)"
    );
    lm.FormatString ="$#0.0";
    lm.Description = "SUM of " + medida + " for previous month"; 

    // Adding YoY measure
    var yoy = Model.Tables[tableName].AddMeasure(medida+" YoY", 
        "DIVIDE(" +
        "\n\t [" + medida + " AC] - [" + medida +" LY]" +
        "\n\t, [" + medida +" LY]" +
        "\n)"
    );
    yoy.FormatString ="#,#0.0%";
    yoy.Description = "Year over year of " + medida + "."; 

    // Adding YTD measure
    var ytd = Model.Tables[tableName].AddMeasure(medida+" YTD", 
        "CALCULATE(" +
        "\n\t["+medida+" AC]" +
        "\n\t, DATESYTD(" + dateColumn + ")" +
        "\n)"
    );
    ytd.FormatString ="$#0.0";
    ytd.Description = "Year to date of the SUM of " + medida + "."; 
}