
"use strict";
var $ = document.querySelector.bind(document);
var currentSelectedCategory = null;

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var id_token = googleUser.getAuthResponse().id_token;
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    //request.post('/oauth_check')
    //    .send({ token: id_token })
    //    .end(function(err, res){
    //        if (res.text == "ok") {
    //            alert("Logged in successfuly");
    //        }
    //    });
}

function loadInPageContent(url, title) {
    fetch(url, {
      credentials: 'same-origin', //send cookies
      }).then(function(response) {
        return response.text();
      }).then(function(body) {
        $("#header-title").textContent = title + " - Catalog App";
        $(".page-content").innerHTML = body;
        componentHandler.upgradeDom();
      });

}

/* updates title, and loads category content page */
function selectCategory(name, id) {
    loadInPageContent('/category/'+id+'/items', name);
    // used for "going back"
    currentSelectedCategory = { id: id, name: name };
}

function createNewItem(id) {
    loadInPageContent('/category/'+id+'/items/new', 'Adding New Item');
}

function editItem(id) {
    loadInPageContent('/item/'+id+'/edit', 'Editing Item');
}

function cancelNewItem() {
  loadLastCategory();
}

function loadLastCategory() {
  if (currentSelectedCategory) {
    selectCategory(currentSelectedCategory.name, currentSelectedCategory.id);
  }
}

function postItem(url) {
  fetch(url, {
    credentials: 'same-origin', //send cookies
    method: 'post',
    body: new FormData($("form"))
  }).then(function(response) {
    return response.text();
  }).then(function(body) {
    if ( body == 'ok'){
      loadLastCategory();
    } else {
      $(".page-content").innerHTML = body;
      componentHandler.upgradeDom();
    }
  });
}
