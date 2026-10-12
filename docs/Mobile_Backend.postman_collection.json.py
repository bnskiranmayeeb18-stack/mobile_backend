pm.test("Set token", function(){
  var json = pm.response.json();
  pm.environment.set("ACCESS_TOKEN", json.access);
  pm.environment.set("REFRESH_TOKEN", json.refresh);
});
