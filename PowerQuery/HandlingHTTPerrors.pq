let
    Source = Web.Contents("api.github.com", [RelativePath="/repos/LaDataWeb/data-quality-report/commitsss", ManualStatusHandling={404}]),    
    Navigation = Json.Document(Source),
    #"Converted to Table" = Table.FromList(Navigation, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", 
        {"sha", "node_id", "commit", "url", "html_url", "comments_url", "author", "committer", "parents"}, 
        {"sha", "node_id", "commit", "url", "html_url", "comments_url", "author", "committer", "parents"}
    ),
    GetMetadata = Value.Metadata(Source),
    Output = if GetMetadata[Response.Status] <> 404 
        then #"Expanded Column1" 
        else #table({"sha", "node_id", "commit", "url", "html_url", "comments_url", "author", "committer", "parents"},{})                            // Table.FromRecords({[Column1 = 0, Column2 = "value"]})
in
    Output