function displayElement(myId){
    let element = document.getElementById(myId);
    
    if(element.style.display === "none" ) {
      element.style.display = "block";
    } else if(element.style.display === ""){
      element.style.display = "none";
    }
  }