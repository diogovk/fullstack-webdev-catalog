
"use strict";
var $ = document.querySelector.bind(document);

var UserNavigation = {
    /* Keeps track of user navigation, allowing the user to "go back".
     * This is done, by loading the second latest URL accessed by the user */
    lastURL:  null,
    penultimateURL: null,
    access: function(url, title) {
        this.penultimateURL = this.lastURL;
        this.lastURL = { url: url, title: title };
    },
    goBack: function() {
        if (this.penultimateURL) {
            loadInPageContent(this.penultimateURL.url, this.penultimateURL.title);
        }
    }
};

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
        UserNavigation.access(url, title);
        $("#header-title").textContent = title + " - Catalog App";
        $(".page-content").innerHTML = body;
        componentHandler.upgradeDom();
      });

}

/* updates title, and loads category content page */
function selectCategory(name, id) {
    loadInPageContent('/category/'+id+'/items', name);
}

function createNewItem(id) {
    loadInPageContent('/category/'+id+'/items/new', 'Adding New Item');
}


function editItem(id) {
    loadInPageContent('/item/'+id+'/edit', 'Editing Item');
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
      UserNavigation.goBack();
    } else {
      $(".page-content").innerHTML = body;
      componentHandler.upgradeDom();
    }
  });
}


function deleteItem(url) {
  if (! confirm("Are you sure you want to delete this item?")){
      return;
  }
  fetch(url, {
    credentials: 'same-origin', //send cookies
    method: 'delete',
    body: new FormData($("form"))
  }).then(function(response) {
    return response.text();
  }).then(function(body) {
    if ( body == 'ok'){
      UserNavigation.goBack();
    } else {
      alert(body);
      componentHandler.upgradeDom();
    }
  });
}

function toggleShowLoginPanel() {
  var login_panel = $("#login_panel");
  var display = login_panel.style.display == "block" ? "none" : "block";
  login_panel.style.display = display;
}
