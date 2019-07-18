document.getElementById('showUserInputForm').addEventListener('submit', performGetRequest1);
let nextUrl = null;
let previousUrl = null;
baseUrl = 'http://127.0.0.1:5000/';

function performGetRequest1(url){

  if (!url) {
    url = baseUrl + 'users/page'
  }
  var limit = document.getElementById('limit').value;
  var resultElement = document.getElementById('getResult1');
  resultElement.innerHTML = '';
  

  axios.get(url, {
    params: {
      limit:limit
    }
  })
    .then(function (response) {
     resultElement.innerHTML = generateSuccessHTMLOutput(response);
     nextUrl = baseUrl + response.data.next;
     previousUrl = baseUrl + response.data.previous;
    })
    .catch(function (error) {
     resultElement.innerHTML = generateErrorHTMLOutput(error);
    });
}

function previousPage() {
	performGetRequest1(previousUrl);
}

function nextPage() {
	performGetRequest1(nextUrl);
}



document.getElementById('showUserInputForm').addEventListener('submit', searchByUsername);
let nextPageUrl = null;
let previousPageUrl = null;

function searchByUsername(url) {
  if (!url) {
    url = baseUrl + 'filter';
  }
  var searchUsername = document.getElementById('searchUsername').value;
  var pageLimit = document.getElementById('pageLimit').value;
  var resultElement = document.getElementById('getResult2');
  resultElement.innerHTML = '';
  

  axios.get(url, {
    params: {
      username:searchUsername,
      limit:pageLimit
    }
  })
    .then(function (response) {
     resultElement.innerHTML = generateSuccessHTMLOutput(response);
     nextPageUrl = baseUrl + response.data.next
     previousPageUrl = baseUrl + response.data.previous;
    })
    .catch(function (error) {
     resultElement.innerHTML = generateErrorHTMLOutput(error);
    });
}

function nextPageFilter() {
	searchByUsername(nextPageUrl);
}

function previousPageFilter() {
  searchByUsername(previousPageUrl)
}




function generateSuccessHTMLOutput(response) {
  return  '<h4>Result:</h4>' +
          '<h5>Status:</h5>' +
          '<pre>' + response.status + ' ' + response.statusText + '</pre>' +
          '<h5>Headers:</h5>' +
          '<pre>' + JSON.stringify(response.headers, null, '\t') + '</pre>' +
          '<h5>Data:</h5>' +
          '<pre>' + JSON.stringify(response.data, null, '\t') + '</pre>';
}

function generateErrorHTMLOutput(error) {
  return  '<h4>Result:</h4>' +
          '<h5>Message:</h5>' +
          '<pre>' + error.message + '</pre>' +
          '<h5>Status:</h5>' +
          '<pre>' + error.response.status + ' ' + error.response.statusText + '</pre>' +
          '<h5>Headers:</h5>' +
          '<pre>' + JSON.stringify(error.response.headers, null, '\t') + '</pre>' +
          '<h5>Data:</h5>' +
          '<pre>' + JSON.stringify(error.response.data, null, '\t') + '</pre>';
}


document.getElementById('registerInputForm').addEventListener('submit', performPostRegistration);

function performPostRegistration(e) {
  var resultElement = document.getElementById('postResult');
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value
  resultElement.innerHTML = '';

  axios.post('http://127.0.0.1:5000/registration', {
    username: username,
    password: password
  })
  .then(function (response) {
    resultElement.innerHTML = generateSuccessHTMLOutput(response);
  })
  .catch(function (error) {
    resultElement.innerHTML = generateErrorHTMLOutput(error);
  })
  e.preventDefault();
}

document.getElementById('loginInputForm').addEventListener('login', performPostLogin);

function performPostLogin(e) {
  var resultElement = document.getElementById('loginResult');
  var username = document.getElementById('lUsername').value;
  var password = document.getElementById('lPassword').value
  resultElement.innerHTML = '';

  axios.post('http://127.0.0.1:5000/login', {
    username: username,
    password: password
  })
  .then(function (response) {
    resultElement.innerHTML = generateSuccessHTMLOutput(response);
  })
  .catch(function (error) {
    resultElement.innerHTML = generateErrorHTMLOutput(error);
  })
  e.preventDefault();
}

document.getElementById('updateInputForm').addEventListener('update', performUpdatePassword);


function performUpdatePassword(e) {
  var resultElement = document.getElementById('updateResult');
  var username = document.getElementById('uUsername').value;
  var password = document.getElementById('uPassword').value;
  var new_password = document.getElementById('uNew_password').value;
  var access_token = document.getElementById('access_token').value;
  resultElement.innerHTML = '';

  var bodyParameters = {
     username: username,
     password: password,
     new_password: new_password
  }

  const authStr = 'Bearer ' + access_token ;

  axios.put(
    'http://127.0.0.1:5000/update',
     bodyParameters,{
       headers: { 'Content-Type' : 'application/json',
       Authorization: authStr}
     }
  ).then(function (response) {
    resultElement.innerHTML = generateSuccessHTMLOutput(response);
  })
  .catch(function (error) {
    resultElement.innerHTML = generateErrorHTMLOutput(error);
  })
  e.preventDefault();
}

document.getElementById('refreshInputForm').addEventListener('refresh', refreshAccesToken);

function refreshAccesToken(e) {
  var resultElement =  document.getElementById('refreshResult');
  var refreshToken = document.getElementById('nRefreshToken').value;
  resultElement.innerHTML = '';

  const refStr = 'Bearer ' + refreshToken ;

  axios.post(
    'http://127.0.0.1:5000/token/refresh',
     null,{
     headers: { 'Content-Type' : 'application/json',
     'Authorization': refStr}
 }
 ).then(function (response) {
  resultElement.innerHTML = generateSuccessHTMLOutput(response);
 })
 .catch(function (error) {
  resultElement.innerHTML = generateErrorHTMLOutput(error);
 })
 e.preventDefault();
 }



function clearOutput() {
    var resultElement = document.getElementById('getResult1');
    resultElement.innerHTML = '';
    var resultElement = document.getElementById('postResult');
    resultElement.innerHTML = '';
    var resultElement = document.getElementById('loginResult');
    resultElement.innerHTML = '';
    var resultElement = document.getElementById('updateResult');
    resultElement.innerHTML = '';
    var resultElement = document.getElementById('refreshResult');
    resultElement.innerHTML = '';
    var resultElement = document.getElementById('getResult2');
    resultElement.innerHTML = '';
}
