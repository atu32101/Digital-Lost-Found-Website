// Shared minimal frontend helpers.
// Individual pages mostly use inline scripts, but this file is loaded globally by `base.html`.

function getToken() {
  return localStorage.getItem("access_token");
}

function authHeaders() {
  const token = getToken();
  if (!token) return {};
  return { Authorization: "Bearer " + token };
}

