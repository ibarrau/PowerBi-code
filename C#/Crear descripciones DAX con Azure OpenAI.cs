#r "System.Net.Http"
using System.Net.Http;
using System.Text;
using Newtonsoft.Json.Linq;
using System.Threading;

// You need to complete a form at azure portal in order to create the Azure OpenAI resource and get an API key + endpoint 

const string apiKey = "[YOUR API KEY]";
const string deploymentName = "[YOUR DEPLOYMENT NAME]";
const string AzureOpenaiEndpoint = "[YOUR ENDPOINT]"
const string url = AzureOpenaiEndpoint + "openai/deployments/" + deploymentName + "/chat/completions?api-version=2023-05-15" ;
const string question = "Explain the following calculation in Spanish in a few sentences in simple business terms without using DAX function names:\n\n";
var contar = 0;

using (var client = new HttpClient()) {
    client.DefaultRequestHeaders.Clear();
    client.DefaultRequestHeaders.Add("api-key", apiKey);

    foreach (var t in Model.Tables)
    {
        foreach ( var m in t.Measures)
        {
			//30 is the limit of requests per second I have delimited when deploying the model
            if (contar == 30) {
                contar = 0;
                Thread.Sleep(60000);
            } 
            // Only uncomment the following when you want to keep de descriptions that already exists and only add for measures without a description
            if (m.Description == "") {
                var body = "{ \"messages\": [{ \"role\": \"user\" , \"content\": " + JsonConvert.SerializeObject( question + m.Expression ) + "}]}";
                body.Output();
                var res = client.PostAsync(url, new StringContent(body, Encoding.UTF8,"application/json"));
                res.Result.EnsureSuccessStatusCode();
                var result = res.Result.Content.ReadAsStringAsync().Result;
                var obj = JObject.Parse(result);
                var desc = obj["choices"][0]["message"]["content"].ToString().Trim();
                m.Description = desc;
                contar = contar +1;
            }
        }
    }
}