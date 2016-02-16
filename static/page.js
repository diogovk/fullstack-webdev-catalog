
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
        })
        .then(getResponseBody)
        .then(function(body) {
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

function checkStatus(response) {
    // Throws error if http status is not success
    // Assumes the request body is the error message
    if (response.status >= 200 && response.status < 300) {
      return response;
    } else {
      return response.text().then(function (body) {
        throw new Error(body);
      });
    }
}

function postItem(url) {
  // posts an Item to URL, with the data in the form #item_edit_form
  // this can be used for new Items, or to update an item, since they use the same form
  fetch(url, {
    credentials: 'same-origin', //send cookies
    method: 'post',
    body: new FormData($("#item_edit_form"))
  })
  .then(checkStatus)
  .then(getResponseBody)
  .then(function(body) {
    if ( body == 'ok'){
      // item saved successfully
      Navigation.goBack();
    } else {
      // re-render the form with HTML received from server
      // most likely there are validation errors
      $(".page-content").innerHTML = body;
      componentHandler.upgradeDom();
    }
  })
  .catch(function(err) {
    // unexpected error when requesting data
    alert('Request failed: ' + err.message);
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
  })
  .then(getResponseBody)
  .then(function(body) {
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

function ifOkRedirectToHome(body) {
   if (body == "ok") {
     console.log("Login successful. Redirecting.");
     window.location.href="/";
   }
}

function getResponseBody(response) {
    return response.text();
}

function googleLoginCallback(authResult) {
  if (authResult.code){
    $("#googleSignInButton").style.display = "none";
    var data = new FormData($("#csrf_form"));
    data.append('token', authResult.code);
    fetch("/gconnect", {
      credentials: 'same-origin',
      method: 'post',
      body: data
    })
    .then(getResponseBody)
    .then(ifOkRedirectToHome);
  }
  waitForLogin();
}

function logout() {
  fetch("/disconnect", {
    credentials: 'same-origin', //send cookies
  })
  .then(getResponseBody)
  .then(ifOkRedirectToHome);
}

function waitForLogin() {
  /* Disable login buttons and show a message asking to wait for the
   * login process */
  var login_panel = $("#login_panel");
  login_panel.innerHTML="Login in progress.<br>You'll be redirected shortly.";
}

function facebookLoginCallback() {
  var access_token = FB.getAuthResponse().accessToken;
  FB.api('/me', function(response) {
    console.log('Successful login for: ' + response.name);
    var data =new FormData($("#csrf_form"));
    data.append('token', access_token);
    fetch('/fbconnect', {
      credentials: 'same-origin', //send cookies
      method: 'post',
      body: data
    })
    .then(getResponseBody)
    .then(ifOkRedirectToHome);
  });
  waitForLogin();
}
