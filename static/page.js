
"use strict";
console.log("starting");
var request = window.superagent;
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var id_token = googleUser.getAuthResponse().id_token;
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail());
    request.post('/oauth_check')
        .send({ token: id_token })
        .end(function(err, res){
            if (res.text == "ok") {
                alert("Logged in successfuly");
            }
        });
}

/* updates title, and loads category content page */
function selectCategory(name, id) {
    document.getElementById("header-title").textContent=name;
}
