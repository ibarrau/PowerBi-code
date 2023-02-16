// This code was originally created by Darren Gosbell and modified by Ignacio Barrau for API limitations, checking empty descriptions and spanish responses

#r "System.Net.Http"
using System.Net.Http;
using System.Text;
using Newtonsoft.Json.Linq;
using System.Threading;

// You need to signin to https://platform.openai.com/ and create an API key for your profile then paste that key 
// into the apiKey constant below
const string apiKey = "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";
const string uri = "https://api.openai.com/v1/completions";
const string question = "Explain the following calculation in Spanish in a few sentences in simple business terms without using DAX function names:\n\n";
var contar = 0;

using (var client = new HttpClient()) {
    client.DefaultRequestHeaders.Clear();
    client.DefaultRequestHeaders.Add("Authorization", "Bearer " + apiKey);

    foreach (var t in Model.Tables)
    {
        foreach ( var m in t.Measures)
        {
            if (contar == 20) {
                contar = 0;
                Thread.Sleep(60000);
            }
            // Only uncomment the following when you want to keep de descriptions that already exists and only add for measures without a description
            //if (m.Description == "") {
                var body = 
                    "{ \"prompt\": " + JsonConvert.SerializeObject( question + m.Expression ) + 
                    ",\"model\": \"text-davinci-003\" " +
                    ",\"temperature\": 1 " +
                    ",\"max_tokens\": 2048 " +
                    ",\"stop\": \".\" }";

                var res = client.PostAsync(uri, new StringContent(body, Encoding.UTF8,"application/json"));
                res.Result.EnsureSuccessStatusCode();
                var result = res.Result.Content.ReadAsStringAsync().Result;
                var obj = JObject.Parse(result);
                var desc = obj["choices"][0]["text"].ToString().Trim();
                m.Description = desc;
                contar = contar +1;
            //}
        }

    }
}