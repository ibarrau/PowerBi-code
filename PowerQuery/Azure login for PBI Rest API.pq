let
  FunctionToken = () => 
  let
    body = "resource=https://analysis.windows.net/powerbi/api&client_id=[Client id]&grant_type=password&username=[username]&password=[password of username]&scope=openid",
    Data = Web.Contents("https://login.windows.net/common/oauth2/token/",
    [
      Headers = [#"Content-Type"="application/x-www-form-urlencoded"],
      Content=Text.ToBinary(body)
    ]),
    DataRecord = Json.Document(Data),
    Return = DataRecord[access_token]
  in
    Return
in
  FunctionToken