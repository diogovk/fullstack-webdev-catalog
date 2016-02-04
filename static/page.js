
"use strict";
var $ = document.querySelector.bind(document);
var Navigation = {
    /* Keeps track of user navigation, allowing the user to "go back".
     * This is done, by loading the second latest URL accessed by the user */
    lastURL:  null,
    penultimateURL: null,
    access: function(url, title) {
        this.penultimateURL = this.lastURL;
        this.lastURL = { url: url, title: title };
        this.loadInPageContent(url, title);
    },
    goBack: function() {
        if (this.penultimateURL) {
            this.access(this.penultimateURL.url, this.penultimateURL.title);
        }
    },
    loadInPageContent: function(url, title) {
        fetch(url, {
          credentials: 'same-origin', //send cookies
          }).then(function(response) {
            return response.text();
          }).then(function(body) {
            $("#header-title").textContent = title + " - Catalog App";
            $(".page-content").innerHTML = body;
            $(".mdl-layout__content").scrollTop = 0;
            componentHandler.upgradeDom();
          });

    }
};




/* updates title, and loads category content page */
function selectCategory(name, id) {
    Navigation.access('/category/'+id+'/items', name);
}


function createNewItem(id) {
    Navigation.access('/category/'+id+'/items/new', 'Adding New Item');
}


function editItem(id) {
    Navigation.access('/item/'+id+'/edit', 'Editing Item');
}


function postItem(url) {
  fetch(url, {
    credentials: 'same-origin', //send cookies
    method: 'post',
    body: new FormData($("#item_edit_form"))
  }).then(function(response) {
    return response.text();
  }).then(function(body) {
    if ( body == 'ok'){
      Navigation.goBack();
    } else {
      $(".page-content").innerHTML = body;
      componentHandler.upgradeDom();
    }
  });
}


function deleteItem(url, afterDeleteURL) {
  if (! confirm("Are you sure you want to delete this item?")){
      return;
  }
  fetch(url, {
    credentials: 'same-origin', //send cookies
    method: 'delete',
    body: new FormData($("#csrf_form"))
  }).then(function(response) {
    return response.text();
  }).then(function(body) {
    if ( body == 'ok'){
      Navigation.access(afterDeleteURL);
    } else {
      alert(body);
    }
  });
}

function toggleShowLoginPanel() {
  var login_panel = $("#login_panel");
  login_panel.hidden = !login_panel.hidden;
  gapi.signin.go(login_panel);
}

function googleLoginCallback(authResult) {
  if (authResult.code){
    $("#googleSignInButton").style.display = "none";
    var data =new FormData($("#csrf_form"));
    data.append('token', authResult.code);
    fetch("/gconnect", {
      credentials: 'same-origin',
      method: 'post',
      body: data
    }).then(function(response) {
      return response.text();
    }).then(function(body) {
        if (body == "ok") {
          console.log("Login successful. Redirecting.");
          window.location.href="/";
        }
    });
  }
}
