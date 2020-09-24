
window.onload=function starti(){
  var looki = document.getElementById("foodname")
  var button = document.getElementById("button")
  button.addEventListener("click", this.startSearch);
  
}
function startSearch()
{
  var looki = document.getElementById("foodname");
  console.log(looki);
  if(looki === null) {  console.log('nulll')};
  var text = looki.value;

  document.getElementById("Protein").innerHTML = "Protein: 0";
  document.getElementById("Carbs").innerHTML="Carbs: 0";
  document.getElementById("Fat").innerHTML="Fat: 0";
    if(text){
    loki(text);
    }
    else
    {
    console.log("koniec")
    document.getElementById("Protein").innerHTML = "Protein: 0";
    document.getElementById("Carbs").innerHTML="Carbs: 0";
    document.getElementById("Fat").innerHTML="Fat: 0";
    }
}
async function loki(looking){
  console.log(looking);

  var url="https://api.nal.usda.gov/fdc/v1/foods/search?api_key=ahWUUGyJjI9DxYzosPinNb8cNgvpsGF1SU7r9dsh&query="+looking
  const response = await fetch(url);
  const data = await response.json();
  var arrays=[];  
  if
  (data.foods[0].foodNutrients==='undefined'){
    console.log("koniec")
    document.getElementById("full_name").innerHTML = "product not found";
    document.getElementById("Protein").innerHTML = "Protein: 0";
    document.getElementById("Carbs").innerHTML="Carbs: 0";
    document.getElementById("Fat").innerHTML="Fat: 0";
    
  }
  else{
  var arrays=data.foods[0].foodNutrients;
  console.log(arrays.value);
  let anwser_p = arrays.find(is_protein);
  let anwser_f = arrays.find(is_fat);
  let anwser_c = arrays.find(is_carb);
  let name_p=data.foods[0].description;
  console.log('hello');
  console.log(anwser_p.value);
  console.log(anwser_f.value);
  console.log(name_p);
  document.getElementById("full_name").innerHTML = name_p;
  document.getElementById("Protein").innerHTML = 'Protein: '+anwser_p.value+"g";
  document.getElementById("Carbs").innerHTML="Carbs: "+anwser_c.value+"g";
  document.getElementById("Fat").innerHTML="Fat: "+anwser_f.value+"g";
  
  }
}
function is_protein(arrays){
  return arrays.nutrientId===1003;
}
function is_fat(arrays){
return arrays.nutrientId===1004;
}
function is_carb(arrays){
return arrays.nutrientId===1005;
}
