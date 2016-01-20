
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
    body: new FormData($("#item_edit_form"))
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
    body: new FormData($("#csrf_form"))
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

function googleLoginCallback(authResult) {
  if (authResult.code){
    $("#googleSignInButton").style.display = "none";
    var data =new FormData($("#csrf_form"));
    data.append('token', authResult.code);
    console.log(authResult.code);
    fetch("/gconnect", {
      credentials: 'same-origin',
      method: 'post',
      body: data
    }).then(function(response) {
      return response.text();
    }).then(function(body) {
        if (body == "ok") {
          console.log("Login successful. Redirecting.");
//          window.location.href="/";
        }
    });
  }
}
