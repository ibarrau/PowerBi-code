var medidaList = new List<string> { "Unit Cost", "Unit Price", "Unit Discount" };
var tableName = "InternetSales";
var dateColumn = "TablaFecha[Fecha]";
/* 
    Create new measures in the model. 
    For each String in the list adds AC, BU, LY, OrgVsBU, OrgVsBU %, OrgVsLY, OrgVsLY %
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